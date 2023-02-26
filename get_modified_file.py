import boto3
from datetime import datetime


def get_last_mod_file(s3bucketname, file_type=None, substring_to_match=""):
    """
    Querying the last modified file in an s3 bucket. You can filter the file by extension type and substring search
    """
    s3 = boto3.resource("s3")
    my_bucket = s3.Bucket(s3bucketname)
    last_modified_date = datetime(1939, 9, 1).replace(tzinfo=None)

    if any(my_bucket.objects.all()) is False:
        last_modified_file = "None"

    for file in my_bucket.objects.all():
        print(file.key)

        file_date = file.last_modified.replace(tzinfo=None)
        file_name = file.key
        print(file_date, file.key)

        if file_type is None:
            if last_modified_date < file_date and substring_to_match in file_name:
                last_modified_date = file_date
                last_modified_file = file_name
        else:
            if (
                last_modified_date < file_date
                and substring_to_match in file_name
                and file_type == file_name.split(".")[-1]
            ):
                last_modified_date = file_date
                last_modified_file = file_name
    return last_modified_file
