# -*- coding: utf-8 -*-
{
    'name': "Kolapata Purchase Requisition",

    'summary': "Manage Inter company Transaction by Sending Requisition u",

    'description': """ Manage Inter company Transaction by Sending Requisition
    """,

    'author': "Umme Huzaifa",
    'website': "https://www.xsellencebdltd.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'uom', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_partner.xml',
        'views/requisition_transfer.xml',
        'data/data.xml',
        'views/requisition_receive.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}

