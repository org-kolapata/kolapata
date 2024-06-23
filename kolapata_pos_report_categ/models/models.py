# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    pos_category_id = fields.Many2one('pos.category', string='PoS Category', readonly=True)

    def _select(self):
        return super(PosOrderReport, self)._select() + ',ppc.pos_category_id AS pos_category_id'

    def _from(self):
        return super(PosOrderReport, self)._from() + 'LEFT JOIN pos_category_product_template_rel ppc ON (ppc.product_template_id=pt.id)'

    def _group_by(self):
        return super(PosOrderReport, self)._group_by() + ',ppc.pos_category_id'

