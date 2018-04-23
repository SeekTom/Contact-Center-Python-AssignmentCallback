import os
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")
workspace_sid = os.environ.get("TWILIO_ACME_ALT_WORKSPACE")

client = Client(account_sid, auth_token)

worker = client.taskrouter.workspaces(workspace_sid) \
    .workers.create(
    friendly_name='Tom',
    attributes='{"skills":"sales"}'
)

print(worker.friendly_name)
print(worker.sid)
print(worker.attributes)