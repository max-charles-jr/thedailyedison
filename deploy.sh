#!/usr/bin/env bash
# Deployment runbook for The Daily Thomas Edison.
set -euo pipefail

AWS_REGION=us-east-1
ECR_REPO=edison-blog
IMAGE_TAG=$(git rev-parse --short HEAD)
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
IMAGE_URI="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"

# 1. Build and push the container image to ECR.
aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin \
    "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
docker build -t "$IMAGE_URI" .
docker push "$IMAGE_URI"

# 2. Deploy / update the infrastructure stack.
aws cloudformation deploy \
  --stack-name edison-blog \
  --template-file infra/cloudformation.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
      ContainerImage="$IMAGE_URI" \
      KeyPairName=edison-key

# 3. Run migrations and seed via a one-off task on an app instance.
INSTANCE=$(aws autoscaling describe-auto-scaling-instances \
  --query 'AutoScalingInstances[0].InstanceId' --output text)
aws ssm send-command \
  --instance-ids "$INSTANCE" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["docker exec edison python manage.py migrate --noinput"]'

# 4. Sync static assets to S3 for the CloudFront static origin.
python manage.py collectstatic --noinput
aws s3 sync staticfiles/ s3://edison-static-assets/ --delete

echo "Deployment complete: $IMAGE_URI"
