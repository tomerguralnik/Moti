import pika
class RabbitmqConsumer:
    protocol = 'rabbitmq'
    def __init__(self, host, port, exchange_name):
        """
        Initialize connection to the message queue

        :param host: ip of the mq server
        :type host: str
        :param port: port of the mq server
        :type port: int
        :param exchange_name: an exchange to consume from
        :type exchange_name: str 
        """
        connection = pika.BlockingConnection(
                     pika.ConnectionParameters(host = host,
                                               port = port))
        channel = connection.channel()
        self.channel = channel
        self.exchange_name = exchange_name

    def add_queue(self, queue, callback):
        """
        Add queue to consumption with callback as teh callback function
        the exchange names are added to the queues so raw queus and parsed
        queues don't have the same name 

        :param queue: a queue name
        :type queue: str
        :param callback: a callback funtion for the queue, recieves arguments (ch, method, props, body)
        :type callback: callable
        """
        self.channel.queue_declare(queue = f"{self.exchange_name}/{queue}")
        self.channel.basic_consume(queue = f"{self.exchange_name}/{queue}",
                                   on_message_callback = callback, 
                                   auto_ack = True)

    def consume(self):
        """
        Start consuming the queue
        """
        self.channel.start_consuming()