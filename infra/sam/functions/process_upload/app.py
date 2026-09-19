"""Lambda function: Process document upload from S3."""
import json
import urllib.parse


def handler(event, context):
    """Handle S3 upload notifications.

    When a document is uploaded to the S3 bucket, this Lambda
    queues it for processing in the Firecracker sandbox.
    """
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        size = record["s3"]["object"].get("size", 0)

        print(f"New document uploaded: s3://{bucket}/{key} ({size} bytes)")

        # In production: send to SQS for Firecracker processing
        processing_message = {
            "bucket": bucket,
            "key": key,
            "size": size,
            "action": "extract_document",
        }

        print(f"Queued for processing: {json.dumps(processing_message)}")

    return {"statusCode": 200, "body": "Upload processed"}
