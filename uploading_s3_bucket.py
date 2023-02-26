import boto3


def s3_upload(s3_bucket_name, local_filename, s3_keyname):
    s3 = boto3.client("s3")

    for attempt in range(1, 6):
        # Files automatically and upload parts in parallel.
        try:
            s3.upload_file(local_filename, s3_bucket_name, s3_keyname)
        except Exception as e:
            print(str(e))
        else:
            print("Finished Uploading To S3 In Attempt", attempt)
            break


# Testing
s3_upload("test-jmp-book-aaronkyle", "requirements.txt", "upload_test.pdf")
