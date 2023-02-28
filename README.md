# FDA Warning Tracker
Cloud-based(EC2) system built to scrape data, store it(S3), and send notification(SQS, SNS) of completed jobs.

### Dependencies
***
- boto3
- numpy
- pandas
- beautifulsoup4
- lxml


### Technologies Utilized
***
- Python 3.11
- AWS EC2
- AWS SNS
- AWS SQS
- AWS IAM
- AWS S3
- AWS Secrets Manager

### Local Testing
***
```
pip install -r requirements.txt
python3 scraper.py
```

### Production
***
- Log into your EC2 instance from the command line
- Once logged in, upload the necessary files and python packages to run the script

