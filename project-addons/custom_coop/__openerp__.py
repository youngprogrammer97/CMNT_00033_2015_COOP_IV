# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Coop customizations',
    'version': '8.0.2.0.0',
    'category': '',
    'description': """
        -Update stock wizard.
        """,
    'author': 'Comunitea',
    'website': '',
    "depends": ['account',
                'account_asset',
                'acc_analytic_acc_distribution_between',
                'automatic_company',
                'l10n_es_account_asset',
                'analytic',
                'partner_passwd',
                'company_assign_users',
                'company_automatic_account_config',
                'company_open_fiscalyear',
                'custom_colors',
                'custom_email_template',
                'custom_groups',
                'custom_menu',
                'protect_cud_parent_companies',
                'res_partner_farm_data',
                'simplify_invoice',
                'supplier_type',
                'stock'],
    "data": ['wizard/stock_location_update_stock.xml',
             'views/stock.xml',
             'views/partner_view.xml',
             'data/ir_cron.xml',
             'data/account_invoice_workflow.xml',
             'data/tax.xml',
             'data/account.tax.template.csv',
             'views/user_preferences.xml',
             'views/res_company.xml',
             'views/calendar_event.xml',
             'views/document_view.xml',
             'views/res_partner.xml',
             'views/mail_attachment_partner.xml',
             'views/account_asset_asset.xml',
             'security/ir.model.access.csv',
             'data/account_account.xml',
             'data/paperformat.xml',
             'views/analytic_view.xml',
             'views/product.xml',
             'views/res_group.xml',
             'views/account_invoice.xml',
             'views/base_view.xml'],
    "installable": True,

    'qweb': [
        'static/src/xml/suggestions.xml',
    ],
}
