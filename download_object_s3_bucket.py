import boto3
import logging
from botocore.exceptions import ClientError


def download_file_from_s3(s3bucketname, s3_keyname, local_filename):
    """Download a file from s3 bucket"""
    s3 = boto3.resource("s3")

    for attempt in range(1, 6):
        try:
            s3.meta.client.download_file(s3bucketname, s3_keyname, local_filename)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print("The object doesn't exist.")
        except Exception as e:
            print(e)
            logging.info(str(e))
        else:
            print("Downloaded Successfully in Attempt", attempt)

            break


# Testing
download_file_from_s3(
    "test-jmp-book-aaronkyle", "upload_test.pdf", "download_test_aaron.pdf"
)
