import os
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")

client = Client(account_sid, auth_token)
workspace_sid ="WSe196cf7ff1aa17087dbfdd26c5b2f9ae"

task = client.taskrouter.workspaces(workspace_sid) \
    .tasks.create(
    workflow_sid='WW87087adc2f448b8c9b8a2f1a762a60a9',
 attributes='{"selected_product":"sales"}'
)

print(task.sid)
print(task.attributes)
print(task.assignment_status)