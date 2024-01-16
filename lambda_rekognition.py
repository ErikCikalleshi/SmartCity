import boto3
import json
import time

def detect_labels_for_image(rekognition_client, bucket, object_key):
    try:
        response_rekognition = rekognition_client.detect_labels(   
            Image={                                                
                'S3Object': {
                    'Bucket': bucket,
                    'Name': object_key
                }
            },
            MinConfidence=70                                        
        )
        return response_rekognition
    except Exception as error:
        print(error)
        raise RuntimeError('Failed Rekognition for image')

def wait_for_video_analysis(rekognition_client, job_id):
    while True:
        response_job_status = rekognition_client.get_label_detection(JobId=job_id)
        status = response_job_status['JobStatus']
        
        if status in ['SUCCEEDED', 'FAILED']:
            break
        
        # Wait for a while before checking the status again
        time.sleep(5)
    
    return response_job_status, status

def detect_labels_for_video(rekognition_client, bucket, object_key):
    try:
        response_rekognition = rekognition_client.start_label_detection(
            Video={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': object_key
                }
            }
        )
        job_id = response_rekognition['JobId']
        
        response_job_status, status = wait_for_video_analysis(rekognition_client, job_id)
        
        if status == 'SUCCEEDED':
            return response_job_status['Labels']
        else:
            raise RuntimeError('Failed Rekognition for video')
    except Exception as error:
        print(error)
        raise RuntimeError('Failed to start label detection for video')

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    
    bucket = event['detail']['bucket']['name']
    object_key = event['detail']['object']['key']
    
    rekognition_client = boto3.client('rekognition')

    # Check if the uploaded object is an image or video
    if object_key.lower().endswith(('.jpg', '.jpeg', '.png')):
        response_rekognition = detect_labels_for_image(rekognition_client, bucket, object_key)
    elif object_key.lower().endswith(('.mp4', '.mov', '.avi')):
        response_rekognition = detect_labels_for_video(rekognition_client, bucket, object_key)
    else:
        return {
            'statusCode': 400,
            'body': 'Unsupported file format'
        }

    return {
        'statusCode': 200,
        'body': json.dumps(response_rekognition),
        'event_detail': event['detail']
    }
