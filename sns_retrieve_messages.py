import boto3
import json
import create_sns_topic_and_sns_queue
import sns_send_message

sqs = boto3.client("sqs", region_name="us-east-2")
sns = boto3.client("sns", region_name="us-east-2")

sqsResponse = sqs.receive_message(
    QueueUrl=create_sns_topic_and_sns_queue.response_dict["sqsQueueUrl"],
    MessageAttributeNames=["ALL"],
    MaxNumberOfMessages=10,
    WaitTimeSeconds=10,
)

# Parsing SQS Messages
sqsResponse["Messages"]

if "Messages" in sqsResponse:
    for message in sqsResponse["Messages"]:
        message_dict = json.loads(message["Body"])
        message_text = message_dict["Message"]
        subject_text = message_dict["Subject"]
        message_id = message_dict["MessageId"]
        receipt_handle = message["ReceiptHandle"]

        print(f"receipt_handle: {receipt_handle}")
        print(f"message_id: {message_id}")
        print(f"subject_text: {subject_text}")
        print(f"message_text: {message_text}")


# Delete Messages By Receipt Handle
response = sqs.delete_message(
    QueueUrl=create_sns_topic_and_sns_queue.response_dict["sqsQueueUrl"],
    ReceiptHandle=receipt_handle,
)

# Deleting An SNS and SQS Queue
sqs.delete_queue(QueueUrl=create_sns_topic_and_sns_queue.response_dict["sqsQueueUrl"])
sns.delete_topic(TopicArn=create_sns_topic_and_sns_queue.response_dict["snsTopicArn"])
