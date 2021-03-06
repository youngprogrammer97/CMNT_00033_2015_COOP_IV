# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Quality simulator",
    "summary": "",
    "version": "8.0.1.0.0",
    "category": "Uncategorized",
    "website": "comunitea.com",
    "author": "Comunitea",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "custom_report",
    ],
    "data": [
        'views/quality_simulator.xml',
        'views/report_quality_simulator.xml',
        'report.xml',
        'security/ir.model.access.csv',
        'security/security.xml'
    ],
}
