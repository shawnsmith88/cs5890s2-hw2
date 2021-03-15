import boto3


class S3:

    def __init__(self):
        self.s3 = boto3.resource('s3')
        pass

    def create(self, contents, bucket, bucket2):
        client = boto3.client('s3')
        responses = []
        for content in contents:
            response = client.put_object(Body=content['body'], Bucket=bucket2, Key='widgets/' + content['owner'] + '/' + content['key'])
            responses.append(response)
            print('Created item', content['key'], 'successfully')
        return responses

    def get_all_bucket_contents(self, bucket):
        bucket_acl = self.s3.BucketAcl(bucket.name)
        contents = []
        for obj in bucket.objects.all():
            print("Reading item " + obj.key)
            dictionary = {
                'key': obj.key,
                'widget_id': obj.key,
                'owner': bucket_acl.owner['DisplayName'],
                'body': obj.get()['Body'].read(),
                'obj': obj
            }
            contents.append(dictionary)
        return contents

    def delete_all_bucket_contents(self, bucket, contents):
        for object in contents:
            print('cleaning object', object['key'])
            self.s3.Object(bucket.name, object['key']).delete()
