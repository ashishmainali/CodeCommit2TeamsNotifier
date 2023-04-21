# AWS CodeCommit Notifications with Microsoft Teams

This project provides a Lambda function that sends notifications to a Microsoft Teams channel whenever there's a change in an AWS CodeCommit repository. The notifications are triggered by events from AWS SNS, which are delivered to an SNS topic that the Lambda function is subscribed to.

## Prerequisites

- An AWS account
- An AWS CodeCommit repository
- A Microsoft Teams channel
- Python 3.7 or later
- [AWS CLI](https://aws.amazon.com/cli/) **optional**
- [SAM CLI](https://aws.amazon.com/serverless/sam/) **optional**

## Setup

1. Clone this repository and navigate to the root directory.

2. Create an SNS topic in the AWS Console and take note of its ARN.

3. Subscribe the SNS topic to the following CodeCommit events:

   - `CodeCommit Comment on Pull Request`
   - `CodeCommit Repository State Change`
   - `CodeCommit Pull Request State Change`

4. Create a webhook for your Microsoft Teams channel by following [these instructions](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook).

5. Create a lambda function with Python run time environment of 3.x

6. Paste the code in your lambda function. 

8. Export the webhook URL as an environment variable in your lambda environment:

   ```
   export TEAMS_WEBHOOK_URL_TEST=<your_teams_webhook_url>
   ```

6. Deploy the Lambda function.
   ```

7. In the AWS Console, grant the Lambda function permissions to access the SNS topic and the Microsoft Teams webhook:

   ```
   aws lambda add-permission \
       --function-name <your_lambda_function_name> \
       --action lambda:InvokeFunction \
       --statement-id sns \
       --principal sns.amazonaws.com \
       --source-arn <your_sns_topic_arn>

   aws lambda add-permission \
       --function-name <your_lambda_function_name> \
       --action lambda:InvokeFunction \
       --statement-id teams \
       --principal events.amazonaws.com \
       --source-arn <your_sns_topic_arn>
   ```

9. That's it! Whenever there's a change in your CodeCommit repository, you should receive a notification in your Microsoft Teams channel.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
