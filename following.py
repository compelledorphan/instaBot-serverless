import json
from Instagram import InstagramAPI
import time, random, os, sys, datetime
import boto3

dynamoClient = boto3.resource('dynamodb')
accountTable = dynamoClient.Table('accountTable')
instaTable = dynamoClient.Table('instaTable')

def following(event, context):
    username = os.environ['username']
    password = os.environ['password']

    RandomItem = instaTable.scan(
        ProjectionExpression = "pk"
    )
    print(random.choice(RandomItem['Items'])['pk'])

    print(datetime.datetime.now().date())

    account = accountTable.get_item(
        Key={
        'date': str(datetime.datetime.now().date()), 'username': username
        }
    )
    print(account)
 
    try:
        print(account['Item'])
    except KeyError:
        Item = {
            'date': str(datetime.datetime.now().date()),
            'username': username,
            'followed': 0,
            'comments': 0,
            'unfollowed': 0,
            'likes': 0,
            'blocked': False
        }
        accountTable.put_item(Item=Item)
        return
    
    if account['Item']['followed'] >= 100:
        return
    else:
        api = InstagramAPI("npmScripts", "npmScripts8611")
        api.login()
        print(api.follow(int(random.choice(RandomItem['Items'])['pk'])))
        print("FOLLOWINGS=================")
        api.getSelfUsersFollowing()
        print(len(api.LastJson['users']))
        print("FOLLOWERS=================")
        api.getSelfUserFollowers()
        print(len(api.LastJson['users']))
        response = accountTable.update_item(
            Key={
                'date': str(datetime.datetime.now().date()), 'username': username
            },
            AttributeUpdates={
                'followed': {
                    'Value': 1,
                    'Action': 'ADD'
                }
            }
        )