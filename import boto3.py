import boto3

# Replace YOUR_AWS_REGION, YOUR_AWS_ACCESS_KEY_ID, and YOUR_AWS_SECRET_ACCESS_KEY with your own values
client = boto3.client(
    "ses",
    region_name="eu-north-1",
    aws_access_key_id="",
    aws_secret_access_key="",
)

subject = "Test Email"
body = "This is a test email sent from Amazon SES using Python."
sender = "samir.yep@gmail.com"
recipient = "samir.yep@gmail.com"

message = {
    "Subject": {"Data": subject},
    "Body": {"Text": {"Data": body}},
    "Source": sender,
    "Destination": {"ToAddresses": [recipient]},
    "Message": {"Body": {"Text": {"Data": body}}, "Subject": {"Data": subject}},
}

response = client.send_email(Source=message["Source"], Destination=message["Destination"], Message=message["Message"])

print(response)
