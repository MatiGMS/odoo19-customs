# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sales_count_stored = fields.Float(
        string="Total Unidades Vendidas",
        default=0.0,
        index=True,
        copy=False,
        help="Suma histórica de ventas calculada periódicamente para ordenamiento en eCommerce."
    )

    @api.model
    def _cron_update_sales_count_stored(self):
        """
        Recálculo masivo mediante query crudo en PostgreSQL.
        Agrega ventas confirmadas ('sale', 'done') por producto template.
        """
        query = """
            WITH sales_aggregated AS (
                SELECT 
                    pp.product_tmpl_id,
                    COALESCE(SUM(sol.product_uom_qty), 0.0) AS total_sold
                FROM sale_order_line sol
                INNER JOIN sale_order so ON so.id = sol.order_id
                INNER JOIN product_product pp ON pp.id = sol.product_id
                WHERE so.state IN ('sale', 'done')
                GROUP BY pp.product_tmpl_id
            )
            UPDATE product_template pt
            SET sales_count_stored = sa.total_sold
            FROM sales_aggregated sa
            WHERE pt.id = sa.product_tmpl_id;
        """
        self.env.cr.execute(query)