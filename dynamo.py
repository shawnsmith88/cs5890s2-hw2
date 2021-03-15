import boto3


class Dynamo:

    def __init__(self):
        pass

    def create(self, contents, dynamodb=None):
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
