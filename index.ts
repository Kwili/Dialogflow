import * as express from 'express';
import * as cors from 'cors';
import * as bodyParser from 'body-parser';
import * as morgan from 'morgan';

const app = express();

app.use(bodyParser.json());
app.use(cors({
		origin: '*',
		methods: [
			'GET',
			'PUT',
			'POST',
			'PATCH',
			'DELETE',
			'UPDATE'
		],
		credentials: true
	}
));

app.use(morgan('dev'));

app.get('/', (req, res) => {
	return res.sendStatus(200);
});

// TODO: Ne pas utiliser directement l'ID, mais encrypt un token ou autre
// Il faut voir si res.download ne pose pas de problème avec le website
app.get('/reports/:id', (req, res) => {
	const id = req.params.id;
	//return res.sendFile(`/reports/${id}.pdf`, { root: __dirname });
	return res.download(`${__dirname}/reports/${id}.pdf`);
});

/* app.use((err, req, res, next) => {
	if (err instanceof SyntaxError) {
		return res.status(400).send({
			errorCode: 'PARSE_ERROR',
			message: 'Arguments could not be parsed, make sure request is valid.'
		});
	}
	return res.status(500).send('Something broke!', err);
}); */

const PORT = process.env.PORT || 3030;

app.listen(PORT, () => {
	console.log(`Listening on port ${PORT}`);
});