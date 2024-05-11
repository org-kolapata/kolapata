# -*- coding: utf-8 -*-
# from odoo import http


# class KolapataPurchaseRequisition(http.Controller):
#     @http.route('/kolapata_purchase_requisition/kolapata_purchase_requisition', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kolapata_purchase_requisition/kolapata_purchase_requisition/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kolapata_purchase_requisition.listing', {
#             'root': '/kolapata_purchase_requisition/kolapata_purchase_requisition',
#             'objects': http.request.env['kolapata_purchase_requisition.kolapata_purchase_requisition'].search([]),
#         })

#     @http.route('/kolapata_purchase_requisition/kolapata_purchase_requisition/objects/<model("kolapata_purchase_requisition.kolapata_purchase_requisition"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kolapata_purchase_requisition.object', {
#             'object': obj
#         })

