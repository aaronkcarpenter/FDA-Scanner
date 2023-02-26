import logging
import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region, ACL_type):
    """
    Pick an ACL from 'private, 'public-read', 'public-read-write', 'authenticated-read'
    """
    # Create A New S3 Bucket
    try:
        s3_client = boto3.client("s3", region_name=region)
        location = {"LocationConstraint": region}
        s3_client.create_bucket(
            ACL=ACL_type, Bucket=bucket_name, CreateBucketConfiguration=location
        )
    except ClientError as e:
        print(str(e))
        return False
    return True


# Testing The Function
create_bucket("test-jmp-book-aaronkyle", "us-east-2", "private")
