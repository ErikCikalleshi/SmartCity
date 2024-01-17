import json
import boto3

def find_first_matching_elements(list1, list2):
    for element in list1:
        if element in list2:
            return element
    return None
    
    
def find_first_smoking_frame(labels):
    first_smoking_frame = None
    person_frames = []
    smoking_frames = []
    
    for label in labels:
        timestamp = label['Timestamp']
        if 'Person' in label['Label']['Name']:
            person_frames.append(timestamp)
            
    for label in labels:
        timestamp = label['Timestamp']
        if 'Smoking' in label['Label']['Name']:
            smoking_frames.append(timestamp)

    return find_first_matching_elements(person_frames, smoking_frames)
    

def lambda_handler(event, context):
    labels = json.loads(event['body'])
    event_detail = event.get('event_detail', {})
    object_info = event_detail.get('object', {})
        
    bucket = event_detail.get('bucket', {}).get('name')
    object_key = object_info.get('key')
        
    video_path = f"s3://{bucket}/{object_key}" if bucket and object_key else None
    
    frame = find_first_smoking_frame(labels)
    isSmoking = True if frame is not None else False

    person_labels = ['Person']
    smoking_labels = ['Smoking']
    person_present = any(label['Label']['Name'] in person_labels and label['Label']['Confidence'] > 70  for label in labels)
    smoking_present = any(label['Label']['Name'] in smoking_labels and label['Label']['Confidence'] > 70  for label in labels)
    smoking_person = person_present and smoking_present
    
    presigned_url = generate_presigned_url(bucket,object_key)
    
    return {
        'personSmoking': isSmoking,
        'pathToVideo' : presigned_url,
        'smokingFrame' : frame
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