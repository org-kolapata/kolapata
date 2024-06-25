# -*- coding: utf-8 -*-
# from odoo import http


# class KolapataProductCostBom(http.Controller):
#     @http.route('/kolapata_product_cost_bom/kolapata_product_cost_bom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kolapata_product_cost_bom/kolapata_product_cost_bom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kolapata_product_cost_bom.listing', {
#             'root': '/kolapata_product_cost_bom/kolapata_product_cost_bom',
#             'objects': http.request.env['kolapata_product_cost_bom.kolapata_product_cost_bom'].search([]),
#         })

#     @http.route('/kolapata_product_cost_bom/kolapata_product_cost_bom/objects/<model("kolapata_product_cost_bom.kolapata_product_cost_bom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kolapata_product_cost_bom.object', {
#             'object': obj
#         })

