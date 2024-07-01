# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    show_closing_fields = fields.Boolean("Show Session Closing All Items")






