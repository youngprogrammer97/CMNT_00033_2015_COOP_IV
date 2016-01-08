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
from openerp import models, fields, api, exceptions, _, SUPERUSER_ID
from lxml import etree


class ResUsers(models.Model):

    _inherit = 'res.users'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(ResUsers, self).fields_view_get(view_id=view_id,
                                                    view_type=view_type,
                                                    toolbar=toolbar,
                                                    submenu=submenu)
        view_obj = self.env.ref('base.view_users_form')
        if view_type == 'form' and self.env.user.id != SUPERUSER_ID and view_id == view_obj.id:
            view = etree.XML(res['arch'])
            for separator in view.xpath("//notebook/page[1]/group[2]/separator[@string!='" + _("User types") + "']"):
                separator.set("modifiers", '{"invisible": true}')
            id_1 = self.env.ref('custom_groups.group_admin').id
            id_2 = self.env.ref('custom_groups.group_tech_mngnt').id
            id_3 = self.env.ref('custom_groups.group_tech_feed').id
            id_4 = self.env.ref('custom_groups.group_tech_sales').id
            id_5 = self.env.ref('custom_groups.group_rancher').id
            custom_names = ['in_group_%s' % x for x in (id_1, id_2, id_3,
                                                        id_4, id_5)]
            for field in view.xpath("//field[starts-with(@name,'in_group')]"):
                if field.get('name') not in (custom_names):
                    field.set("modifiers", '{"invisible": true}')

            for field in view.xpath("//field[starts-with(@name,'sel_groups')]"):
                field.set("modifiers", '{"invisible": true}')
            res['arch'] = etree.tostring(view)
        if view_type == 'form' and view_id == view_obj.id:
            view = etree.XML(res['arch'])
            description_text = _("<h4>Lorem ipsum dolor sit amet, consectetur adipiscing elit,"
                                 " sed do eiusmod tempor incididunt ut labore et dolore</h4>"
                                 "<p>-Adminsitrador: Ut enim ad minim veniam</p>"
                                 "<p>-Técnico alimentación: quis nostrud exercitation ullamco laboris nisi</p>"
                                 "<p>-...</p><p>-...</p>")
            separator = view.xpath("//notebook/page[1]/group[2]/separator[@string='" + _("User types") + "']")[0]
            separator.addnext(etree.XML('<group colspan="4"><div>%s</div></group>' % description_text))
            res['arch'] = etree.tostring(view)
        return res
