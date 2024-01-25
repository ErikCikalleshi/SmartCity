import redis
import json
import uuid
from datetime import datetime as dt

def storeInDB(description, path):
    # Establish connection
    redis_client = redis.StrictRedis(host='ec2-52-54-106-54.compute-1.amazonaws.com', port=6379, password='1SQRr7hyIb7peXvdcT4pSV3iu7lykHVd2qmMm+aOUBvC/Xt3vuLCzNg2QkSztjdY')

    unique_event_id = str(uuid.uuid4())
    current_time = str(dt.now())
    event_data = {
    "eventId": unique_event_id,
    "eventType": "SmokingPerson",
    "timestamp": current_time,
    "description": description,
    "videoPath": path,
    }

    # Build the key for the event
    event_key = f"{event_data['eventType']}:{event_data['eventId']}"

    # Store the event in Redis
    redis_client.hset("smokingPerson", event_key, json.dumps(event_data))

def lambda_handler(event, context):
    pathToVideo = event.get('pathToVideo')
    description = "detected a smoking Person"
    storeInDB(description, pathToVideo)
    