from twilio.rest import Client
import json
import os

account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")


client = Client(account_sid,auth_token)
workspace_sid ='WSe196cf7ff1aa17087dbfdd26c5b2f9ae'
salesTaskQueue_sid = 'WQaaf8af8ce62aae07dcbebd5b158655e2'

config = {
    'task_routing': {
        'filters':
            [
            {
                'filter_friendly_name':'sales leads',
                'expression':'selected_product =="sales"',
                'targets': [{'queue': salesTaskQueue_sid }]
            }
        ]
    }

}

workflow = client.taskrouter.workspaces(workspace_sid).workflows \
    .create(
    friendly_name='sales',
    task_reservation_timeout=30,
    configuration=json.dumps(config)
)

print(workflow.sid)
print(workflow.friendly_name)
print(workflow.configuration)