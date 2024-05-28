# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.exceptions import UserError


class CashJournalReport(models.TransientModel):
    _name = 'cash.journal.report'
    _description = "Cash Office Journal Report"

    date_end = fields.Date(string="Date", required=True, default=fields.Date.today)

    def get_report(self):
        """Call when button 'Get Report' clicked.
        """

        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
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

        date_end = datetime.strptime(data['form']['date_end'], DATE_FORMAT)

        date_end = fields.Datetime.to_string(date_end)

        cash = self.env['account.account'].sudo().search([('name', '=', 'Cash Office')])
        cash_ids = cash.ids

        orders = self.env['account.move.line'].sudo().search([
            ('account_id', 'in', cash_ids),
            ('date', '<=', date_end), ('parent_state', '=', 'posted')])
        print("orders: ", orders)

        total_balance = 0

        for bl in orders:
            total_balance = total_balance + bl.debit - bl.credit

        print("total_balance: ", total_balance)


        products = {}

        for line in orders:

            products.setdefault(line.company_id,
                                {'company': line.company_id.name, 'debit': 0.0, 'credit': 0.0, 'balance': 0.0})
            products[line.company_id]['debit'] += line.debit
            products[line.company_id]['credit'] += line.credit
            products[line.company_id]['balance'] += (line.debit - line.credit)

        print("products: ", list(products.values()))

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'total_balance': total_balance,
            'date_end': date_end,
            'products': list(products.values()),
        }
