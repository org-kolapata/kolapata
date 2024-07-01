# -*- coding: utf-8 -*-
# from odoo import http


# class KolapataPosCustom(http.Controller):
#     @http.route('/kolapata_pos_custom/kolapata_pos_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kolapata_pos_custom/kolapata_pos_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kolapata_pos_custom.listing', {
#             'root': '/kolapata_pos_custom/kolapata_pos_custom',
#             'objects': http.request.env['kolapata_pos_custom.kolapata_pos_custom'].search([]),
#         })

#     @http.route('/kolapata_pos_custom/kolapata_pos_custom/objects/<model("kolapata_pos_custom.kolapata_pos_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kolapata_pos_custom.object', {
#             'object': obj
#         })

