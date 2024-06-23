# -*- coding: utf-8 -*-
# from odoo import http


# class KolapataPosReportCateg(http.Controller):
#     @http.route('/kolapata_pos_report_categ/kolapata_pos_report_categ', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kolapata_pos_report_categ/kolapata_pos_report_categ/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kolapata_pos_report_categ.listing', {
#             'root': '/kolapata_pos_report_categ/kolapata_pos_report_categ',
#             'objects': http.request.env['kolapata_pos_report_categ.kolapata_pos_report_categ'].search([]),
#         })

#     @http.route('/kolapata_pos_report_categ/kolapata_pos_report_categ/objects/<model("kolapata_pos_report_categ.kolapata_pos_report_categ"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kolapata_pos_report_categ.object', {
#             'object': obj
#         })

