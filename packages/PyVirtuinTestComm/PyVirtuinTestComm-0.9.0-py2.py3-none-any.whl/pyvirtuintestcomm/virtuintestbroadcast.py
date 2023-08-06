"""VirtuinTestBroadcast consists of two classes: VirtuinTestPublisher and
VirtuinTestSubscriber.
VirtuinTestPublisher shall be used by a running test to update status via RabbitMQ.
VirtuinTestPublisher shall be used by any process wanting to receive test
status updates via RabbitMQ.
"""
import json
from datetime import datetime
import pika


# pylint: disable=too-many-instance-attributes
class VirtuinTestPublisher(object):
    """VirtuinTestPublisher is used to publish status updates over AMQP
    (via RabbitMQ).

    Attributes:
        None
    """
    def __init__(self, stationName, testName, testUUID=None):
        self.version = '0.9.0'
        self.exName = '{:s}'.format(stationName)
        self.testName = testName
        if testUUID:
            self.testUUID = testUUID
        else:
            dateStr = datetime.now().strftime('%c')
            self.testUUID = str.format('{:s}_{:s}', testName, dateStr)
        self.state = "STARTED"
        self.progress = 0
        self.passed = None
        self.conn = None
        self.ch = None
        self.isOpen = False

    def open(self, hostName='localhost'):
        """Open connection to RabbitMQ
        Args:
            hostName (str): Address of broker
        Returns:
            None
        """
        connParams = pika.ConnectionParameters(host=hostName)
        self.conn = pika.BlockingConnection(connParams)
        self.ch = self.conn.channel()
        self.ch.exchange_declare(exchange=self.exName, exchange_type='fanout')
        self.isOpen = True

    def close(self, tearDown=False):
        """Close connection to RabbitMQ
        Args:
            tearDown (bool, optional):
                To tear down RMQ exchange.
                Useful to clean environment.
        Returns:
            None
        """
        if not self.isOpen:
            return
        if tearDown:
            self.ch.exchange_delete(
                exchange=self.exName
            )
        if self.conn:
            self.conn.close()
        self.conn = None
        self.ch = None
        self.isOpen = False

    def _getBasePayload(self, message="", error=None):
        """Create base payload object to be published
        Args:
            message (str): General status message
            error (str): Error message
        Returns:
            dict: Payload object
        """
        return dict(
            version=self.version,
            status=dict(
                testUUID=self.testUUID,
                testName=self.testName,
                state=self.state,
                passed=self.passed,
                progress=self.progress,
                error=error,
                message=message
            ),
        )

    def _publishData(self, data):
        """Publishes payload object
        Args:
            data (dict): Payload object
        Returns:
            None
        """
        dataStr = json.dumps(data)
        self.ch.basic_publish(exchange=self.exName, routing_key='', body=dataStr)

    def clearStatus(self):
        """Resets status to default values.
        Args:
            None
        Returns:
            None
        """
        self.state = None
        self.progress = 0
        self.passed = None

    def updateStatus(self, state=None, progress=None, passed=None):
        """Update status values.
        Args:
            state (str): State of test (STARTING, ..., FINISHED)
            progress (float): Progress of test [0-100]
            passed (bool): If test passed/failed
        Returns:
            None
        """
        self.state = state if state else self.state
        self.progress = progress if progress is not None else self.progress
        self.passed = passed if passed is not None else self.passed

    def publish(self, message="", error=None, results=None, customDict=None):
        """Publish test status payload.
        Args:
            message (str): General status message
            error (str): Critical error message
            results (dict): Serializable database results object
            customDict (dict): Serializable object to merge into status payload
        Returns:
            None
        """
        data = self._getBasePayload(message, error)
        if results:
            data['results'] = results
        if customDict:
            data.update(customDict)
        self._publishData(data)

# pylint: disable=too-many-instance-attributes
class VirtuinTestSubscriber(object):
    """VirtuinTestSubscriber is used to subscribe to test's status updates
    over AMQP (via RabbitMQ).

    Attributes:
        None
    """
    def __init__(self, stationName):
        self.version = '0.9.0'
        self.exName = str.format('{:s}', stationName)
        self.conn = None
        self.ch = None
        self.qName = None
        self.isOpen = False
        self.isSubscribing = False
        self.subscriber = None
        self.subscribeTag = None

    def open(self, hostName='localhost'):
        """Open connection to RabbitMQ
        Args:
            hostName (str): Address of broker
        Returns:
            None
        """
        connParams = pika.ConnectionParameters(host=hostName)
        self.conn = pika.BlockingConnection(connParams)
        self.ch = self.conn.channel()
        self.ch.exchange_declare(exchange=self.exName, exchange_type='fanout')
        q = self.ch.queue_declare(queue='', exclusive=True, durable=False)
        qName = q.method.queue
        self.ch.queue_bind(queue=qName, exchange=self.exName)
        self.qName = qName
        self.isOpen = True

    def close(self):
        """Close connection to RabbitMQ
        Args:
            None
        Returns:
            None
        """
        if self.isOpen:
            return
        if self.isSubscribing:
            self.unsubscribe()
        if self.conn:
            self.conn.close()
        self.conn = None
        self.ch = None
        self.isOpen = False

    # pylint: disable=unused-argument
    def _consume(self, ch, method, props, body):
        """Callback routine for incoming status updates.
        This is set in subscribe(). Subsequently calls
        subscriber callback routine with dict result.
        Args:
            ch (str): RabbitMQ channel
            method: RabbitMQ method
            props: RabbitMQ props
            body: RabbitMQ Payload
        Returns:
            None
        """
        if self.subscriber and callable(self.subscriber):
            try:
                jsonData = json.loads(body.decode('utf8'))
                self.subscriber(None, jsonData)
            # pylint: disable=broad-except
            except Exception as err:
                self.subscriber(err, None)

    def consume(self):
        """Gets next broadcast packet. This method does not block.
        If no packet available, returns None
        Args:
            None
        Returns:
            dict|None: Status packet or None
        """
        if not self.isOpen:
            raise Exception('Connection not open.')
        method, _, body = self.ch.basic_get(queue=self.qName)
        if method:
            jsonData = json.loads(body.decode('utf8'))
            return jsonData
        return None

    def subscribe(self, subscriber):
        """Subscribes using callback. This method blocks.
        To release, call unsubscribe in callback function.
        Args:
            subscriber (callable): Callback function triggered when
            status updates received. cb(err, result) => None
        Returns:
            str: subscription consumer tag
        """
        try:
            if not self.isOpen or self.isSubscribing:
                raise Exception('Connection not open or already subscribing.')
            self.isSubscribing = True
            self.subscriber = subscriber
            self.subscribeTag = self.ch.basic_consume(self._consume, queue=self.qName)
            self.ch.start_consuming()  # This blocks
            return self.subscribeTag
        # pylint: disable=broad-except,unused-variable
        except Exception as err:
            return self.subscribeTag

    def unsubscribe(self):
        """Stop subscribing to test status updates.
        Args:
            None
        Returns:
            None
        """
        if not self.open or not self.isSubscribing:
            return None
        self.ch.basic_cancel(self.subscribeTag)
        self.subscriber = None
        self.isSubscribing = False
        self.subscribeTag = None
        return None
