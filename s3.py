import boto3


class S3:

    def __init__(self):
        pass

    def create(self, s3, bucket, bucket2):
        client = boto3.client('s3')
        contents = get_all_bucket_contents(bucket)
        for content in contents:
            client.put_object(Body=content['body'], Bucket=bucket2, Key=content['key'])
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
