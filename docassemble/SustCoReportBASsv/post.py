from docassemble.base.util import get_config
from docassemble.base.util import log
from docassemble.base.util import DAFile
from datetime import datetime
import psycopg2
import json
import requests
import os
import base64



def store_interview_results(data):
    """ Post interview to django backend. """

    data["received_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:

        json_data = json.dumps(data)
        url = "http://django:8000/webhooks/docassemble_receiver/"
        response = requests.post(
            url,
            data=json_data,
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        if response.status_code != 200:
            log(f"An error occured: {response.content}", "console")
        return response.status_code, response.content
    except Exception as e:
        log(f"A connection error occured when submitting the interview: {e}", "console")
        return 400, None

