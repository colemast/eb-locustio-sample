import json
from locust import events

from boto import kinesis as aws_kinesis
import boto

import testdata
import time


class TimeoutError(Exception):
    pass


class KinesisClient():

    def __init__(self, region, stream_name, number_of_shards):
        # Connect to Kinesis
        self.kinesis = aws_kinesis.connect_to_region(region)
        self.stream_name = stream_name

    def put_data_in_stream(self, data, event_type):
        request_meta = {}
        request_meta["start_time"] = time.time()
        request_meta["method"] = 'Message'
        request_meta["name"] = event_type
        self.kinesis.put_record(
            self.stream_name, json.dumps(data), "partitionkey")
        request_meta["response_time"] = (
            time.time() - request_meta["start_time"]) * 1000
        events.request_success.fire(
            request_type=request_meta["method"],
            name=request_meta["name"],
            response_time=request_meta["response_time"],
            response_length=0
        )

    # def get_kinesis_data_iterator(self, minutes_running):
    #     # Get data about Kinesis stream for Tag Monitor
    #     kinesis_stream = self.kinesis.describe_stream(self.stream_name)
    #     # Get the shards in that stream
    #     shards = kinesis_stream['StreamDescription']['Shards']
    #     # Collect together the shard IDs
    #     shard_ids = [shard['ShardId'] for shard in shards]
    #     # Get shard iterator
    #     iter_response = self.kinesis.get_shard_iterator(
    #         self.stream_name, shard_ids[0], "TRIM_HORIZON")
    #     shard_iterator = iter_response['ShardIterator']

    #     while True:
    #         try:
    #             # Get data
    #             record_response = self.kinesis.get_records(shard_iterator)
    #             # Stop looping if no data returned. This means it's done
    #             if not record_response:
    #                 break
    #             # yield data to outside calling iterator
    #             for record in record_response['Records']:
    #                 last_sequence = record['SequenceNumber']
    #                 if 'Data' in record:
    #                     yield json.loads(record['Data'])
    #                 else:  # iterator is exhausted
    #                     break
    #             # Get next iterator for shard from previous request
    #             shard_iterator = record_response['NextShardIterator']
    #         # Catch exception meaning hitting API too much
    #         except boto.kinesis.exceptions.ProvisionedThroughputExceededException:
    #             print 'ProvisionedThroughputExceededException found. Sleeping for 0.5 seconds...'
    #             time.sleep(1)
    #         # Catch exception meaning iterator has expired
    #         except boto.kinesis.exceptions.ExpiredIteratorException:
    #             iter_response = self.kinesis.get_shard_iterator(
    #                 self.stream_name, shard_ids[0], "AFTER_SEQUENCE_NUMBER", last_sequence)
    #             shard_iterator = iter_response['ShardIterator']

    #     self.kinesis.close()
