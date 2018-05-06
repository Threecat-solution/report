from flask import Flask
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
import datetime

app = Flask(__name__)
api = Api(app)
db_uri = 'postgresql://billing:billing@localhost/billing'
db = create_engine(db_uri)

class invoice_summaries(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("start_time",
            type=str,
            required=True,
            help='This field cannot be left blank!'
        )
        parser.add_argument("end_time",
            type=str,
            required=True,
            help='This field cannot be left blank!'
        )
        date = parser.parse_args()
        start_time =   date['start_time']
        end_time = date['end_time']
        query = "SELECT invoice_summaries.id, invoice_summaries.status, invoice_summaries.duedate, invoice_summaries.invoice_code, invoices.balance, invoices.paid_amount FROM invoice_summaries INNER JOIN invoice_summary_mapping ON invoice_summaries.id = invoice_summary_mapping.summary_id INNER JOIN invoices ON invoice_summary_mapping.invoice_id = invoices.id WHERE duedate BETWEEN '{}' and '{}'"
        invoice_summaries = db.execute(query.format(start_time, end_time))
        result = []
        for id, status, duedate, invoice_code, balance, paid_amount in invoice_summaries:
            invoice_summarie = {
                'id': id,
                'status': status,
                'duedate': duedate.strftime('%Y-%m-%d %H:%:%S.%f'),
                'invoice_code': invoice_code,
                'balance': '{}'.format(balance),
                'paid_amount': '{}'.format(paid_amount)
            }
            result.append(invoice_summarie)
        if invoice_summaries is not None:
            return {'invoice_summaries': result}, 201
        return {'message': 'No invoice_summaries'}, 400

api.add_resource(invoice_summaries, '/invoice_summaries')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
