# -*- coding: utf-8 -*-
import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    # def create_invoices(self):
    #     invoice = super(SaleAdvancePaymentInv, self).create_invoices()
    #     print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    #     print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL",invoice)
    #     return invoice

    # def create_invoices(self):
    #     sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
    #
    #     if self.advance_payment_method == 'delivered':
    #         sale_orders._create_invoices(final=self.deduct_down_payments)
    #     else:
    #         # Create deposit product if necessary
    #         if not self.product_id:
    #             vals = self._prepare_deposit_product()
    #             self.product_id = self.env['product.product'].create(vals)
    #             self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)
    #
    #         sale_line_obj = self.env['sale.order.line']
    #         for order in sale_orders:
    #             if self.advance_payment_method == 'percentage':
    #                 amount = order.amount_untaxed * self.amount / 100
    #             else:
    #                 amount = self.fixed_amount
    #             if self.product_id.invoice_policy != 'order':
    #                 raise UserError(_('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
    #             if self.product_id.type != 'service':
    #                 raise UserError(_("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
    #             taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
    #             if order.fiscal_position_id and taxes:
    #                 tax_ids = order.fiscal_position_id.map_tax(taxes, self.product_id, order.partner_shipping_id).ids
    #             else:
    #                 tax_ids = taxes.ids
    #             context = {'lang': order.partner_id.lang}
    #             analytic_tag_ids = []
    #             for line in order.order_line:
    #                 analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]
    #             so_line = sale_line_obj.create({
    #                 'name': _('Down Payment: %s') % (time.strftime('%m %Y'),),
    #                 'price_unit': amount,
    #                 'product_uom_qty': 0.0,
    #                 'order_id': order.id,
    #                 'discount': 0.0,
    #                 'product_uom': self.product_id.uom_id.id,
    #                 'product_id': self.product_id.id,
    #                 'analytic_tag_ids': analytic_tag_ids,
    #                 'tax_id': [(6, 0, tax_ids)],
    #                 'is_downpayment': True,
    #             })
    #             # del context
    #             self._create_invoice(order, so_line, amount)
    #     if self._context.get('open_invoices', False):
    #         return sale_orders.action_view_invoice()
    #     return {'type': 'ir.actions.act_window_close'}



# class SaleAdvancePaymentInv(models.TransientModel):
#     _inherit = 'sale.advance.payment.inv'
#
#     def create_invoices(self):
#         res = super(SaleAdvancePaymentInv, self).create_invoices()
#         print(">>>>>>>>>>>>", res)
#         res['context'].update({
#             'default_date_of_prealert': self.date_of_prealert,
#             'default_eta_date': self.eta_date,
#             'default_po_date': self.po_date,
#             'default_saddad_payment_date': self.saddad_payment_date,
#             'default_consinee': self.consinee.id,
#             'default_bill_of_lading': self.bill_of_lading,
#             'default_bayan': self.bayan,
#             'default_shipping_line': self.shipping_line.id,
#             'default_landing_place': self.landing_place.id,
#             'default_order_status_id': self.order_status_id.id,
#         })
#         # res['context'].update({'default_landing_place': 'landing_place'})
#         print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#         print(">>>>>>>>>>>>", res['context'])
#         # print("sale_orders", res)
#         # print("sale_orders", res['sale_orders'])
#         return res
#
#     def _create_invoice(self, order, so_line, amount):
#         # res = super(SaleAdvancePaymentInv, self)._create_invoice(self, order, so_line, amount)
#         # print(">>>>>>>>>>>>", res['context'])
#         # res['context'] = {'default_bayan':'bayanbayanbayanbayanbayan'}
#         # res['context']['default_landing_place'] = 'landing_place'
#         print(">>>>>>>>>>>>>>>>>>>second function>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#         # print(">>>>>>>>>>>>", res)
#         # res = super(SaleAdvancePaymentInv, self)._create_invoice(self, order, so_line, amount)
#         print(">>>>>>>>>>>>", order)
#         # print("sale_orders", res)
#         # print("sale_orders", res['sale_orders'])
#         # return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    arabic_name = fields.Char(related='product_id.arabic_name')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_of_prealert = fields.Date(string="Date of pre alert")
    eta_date = fields.Date(string="ETA")
    po_date = fields.Date(string="D.O Date")
    saddad_payment_date = fields.Date(string="Saddad Payment Date")
    consinee = fields.Many2one('consinee.sale.order', string="Consinee")
    bill_of_lading = fields.Char(string="Bill of Lading")
    bayan = fields.Char(string="Bayan")
    shipping_line = fields.Many2one('shipping.sale.order', string="Shipping line")
    landing_place = fields.Many2one('sea.port')
    order_status_id = fields.Many2one('fmt.order.status', string="Order Status", track_visibility='onchange')

    def action_view_invoice(self):
        res = super(SaleOrder, self).action_view_invoice()
        res['context'].update({
            'default_date_of_prealert': self.date_of_prealert,
            'default_eta_date': self.eta_date,
            'default_po_date': self.po_date,
            'default_saddad_payment_date': self.saddad_payment_date,
            'default_consinee': self.consinee.id,
            'default_bill_of_lading': self.bill_of_lading,
            'default_bayan': self.bayan,
            'default_shipping_line': self.shipping_line.id,
            'default_landing_place': self.landing_place.id,
            'default_order_status_id': self.order_status_id.id,
        })
        return res


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    arabic_name = fields.Char(related='product_id.arabic_name')


class AccountMove(models.Model):
    _inherit = 'account.move'

    date_of_prealert = fields.Date(string="Date of pre alert")
    eta_date = fields.Date(string="ETA")
    po_date = fields.Date(string="D.O Date")
    saddad_payment_date = fields.Date(string="Saddad Payment Date")
    consinee = fields.Many2one('consinee.sale.order', string="Consinee")
    bill_of_lading = fields.Char(string="Bill of Lading")
    bayan = fields.Char(string="Bayan")
    shipping_line = fields.Many2one('shipping.sale.order', string="Shipping line")
    landing_place = fields.Many2one('sea.port')
    order_status_id = fields.Many2one('fmt.order.status', string="Order Status", track_visibility='onchange')

    def get_line_with_vat(self):
        total_with_vat = 0
        total_without_vat = 0
        for rec in self:
            for line in rec.invoice_line_ids:
                if line.tax_ids:
                    total_with_vat += line.price_subtotal
                else:
                    total_without_vat += line.price_subtotal
        vals= {'total_with_vat': total_with_vat ,'total_without_vat': total_without_vat,}
        return vals


class FmtOrderStatus(models.Model):
    _name = 'fmt.order.status'

    name = fields.Char(required=1)


class ConsineeSaleOrder(models.Model):
    _name = 'consinee.sale.order'

    name = fields.Char(required=1)


class ShippingSaleOrder(models.Model):
    _name = 'shipping.sale.order'

    name = fields.Char(required=1)


class SeaPort(models.Model):
    _name = 'sea.port'

    name = fields.Char(required=1)
