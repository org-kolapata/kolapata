# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    transfer = fields.Boolean(string="Allow Requisition", default=False)
    partner_company = fields.Many2one('res.company', 'Partner Company')
