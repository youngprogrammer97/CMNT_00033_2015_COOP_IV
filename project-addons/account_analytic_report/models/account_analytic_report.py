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
import time
from datetime import date, datetime


class AccountAnalyticReport(models.Model):

    _name = 'account.analytic.report'

    name = fields.Char('Name', required=True)
    template_id = fields.Many2one('account.analytic.report.template',
                                  'Template', required=True)

    calc_date = fields.Date('Calc date')
    ref_1 = fields.Reference(
        selection=[('res.company', 'Company'),
                   ('res.partner.category', 'Farm group')], string='Reference')
    from_date_1 = fields.Date('From date')
    to_date_1 = fields.Date('To date')
    milk_1 = fields.Float('Milk')
    total_cows_1 = fields.Float('Total cows')
    employees_1 = fields.Float('Total employees')
    total_heifer_1 = fields.Float('Total heifer')
    hectare_1 = fields.Float('Hectare')
    milk_and_dry_1 = fields.Integer('Milk and dry cows')
    milk_cows_1 = fields.Integer('Milk cows')
    zero_three_heifer_1 = fields.Integer('0-3 months heifer')
    three_twelve_heifer_1 = fields.Integer('3-12 months heifer')
    plus_twelve_heifer_1 = fields.Integer('plus 12 months heifer')
    months_1 = fields.Float('Months')
    cost_feed_milk_cow_day_1 = fields.Float('Coste de Alimentación vaca lactación/día (€)')
    cost_feed_dry_cow_day_1 = fields.Float('Coste de Alimentación vaca seca/día (€)')
    corn_hectares_1 = fields.Float('Corn hectares')
    kg_corn_1 = fields.Float('Corn Kg')
    grass_hectares_1 = fields.Float('Grass hectares')
    kg_grass_1 = fields.Float('Grass Kg')
    cereal_hectares_1 = fields.Float('Cereal hectares')
    kg_cereal_1 = fields.Float('Cereal Kg')
    dry_grass_hectares_1 = fields.Float('Dry grass hectares')
    kg_dry_grass_1 = fields.Float('Dry grass Kg')
    another_hectares_1 = fields.Float('Another hectares')
    kg_another_1 = fields.Float('Another Kg')
    cow_buy_1 = fields.Float('Livestock purchased')
    inventory_difference_1 = fields.Float('Inventory difference')

    ref_2 = fields.Reference(
        selection=[('res.company', 'Company'),
                   ('res.partner.category', 'Farm group')], string='Reference')
    from_date_2 = fields.Date('From date')
    to_date_2 = fields.Date('To date')
    milk_2 = fields.Float('Milk')
    total_cows_2 = fields.Float('Total cows')
    employees_2 = fields.Float('Total employees')
    total_heifer_2 = fields.Float('Total heifer')
    hectare_2 = fields.Float('Hectare')
    milk_and_dry_2 = fields.Integer('Milk and dry cows')
    milk_cows_2 = fields.Integer('Milk cows')
    zero_three_heifer_2 = fields.Integer('0-3 months heifer')
    three_twelve_heifer_2 = fields.Integer('3-12 months heifer')
    plus_twelve_heifer_2 = fields.Integer('plus 12 months heifer')
    months_2 = fields.Float('Months')
    cost_feed_milk_cow_day_2 = fields.Float('Coste de Alimentación vaca lactación/día (€)')
    cost_feed_dry_cow_day_2 = fields.Float('Coste de Alimentación vaca seca/día (€)')
    corn_hectares_2 = fields.Float('Corn hectares')
    kg_corn_2 = fields.Float('Corn Kg')
    grass_hectares_2 = fields.Float('Grass hectares')
    kg_grass_2 = fields.Float('Grass Kg')
    cereal_hectares_2 = fields.Float('Cereal hectares')
    kg_cereal_2 = fields.Float('Cereal Kg')
    dry_grass_hectares_2 = fields.Float('Dry grass hectares')
    kg_dry_grass_2 = fields.Float('Dry grass Kg')
    another_hectares_2 = fields.Float('Another hectares')
    kg_another_2 = fields.Float('Another Kg')
    cow_buy_2 = fields.Float('Livestock purchased')
    inventory_difference_2 = fields.Float('Inventory difference')

    line_ids = fields.One2many('account.analytic.report.line', 'report_id',
                               'Lines')
    state = fields.Selection(
        [('draft', 'Draft'), ('calc', 'Calculating'),
         ('calc_done', 'Calculated'), ('done', 'Done'), ('cancel', 'Cancel')],
        'State', default='draft')

    title_1 = fields.Char('Title value 1')
    title_2 = fields.Char('Title value 2')

    def _get_company(self):
        return self.env.user.company_id

    company_id = fields.Many2one('res.company', 'Company', default=_get_company)

    @api.multi
    def _get_companies(self, company_1_2=1):
        self.ensure_one()
        companies = self.env['res.company']
        ref_field = 'ref_%s' % str(company_1_2)
        if not self[ref_field]:
            return companies
        if 'res.company' == str(self[ref_field]._model):
            companies = self[ref_field]
        elif 'res.partner.category' == str(self[ref_field]._model):
            partners = self.env['res.partner'].search(
                [('category_id', '=', self[ref_field].id)])
            companies = partners.filtered(
                lambda partner: partner.farm).mapped('company_id')
        return companies

    @api.multi
    def _set_milk_fields(self):
        self.ensure_one()
        for i in (1, 2):
            from_date = 'from_date_' + str(i)
            to_date = 'to_date_' + str(i)
            companies = self._get_companies(i)
            partner_companies = companies.mapped('partner_id')
            quotas = self.env['output.quota'].search(
                [('farm_id', 'in', partner_companies._ids),
                 ('date', '>=', self[from_date]),
                 ('date', '<=', self[to_date])])
            self['milk_' + str(i)] = sum([x.value for x in quotas])

    @api.multi
    def _set_total_cows_fields(self):
        self.ensure_one()
        for i in (1, 2):
            from_date = 'from_date_' + str(i)
            to_date = 'to_date_' + str(i)
            companies = self._get_companies(i)
            partner_companies = companies.mapped('partner_id')
            total_cows = 0
            tota_heifer = 0
            milk_and_dry = 0
            milk_cows = 0
            zero_three_heifer = 0
            plus_twelve_heifer = 0
            for partner in partner_companies:
                cow_counts = self.env['cow.count'].search(
                    [('partner_id', '=', partner.id),
                     ('date', '>=', self[from_date]),
                     ('date', '<=', self[to_date])])
                if not cow_counts:
                    continue
                total_count = len(cow_counts)
                heifer_0_3 = sum(cow_counts.mapped('heifer_0_3')) / total_count
                heifer_3_12 = sum(cow_counts.mapped('heifer_3_12')) / total_count
                heifer_plus_12 = sum(cow_counts.mapped('heifer_plus_12')) / total_count
                milk_cow = sum(cow_counts.mapped('milk_cow')) / total_count
                dry_cow = sum(cow_counts.mapped('dry_cow')) / total_count
                total_cows += sum((heifer_0_3, heifer_3_12, heifer_plus_12, milk_cow, dry_cow))
                tota_heifer += sum((heifer_0_3, heifer_3_12, heifer_plus_12))
                milk_and_dry += milk_cow + dry_cow
                milk_cows += milk_cow
                zero_three_heifer += heifer_3_12
                plus_twelve_heifer += heifer_plus_12
            self['total_cows_' + str(i)] = total_cows
            self['total_heifer_' + str(i)] = tota_heifer
            self['milk_and_dry_' + str(i)] = milk_and_dry
            self['milk_cows_' + str(i)] = milk_cows
            self['zero_three_heifer_' + str(i)] = zero_three_heifer
            self['plus_twelve_heifer_' + str(i)] = plus_twelve_heifer

    @api.multi
    def _set_employee_fields(self):
        self.ensure_one()
        for i in (1, 2):
            from_date = 'from_date_' + str(i)
            to_date = 'to_date_' + str(i)
            companies = self._get_companies(i)
            partner_companies = companies.mapped('partner_id')
            total_employee = 0
            for partner in partner_companies:
                employee_count = self.env['employee.farm.count'].search(
                    [('partner_id', '=', partner.id),
                     ('date', '>=', self[from_date]),
                     ('date', '<=', self[to_date])])
                if not employee_count:
                    continue
                total_count = len(employee_count)
                total_employee += sum(employee_count.mapped('quantity')) / total_count
            self['employees_' + str(i)] = total_employee

    @api.multi
    def _set_hectare_fields(self):
        self.ensure_one()
        for i in (1, 2):
            from_date = 'from_date_' + str(i)
            to_date = 'to_date_' + str(i)
            if self[from_date] and self[to_date]:
                years = [str(self[from_date][:4]), str(self[to_date][:4])]
                years = list(set(years))
            else:
                years = [str(date.today().year)]
            companies = self._get_companies(i)
            partner_companies = companies.mapped('partner_id')
            hectare = 0
            for partner in partner_companies:
                total = 0
                for year in years:
                    total += partner.with_context(use_year=year).total_net_surface
                hectare += total / len(years)
            self['hectare_' + str(i)] = hectare

    @api.multi
    def _set_months(self):
        self.ensure_one()
        for i in (1, 2):
            from_date_str = self['from_date_' + str(i)]
            to_date_str = self['to_date_' + str(i)]
            if from_date_str and to_date_str:
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
                self['months_' + str(i)] = abs((from_date - to_date).days) / 30.0

    @api.multi
    def act_button_update_fields(self):
        for report in self:
            report._set_milk_fields()
            report._set_total_cows_fields()
            report._set_employee_fields()
            report._set_hectare_fields()
            report._set_months()
        return True

    @api.multi
    def refresh_values(self):
        companies_1 = self._get_companies(1)
        companies_2 = self._get_companies(2)
        self.line_ids.set_values(companies_1, companies_2)

    @api.multi
    def act_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def act_done(self):
        self.write({'state': 'done'})

    @api.multi
    def calculate(self):
        self.write({
            'state': 'calc',
            'calc_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'title_1': self.template_id.title_1,
            'title_2': self.template_id.title_2,
        })
        self.line_ids.unlink()
        for line in self.template_id.line_ids:
            self.env['account.analytic.report.line'].create({
                'report_id': self.id,
                'code': line.code,
                'sequence': line.sequence,
                'name': line.name,
                'notes': '',
                'template_line_id': line.id,
                'css_style': line.css_style
            })
        for line in self.line_ids:
            if line.template_line_id.parent_id:
                parent_line = self.env['account.analytic.report.line'].search(
                    [('template_line_id', '=',
                      line.template_line_id.parent_id.id),
                     ('report_id', '=', self.id)])
                line.parent_id = parent_line
        self.refresh_values()
        self.state = 'calc_done'


