# -*- coding: utf-8 -*-
{
    'name': "Auto Update Product Cost from BOM",

    'summary': "Kolapata Auto Update Product Cost from BOM and Add Unit Cost in pos order line",

    'description': """ Kolapata Auto Update Product Cost from BOM and Add Unit Cost in pos order line
    """,

    'author': "Umme Huzaifa",
    'website': "https://xsellence-bangladesh-ltd.odoo.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '17.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'product', 'point_of_sale'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}

