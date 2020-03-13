// https://pdfkit.org/docs/text.html

import * as PDFDocument from 'pdfkit';
import * as fs from 'fs';

export default class PDF {
	constructor() {

	}

	create = (body) => {
		const doc = new PDFDocument;
		doc.pipe(fs.createWriteStream(`${__dirname}/reports/${body.id}.pdf`));
		doc.image(`${__dirname}/assets/logo.png`, {
			fit: [250, 300],
			align: 'center',
			valign: 'center'
		});
		doc.moveDown();
		doc.text('Some random text hello world!', {
			align: 'left'
		});
		doc.moveDown();
		doc.text('Some random text hello world!', {
			align: 'left'
		});
		doc.end();
	}

	delete = (id) => {

	}
}