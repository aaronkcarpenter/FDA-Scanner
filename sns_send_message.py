import boto3
import os
from dotenv import load_dotenv
import create_sns_topic_and_sns_queue

load_dotenv()
client = boto3.client("sns", region_name=os.environ['REGION_NAME'])
response = client.publish(
    TopicArn=create_sns_topic_and_sns_queue.response_dict["snsTopicArn"],
    Message="This is a Test of SNS and SQS 1",
    Subject="Test_SNS_SQS_AGAIN!",
    MessageStructure="string",
)
