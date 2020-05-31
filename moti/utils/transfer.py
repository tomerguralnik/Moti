from furl import furl
from .consumer import Consumer

class Transfer:
    """
    Transfer is class that recives a publishing method and queue to consume from
    It sets up a Consumer and adds all the queues in queues with the appropriate
    callback functions
    The start method begins the consumers consumption
    The transfer should be initialized with either a publish factory or a publish
    publish factory takes precedence
    """
    def __init__(self, input_url, queues, publish_factory = None, publish = None):
        """
        :param input_url: this url should define a consumer
        :type input_url: str
        :param queues: list of queue names to consume from and publish to
        :type queues: list
        :param publish_factory: a publisher that recieves a queue when publishing
        :type publish_factory: Publisher
        :param publish: a publisher that does'nt receive a queue
        :type publish: Publisher
        """
        self.consumer = Consumer(input_url)
        self.publish_factory = publish_factory
        for queue in queues:
            if publish_factory:
                self.consumer.add_queue(queue, self.callback_factory(queue))
            elif publish:
                self.consumer.add_queue(queue, lambda ch, method, props, body: publish(body))
            else:
                Warning("No publishing method {queue}")

    def start(self):
        self.consumer.consume()

    def callback_factory(self, queue):
        """
        Creates a callback function of the right format

        :param queue: name of a queue
        :type queue: str
        :return: creates a callback functions fit for message queues
        :rtype: callable
        """
        def callback(ch, method, props, body):
            self.publish_factory(body, queue)
        return callback