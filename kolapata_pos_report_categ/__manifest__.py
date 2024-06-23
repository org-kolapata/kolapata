# -*- coding: utf-8 -*-
{
    'name': "Category Wise POS Pivot Report",

    'summary': """
        Kolapata Category Wise POS Order Pivot Report""",

    'description': """
        Kolapata Category Wise POS Order Pivot Report
    """,

    'author': "Umme Huzaifa",
    'website': "https://xsellence-bangladesh-ltd.odoo.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '17.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
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