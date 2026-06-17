from odoo import models

import base64
from io import BytesIO
from PyPDF2 import PdfMerger


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_print_all_documents(self):
        self.ensure_one()
        reports = []

        sale_report = self.env.ref('sale.report_saleorder')
        pdf_sale, _ = sale_report._render_qweb_pdf(self.id)
        reports.append(pdf_sale)

        pickings = self.picking_ids.filtered(lambda p: p.state in ['assigned', 'done'])
        if pickings:
            delivery_report = self.env.ref('stock.action_report_delivery')
            pdf_picking, _ = delivery_report._render_qweb_pdf(pickings.ids)
            reports.append(pdf_picking)

        invoices = self.invoice_ids.filtered(lambda inv: inv.state == 'posted')
        if invoices:
            invoice_report = self.env.ref('account.report_invoice')
            pdf_invoice, _ = invoice_report._render_qweb_pdf(invoices.ids)
            reports.append(pdf_invoice)

        if not reports:
            return {'type': 'ir.actions.act_window_close'}

        merger = PdfMerger()
        for pdf_bytes in reports:
            merger.append(BytesIO(pdf_bytes))
        buffer_out = BytesIO()
        merger.write(buffer_out)
        merger.close()
        merged_pdf = buffer_out.getvalue()

        attachment = self.env['ir.attachment'].create({
            'name': '%s_documentos.pdf' % self.name,
            'type': 'binary',
            'datas': base64.b64encode(merged_pdf),
            'res_model': 'sale.order',
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })

        url = '/web/content/%s?download=true' % attachment.id
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }