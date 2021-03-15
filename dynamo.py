import boto3


class Dynamo:

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def create(self, contents, dynamodb=None):
        if not dynamodb:
            dynamodb = self.dynamodb
        table = dynamodb.Table('widgets')
        responses = []
        for content in contents:
            response = table.put_item(
                Item={
                    'widget_id': content['widget_id'],
                    'contents': content['body'],
                    'owner': content['owner']
                }
            )
            responses.append(response)
            print('Created item', content['key'], 'successfully')
        return responses
