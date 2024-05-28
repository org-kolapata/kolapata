# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.exceptions import UserError


class CashJournalReport(models.TransientModel):
    _name = 'cash.journal.report'

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)


    def get_report(self):
        """Call when button 'Get Report' clicked.
        """

        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        return self.env.ref('kolapata_cash_journal_report.journal_report').report_action(self, data=data)


class JournalReportUSer(models.AbstractModel):
    """Abstract Model for report template.

    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.kolapata_cash_journal_report.journal_report_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("get value working")
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))

        date_start = datetime.strptime(data['form']['date_start'], DATE_FORMAT)
        date_end = datetime.strptime(data['form']['date_end'], DATE_FORMAT)

        date_start = fields.Datetime.to_string(date_start)
        date_end = fields.Datetime.to_string(date_end)

        orders = self.env['account.move'].search(
            [('date', '>=', date_start), ('date', '<=', date_end), ('state', '=', 'posted'), ('journal_id.name', '=', 'Cash Office')])
        print("orders: ", orders)


        products = {}

        for line in orders:

            products.setdefault(line.company_id,
                                {'company': line.company_id.name, 'amount_total_signed': 0.0})
            products[line.company_id]['amount_total_signed'] += line.amount_total_signed

        print("products: ", list(products.values()))

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'products': list(products.values()),
        }
