# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_round, format_date, get_lang


class ResPartner(models.Model):
    _inherit = "res.partner"

    allow_pricelist_download = fields.Boolean("Portal Pricelist Download")
    show_product_stock = fields.Boolean("Show Stock")
    stock_display_option = fields.Selection(
        [('quantity', 'Show Actual Stock Quantity'), ('status', 'Show Stock Status Only')],
        string="Stock Display Option", default='status')

    @api.onchange("allow_pricelist_download")
    def allow_pricelist_download_change(self):
        if not self.allow_pricelist_download:
            self.show_product_stock = False
            self.stock_display_option = 'status'

    def get_pricelist_rules(self, pricelist_id, ecom_category=None, availability_filter=None, group_by_category=False):
        product_ids = {}
        if pricelist_id:
            item_ids = pricelist_id.item_ids
            for rule in item_ids:
                if rule.applied_on == "0_product_variant":
                    product_id = rule.product_id
                    if ecom_category and not product_id.public_categ_ids:
                        continue
                    if ecom_category and product_id.public_categ_ids:
                        if not set(ecom_category) & set(product_id.public_categ_ids.ids):
                            continue
                    product_ids[product_id.id] = product_id
                elif rule.applied_on == "1_product":
                    if ecom_category and not rule.product_tmpl_id.public_categ_ids:
                        continue
                    if ecom_category and rule.product_tmpl_id.public_categ_ids:
                        if not set(ecom_category) & set(rule.product_tmpl_id.public_categ_ids.ids):
                            continue
                    product_variant_ids = rule.product_tmpl_id.product_variant_ids
                    for product_id in product_variant_ids:
                        product_ids[product_id.id] = product_id

                elif rule.applied_on == "2_product_category":
                    categ_id = rule.categ_id
                    domain = [("categ_id", "child_of", categ_id.id)]
                    if ecom_category:
                        domain.append(("public_categ_ids.id", "in", ecom_category))

                    product_variant_ids = self.env["product.product"].search(domain)
                    for product_id in product_variant_ids:
                        product_ids[product_id.id] = product_id

                elif rule.applied_on == "3_global":
                    domain = []
                    if ecom_category:
                        domain.append(("public_categ_ids.id", "in", ecom_category))
                    product_variant_ids = self.env["product.product"].search(domain)
                    for product_id in product_variant_ids:
                        product_ids[product_id.id] = product_id

        pricelist_products = []
        for product_id in product_ids.values():
            rule_id = pricelist_id._get_product_rule(
                product_id,
                1,
                uom=product_id.uom_id,
                date=fields.Date.to_date(self.env.context.get('date') or fields.Date.today()),
            )
            rule = self.env["product.pricelist.item"].browse(rule_id)
            if not rule:
                continue
            rule_data = self.get_price_rule_data(pricelist_id, rule, product_id)
            if self._filter_by_availability(rule_data, availability_filter):
                pricelist_products.append(rule_data)

        if group_by_category:
            return self._group_products_by_category(pricelist_products)

        pricelist_products = sorted(pricelist_products, key=lambda item: item['product_id'].with_context(
            display_default_code=False).display_name)
        return pricelist_products

    def _group_products_by_category(self, pricelist_products):
        grouped = {}
        for product_data in pricelist_products:
            categs = product_data['product_id'].public_categ_ids
            if not categs:
                if 'uncategorized' not in grouped:
                    grouped['uncategorized'] = {'category': self.env['product.public.category'],
                                                'category_name': 'Uncategorized', 'products': []}
                grouped['uncategorized']['products'].append(product_data)
            else:
                for categ in categs:
                    if categ.id not in grouped:
                        grouped[categ.id] = {'category': categ, 'category_name': categ.name, 'products': []}
                    grouped[categ.id]['products'].append(product_data)

        result = []
        for key in sorted(grouped.keys(), key=lambda x: grouped[x]['category_name'] if isinstance(x, int) else 'zzz'):
            result.append(grouped[key])
        return result

    def get_price_rule_data(self, pricelist_id, rule, product_id):
        min_quantity = 0
        price_duration = "-"
        precision = product_id.uom_id.rounding
        if rule.min_quantity:
            min_quantity = float_round(rule.min_quantity, precision_rounding=precision)
        if rule.date_start and rule.date_end:
            price_duration = format_date(self.env, rule.date_start,
                                         lang_code=get_lang(self.env).code) + " - "
            price_duration += format_date(self.env, rule.date_end,
                                          lang_code=get_lang(self.env).code)
        else:
            if rule.date_start:
                price_duration = format_date(self.env, rule.date_start,
                                             lang_code=get_lang(self.env).code)
            if rule.date_end:
                price_duration = format_date(self.env, rule.date_end,
                                             lang_code=get_lang(self.env).code)
        if rule.date_start:
            date = rule.date_start
        else:
            date = self.env.context.get('date') or fields.Date.today()
            date = fields.Date.to_date(date)
        price_uom = product_id.uom_id
        price = rule._compute_price(product_id, quantity=rule.min_quantity or 1, uom=price_uom, date=date)

        website = self.env['website'].get_current_website()
        free_qty = website._get_product_available_qty(product_id)
        if free_qty < 0:
            free_qty = 0
        return {
            "product_id": product_id,
            "min_qty": min_quantity,
            "price_duration": price_duration,
            "price": price,
            "show_product_stock": self.show_product_stock,
            "stock_display_option": self.stock_display_option,
            "stock_on_hand": free_qty
        }

    def _filter_by_availability(self, rule_data, availability_filter):
        if not availability_filter:
            return True

        stock_qty = rule_data['stock_on_hand']
        if availability_filter == 'in_stock':
            return stock_qty > 0
        elif availability_filter == 'out_of_stock':
            return stock_qty <= 0

        return True
