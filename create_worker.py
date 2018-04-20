import os
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")

client = Client(account_sid, auth_token)
workspace_sid ="WSe196cf7ff1aa17087dbfdd26c5b2f9ae"

worker = client.taskrouter.workspaces(workspace_sid) \
    .workers.create(
    friendly_name='Tom',
    attributes='{"skills":"sales"}'
)

print(worker.friendly_name)
print(worker.sid)
print(worker.attributes)