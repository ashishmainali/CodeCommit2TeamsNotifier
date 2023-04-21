import json
import os
import boto3
import requests

def lambda_handler(event, context):
    TEAMS_WEBHOOK_URL = os.environ.get("TEAMS_WEBHOOK_URL_TEST")

    if not TEAMS_WEBHOOK_URL:
        return {
            "statusCode": 500,
            "body": "TEAMS_WEBHOOK_URL environment variable is not set"
        }
    message = json.loads(event['Records'][0]['Sns']['Message'])
    detail_type = message['detailType']

    if detail_type == 'CodeCommit Comment on Pull Request':
        # Process Comment on Pull Request SNS message
        print("Process Comment on Pull Request SNS message")
        print("Process Comment on Pull Request SNS message")
        comment_author = message['additionalAttributes']['comments'][-1]['authorArn'].split(':')[-1]
        comment_text = message['additionalAttributes']['comments'][-1]['commentText']
        pull_request_id = message['detail']['pullRequestId']

        file_path = message['additionalAttributes'].get('filePath', None)
        commented_line_number = message['additionalAttributes'].get('commentedLineNumber', None)

        card = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": f"{comment_author} commented on Pull Request {pull_request_id}",
            "title": f"{comment_author} commented on Pull Request {pull_request_id}",
            "text": f"{comment_text}",
            "sections": [
                {
                    "activityTitle": "Previous Comments",
                    "activitySubtitle": "All previous comments on this Pull Request",
                    "activityImage": "https://i.imgur.com/4f6y1pW.png",
                    "facts": [],
                    "markdown": True
                }
            ],
            "potentialAction": [
                {
                    "@type": "OpenUri",
                    "name": "View Pull Request",
                    "targets": [
                        {
                            "os": "default",
                            "uri": f"https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/HTG-UI/pull-requests/{pull_request_id}/activity"
                        }
                    ]
                }
            ]
        }

        if file_path and commented_line_number:
            card['sections'][0]['facts'].append({"name": "File Path", "value": f"{file_path}"})
            card['sections'][0]['facts'].append({"name": "Line Number", "value": f"{commented_line_number}"})

        comments = message['additionalAttributes']['comments'][:-1]
        if comments:
            for i, c in enumerate(comments[::-1]):
                card['sections'][0]['facts'].append({"name": f"Comment {len(comments)-i}", "value": f"{c['commentText']} - {c['authorArn'].split(':')[-1]}"})

        response = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": f"{comment_author} commented on Pull Request {pull_request_id}",
            "title": f"{comment_author} commented on Pull Request {pull_request_id}",
            "text": f"{comment_text}",
            "sections": card['sections'],
            "potentialAction": card['potentialAction']
        }
        print (response)
    elif detail_type == 'CodeCommit Repository State Change':
        # Process Repository State Change SNS message
        print("# Process Repository State Change SNS message")
        detail = message['detail']
        repository_name = detail['repositoryName']
        reference_name = detail['referenceName']
        commit_id = detail['commitId']
        caller_user_arn = detail['callerUserArn']
        author = caller_user_arn.split(':')[-1]
    
        card = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "title": f"{author} merged a change to {reference_name} in {repository_name}",
            "text": f"Commit ID: {commit_id}",
            "potentialAction": [
                {
                    "@type": "OpenUri",
                    "name": "View Repository",
                    "targets": [
                        {
                            "os": "default",
                            "uri": f"https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/{repository_name}/browse/{reference_name}?region=us-east-1"
                        }
                    ]
                }
            ]
        }
        response = card
        print (response)
    elif detail_type == 'CodeCommit Pull Request State Change':
        print ("CodeCommit Pull Request State Change")
        detail = message['detail']
        event_type = detail['event']
        repository_name = detail['repositoryNames'][0]
        pull_request_id = detail['pullRequestId']
        title = detail['title']
        author_arn = detail['author']
        author = author_arn.split(':')[-1]
        
        if event_type == 'pullRequestMergeStatusUpdated':
            pull_request_status = detail['pullRequestStatus']
            card = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": "0076D7",
                "title": f"{author} closed Pull Request {pull_request_id} in {repository_name}",
                "text": f"Title: {title}\nStatus: {pull_request_status}",
                "potentialAction": [
                    {
                        "@type": "OpenUri",
                        "name": "View Pull Request",
                        "targets": [
                            {
                                "os": "default",
                                "uri": f"https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/{repository_name}/pull-requests/{pull_request_id}?region=us-east-1"
                            }
                        ]
                    }
                ]
            }
            print (card)
        elif event_type == 'pullRequestCreated':
            print ("pullRequestCreated")
            card = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": "0076D7",
                "title": f"{author} created Pull Request {pull_request_id} in {repository_name}",
                "text": f"Title: {title}",
                "potentialAction": [
                    {
                        "@type": "OpenUri",
                        "name": "View Pull Request",
                        "targets": [
                            {
                                "os": "default",
                                "uri": f"https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/{repository_name}/pull-requests/{pull_request_id}?region=us-east-1"
                            }
                        ]
                    }
                ]
            }
        elif event_type == 'pullRequestApprovalStateChanged':
            approval_status = detail['approvalStatus']
            card = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": "0076D7",
                "title": f"{author} updated their approval state for Pull Request {pull_request_id} in {repository_name}",
                "text": f"Approval Status: {approval_status}",
                "potentialAction": [
                    {
                        "@type": "OpenUri",
                        "name": "View Pull Request",
                        "targets": [
                            {
                                "os": "default",
                                "uri": f"https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/{repository_name}/pull-requests/{pull_request_id}?region=us-east-1"
                            }
                        ]
                    }
                ]
            }
        response = card
        print (response)
    else:
        print(f"Unhandled event: {event_type}")
        return

    send_teams_notification(TEAMS_WEBHOOK_URL, response)

def send_teams_notification(webhook_url, response):
    print ("Processing Request....")
    headers = {
        "Content-Type": "application/json"
    }

    teams_response = requests.post(webhook_url, headers=headers, data=json.dumps(response))
    if teams_response.status_code != 200:
        return {
            "statusCode": 500,
            "body": f"Failed to send notification to Microsoft Teams: {teams_response.text}"
        }
    return {
        "statusCode": 200,
        "body": "Notification sent to Microsoft Teams successfully"
    }
