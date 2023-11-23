# -*- coding: utf-8 -*-

"""
Copyright (c) 2021 xxx.com, Inc. All Rights Reserved
datetime: 2021/11/23 3:06 下午
"""

from kafka import KafkaProducer
from kafka.errors import KafkaError


class KafkaClient(object):
    """
    send message
    """

    def __init__(self):
        self.sender = None
        self.config = None

    @staticmethod
    def on_send_success(record_metadata):
        """
        如果消息成功写入 Kafka，broker 将返回 RecordMetadata 对象（包含 topic，partition 和 offset）；
        """
        print("Success:[{0}] send success".format(record_metadata))

    @staticmethod
    def on_send_error(excp):
        """
        相反，broker 将返回 error。这时 producer 收到 error 会尝试重试发送消息几次，直到 producer 返回 error。
        """
        print("INFO" + "Fail:send fail cause:{0}".format(excp))

    def product(self, kafka_config):
        """
        设置配置信息
        """
        self.config = kafka_config
        # 创建一个生产者
        self.sender = KafkaProducer(**self.config)

    def send(self, topic, value=None, key=None):
        """
        必须包含 Topic 和 Value，key 和 partition 可选。然后，序列化 key 和 value 对象为 ByteArray，并发送到网络。
        """
        future = self.sender.send(topic, value=value, key=key)
        try:
            record_metadata = future.get(timeout=10)
            self.on_send_success(record_metadata)
        except KafkaError as e:
            self.on_send_error(e)


if __name__ == '__main__':
    bootstrap_servers = ["10.xx.12.66:9092", ]
    kafka_config = {
        "bootstrap_servers": bootstrap_servers,
        "key_serializer": None,
        "value_serializer": None,
        "acks": 0,
        "compression_type": None,
        "retries": 0,
        "batch_size": 16384,
        "linger_ms": 0
    }

    # data = json.dumps({
    #     "test": "test"
    # })
    data = "1111lxb,48,Beijing,2024-10-01 11:11:12"
    topic = 'test'

    client = KafkaClient()
    client.product(kafka_config)
    client.send(topic, value=bytes(data, encoding="utf8"), key=None)
