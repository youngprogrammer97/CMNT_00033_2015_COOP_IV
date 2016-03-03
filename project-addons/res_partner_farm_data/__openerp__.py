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
    'name': 'Partner farm fields',
    'version': '1.0',
    'category': '',
    'description': """This module adds the fields required for a farm""",
    'author': 'Comunitea',
    'website': '',
    "depends": ['base', 'product', 'stock', 'account', 'account_asset',
                'account_analytic_plans', 'supplier_type', 'base_vat',
                'email_template', 'company_automatic_account_config',
                'automatic_company', 'partner_passwd', 'custom_groups'],
    "data": ['views/cost_imputation.xml', 'views/stock.xml',
             'views/output_quota_view.xml', 'views/lot_view.xml',
             'security/ir.model.access.csv', 'views/res_partner_view.xml',
             'views/lot_analysis.xml', 'views/res_company.xml',
             'views/product.xml', 'views/lot_report_template.xml',
             'lot_report.xml', 'data/lot_detail_sequence.xml',
             'wizard/lot_analysis_import.xml',
             'security/security.xml'],
    "installable": True
}
