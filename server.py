
import os
from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS, cross_origin
from flask_api import status
from pdf_handler import create_pdf

env = os.getenv('PYTHON_ENV', 'dev')

application = Flask('Forward')
application.config['DEBUG'] = True if env == 'dev' else False
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'


default_dir = './reports/' if env == 'dev' else '/tmp/reports/'

print(default_dir)

def ensure_path(path):
	if not os.path.exists(path):
		os.makedirs(path)

ensure_path(default_dir)


@application.route('/', methods=['GET'])
@cross_origin()
def home():
	return 'You are on Forward\'s API'

@application.route('/reports/<report_id>', methods=['GET'])
@cross_origin()
def get_reports(report_id):
	path = default_dir + report_id + '.pdf'
	return send_file(path, as_attachment=True)

@application.route('/reportsdl/<report_id>', methods=['GET'])
@cross_origin()
def download_report(report_id):
	return send_from_directory(directory=default_dir, filename= report_id + '.pdf')
@application.route('/reports/<report_id>', methods=['POST'])
@cross_origin()
def post_report(report_id):
	conversation_id = report_id # conversation_id
	body = request.get_json()
	diagnosis = {
		'pain': body['pain'],
		'body_part': body['body_part']
	} # Où se situe la douleur, niveau de douleur...
	allergies = body['allergies']
	background = body['background']
	create_pdf(default_dir, conversation_id, diagnosis, allergies, background)
	return 'Success'

if __name__ == "__main__":
	application.run(host='0.0.0.0', port='3030')
