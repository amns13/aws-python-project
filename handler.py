import io
from datetime import datetime
import json
import boto3
from cgi import FieldStorage

BUCKET_NAME = "serverless-demo-bucket-amns"

def download_file(event, context):
    file_key = event['pathParameters']['key']
    client = boto3.client('s3')
    response =  client.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': file_key})
    return {"statusCode": 200, "body": json.dumps(response)}

def upload_file(event, context):
    client = boto3.client('s3')
    fs = FieldStorage(
        fp=io.BytesIO(str.encode(event['body'])),
        environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':event['headers']['Content-Type'], }
    )['file']
    originalFileName = fs.filename
    content_type = fs.type
    binaryFileData = fs.file.read().decode()
    response = client.put_object(Body=binaryFileData, Bucket=BUCKET_NAME, Key=f"{str(datetime.timestamp(datetime.now())).replace('.', '')}_{originalFileName}", ContentType=content_type)
    body = {
        "message": "Successful"
    }

    return {"statusCode": 200, "body": json.dumps(body)}

def file_list(event, context):
    client = boto3.client('s3')
    file_details = client.list_objects(Bucket=BUCKET_NAME)
    file_keys = {"keys": [f["Key"] for f in file_details["Contents"]]}
    return {"statusCode": 200, "body": json.dumps(file_keys)}
