
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
from flask_api import status
from pdf_handler import create_pdf


app = Flask('Forward')
app.config['DEBUG'] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
@cross_origin()
def home():
	return 'You are on Forward\'s API'

@app.route('/reports/<report_id>', methods=['GET'])
@cross_origin()
def get_reports(report_id):
	path = './reports/' + report_id + '.pdf'
	return send_file(path, as_attachment=True)

@app.route('/reports/<report_id>', methods=['POST'])
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
	create_pdf(conversation_id, diagnosis, allergies, background)
	return 'Success'

app.run(host='0.0.0.0', port='3030')
