import boto3
import json
import sys
import time

def create_topic_and_queue(topic_name, email_address):
    sqs = boto3.client('sqs')
    sns = boto3.client('sns')
    millis = str(int(round(time.time() * 1000)))
    
    # Create An SNS Topic
    sns_topic_name = topic_name + millis