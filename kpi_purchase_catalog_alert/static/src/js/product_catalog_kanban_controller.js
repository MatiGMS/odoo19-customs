/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductCatalogKanbanController } from "@product/product_catalog/kanban_controller";

// Variable de debounce/flag local para evitar repetir la alerta en ráfagas de clicks rápidos
let isNotificationShown = false;

patch(ProductCatalogKanbanController.prototype, {
    async _updateOrderLineInfo(product_id, quantity) {
        const res = await super._updateOrderLineInfo(...arguments);

        // Si el backend reporta alerta de stock
        if (res && res.stock_warning && res.stock_warning.has_warning) {
            if (!isNotificationShown) {
                isNotificationShown = true;
                
                this.env.services.notification.add(res.stock_warning.message, {
                    title: res.stock_warning.title,
                    type: "warning",
                    sticky: false,
                });

                // Resetear tras 4 segundos para volver a alertar si sigue interactuando
                setTimeout(() => {
                    isNotificationShown = false;
                }, 4000);
            }
        }
        return res;
    },
});