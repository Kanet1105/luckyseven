from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Consumer
from confluent_kafka import Producer
from threading import Thread
import sys


class MyConsumer(Thread):
    def __init__(self, client_id):
        super().__init__()
        self.daemon = True
        self.configs = {
            'bootstrap.servers': '61.254.240.172:9092',
            'group.id': 'users',
            'client.id': client_id,
            'enable.auto.commit': True,
        }
        self.consumer = Consumer(self.configs)
        self.consumer.subscribe(['all'])
        self.running = True
        self.start()

    def run(self):
        while self.running:
            msg = self.consumer.poll(0.1)
            if msg is None:
                continue
            if msg.error():
                print(msg.value)
                continue
            else:
                print(msg.value())

        self.consumer.close()
        print('consumer closed')


class MyProducer:
    def __init__(self, client_id):
        self.daemon = True
        self.configs = {
            'bootstrap.servers': '61.254.240.172:9092',
        }
        self.producer = Producer(self.configs)


if __name__ == '__main__':
    c = MyConsumer('ldh1')
    p = MyProducer('ldh2')
    while True:
        try:
            message = input()
            p.producer.produce(topic='all', value=message)
        except KeyboardInterrupt:
            c.running = False
            c.join()
            sys.exit()
