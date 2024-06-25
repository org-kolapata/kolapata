# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    unit_cost_kolap = fields.Float("Unit Cost", compute='_compute_unit_cost_kolap', store=True, readonly=True)

    @api.depends('product_id')
    def _compute_unit_cost_kolap(self):
        for line in self:
            line.unit_cost_kolap = 0.0
            if line.product_id:
                product = line.product_id
                product_template = self.env['product.template'].search(
                        [('id', '=', product.product_tmpl_id.id)])

                if product.bom_count > 0:
                    mrp_bom = self.env['mrp.bom'].search(
                        [('product_tmpl_id', '=', product_template.id), ('company_id', '=', line.company_id.id)])
                    for boms in mrp_bom:
                        for components in boms.bom_line_ids:
                            cp_product = components.product_id
                            print("cp_product: ", cp_product.name)
                            if cp_product.bom_count > 0:
                                cp_product.button_bom_cost()
                                print("cp_product.standard_price: ", cp_product.standard_price)
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
