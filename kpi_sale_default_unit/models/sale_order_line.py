from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_set_default_packaging_unit(self):
        """
        Al seleccionar el producto, si tiene un embalaje configurado para ventas,
        se fuerza dicho embalaje en la línea y se actualizan las cantidades.
        """
        for line in self:
            if not line.product_id:
                continue

            # Obtención segura de empaques desde product.template o product.product
            packagings = line.product_id.packaging_ids.filtered(lambda p: getattr(p, 'sales', True))
            if not packagings:
                continue

            default_pack = packagings[0]

            # 1. Si la línea usa el campo nativo de empaque:
            if hasattr(line, 'product_packaging_id'):
                line.product_packaging_id = default_pack.id
            if hasattr(line, 'product_packaging_qty'):
                line.product_packaging_qty = 1.0

            # 2. Sincronizar la cantidad base de la unidad
            line.product_uom_qty = default_pack.qty

            # 3. Si el dropdown "Unidad" está enlazado a una UdM secundaria o campo específico:
            # En caso de que el selector sea product_uom / product_uom_id y el empaque
            # defina una unidad asociada:
            if hasattr(default_pack, 'product_uom_id') and default_pack.product_uom_id:
                line.product_uom_id = default_pack.product_uom_id.id
            elif hasattr(line, 'product_uom') and hasattr(default_pack, 'package_type_id'):
                # Si el widget agrupa paquetes bajo el selector de UoM
                pass