# -*- coding: utf-8 -*-
{
    'name': "Kolapata pos custom",

    'summary': "Hide some fields in POS Closing Pop Up",

    'description': """
    Hide some fields in POS Closing Pop Up
    """,

    'author': "Umme Huzaifa",
    'website': "https://xsellence-bangladesh-ltd.odoo.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '17.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

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
    'assets': {
        'point_of_sale._assets_pos': [
            'kolapata_pos_custom/static/src/xml/templates.xml',
        ],
    },
    'application': True,
    'license': 'LGPL-3',
}

