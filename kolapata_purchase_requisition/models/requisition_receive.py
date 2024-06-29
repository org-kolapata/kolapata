# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import ValidationError, UserError


class RequisitionReceive(models.Model):
    _name = 'requisition.receive'
    _description = "Received Requisition"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = "id desc"

    name = fields.Char(string='Name', copy=False, readonly=True, tracking=True,
                       index=True, default=lambda self: _('New'))
    received_order_line_ids = fields.One2many('requisition.receive.line', 'received_requisition_id', string='Received Order Lines')

    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'), ('confirm', 'Approved'), ('cancel', 'Cancelled')], readonly=True,
        default='draft', copy=False,  string="Status", tracking=True)
    date_transfer = fields.Date(string='Transfer Date', default=fields.Date.context_today, required=True, copy=False)
    date_confirm = fields.Date(string='Confirmation Date')
    sale_id = fields.Many2many('sale.order', 'rcv_req_id', string='Sales Order No')
    sale_count = fields.Integer(string='Total Sale', compute='_compute_sale_ids')

    transfer_req_id = fields.Many2one('requisition.transfer', string='Transfer Requisition No')
    req_department_id = fields.Many2one('req.department', 'Department', tracking=True)
    sender_user_id = fields.Many2one('res.users', string='Requester (User)', readonly=True)
    current_user_id = fields.Many2one('res.users', string='Current User', readonly=True, compute="_compute_current_user")
    receiver_user_id = fields.Many2one('res.users', string='Provider (User)', required=True)
    sender_partner = fields.Many2one('res.partner', string='Requester (Partner)', required=True,
                                     domain=[('transfer', '=', True)])
    receiver_partner = fields.Many2one('res.partner', string='Provider (Partner)', required=True,
                                       domain=[('transfer', '=', True)])
    from_company = fields.Many2one('res.company', 'Sender Company', required=True, readonly=True, index=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', index=True, compute="_compute_warehouse")
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    to_company = fields.Many2one('res.company', 'Company', required=True, index=True, readonly=True)
    user_check = fields.Boolean('Check User', required=True, index=True, compute="_compute_user_check")

    def _compute_sale_ids(self):
        for rec in self:
            rec.sale_count = 0

            rec.sale_id = rec.env['sale.order'].sudo().search(
                [('rcv_req_id', '=', rec.id), ('company_id', '=', rec.to_company.id)])
            rec.sale_count = len(rec.sale_id)

            print("rec.sale_count", rec.sale_count)


    def _compute_current_user(self):
        self.current_user_id = self.env.uid

    def _compute_warehouse(self):
        for rec in self:
            warehouse = self.env['stock.warehouse'].sudo().search([('company_id', '=', rec.to_company.id)])
            rec.warehouse_id = warehouse.id
            print("warehouse_id: ", rec.warehouse_id.name)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'requisition.receive.sequence') or _('New')

        return super(RequisitionReceive, self).create(vals_list)


    def cancel(self):
        """ Sets state to Cancel """
        self.state = 'cancel'
        self.transfer_req_id.state = 'cancel'

    def unlink(self):
        for order in self:
            if order.state != 'draft':
                raise UserError(
                    _('You can not delete a Approved or submitted Transferred Requisition.'))
        return super(RequisitionReceive, self).unlink()

    def action_confirm(self):
        # self.ensure_one()

        if not self.received_order_line_ids:
            raise UserError(
                _('Please Enter Order Line information.'))

        if not self.pricelist_id:
            raise UserError(
                _('Please Select desired pricelist.'))

        for rec in self.received_order_line_ids:

            if rec.quantity > rec.onhand_qty:
                raise ValidationError(
                    _("You can not Transfer Product having greater qty of On hand qty.\n The On hand qty of product '%s' is '%s' ") % (rec.product_id.name, rec.onhand_qty))

        self.date_confirm = date.today()

        print("rec.warehouse_id: ", self.warehouse_id)
        # For Creating Sale Order
        sale_order = {}
        sale_order['partner_id'] = self.sender_partner.id
        sale_order['user_id'] = self.receiver_user_id.id
        sale_order['pricelist_id'] = self.pricelist_id.id
        sale_order['date_order'] = self.date_confirm
        sale_order['company_id'] = self.to_company.id
        sale_order['transfer_req_id'] = self.transfer_req_id.id
        sale_order['rcv_req_id'] = self.id

        sale_order['order_line'] = [
            (0, 0, {
                'name': p.product_id.display_name,
                'product_id': p.product_id.id,
                'product_uom_qty': p.quantity,
            }) for p in self.received_order_line_ids
        ]

        sale_order_list = []
        sale_order_list.append(sale_order)
        print("sale_order_list: ", sale_order_list)

        sale = self.env['sale.order'].sudo().with_context(force_company=self.to_company.id, default_company_id=self.to_company.id).create(sale_order_list)
        sale.write({'rcv_req_id': self.id})
        print("sale: ", sale)

        # For auto confirming Auto created Purchase order
        # sale.with_context(force_company=self.to_company.id, default_company_id=self.to_company.id).action_confirm()
        #
        # # For auto confirming Auto created Purchase order
        # auto_purchase = self.env['purchase.order'].sudo().with_context(
        #     default_company_id=self.from_company.id).search(
        #     [('auto_sale_order_id', '=', sale.id)])
        # auto_purchase.with_context(force_company=self.from_company.id, default_company_id=self.from_company.id).button_confirm()

        self.transfer_req_id.state = 'confirm'
        self.state = 'confirm'

    def action_view_sale(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Order',
            'res_model': 'sale.order',
            'view_type': 'form',
            'domain': [('rcv_req_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }


class ReqRcvLine(models.Model):
    _name = "requisition.receive.line"
    _description = "Received Requisition Line"

    received_requisition_id = fields.Many2one('requisition.receive', string='Received Order No')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    free_qty = fields.Float(string='Free To Use', compute='_compute_available_qty')
    onhand_qty = fields.Float(string='Onhand Qty', compute='_compute_available_qty')
    uom_id = fields.Many2one('uom.uom', 'UoM')


    def _compute_available_qty(self):
        for rec in self:
            if rec.product_id:
                print("product has")
                quant = rec.product_id.with_context(warehouse=rec.received_requisition_id.warehouse_id.id)
                rec.free_qty = quant.free_qty
                print("rec.free_qty: ", rec.free_qty)
                rec.onhand_qty = quant.qty_available
                print("onhand_qty: ", rec.onhand_qty)
            else:
                rec.free_qty = 0.0
                rec.onhand_qty = 0.0


class SaleOrder(models.Model):

    _inherit = "sale.order"

    transfer_req_id = fields.Many2one('requisition.transfer', "Requisition Transfer No", readonly=True)
    rcv_req_id = fields.Many2one('requisition.receive', "Requisition Receive No", readonly=True)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for rec in self:
            if rec.rcv_req_id:
                # For auto confirming Auto created Purchase order
                auto_purchase = self.env['purchase.order'].sudo().with_context(
                    default_company_id=rec.rcv_req_id.from_company.id).search(
                    [('auto_sale_order_id', '=', rec.id)])
                auto_purchase.transfer_req_id = rec.transfer_req_id.id
                auto_purchase.rcv_req_id = rec.rcv_req_id.id
                auto_purchase.with_context(force_company=rec.rcv_req_id.from_company.id,
                                           default_company_id=rec.rcv_req_id.from_company.id).button_confirm()
                auto_purchase.with_context(force_company=rec.rcv_req_id.from_company.id,
                                           default_company_id=rec.rcv_req_id.from_company.id).button_done()


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    transfer_req_id = fields.Many2one('requisition.transfer', "Req Transfer No", readonly=True)
    rcv_req_id = fields.Many2one('requisition.receive', "Req Receive No", readonly=True)
    state = fields.Selection(selection_add=[('wrong', 'Wrong Order')])

    def action_wrong(self):
        self.state = 'wrong'



