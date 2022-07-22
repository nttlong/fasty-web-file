import threading

import boto3
import botocore
from botocore.client import Config
__client__ = None
__lock__ = threading.Lock()
__session__ = None
class S3Stream:
    def __init__(self,
                 aws_access_key_id:str,
                 aws_secret_access_key:str,
                 bucket_name:str,
                 res_path:str):
        global __session__

        self.aws_access_key_id=aws_access_key_id
        self.aws_secret_access_key= aws_secret_access_key
        self.bucket= bucket_name
        self.res_path = res_path
        if __session__ is None:
            __lock__.acquire()
            try:
                __session__ = boto3.Session(
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key
                    )
            finally:
                __lock__.release()

        self.session = __session__
        global __client__
        if __client__ is None:
            __lock__.acquire()
            try:
                __client__= __session__.client('s3')
            finally:
                __lock__.release()
        # self.config = Config(connect_timeout=15, retries={'max_attempts': 10})
        self.client = __client__
        self.position=0
        self.data:dict= self.client.get_object(Bucket=self.bucket, Key=self.res_path)
        self._size =int(self.data['ResponseMetadata']['HTTPHeaders']['content-length'])
        self.res_body:botocore.response.StreamingBody = self.data['Body']


        # fx.get_object(Bucket=self.bucket, Key=self.res_path)['ResponseMetadata']
        # {'RequestId': 'N5CJCQRATY1F0RZJ',
        #  'HostId': 'ZSa8+m1byTsHRb1y8M/tg+OZR1cuJt2UgFm47OAdLcMpm+TM+NEu2/N4GpPpINc08SGnUegvj8Q=',
        #  'HTTPStatusCode': 200,
        #  'HTTPHeaders': {'x-amz-id-2': 'ZSa8+m1byTsHRb1y8M/tg+OZR1cuJt2UgFm47OAdLcMpm+TM+NEu2/N4GpPpINc08SGnUegvj8Q=',
        #                  'x-amz-request-id': 'N5CJCQRATY1F0RZJ', 'date': 'Thu, 28 Jul 2022 02:30:34 GMT',
        #                  'last-modified': 'Wed, 27 Jul 2022 10:28:59 GMT',
        #                  'etag': '"9e2cb27565f3a77c3c0d253da60bd76a-18"', 'accept-ranges': 'bytes',
        #                  'content-type': 'binary/octet-stream', 'server': 'AmazonS3', 'content-length': '939279446'},
        #  'RetryAttempts': 0}
        # fx.get_object(Bucket=self.bucket, Key=self.res_path)['ResponseMetadata']['HTTPHeaders']
        # {'x-amz-id-2': '3XrZ9aM1p4o4VKk6WvxkdyMN5t1RB1j3nfnKzpcGbjkL9pUDTnELEsmng7gGztw9zkevvgVY/FI=',
        #  'x-amz-request-id': 'QRZ7QJASPFN5MNS4', 'date': 'Thu, 28 Jul 2022 02:30:48 GMT',
        #  'last-modified': 'Wed, 27 Jul 2022 10:28:59 GMT', 'etag': '"9e2cb27565f3a77c3c0d253da60bd76a-18"',
        #  'accept-ranges': 'bytes', 'content-type': 'binary/octet-stream', 'server': 'AmazonS3',
        #  'content-length': '939279446'}
        # fx.get_object(Bucket=self.bucket, Key=self.res_path)['ResponseMetadata']['HTTPHeaders']['content-length']
        # '939279446'
    def seek(self,offset:int):
        self.position+=offset
        return self
    def size(self)->int:
        if self._size is None:
            str_size = self.client.get_object(Bucket=self.bucket, Key=self.res_path)['ResponseMetadata']['HTTPHeaders']['content-length']
            self._size= int(str_size)
        return self._size
    def tell(self)->int:
        return self.position
    def close(self):
        pass
    def read(self,read_size=None):
        _session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
        __client = _session.client('s3')
        if  read_size is None:
            read_size = self.size()
        start= self.position
        end = min(self.size(),self.position+read_size)
        Bytes_range = f'bytes={start}-{end}'
        if start>=end:
            return b''
        print(Bytes_range)
        # client = self.session.client('s3')
        resp = __client.get_object(Bucket=self.bucket, Key=self.res_path, Range=Bytes_range)
        res_body: botocore.response.StreamingBody = resp['Body']
        data = res_body.iter_chunks(read_size)
        for x in data:
            yield x
        res_body.close()


def open_s3_stream(
        aws_access_key_id:str,
        aws_secret_access_key:str,
        bucket_name:str,
        res_path:str

)->S3Stream:
    ret= S3Stream(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        bucket_name=bucket_name,
        res_path=res_path
    )
    return ret