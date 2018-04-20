from twilio.rest import Client
import os

account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")


client = Client(account_sid, auth_token)

workspace = client.taskrouter.workspaces.create(
    friendly_name='NewWorkSpace',
    template='FIFO'
)

print(workspace.friendly_name)
print(workspace.sid)