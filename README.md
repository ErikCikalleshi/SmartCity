# Smartcity

## Structure
All the lambda functions are within the `aws_lambdas`-folder. The workflow is provided in both, `.json` and `.yaml`- format.

The `input.json` is the mock-input for the workflow: TODO!

We provide 3 example files for the step functions, which are within the `file-examples`- folder. The datasets that we used were from kaggle:
- [violence CCTV](https://www.kaggle.com/datasets/toluwaniaremu/smartcity-cctv-violence-detection-dataset-scvd) and [violence2 CCTV](https://www.kaggle.com/datasets/mohamedmustafa/real-life-violence-situations-dataset)
- [fire CCTV](https://www.kaggle.com/datasets/ritupande/fire-detection-from-cctv)
- [smoking example](https://www.youtube.com/watch?v=36MIpHAwFSM&ab_channel=VideoForNeed-RoyaltyFreeVideos)


## How to make the project work

### 1.0-Redis Database
First of all, you need to set up a redis database on an EC2 machine. The database can simply be started using redis-server. Preferably it would be good to write a custom config file, adding a requirepass password for more security. 
Make sure to configure the inbound rules for the EC2 instance on port 6379 to be open for everyone, so that the Lambda functions can have access to the database running on your EC2 instance.

**IMPORTANT NOTE:** After some time your EC2 instance will change its name, leading to every Lambda function which connects to the database to not work since it is using an old hostname. Please always check to have the most current hostname in the Lambda functions that try to connect to the redis Database running on your EC2 instance. In every Lambda function this has also been marked using comments above the respective line of code!

### 1.1-Step Function

1. Paste the workflow.yaml in the Step Function
2. For each lambda-process you have to create the lambda function separately and paste the code 

### 1.2-Bucket & EventBridge

1. Create a bucket in S3

To trigger the whole State Machine of the Step Function you have to create an EventBridge rule that triggers the Step
Function when a file is uploaded in the bucket.

2. Create an EventBridge rule
3. Define the rule detail with the rule type as Event Pattern
4. As Event Source "AWS events or EventBridge partner events" <br>
   a. Creation method: Use pattern form <br>
   b. Event pattern
```json
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"],
  "detail": {
    "bucket": {
      "name": ["smartcity1"]
    }
  }
}
```
<br>
    &nbsp &nbsp c. Event type Specification 2: specific bucket name previously created <br> <br
5. In target select Step Function and select the State Machine previously created
6. Also use the existing "LabRole"

Now you can upload a video in the bucket and the State Machine will be triggered.

For reference, you can also follow [this](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-cloudwatch-events-s3.html) tutorial, that was also helpful for us.

# Angular x FastApi Demo

This project is just a demo project and does not contain clean code! It is just here for demo purposes.

## Requirements

First of all you need the demo project, which can be cloned from [this](https://github.com/Joe02exe/demo_ds) Repo.

Then enter the repository and install the dependencies for the backend from the requirements.txt file:

```bash
pip install -r requirements.txt
```

For the frontend, install the packages with npm:
```bash
npm install
```

Another very important thing is, that the host must be set differently, because the hostname changes after every restart. To do that, you have to go into the demo-project and then navigate to `./backend/backend.py` and change the following string accordingly (line 13):

```python
host= 'ec2-54-91-154-144.compute-1.amazonaws.com'
```

## Start the app in debug mode

Then you can start the backend with:

```bash
uvicorn backend:app
```

and to start the frontend, enter the `frontend_ds` folder and type:

```bash
ng serve
```
