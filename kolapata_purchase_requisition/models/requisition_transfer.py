# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class RequisitionTransfer(models.Model):

    _name = "requisition.transfer"
    _description = "Transfer Requisition"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = "id desc"

    name = fields.Char(string='Name', copy=False, readonly=True,
                       index=True, default=lambda self: _('New'), tracking=True)
    order_line_ids = fields.One2many('requisition.transfer.line', 'transfer_id', string='Transfer Order Lines')

    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'), ('confirm', 'Approved'), ('cancel', 'Cancelled')], readonly=True,
        default='draft', copy=False,
        string="Status", tracking=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True, copy=False)
    sender_user_id = fields.Many2one('res.users', string='Requester (User)', default=lambda self: self.env.user,
                                     readonly=True)
    receiver_user_id = fields.Many2one('res.users', string='Provider (User)', required=True)
    sender_partner = fields.Many2one('res.partner', string='Requester (Partner)', required=True,
                                     domain=[('transfer', '=', True)])
    receiver_partner = fields.Many2one('res.partner', string='Provider (Partner)', required=True,
                                       domain=[('transfer', '=', True)])
    from_company = fields.Many2one('res.company', 'Company', required=True, readonly=True, index=True,
                                   default=lambda self: self.env.company)
    to_company = fields.Many2one('res.company', 'Provider (Company)', required=True, index=True)
    received_transfer_id = fields.Many2one('requisition.receive', 'Received Transfer No', readonly=True, )


    @api.onchange('from_company')
    def onchange_from_company(self):
        for rec in self:
            rec.sender_partner = rec.from_company.partner_id

    @api.onchange('receiver_partner')
    def _onchange_receiver_partner_user(self):
        for rec in self:
            if rec.receiver_partner:
                rec.to_company = rec.receiver_partner.partner_company
                return {'domain': {'receiver_user_id': [('company_id', '=', rec.receiver_partner.partner_company.id)]}}

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'requisition.transfer.sequence') or _('New')

        res = super(RequisitionTransfer, self).create(vals)
        return res

    def action_submit(self):
        print("Submitted")
        if not self.order_line_ids:
            raise UserError(
                _('Please Enter Order Line information.'))

        received_requisition = {}
        received_requisition['sender_partner'] = self.sender_partner.id
        received_requisition['receiver_partner'] = self.receiver_partner.id
        received_requisition['to_company'] = self.to_company.id
        received_requisition['from_company'] = self.from_company.id
        received_requisition['sender_user_id'] = self.sender_user_id.id
        received_requisition['receiver_user_id'] = self.receiver_user_id.id
        received_requisition['date_transfer'] = self.date
        received_requisition['transfer_req_id'] = self.id

        received_requisition['received_order_line_ids'] = [
            (0, 0, {
                'product_id': p.product_id.id,
                'quantity': p.quantity,
                'uom_id': p.uom_id.id,
            }) for p in self.order_line_ids
        ]

        received_requisition_list = []
        received_requisition_list.append(received_requisition)
        print("received_requisition_list: ", received_requisition_list)

        received_requisition = self.env['requisition.receive']. \
            sudo().with_context(force_company=self.to_company.id, default_company_id=self.to_company.id).create(
            received_requisition_list)
        received_requisition.write({'transfer_req_id': self.id})
        print("received_requisition: ", received_requisition)
        self.write({'received_transfer_id': received_requisition.id})
        received_requisition.write({'state': 'submit'})
        self.write({'state': 'submit'})

class TransferLine(models.Model):
    _name = "requisition.transfer.line"

    transfer_id = fields.Many2one('requisition.transfer', string='Requisition Transfer No')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    uom_id = fields.Many2one('uom.uom', 'UoM')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            rec.uom_id = rec.product_id.uom_id.id










