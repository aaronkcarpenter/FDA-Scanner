import boto3


def list_buckets():
    """List All Current S3 Buckets"""
    s3 = boto3.client("s3")
    response = s3.list_buckets()

    for bucket in response["Buckets"]:
        print({bucket["Name"]})
        print("*" * 20)


# Testing
list_buckets()
