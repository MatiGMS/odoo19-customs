# -*- coding: utf-8 -*-
import io

import xlsxwriter
from odoo.addons.portal.controllers.portal import CustomerPortal

from odoo import http, fields
from odoo.http import request, content_disposition
from odoo.tools import format_date, get_lang


class CustomerPortalEx(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        if 'pricelist_count' in counters:
            if partner.property_product_pricelist and partner.allow_pricelist_download:
                pricelist_count = 1
            else:
                pricelist_count = 0
            values.update({
                'pricelist_count': pricelist_count,
            })
        return values

    @http.route(['/my/product-pricelist'], type='http', auth="user", website=True)
    def portal_my_product_pricelist(self, **kw):
        partner = request.env.user.partner_id
        if partner.property_product_pricelist and partner.allow_pricelist_download:
            categories = request.env["product.public.category"].search_read([], ["id", "name"])
            values = {
                "page_name": "product_pricelist",
                "ecom_categories": categories,
                "show_stock_filter": partner.show_product_stock
            }
            return request.render("pricelist_portal_download_pyb.portal_product_pricelist_page", values)
        else:
            return request.render('website.page_404')

    @http.route("/customer/pricelist", type="http", auth="user", website=True, methods=['POST'])
    def get_customer_pricelist(self, **post):
        partner = request.env.user.partner_id
        pricelist = partner.property_product_pricelist
        if pricelist and partner.allow_pricelist_download:
            pricelist_file_type = post.get("pricelist_file_type")
            pricelist_product_categ = request.httprequest.form.getlist("pricelist_product_categ")
            availability_filter = post.get("availability_filter")
            group_by_category = post.get("group_by_category") == '1'
            values_to_render = {'report_type': 'pdf', 'group_by_category': group_by_category}

            if pricelist_product_categ:
                category_ids = [int(cat_id) for cat_id in pricelist_product_categ]
                e_com_categ = request.env["product.public.category"].browse(category_ids)
                e_com_categ_self_child = e_com_categ
                for categ in e_com_categ:
                    e_com_categ_self_child += categ.child_id
                pricelist_products = partner.get_pricelist_rules(
                    pricelist,
                    ecom_category=e_com_categ_self_child.ids,
                    availability_filter=availability_filter,
                    group_by_category=group_by_category,
                )
                values_to_render.update(e_com_categ=e_com_categ)
            else:
                pricelist_products = partner.get_pricelist_rules(
                    pricelist,
                    availability_filter=availability_filter,
                    group_by_category=group_by_category,
                )
            values_to_render.update(pricelist_products=pricelist_products,
                                    currency_id=pricelist.currency_id,
                                    current_date=format_date(request.env, fields.Datetime.now(),
                                                             lang_code=get_lang(request.env).code))
            if pricelist_file_type == "pdf":

                report = request.env['ir.actions.report']._render_qweb_pdf(
                    "pricelist_portal_download_pyb.product_pricelist_action_report", data=values_to_render)[0]
                filename = "Product Pricelist - " + fields.Datetime.now().strftime("%Y/%m/%d") + ".pdf"

                content_type = ('Content-Type', 'application/pdf')
                disposition_content = ('Content-Disposition', content_disposition(filename))
                return request.make_response(report, [content_type, disposition_content])
            elif pricelist_file_type == "excel":
                file_content = self.render_excel_pricelist(values_to_render)

                filename = "Product Pricelist - " + fields.Datetime.now().strftime("%Y-%m-%d") + ".xlsx"

                content_type = (
                    'Content-Type',
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )
                disposition_content = ('Content-Disposition', content_disposition(filename))
                return request.make_response(file_content, [content_type, disposition_content])

        else:
            return request.render('website.page_404')

    def render_excel_pricelist(self, values_to_render):
        target_stream = io.BytesIO()
        workbook = xlsxwriter.Workbook(target_stream)
        worksheet = workbook.add_worksheet("Product Pricelist")
        head_format = workbook.add_format({'valign': 'vcenter', 'align': 'center', 'bold': True, 'bg_color': 'gray'})
        head_format_center = workbook.add_format(
            {'valign': 'vcenter', 'align': 'center', 'bold': True, 'bg_color': 'gray'})
        head_format_left = workbook.add_format({'valign': 'vcenter', 'bold': True, })
        format_right = workbook.add_format({'valign': 'vcenter', 'bold': True, 'align': 'right'})
        money_format = workbook.add_format({'num_format': '#,##0.00', 'valign': 'vcenter', 'align': 'right'})
        format_center = workbook.add_format({'valign': 'vcenter', 'bold': False, 'align': 'center'})
        presentation_format = workbook.add_format({'valign': 'vcenter', 'align': 'center'})
        categ_header_format = workbook.add_format({'valign': 'vcenter', 'bold': True, 'bg_color': '#D3D3D3', 'font_size': 12})
        table_row = 5
        for i in range(8):
            worksheet.set_column(0, i, 20)
        if values_to_render.get("pricelist_products"):
            worksheet.merge_range(0, 0, 1, 7, "Lista de precios", head_format_center)
            worksheet.write(2, 0, "Fecha: " + values_to_render["current_date"], head_format_left)

            if values_to_render.get("e_com_categ"):
                categ_names = ", ".join(values_to_render["e_com_categ"].mapped('name'))
                worksheet.write(3, 0, "Product Category: " + categ_names, head_format_left)
            worksheet.set_column('D:D', 18)
            worksheet.set_column('E:E', 40)
            worksheet.set_column('F:F', 18)
            worksheet.set_column('G:G', 18)
            worksheet.set_column('C:C', 40)

            if values_to_render.get('group_by_category'):
                for group in values_to_render.get("pricelist_products"):
                    categ_name = group.get('category_name', group['category'].name if group['category'] else 'Uncategorized')
                    worksheet.merge_range(table_row, 0, table_row, 7 if group['products'][0]['show_product_stock'] else 6, categ_name, categ_header_format)
                    table_row += 1
                    worksheet.write(table_row, 0, 'Código', head_format)
                    worksheet.write(table_row, 1, 'Código de barras', head_format)
                    worksheet.write(table_row, 2, 'Nombre del producto', head_format)
                    worksheet.write(table_row, 3, 'Presentación', head_format)
                    worksheet.write(table_row, 4, 'IVA', head_format)
                    worksheet.write(table_row, 5, 'Precio', head_format)
                    worksheet.write(table_row, 6, 'Última actualización', head_format)
                    if group['products'][0]['show_product_stock']:
                        worksheet.write(table_row, 7, 'Disponibilidad', head_format)
                    table_row += 1

                    for pricelist_product in group['products']:
                        self._write_product_row(worksheet, table_row, pricelist_product, values_to_render, format_center, presentation_format, format_right, money_format)
                        table_row += 1
                    table_row += 1
            else:
                worksheet.write(table_row, 0, 'Código', head_format)
                worksheet.write(table_row, 1, 'Código de barras', head_format)
                worksheet.write(table_row, 2, 'Nombre del producto', head_format)
                worksheet.write(table_row, 3, 'Presentación', head_format)
                worksheet.write(table_row, 4, 'IVA', head_format)
                worksheet.write(table_row, 5, 'Precio', head_format)
                worksheet.write(table_row, 6, 'Última actualización', head_format)
                if values_to_render.get("pricelist_products") and values_to_render["pricelist_products"][0]['show_product_stock']:
                    worksheet.write(table_row, 7, 'Disponibilidad', head_format)

                table_row += 1
                for pricelist_product in values_to_render.get("pricelist_products"):
                    self._write_product_row(worksheet, table_row, pricelist_product, values_to_render, format_center, presentation_format, format_right, money_format)
                    table_row += 1
        else:
            worksheet.merge_range(0, 0, 1, 5, "You do not have any products in the pricelist!", head_format_left)
        workbook.close()
        target_stream.seek(0)
        return target_stream.getvalue()

    def _format_last_update(self, value):
        if not value:
            return ""
        if isinstance(value, str):
            return value.replace('T', ' ').split('.')[0]
        return value.strftime('%d/%m/%Y %H:%M')

    def _format_tax_names(self, taxes):
        if not taxes:
            return ""
        return ", ".join(tax.name for tax in taxes if getattr(tax, 'name', False))

    def _write_product_row(self, worksheet, row, pricelist_product, values_to_render, format_center, presentation_format, format_right, money_format):
        # Columns: Código, Código de barras, Nombre del producto, Presentación, IVA, Precio, Última actualización, [Disponibilidad]
        product = pricelist_product['product_id']
        worksheet.write(row, 0, product.default_code or "")
        worksheet.write(row, 1, product.barcode or "")
        worksheet.write(row, 2, product.with_context(display_default_code=False).display_name)
        presentation = getattr(product, 'x_studio_presentacion', '')
        worksheet.write(row, 3, presentation or "", presentation_format)
        taxes = getattr(product, 'taxes_id', []) or getattr(getattr(product, 'product_tmpl_id', False), 'taxes_id', [])
        worksheet.write(row, 4, self._format_tax_names(taxes), format_center)
        price_value = pricelist_product.get('price') if pricelist_product.get('price') is not None else 0.0
        try:
            worksheet.write_number(row, 5, float(price_value), money_format)
        except Exception:
            worksheet.write(row, 5, price_value, format_right)
        last_update = getattr(product, 'write_date', False) or getattr(getattr(product, 'product_tmpl_id', False), 'write_date', False)
        worksheet.write(row, 6, self._format_last_update(last_update), format_center)
        if pricelist_product['show_product_stock']:
            if pricelist_product['stock_display_option'] == 'quantity':
                worksheet.write(row, 7, pricelist_product['stock_on_hand'], format_center)
            else:
                worksheet.write(row, 7, "Disponible" if pricelist_product['stock_on_hand'] > 0 else "Sin stock", format_center)

