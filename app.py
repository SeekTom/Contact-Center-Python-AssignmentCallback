from flask import Flask, request, Response, render_template, jsonify
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Conference, Enqueue, Dial

import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/incoming_call')
def hello_customer():
    resp = VoiceResponse()
    with resp.gather(num_digits="1", action="/process_digits", timeout=10) as g:
        g.say("Hello, welcome to ACMECorp, thanks for calling please select from the following options, for sales press one, for support press, billing press three")
    return Response(str(resp), mimetype="text/xml")


@app.route('/process_digits')
def handle_input():
    if 'Digits' in request.values:
        choice = int(request.values['Digits'])
        switcher = {
            1: os.environ.get("TWILIO_ACME_SALES_WORKFLOW"),
            2: os.environ.get("TWILIO_ACME_SUPPORT_WORKFLOW"),
            3: os.environ.get("TWILIO_ACME_BILLING_WORKFLOW")
        }

        dept = {
            1: "sales",
            2: "support",
            3: "billing"

        }

        resp = VoiceResponse()

        with resp.enqueue(workflow_sid=switcher[choice]) as e:
            e.task('{"selected_product" : "' + dept[choice] + '"}')

    else:
        resp = VoiceResponse()
        resp.say("No digits detected")
        resp.redirect('/incoming_call')

    return Response(str(resp), mimetype='text/xml')

@app.route('/asssignment_callback')
def assign_task(task_sid, reservation_sid):

    account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")
    workspace_sid = os.environ.get("TWILIO_ACME_WORKSPACE_SID")

    client = Client(account_sid, auth_token)

    task_sid = request.args.get('task_sid')

    reservation_sid = request.args.get('reservation_sid')
    reservation = client.taskrouter.workspaces(workspace_sid) \
        .tasks(task_sid).reservations(reservation_sid) \
        .update(reservation_status='accepted')

    resp = Response({}, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run()
