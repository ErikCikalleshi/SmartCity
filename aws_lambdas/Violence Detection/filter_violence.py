import json
import boto3
def generate_presigned_url(bucket, object_key):
    s3_client = boto3.client('s3')
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': object_key},
            ExpiresIn=720
        )
        return url
    except ClientError as e:
        print(f"Error generating pre-signed URL: {e}")
        return None

def lambda_handler(event, context):
    labels = json.loads(event['body'])
    event_detail = event.get('event_detail', {})
    object_info = event_detail.get('object', {})

    bucket = event_detail.get('bucket', {}).get('name')
    object_key = object_info.get('key')
            
    violent_labels = ['Fighting', 'Kicking', 'Riot', 'Vandalism']
    fighting_present = any(label['Label']['Name'] in violent_labels for label in labels)
    
    presigned_url = generate_presigned_url(bucket,object_key)
    return {
        'fightingPresent': fighting_present,
        'pathToVideo' : presigned_url
    }
