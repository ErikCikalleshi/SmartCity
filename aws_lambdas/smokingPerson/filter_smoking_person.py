import json
import boto3

def find_first_matching_elements(list1, list2):
    for element in list1:
        if element in list2:
            return element
    return None
    

def lambda_handler(event, context):
    labels = json.loads(event['body'])
    event_detail = event.get('event_detail', {})
    object_info = event_detail.get('object', {})
        
    bucket = event_detail.get('bucket', {}).get('name')
    object_key = object_info.get('key')
        
    video_path = f"s3://{bucket}/{object_key}" if bucket and object_key else None
    

    person_labels = ['Person']
    smoking_labels = ['Smoke Pipe', 'Cigarette']

    person_present = any(label['Label']['Name'] in person_labels and label['Label']['Confidence'] > 70  for label in labels)
    smoking_present = any(label['Label']['Name'] in smoking_labels and label['Label']['Confidence'] > 70  for label in labels)
    smoking_person = person_present and smoking_present
    
    presigned_url = generate_presigned_url(bucket,object_key)
    return {
        'personSmoking': smoking_person,
        'pathToVideo' : presigned_url,
    }
    
    
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