class AccountAnalyticReportLine(models.Model):

    _name = 'account.analytic.report.line'

    report_id = fields.Many2one('account.analytic.report', 'report')
    code = fields.Char('Code', required=True)
    sequence = fields.Integer('sequence', default=10)
    name = fields.Char('Name', required=True)
    notes = fields.Text('Notes')
    value_1_1 = fields.Text('Value 1.1')
    value_1_2 = fields.Text('Value 1.2')
    value_2_1 = fields.Text('Value 2.1')
    value_2_2 = fields.Text('Value 2.2')
    template_line_id = fields.Many2one('account.analytic.report.template.line',
                                       'Template line')
    parent_id = fields.Many2one('account.analytic.report.line', 'Parent')
    child_ids = fields.One2many('account.analytic.report.line', 'parent_id',
                                'Childs')
    css_style = fields.Selection(
        [('red_bold', 'Red bold'), ('green_bold', 'Green bold'), ('bold', 'Bold'), ('red', 'Red')],
        'Css style')

    @api.multi
    def set_values(self, companies_1, companies_2):
        for line in self:
            for field in ['value_1_1', 'value_1_2']:
                field_val = 0.0
                for company in companies_1:
                    field_val += line.eval_field(company,field)
                line[field] = field_val
            for field in ['value_2_1', 'value_2_2']:
                field_val = 0.0
                for company in companies_2:
                    field_val += line.eval_field(company,field)
                line[field] = field_val

    @api.multi
    def eval_field(self, company, field):
        self.ensure_one()
        if not self.template_line_id[field]:
            return sum([x.eval_field(company, field) for x in self.child_ids])
        vals = self.template_line_id[field].replace(' ', '').split(',')
        final_vals = []
        for val in vals:
            # Se controla si hay parentesis en el valor
            init_par = val.count('(')
            end_par = val.count(')')
            val = val.replace('(', '').replace(')', '')
            if val[0] in '+-*/':
                sign = init_par and val[0] + ('(' * init_par) or val[0]
            else:
                sign = init_par and '+' + ('(' * init_par) or '+'
                val = '+' + val
            if val[1] == '[': # se referencia a otro valor de la misma linea
                another_field = 'value_' + val[2:-1]
                val = sign + str(self[another_field])

            elif val[1] == '.':  # Se referencia a otra linea
                code_line = val.replace('.', '')[1:]
                line = self.search([('report_id', '=', self.report_id.id),
                                    ('code', '=', code_line)])
                if not line:
                    raise exceptions.Warning(
                        _('Line not found'),
                        _('Line with code %s not found') % code_line)
                val = sign + str(line[field])
            elif val[1] == "'":  # Valor literal
                val = sign + val[2:]
            elif val[1] == '#':  # Se referencia a un campo del informe.
                called_field = val.replace('#', '')[1:] + '_' + field[-3]
                val = sign + str(self.report_id[called_field])
            else:  # se referencia a una cuenta
                account = self.env['account.analytic.account'].search(
                    [('code', '=', val[1:])])
                if not account:
                    raise exceptions.Warning(
                        _('Account not found'),
                        _('Account with code %s not found') % val[1:])
                from_date = self.report_id.from_date_1
                to_date = self.report_id.to_date_1
                val = sign + str(account.with_context(company_id=company.id,
                                 from_date=from_date, to_date=to_date).balance)
            if end_par:
                val += ')' * end_par
            final_vals.append(val)
        try:
            result = round(eval(''.join(final_vals)),2)
        except ZeroDivisionError:
            raise exceptions.Warning(_('Calc error'), _('Missing data cover'))
        return result
