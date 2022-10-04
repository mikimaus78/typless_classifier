import json
import os

import flask_cors
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import base64
import requests
import sqlite3
from db_helper import insert_record

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('BACKEND')
APIKEY = "d0d721cef1254a3e8bdc5cb316829afb "
UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "2352GSGHSH"


@app.route('/upload', methods=['POST'])
def fileUpload():
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    logger.info("uploading file....")
    file = request.files['file']
    filename = secure_filename(file.filename)
    destination = "/".join([UPLOAD_FOLDER, filename])
    file.save(destination)
    logger.info("uploading finished....")

    file_name = destination
    session['uploadFilePath'] = destination

    logger.info("typless classification....")
    with open(file_name, 'rb') as file:
        base64_data = base64.b64encode(file.read()).decode('utf-8')

        url = "https://developers.typless.com/api/extract-data"

        payload = {
            "file": base64_data,
            "file_name": file_name,
            "document_type_name": "simple-invoice"
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Token d0d721cef1254a3e8bdc5cb316829afb"
        }

    logger.info("parsing response....")
    response = requests.request("POST", url, json=payload, headers=headers)

    data = parse_response(response)
    logger.info("processing finished!")
    return data


def parse_response(response):
    output = {}
    for field in response.json()['extracted_fields']:
        print(f'{field["name"]}: {field["values"][0]["value"]}')
        if (field["name"]) == 'supplier_name':
            output['supplier_name'] = field["values"][0]["value"]
        if (field["name"]) == 'issue_date':
            output['issue_date'] = field["values"][0]["value"]
        if (field["name"]) == 'pay_due_date':
            output['pay_due_date'] = field["values"][0]["value"]
        if (field["name"]) == 'total_amount':
            output['total_amount'] = field["values"][0]["value"]
        if (field["name"]) == 'invoice_number':
            output['invoice_number'] = field["values"][0]["value"]
        if (field["name"]) == 'invoice_number':
            output['invoice_number'] = field["values"][0]["value"]

    return output


@app.route('/save', methods=['POST'])
def saveToDb():
    logger.info("saving data to database...")
    data = json.loads(request.data)
    insert_record(data)
    logger.info("data saved...")
    return {"result": "ok"}


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="0.0.0.0", use_reloader=False)

flask_cors.CORS(app, expose_headers='Authorization')
