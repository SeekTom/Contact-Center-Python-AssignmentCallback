import os
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")

client = Client(account_sid, auth_token)
workspace_sid ="WSe196cf7ff1aa17087dbfdd26c5b2f9ae"

activities = client.taskrouter.workspaces(workspace_sid).activities.list()

activity_sid = {}

for activity in activities:
    activity_sid[activity.friendly_name] = activity.sid

taskqueue = client.taskrouter.workspaces(workspace_sid) \
    .task_queues.create(
    friendly_name='Sales',
    assignment_activity_sid=activity_sid['Busy'],
    reservation_activity_sid=activity_sid['Reserved'],
    target_workers='skills HAS "sales"'
)

print(taskqueue.friendly_name)
print(taskqueue.sid)