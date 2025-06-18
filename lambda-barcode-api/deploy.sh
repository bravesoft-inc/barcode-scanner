#!/bin/bash

# 環境変数設定
ENVIRONMENT=${1:-dev}
REGION=${2:-ap-northeast-1}
STACK_NAME="barcode-scanner-api-${ENVIRONMENT}"

echo "Deploying to environment: ${ENVIRONMENT}"
echo "Region: ${REGION}"

# Python依存関係の準備
echo "Preparing Python dependencies..."
cd layers/python-libs
pip install -r requirements.txt -t python/
cd ../..

# SAM build
echo "Building SAM application..."
sam build

# SAM deploy
echo "Deploying SAM application..."
sam deploy \
  --stack-name ${STACK_NAME} \
  --region ${REGION} \
  --parameter-overrides Environment=${ENVIRONMENT} \
  --capabilities CAPABILITY_IAM \
  --resolve-s3 \
  --confirm-changeset

# API URLの取得
echo "Getting API URL..."
API_URL=$(aws cloudformation describe-stacks \
  --stack-name ${STACK_NAME} \
  --region ${REGION} \
  --query 'Stacks[0].Outputs[?OutputKey==`BarcodeApi`].OutputValue' \
  --output text)

echo "Deployment complete!"
echo "API URL: ${API_URL}"
echo ""
echo "Update your React app's .env file:"
echo "REACT_APP_API_URL=${API_URL}" 