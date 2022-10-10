import json
import boto3

BUCKET_NAME = "serverless-demo-bucket-amns"

def get_presigned_url(key, upload=False):
    client = boto3.client('s3')
    response =  client.generate_presigned_url('put_object' if upload else 'get_object', Params={'Bucket': BUCKET_NAME, 'Key': key})
    return {"statusCode": 200, "body": json.dumps(response)}

def download_file(event, context):
    return get_presigned_url(event['pathParameters']['key'])

def upload_file(event, context):
    return get_presigned_url(event['pathParameters']['key'], upload=True)

def file_list(event, context):
    client = boto3.client('s3')
    file_details = client.list_objects(Bucket=BUCKET_NAME)
    file_keys = {"keys": [f["Key"] for f in file_details["Contents"]]}
    return {"statusCode": 200, "body": json.dumps(file_keys)}
