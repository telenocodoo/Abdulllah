# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class SaleAdvancePaymentInv(models.TransientModel):
#     _inherit = 'sale.advance.payment.inv'
#
#
#     def create_invoices(self):
#         res = super(SaleAdvancePaymentInv, self).create_invoices()
#         # print(">>>>>>>>>>>>", res['context'])
#         res['context'] = {'default_bayan':'bayanbayanbayanbayanbayan'}
#         res['context']['default_landing_place'] = 'landing_place'
#         print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#         # print(">>>>>>>>>>>>", res['context'])
#         # print("sale_orders", res)
#         # print("sale_orders", res['sale_orders'])
#         return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    arabic_name = fields.Char(related='product_id.arabic_name')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_of_prealert = fields.Date(string="Date of pre alert")
    eta_date = fields.Date(string="ETA")
    po_date = fields.Date(string="P.O Date")
    saddad_payment_date = fields.Date(string="Saddad Payment Date")
    consinee = fields.Many2one('consinee.sale.order', string="Consinee")
    bill_of_lading = fields.Char(string="Bill of Lading")
    bayan = fields.Char(string="Bayan")
    shipping_line = fields.Many2one('shipping.sale.order', string="Shipping line")
    landing_place = fields.Char('Sea Port')
    order_status_id = fields.Many2one('fmt.order.status', string="Order Status", track_visibility='onchange')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    arabic_name = fields.Char(related='product_id.arabic_name')


class AccountMove(models.Model):
    _inherit = 'account.move'

    date_of_prealert = fields.Date(string="Date of pre alert")
    eta_date = fields.Date(string="ETA")
    po_date = fields.Date(string="P.O Date")
    saddad_payment_date = fields.Date(string="Saddad Payment Date")
    consinee = fields.Many2one('consinee.sale.order', string="Consinee")
    bill_of_lading = fields.Char(string="Bill of Lading")
    bayan = fields.Char(string="Bayan")
    shipping_line = fields.Many2one('shipping.sale.order', string="Shipping line")
    landing_place = fields.Char('Sea Port')
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
