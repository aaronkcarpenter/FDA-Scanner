import boto3

s3 = boto3.client("s3")
bucket_name = "test-jmp-book-aaronkyle"
key_name = "upload_test.pdf"

response = s3.delete_object(Bucket=bucket_name, Key=key_name)


def delete_all_objects(bucket_name):
    """Delete all files/keys in an object/bucket"""
    result = []
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    for obj_version in bucket.object_versions.all():
        result.append({"Key": obj_version.object_key, "VersionId": obj_version.id})

    print(result)
    bucket.delete_object(Delete={"Objects": result})


def delete_bucket(bucket_name):
    """Delete a Specific Bucket and deleting files in the bucket beforehand if necessary"""
    s3 = boto3.resource("s3")
    my_bucket = s3.Bucket(bucket_name)

    if any(my_bucket.objects.all()) is True:
        delete_all_objects(bucket_name)

    my_bucket.delete()
    return True


# testing deletion of an object/bucket
delete_bucket("test-jmp-book-aaronkyle")
