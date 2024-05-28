# -*- coding: utf-8 -*-
{
    'name': "Cash Journal Report",

    'summary': "Cash Office Journal Report",

    'description': """ Cash Office Journal Report
    """,

    'author': "Umme Huzaifa",
    'website': "https://xsellence-bangladesh-ltd.odoo.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '17.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/report.xml',
        'reports/wizard.xml',
        'reports/cash_journal_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}

