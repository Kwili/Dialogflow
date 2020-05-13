
import os
import uuid
from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS, cross_origin
from flask_api import status
from pdf_handler import create_pdf

import sys

env = os.getenv('PYTHON_ENV', 'dev')

application = Flask('Forward')
application.config['DEBUG'] = True if env == 'dev' else False
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'

default_dir = './reports/' if env == 'dev' else '/tmp/reports/'
default_url = 'http://localhost:3030/' if env == 'dev' else 'http://kwili-dialogflow.herokuapp.com/'

def ensure_path(path):
	if not os.path.exists(path):
		os.makedirs(path)

ensure_path(default_dir)

@application.route('/', methods=['GET'])
@cross_origin()
def home():
	return 'You are on Forward\'s API'

@application.route('/reportsdl/<report_id>', methods=['GET'])
@cross_origin()
def get_reports(report_id):
	path = default_dir + report_id + '.pdf'
	if not os.path.exists(path):
		return 'File does not exist', 400
	return send_file(path, as_attachment=True)

@application.route('/reports/<report_id>', methods=['GET'])
@cross_origin()
def download_report(report_id):
	filename = report_id + '.pdf'
	if not os.path.exists(default_dir + filename):
		return 'File does not exist', 400
	return send_from_directory(directory=default_dir, filename=filename)


@application.route('/reports', methods=['POST'])
@cross_origin()
def post_report():
	body = request.get_json()
	parameters = {}
	session_id = str(uuid.uuid1())
	session_string = 'sessions/'
	context_string = '/contexts/'
	for attrs in body:
		if "/injury-followup" in attrs['name']:
			parameters = attrs['parameters']
			name = attrs['name']
			session_pos = name.find(session_string) + len(session_string)
			tmp = name[session_pos:]
			context_post = tmp.find(context_string)
			#session_id = tmp[:context_post]
	diagnosis = {
		'pain': parameters['damageValue'],
		'body_part': parameters['bodypart'],
		'smoke': 0 if 'smoke' not in parameters else parameters['smoke'],
		'height': parameters['height.original'],
		'weight': parameters['weight.original'] + 'kg'
	}
	print('Parameters :', parameters)
	allergies = [] if 'allergies' not in parameters else parameters['allergies'].split(' ')
	background = []# if 'background' not in parameters else parameters['background']
	create_pdf(default_dir, session_id, diagnosis, allergies, background)
	return default_url + 'reports/' + session_id

if __name__ == "__main__":
	application.run(host='0.0.0.0', port='3030')
