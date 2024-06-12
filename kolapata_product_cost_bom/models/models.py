# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    unit_cost_kolap = fields.Float("Unit Cost", compute='_compute_unit_cost_kolap', store=True, readonly=True)

    @api.depends('product_id')
    def _compute_unit_cost_kolap(self):
        for line in self:
            line.unit_cost_kolap = 0.0
            if line.product_id:
                product = line.product_id
                if product.bom_count > 0:
                    product.button_bom_cost()
                product_cost = product.standard_price
                line.total_cost = line.qty * product.cost_currency_id._convert(
                    from_amount=product_cost,
                    to_currency=line.currency_id,
                    company=line.company_id or self.env.company,
                    date=line.order_id.date_order or fields.Date.today(),
                    round=False,
                )
                line.is_total_cost_computed = True
                line.unit_cost_kolap = product_cost
