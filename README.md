## Template.yaml
以下の環境変数を書き換え。

CHANNEL_ACCESS_TOKEN: \<channel-access-token\> ←Line botチャンネルのチャンネルアクセストークンを設定する。

LINE_USER_ID: \<line-user-id\> ←Line botチャンネルのユーザーIDを設定する。

LINE_CHANNEL_SECRET: \<line-channel-secret\> ←Line botチャンネルのチャンネルシークレットを設定する。

DeviceId: \<deviceid\> ←AWS IoT 1-Clickサービスに登録したデバイスのIDを設定する。

## Deploy
```bash
sam build
sam package --s3-bucket <s3-bucket> --output-template-file .aws-sam/out.yaml --profile XXXX
sam deploy --template-file .aws-sam/out.yaml --stack-name sam-app --capabilities CAPABILITY_NAMED_IAM  --profile XXXX
```
