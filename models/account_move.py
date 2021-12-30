# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        for invoice in vals_list:
            for item in invoice.get('invoice_line_ids'):
                inv_line = item[2]
                product_id = inv_line.get('product_id')
                if inv_line.get('sale_line_ids', False):
                    so_line_id = inv_line.get('sale_line_ids')[0][1]
                    so_line = self.env['sale.order.line'].browse([so_line_id])
                    if so_line.pack_parent_line_id:
                        pack_line = so_line.pack_parent_line_id
                        product_pack = pack_line.product_id
                        pack_qty = len(product_pack.pack_line_ids)
                        unit_price = pack_line.price_unit / pack_qty
                        for pl in product_pack.pack_line_ids:
                            if product_id == pl.product_id.id:
                                inv_line['price_unit'] = unit_price * pl.quantity

        return super(AccountMove, self).create(vals_list)
