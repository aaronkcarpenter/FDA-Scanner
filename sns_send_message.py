import boto3
import create_sns_topic_and_sns_queue

client = boto3.client("sns", region_name="us-east-2")
response = client.publish(
    TopicArn=create_sns_topic_and_sns_queue.response_dict["snsTopicArn"],
    Message="This is a Test of SNS and SQS Yessuhhh",
    Subject="Test_SNS_SQS_BROTHA!",
    MessageStructure="string",
)
