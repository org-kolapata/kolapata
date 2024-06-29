# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ReqDepartment(models.Model):
    _name = "req.department"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Department Details"
    _order = 'id desc'

    name = fields.Char("Name", required=True, tracking=True)

    _sql_constraints = [
        ('unique_name',
         'unique(name)', 'Department Name should be unique!')]