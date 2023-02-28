import boto3
import json
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()
def create_topic_and_queue(topic_name, email_address):
    sqs = boto3.client("sqs", region_name=os.environ['REGION_NAME'])
    sns = boto3.client("sns", region_name=os.environ['REGION_NAME'])
    millis = str(int(round(time.time() * 1000)))

    # Create An SNS Topic
    sns_topic_name = topic_name + millis

    topic_response = sns.create_topic(Name=sns_topic_name)
    snsTopicArn = topic_response["TopicArn"]

    # Subscribe Email_Address to SNS Topic
    if email_address is not None:
        email_response = sns.subscribe(
            TopicArn=snsTopicArn,
            Protocol="email",
            Endpoint=email_address,
            ReturnSubscriptionArn=True,
        )
        emailArn = email_response["SubscriptionArn"]
    else:
        emailArn = None

    # Create SQS Queue
    sqsQueueName = topic_name + millis
    sqs.create_queue(QueueName=sqsQueueName)
    sqsQueueUrl = sqs.get_queue_url(QueueName=sqsQueueName)["QueueUrl"]

    attribs = sqs.get_queue_attributes(
        QueueUrl=sqsQueueUrl, AttributeNames=["QueueArn"]
    )["Attributes"]

    sqsQueueArn = attribs["QueueArn"]

    # Subscribe SQS Queue to SNS topic
    sns.subscribe(TopicArn=snsTopicArn, Protocol="sqs", Endpoint=sqsQueueArn)

    # Authorize SNS to Write SQS Queue
    policy = """{{
        "Version": "2012-10-17",
        "Statement": [
            {{
                "Sid": "MyPolicy",
                "Effect": "Allow",
                "Principal": {{ "AWS" : "*"}},
                "Action": "SQS:SendMessage",
                "Resource": "{}",
                "Condition": {{
                    "ArnEquals":{{
                        "aws:SourceArn": "{}"
                    }}
                }}    
            }}
        ]
    }}""".format(
        sqsQueueArn, snsTopicArn
    )

    response = sqs.set_queue_attributes(
        QueueUrl=sqsQueueUrl, Attributes={"Policy": policy}
    )

    return {
        "snsTopicArn": snsTopicArn,
        "sqsQueueArn": sqsQueueArn,
        "sqsQueueUrl": sqsQueueUrl,
        "emailArn": emailArn,
    }


response_dict = create_topic_and_queue(os.environ['TOPIC_NAME'], os.environ['EMAIL_ADDRESS'])
