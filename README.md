## Deploy
```bash
sam build
sam package --s3-bucket <s3-bucket> --output-template-file .aws-sam/out.yaml --profile XXXX
sam deploy --template-file .aws-sam/out.yaml --stack-name sam-app --capabilities CAPABILITY_NAMED_IAM  --profile XXXX
```