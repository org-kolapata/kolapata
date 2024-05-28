# -*- coding: utf-8 -*-
# from odoo import http


# class KolapataCashJournalReport(http.Controller):
#     @http.route('/kolapata_cash_journal_report/kolapata_cash_journal_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kolapata_cash_journal_report/kolapata_cash_journal_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kolapata_cash_journal_report.listing', {
#             'root': '/kolapata_cash_journal_report/kolapata_cash_journal_report',
#             'objects': http.request.env['kolapata_cash_journal_report.kolapata_cash_journal_report'].search([]),
#         })

#     @http.route('/kolapata_cash_journal_report/kolapata_cash_journal_report/objects/<model("kolapata_cash_journal_report.kolapata_cash_journal_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kolapata_cash_journal_report.object', {
#             'object': obj
#         })

