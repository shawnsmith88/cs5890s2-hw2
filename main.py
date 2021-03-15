import sys
import boto3


def consumer():
    if len(sys.argv) < 4:
        print('Invalid argument list. use python main.py <storage strategy> <resources> <bucket name> [bucket 2 name]')
        exit(-1)
    strategy = sys.argv[1]
    resources = sys.argv[2]
    bucket_name = sys.argv[3]
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    if strategy.upper() == "CREATE":
        if resources.upper() == "DYNAMO":
            create_dynamo(get_all_bucket_contents(bucket))
            delete_all_bucket_contents(bucket)
        if resources.upper() == "S3":
            if len(sys.argv) < 5:
                print('Invalid argument list. s3 resource requires two buckets use python main.py <storage strategy> '
                      's3 <bucket name> <bucket 2 name>')
                exit(-1)
            bucket2 = sys.argv[4]
            create_s3(s3, bucket, bucket2)


def create_s3(s3, bucket, bucket2):
    client = boto3.client('s3')
    contents = get_all_bucket_contents(bucket)
    for content in contents:
        client.put_object(Body=content['body'], Bucket=bucket2, Key=content['key'])
        print('Created item', content['key'], 'successfully')


def create_dynamo(contents, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('widgets')
    for content in contents:
        response = table.put_item(
            Item={
                'widget_id': content['key'],
                'contents': content['body'],
                'owner': 'boto3'
            }
        )
        print('Created item', content['key'], 'successfully')


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

