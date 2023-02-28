import boto3
import io
import os
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import create_sns_topic_and_sns_queue

load_dotenv()
def s3_upload(s3_bucket_name, local_filename, s3_keyname):
    s3 = boto3.client("s3")

    for attempt in range(1, 6):
        try:
            # Files automatically and upload parts in parallel
            s3.upload_file(local_filename, s3_bucket_name, s3_keyname)
        except Exception as e:
            print(str(e))
        else:
            print("Finished uploading to s3 in attempt", attempt)

            break

def get_abs_url(html_tag):
    soup = BeautifulSoup(html_tag, "lxml")
    custom_url = soup.find("a")["href"]
    abs_url = os.environ['ABS_URL'] + custom_url
    print(abs_url)
    company_name = soup.find("a").get_text()
    return abs_url, company_name


if __name__ == "__main__":
    my_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        + " (KHTML, like Gecko) Chrome/61.0.3163.100Safari/537.36"
    }
    test_url = os.environ["TEST_URL"]
    r = requests.get(url=test_url, headers=my_headers)
    print(f"Request Code {r.status_code}")
    html_response = r.text
    string_json2 = io.StringIO(html_response)
    df = pd.read_json(string_json2)
    df["abs_url"], df["company_name"] = zip(
        *df["field_company_name_warning_lette"].apply(get_abs_url)
    )
    df.to_csv(os.environ['LOCAL_FILENAME'])
    s3_keyname = os.environ['S3_KEYNAME']
    local_filename = os.environ['LOCAL_FILENAME']
    s3bucket_name = os.environ['S3BUCKET_NAME']
    s3_upload(s3bucket_name, local_filename, s3_keyname)

    # Send a Message Through SNS
    message_test = f"{s3_keyname} successfully uploaded to {s3bucket_name}"
    client = boto3.client("sns", region_name="us-east-2")
    response = client.publish(
        TopicArn=create_sns_topic_and_sns_queue.response_dict["snsTopicArn"],
        Message=message_test,
        Subject="S3 Upload Successful",
        MessageStructure="string",
    )
