# Smartcity

## How to make the project work

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

Now you can upload a video in the bucket and the State Machine will be triggered

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

## Start the app in debug mode

Then you can start the backend with:

```bash
uvicorn backend:app
```

and to start the frontend, enter the `frontend_ds` folder and type:

```bash
ng serve
```