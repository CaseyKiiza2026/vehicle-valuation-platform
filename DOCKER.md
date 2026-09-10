# Docker and API Deployment

The frozen V1 LightGBM model and preprocessing pipeline are served through FastAPI, packaged in Docker, stored in Amazon ECR, and deployed using Amazon ECS.

## Run Locally with Docker

From the project root, build the image:

```bash
docker build -t vehicle-api .
```

Run the container:

```bash
docker run --rm -p 8000:8000 vehicle-api
```

Open the interactive API documentation:

[http://localhost:8000/docs](http://localhost:8000/docs)

To test the model:

1. Open `POST /predict`.
2. Click **Try it out**.
3. Copy a vehicle from [Test Examples](Test_examples/demo_examples.md).
4. Paste the JSON into the request body.
5. Click **Execute**.

Press `Ctrl+C` in the terminal to stop the container.

## Push the Image to Amazon ECR

AWS region: `us-east-2`

Authenticate Docker with Amazon ECR:

```bash
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 927709485681.dkr.ecr.us-east-2.amazonaws.com
```

Tag the image:

```bash
docker tag vehicle-api:latest 927709485681.dkr.ecr.us-east-2.amazonaws.com/vehicle-api:latest
```

Push the image:

```bash
docker push 927709485681.dkr.ecr.us-east-2.amazonaws.com/vehicle-api:latest
```

## Amazon ECS Deployment

The ECR image is deployed through the Amazon ECS Express service `vehicle-api-2e44` in the `default` cluster.

**Live API:**  
[https://ve-243aeac9ad8141ecaa6bd9ae8ed5af86.ecs.us-east-2.on.aws/docs](https://ve-243aeac9ad8141ecaa6bd9ae8ed5af86.ecs.us-east-2.on.aws/docs)

The deployment provides a public HTTPS endpoint while the model and preprocessing artifacts remain packaged inside the container.

## Updating the Deployment

After changing the API or inference code:

```bash
docker build -t vehicle-api .
docker tag vehicle-api:latest 927709485681.dkr.ecr.us-east-2.amazonaws.com/vehicle-api:latest
docker push 927709485681.dkr.ecr.us-east-2.amazonaws.com/vehicle-api:latest
```

After pushing the updated image, open the ECS service and trigger a new deployment.