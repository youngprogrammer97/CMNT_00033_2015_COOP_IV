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
from datetime import date

class ResPartner(models.Model):

    _inherit = 'res.partner'

    _sql_constraints = [
        ('vat_uniq', 'unique (vat)',
         _('Error! Specified VAT Number already exists for any other registered partner.'))
    ]

    farm = fields.Boolean('Farm')
    temporary_farm = fields.Boolean('Temporary farm', readonly=True, related='company_id.not_configured_accounting')
    is_cooperative = fields.Boolean('Cooperative', readonly=True, related='company_id.is_cooperative')
    partner_of = fields.Char('Partner of')
    exploitation_technician = fields.Many2one('res.users',
                                              'Exploitation technician')
    secondary_technician = fields.Many2one('res.users', 'Secondary technician')
    barn_type = fields.Selection((('free', 'Free'), ('stuck', 'Stuck'),
                                  ('mixed', 'Mixed')), 'Barn type')
    dairy_company = fields.Many2one('res.partner', 'Dairy company')
    bed_suppliers = fields.Many2many('res.partner', 'farm_bed_supplier_rel',
                                     'farm_id', 'bed_supplier_id',
                                     'Bed suppliers',
                                     domain=[('supplier', '=', True)])
    production_orientation = fields.Selection(
        (('milk', 'Milk'), ('meat', 'Meat'), ('mixed', 'Mixed'),
         ('orchard', 'Orchard'), ('other', 'Other')), 'Production orientation')
    cornadizas = fields.Integer('Cornadizas quantity')
    electric_power = fields.Integer('Electric power')
    average_annual_consumption = fields.Integer('Average annual consumption')
    pickup_frequency = fields.Integer('Pickup frequency')
    milk_tank_liter = fields.Integer('Milk tank liter')
    supplies_technician = fields.Many2one('res.users', 'Supplies technician')
    lactating_cows = fields.Many2one('product.product', 'Lactating cows')
    dry_cows = fields.Many2one('product.product', 'Dry cows')
    heifers = fields.Many2one('product.product', 'Heifers')
    bait = fields.Many2one('product.product', 'Bait')
    feeding_supplier = fields.Many2one('res.partner', 'Feeding supplier',
                                       domain=[('supplier', '=', True)])
    milk_quality_supplier = fields.Many2one('res.partner',
                                            'Milk quality supplier',
                                            domain=[('supplier', '=', True)])
    counselling_supplier = fields.Many2one('res.partner',
                                           'Counselling supplier',
                                           domain=[('supplier', '=', True)])
    clinic_supplier = fields.Many2one('res.partner', 'Clinic supplier',
                                      domain=[('supplier', '=', True)])
    mixer_truck_supplier = fields.Many2one('res.partner',
                                           'Mixer truck supplier',
                                           domain=[('supplier', '=', True)])
    replacement_supplier = fields.Many2one('res.partner',
                                           'Replacement supplier',
                                           domain=[('supplier', '=', True)])
    reproduction_supplier = fields.Many2one('res.partner',
                                            'Reproduction supplier',
                                            domain=[('supplier', '=', True)])
    adsg_certification_supplier = fields.Many2one(
        'res.partner', 'ADSG certification supplier',
        domain=[('supplier', '=', True)])
    special_mix = fields.Integer('Special mix')
    dry_mix = fields.Integer('Dry mix')
    mh = fields.Integer('mh')
    standard_fodder = fields.Integer('Standard fodder')
    concentrate_capacity = fields.Integer('concentrate capacity')
    forage_silos = fields.Integer('Forage silos')
    manure_pit = fields.Integer('Manure pit')
    manure_pit_outdoor = fields.Integer('Manure pit outdoor')
    trailer_access = fields.Boolean('Trailer access')
    employees_quantity = fields.Integer('Employees quantity')
    employee_count_ids = fields.One2many('employee.farm.count', 'partner_id', 'Employees')
    cow_count_ids = fields.One2many('cow.count', 'partner_id', 'Cows')
    heifer_0_3 = fields.Integer('Heifer 0-3 months')
    heifer_3_12 = fields.Integer('Heifer 3-12 months')
    heifer_plus_12 = fields.Integer('Heifer >12 months')
    milk_cow = fields.Integer('Milk cows')
    dry_cow = fields.Integer('Dry cows')

    @api.model
    def create(self, vals):
        if self._context.get('company_partner', False):
            vals['farm'] = True
        elif vals.get('farm', False):
            # El partner ha sido creado a mano.
            raise exceptions.Warning(_('Farm creation error'), _('To create farm must do it from the menu farm High'))
        res = super(ResPartner, self).create(vals)
        if vals.get('exploitation_technician', False):
            res.message_subscribe([res.exploitation_technician.partner_id.id])
        if vals.get('secondary_technician', False):
            res.message_subscribe([res.secondary_technician.partner_id.id])
        if res.employees_quantity:
            count_args = {
                        'partner_id': res.id,
                        'date': date.today(),
                        'user_id': self.env.user.id,
                        'quantity': res.employees_quantity,
            }
            self.env['employee.farm.count'].create(count_args)
        return res

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        for partner in self:
            if vals.get('employees_quantity', False):

                if not self.employee_count_ids:
                    count_args = {
                        'partner_id': self.id,
                        'date': date.today(),
                        'user_id': self.env.user.id,
                        'quantity': vals.get('employees_quantity'),
                    }
                    self.env['employee.farm.count'].create(count_args)
                else:
                    current = self.employee_count_ids.filtered(lambda record: record.state == 'current')
                    current.sudo().write({'quantity': vals.get('employees_quantity'),
                                          'user_id': self.env.user.id})
            if vals.get('heifer_0_3', False) or vals.get('heifer_3_12', False) or \
                    vals.get('heifer_plus_12', False) or vals.get('milk_cow', False) or \
                    vals.get('dry_cow', False):

                if not self.cow_count_ids:
                    count_args = {
                        'partner_id': self.id,
                        'date': date.today(),
                        'user_id': self.env.user.id,
                        'heifer_0_3': vals.get('heifer_0_3', 0),
                        'heifer_3_12': vals.get('heifer_3_12', 0),
                        'heifer_plus_12': vals.get('heifer_plus_12', 0),
                        'milk_cow': vals.get('milk_cow', 0),
                        'dry_cow': vals.get('dry_cow', 0),
                    }
                    self.env['cow.count'].create(count_args)
                else:
                    current = self.cow_count_ids.filtered(lambda record: record.state == 'current')
                    current.sudo().write({
                        'heifer_0_3': vals.get('heifer_0_3', self.heifer_0_3),
                        'heifer_3_12': vals.get('heifer_3_12', self.heifer_3_12),
                        'heifer_plus_12': vals.get('heifer_plus_12', self.heifer_plus_12),
                        'milk_cow': vals.get('milk_cow', self.milk_cow),
                        'dry_cow': vals.get('dry_cow', self.dry_cow),
                        'user_id': self.env.user.id,
                    })
            if vals.get('exploitation_technician', False):
                partner.message_subscribe(
                    [partner.exploitation_technician.partner_id.id])
            if vals.get('secondary_technician', False):
                partner.message_subscribe(
                    [partner.secondary_technician.partner_id.id])
        return res

    @api.multi
    def action_account_assets(self):
        return {
            'domain': "[('company_id','=', " + str(self.company_id.id) + ")]",
            'name': _('Assets'),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'context': {'tree_view_ref':
                        'account_asset.view_account_asset_asset_tree'},
            'res_model': 'account.asset.asset',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def action_locations(self):
        return {
            'domain': "[('company_id','='," + str(self.company_id.id) + "), ('usage', '=', 'internal')]",
            'name': _('Locations'),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'context': {'tree_view_ref':
                        'stock.view_location_tree2',
                        'default_company_id': self.company_id.id},
            'res_model': 'stock.location',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def action_analytic_plan(self):

        return {
            'domain': "[('company_id','='," + str(self.company_id.id) + ")]",
            'name': _('Analytic Plan'),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'context': {'default_company_id': self.company_id.id},
            'res_model': 'account.analytic.default',
            'type': 'ir.actions.act_window',
                }

class ResPartnerCategory(models.Model):

    _inherit = 'res.partner.category'

    description = fields.Text('Description')
    partner_id = fields.Many2many('res.partner', 'res_partner_res_partner_category_rel',
                                  'category_id', 'partner_id', 'Partners')
