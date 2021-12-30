# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_invoiceable_lines(self, final=False):
        """Return the invoiceable lines for order `self`."""
        invoiceable_line_ids = self.env['sale.order.line']
        sale_order_lines = super(SaleOrder, self)._get_invoiceable_lines(final)
        # Exclude product pack from lines
        for line in sale_order_lines:
            if line.product_id.pack_ok:
                continue
            invoiceable_line_ids |= line

        return invoiceable_line_ids
