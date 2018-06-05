from flask import Flask, request, Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

import os

app = Flask(__name__)

workflow_sid = ''
account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")
workspace_sid = os.environ.get("TWILIO_ACME_ALT_WORKSPACE")
caller_id = os.environ.get("TWILIO_ACME_CALLER_ID")
wrap_up = os.environ.get("TWILIO_ACME_ALT_WRAP_UP_ACTIVITY")

client = Client(account_sid, auth_token)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/incoming_call', methods=['POST', 'GET'])
def hello_customer():
    resp = VoiceResponse()
    with resp.gather(num_digits="1", action="/process_digits", method="GET", timeout=10) as g:
        g.say("Hello, welcome to ACMECorp, thanks for calling please select from the following options, for sales press one, for support press, billing press three")
    return Response(str(resp), mimetype="text/xml")


@app.route('/process_digits', methods=['POST', 'GET'])
def handle_input():
    if 'Digits' in request.values:
        choice = int(request.values['Digits'])
        dept = {
            1: "sales",
            2: "support",
            3: "billing"

        }

        resp = VoiceResponse()

        with resp.enqueue(workflow_sid=workflow_sid) as e:
            e.task('{"selected_product" : "' + dept[choice] + '"}')

    else:
        resp = VoiceResponse()
        resp.say("No digits detected")
        resp.redirect('/incoming_call')

    return Response(str(resp), mimetype='text/xml')

@app.route('/assignment_callback', methods=['POST', 'GET'])
def assign_task():
    
    task_sid = request.values.get('TaskSid')
    reservation_sid = request.values.get('ReservationSid')
    print(reservation_sid)

    reservation = client.taskrouter.workspaces(workspace_sid) \
           .tasks(task_sid).reservations(reservation_sid) \
        .update(reservation_status='accepted')

    ret = '{"instruction": "dequeue", "from":"'+ caller_id +'", "post_work_activity_sid":"'+wrap_up+'"}'  # a verified phone number from your twilio account

    resp = Response(ret, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run()
