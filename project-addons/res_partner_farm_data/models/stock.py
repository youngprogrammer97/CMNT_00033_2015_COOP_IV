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
from openerp import models, fields, api, exceptions, _


class StockLocation(models.Model):

    _inherit = 'stock.location'

    type = fields.Selection(
        (('vertical', 'Vertical'), ('trentch', 'Trentch'), ('walls', 'Walls')),
        'Type')
    total_capacity = fields.Float('Total capacity')
    attachment_count = fields.Integer(compute='_compute_attachment_count')

    def _compute_attachment_count(self):
        for location in self:
            location.attachment_count = len(self.env['ir.attachment'].search(
                [('res_model', '=', 'stock.location'),
                 ('res_id', '=', location.id)]))
