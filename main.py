import sys
import boto3
from dynamo import Dynamo
from s3 import S3


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
            dynamo_service.create(get_all_bucket_contents(bucket))
            delete_all_bucket_contents(bucket)
        if resources.upper() == "S3":
            if len(sys.argv) < 5:
                print('Invalid argument list. s3 resource requires two buckets use python main.py <storage strategy> '
                      's3 <bucket name> <bucket 2 name>')
                exit(-1)
            bucket2 = sys.argv[4]
            s3_service.create(s3, bucket, bucket2)
            delete_all_bucket_contents(bucket)


def get_all_bucket_contents(bucket):
    contents = []
    for obj in bucket.objects.all():
        dictionary = {
            'key': obj.key,
            'body': obj.get()['Body'].read()
        }
        contents.append(dictionary)
    return contents


def delete_all_bucket_contents(bucket):
    bucket.objects.all().delete()


if __name__ == '__main__':
    consumer()

