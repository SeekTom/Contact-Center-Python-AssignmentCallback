import os
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")
workspace_sid = os.environ.get("TWILIO_ACME_ALT_WORKSPACE")
salesTaskQueue_sid = workspace_sid = os.environ.get("TWILIO_ACME_SALES_TASKQUEUE")

client = Client(account_sid, auth_token)

task = client.taskrouter.workspaces(workspace_sid) \
    .tasks.create(
    workflow_sid=salesTaskQueue_sid,
 attributes='{"selected_product":"sales"}'
)

print(task.sid)
print(task.attributes)
print(task.assignment_status)