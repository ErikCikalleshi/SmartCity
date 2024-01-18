#IMPORTANT: This Lambda function has to have a layer containing a Redis installation.
import redis
import json
import uuid
from datetime import datetime as dt
def storeInDB(description, path):
    # Establish connection and update hostname if needed
    redis_client = redis.StrictRedis(host='ec2-3-80-119-167.compute-1.amazonaws.com', port=6379, password='1SQRr7hyIb7peXvdcT4pSV3iu7lykHVd2qmMm+aOUBvC/Xt3vuLCzNg2QkSztjdY')

    unique_event_id = str(uuid.uuid4())
    current_time = str(dt.now())
    event_data = {
    "eventId": unique_event_id,
    "eventType": "Fire",
    "timestamp": current_time,
    "description": description,
    "videoPath": path,
    }

    # Build the key for the event
    event_key = f"{event_data['eventType']}:{event_data['eventId']}"

    # Store the event in Redis
    redis_client.hset("firedepartment_reports", event_key, json.dumps(event_data))

def lambda_handler(event, context):
    pathToVideo = event.get('pathToVideo')
    description = "Fire detected"
    storeInDB(description, pathToVideo)