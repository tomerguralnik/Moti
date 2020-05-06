from .parser import Parser
import pika
class Consumer:
    def __init__(self, context, publish = None, publish_factory = None, host = '127.0.0.1', port = 5672, name = 'Server', parsers = None):
        if parsers == None:
            self.parsers = Parser().parsers
        else:
            self.parsers = parsers
        self.name = name
        self.context = context
        self.publish = publish
        self.publish_factory = publish_factory
        connection = pika.BlockingConnection(
                     pika.ConnectionParameters(host = host,
                                               port = port))
        channel = connection.channel()
        channel.exchange_declare(exchange = name,
                                exchange_type = 'fanout')
        self.channel = channel
        for parser in self.parsers:
            self.channel.queue_declare(queue = parser.__name__  + self.name)
            self.channel.queue_bind(exchange = self.name,
                                    queue = parser.__name__  + self.name)

    def consume(self):
        for parser in self.parsers:
            self.channel.basic_consume(queue = parser.__name__  + self.name,
                                       on_message_callback = self.create_callback(parser),
                                       auto_ack = True)
        self.channel.start_consuming()

    def create_callback(self, parser):
        if self.publish:
            def callback(ch, method, properties, body):
                print("HI")
                self.publish(parser(body, self.context))
        elif self.publish_factory:
            def callback(ch, method, properties, body):
                print("hi")
                self.publish_factory(parser(body, self.context), parser)
        return callback

            
