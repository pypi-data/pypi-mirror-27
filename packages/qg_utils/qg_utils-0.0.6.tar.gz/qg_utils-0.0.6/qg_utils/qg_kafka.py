'''
module for qg_kafka
Class: QGKafkaConsumer
    It inherits from KafkaConsumer and used to stop repeated consumtion
    of messages from kafka queue.
    It stores offset of last 1000 messages from kafka and
    if current message is present in list of previsous 1000
    we skip the message and writes message in stderr file
'''
from __future__ import print_function
import sys
import time
from kafka import KafkaConsumer

class QGKafkaConsumer(KafkaConsumer):
    ''' Class for QGKafkaConsumer '''
    def __init__(self, *args, **kwargs):
        '''
        constructor for QGKafkaConsumer
        It is same as that of KafkaConsumer
        With additional feature of keeping track of last consumed offset for given
        (topic, partition) and prints message to stderr on repeat consumption of data
        '''
        super(QGKafkaConsumer, self).__init__(*args, **kwargs)
        self.repeats_found = 0
        self.topic_partition_to_last_offset = {}

    def __next__(self):
        '''
        implementing __next__ such that if a message is repeats
        we will catch it and write it to stderr
        '''
        while True:
            message = super(QGKafkaConsumer, self).__next__()
            if not self.is_repeat_message(message):
                return message

    def is_repeat_message(self, message):
        '''
        this function takes kafka message as input and checks if message is already consumed
        Logic:
            it saves offset mapped with (topic, partition)
            if current offset for message is less than previsous message for given topic, offset
            then message is repeated
        '''
        topic = message.topic
        offset = message.offset
        partition = message.partition
        self.topic_partition_to_last_offset.setdefault((topic, partition), 0)
        if self.topic_partition_to_last_offset[(topic, partition)] < offset:
            self.topic_partition_to_last_offset[(topic, partition)] = offset
            return False
        else:
            self.repeats_found += 1
            err_message = 'Message is repeated [ {} ] times'.format(self.repeats_found)
            print(err_message, file=sys.stderr)
            return True
