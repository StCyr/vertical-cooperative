# -*- coding: utf-8 -*-
# © 2013-2018 Open Architects Consulting SPRL.
# © 2018 Coop IT Easy SCRLfs. (<http://www.coopiteasy.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Easy My Coop",
    "version": "9.1.0.0.0",
    "depends": ["base",
                "sale",
                "purchase",
                "account_accountant",
                "product",
                "partner_firstname",
                "partner_contact_birthdate",
                "partner_contact_address",
                "website",
                "website_recaptcha_reloaded",
                "theme_light",
                "base_iban",
                "email_template_config",
                ],
    "author": "Houssine BAKKALI <houssine@coopiteasy.be>",
    "category": "Cooperative management",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "description": """
    This module allows to manage the cooperator subscription and all the
     cooperative business processes.
    """,
    'data': [
        'security/easy_my_coop_security.xml',
        'security/ir.model.access.csv',
        # 'wizard/cooperative_history_wizard.xml',   # not loaded, why?
        'wizard/create_subscription_from_partner.xml',
        'wizard/update_partner_info.xml',
        'wizard/validate_subscription_request.xml',
        'wizard/update_share_line.xml',
        'view/subscription_request_view.xml',
        'view/email_template_view.xml',
        'view/res_partner_view.xml',
        'view/cooperator_register_view.xml',
        'view/operation_request_view.xml',
        'view/account_invoice_view.xml',
        'view/subscription_template.xml',
        'view/product_view.xml',
        'view/res_company_view.xml',
        'view/account_journal_view.xml',
        'view/menu.xml',
        'data/easy_my_coop_data.xml',
        'report/easy_my_coop_report.xml',
        'report/cooperator_invoice_G002.xml',
        'report/cooperator_certificat_G001.xml',
        'report/cooperator_subscription_G001.xml',
        'report/cooperator_register_G001.xml',
        'data/mail_template_data.xml',
    ],
    'installable': True,
    'application': True,
}
