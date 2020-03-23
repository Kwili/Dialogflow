
# TODO: Fix [Empty Response] from Dialogflow

import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))


def append_block(body, text, space_width=12):
	if (space_width > 0):
		body.append(Spacer(1, space_width))
	body.append(Paragraph(text, styles["Normal"]))


def create_pdf(default_dir, conversation_id, diagnosis, allergies, background):
	doc = SimpleDocTemplate(default_dir + conversation_id + '.pdf', pagesize=letter,
                         rightMargin=72, leftMargin=72,
                         topMargin=72, bottomMargin=18)
	body = []
	logo = "./assets/logo.png"
	#formatted_time = time.ctime()
	im = Image(logo, 125, 150)
	body.append(im)
	body.append(Spacer(1, 36))
	append_block(
		body, '<font size="12">Indentifiant de conversation: %s</font>' % conversation_id)
	append_block(body, '<font size="12">Niveau de douleur: %s</font>' %
	             diagnosis['pain'], 0)
	append_block(body, '<font size="12">Partie du corps: %s</font>' %
	             diagnosis['body_part'], 12)
	append_block(body, '<font size="12">Allergies:</font>', 12)
	for a in allergies:
		ptext = '<font size="12">- %s</font>' % a.strip()
		append_block(body, ptext, 0)
	append_block(body, '<font size="12">Antécédents:</font>', 12)
	for b in background:
		ptext = '<font size="12">- %s</font>' % b.strip()
		append_block(body, ptext, 0)
	body.append(Spacer(1, 48))
	append_block(body, '<font size="10">Made by Kwili</font>', 12)
	doc.build(body)
