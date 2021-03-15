import sys
import boto3
from dynamo import Dynamo
from s3 import S3
import time

MAX = 5


def main():
    x = 0
    while x < MAX:
        print("Consuming data...")
        consumer()
        x += 1
        time.sleep(5)


def consumer():
    if len(sys.argv) < 4:
        print('Invalid argument list. use python main.py <storage strategy> <resources> <bucket name> [bucket 2 name]')
        exit(-1)
    strategy = sys.argv[1]
    resources = sys.argv[2]
    bucket_name = sys.argv[3]
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    dynamo_service = Dynamo()
    s3_service = S3()

    if strategy.upper() == "CREATE":
        if resources.upper() == "DYNAMO":
            contents = s3_service.get_all_bucket_contents(bucket)
            print(dynamo_service.create(contents))
            s3_service.delete_all_bucket_contents(bucket, contents)
        if resources.upper() == "S3":
            if len(sys.argv) < 5:
                print('Invalid argument list. s3 resource requires two buckets use python main.py <storage strategy> '
                      's3 <bucket name> <bucket 2 name>')
                exit(-1)
            bucket2 = sys.argv[4]
            contents = s3_service.get_all_bucket_contents(bucket)
            print(s3_service.create(contents, bucket, bucket2))
            s3_service.delete_all_bucket_contents(bucket, contents)


if __name__ == '__main__':
    main()
