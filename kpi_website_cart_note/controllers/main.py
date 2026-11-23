from odoo import http
from odoo.http import request

class WebsiteSalespersonInfo(http.Controller):

    @http.route('/shop/cart/update_ws_info', type='json', auth="public", website=True)
    def update_ws_info(self, field_name, field_value, **kwargs):
        order = request.website.sale_get_order()
        
        # Lista blanca de campos permitidos por seguridad
        allowed_fields = ['ws_client_name', 'ws_commission', 'ws_indications', 'ws_is_new_client']
        
        if order and field_name in allowed_fields:
            # Casteo para el campo booleano
            if field_name == 'ws_is_new_client':
                field_value = bool(field_value)
                
            order.sudo().write({field_name: field_value})
            return {'status': 'success', 'field': field_name}
            
        return {'status': 'error', 'message': 'Invalid field or no active order'}