/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSaleDefaultPackaging = publicWidget.Widget.extend({
    selector: '.oe_website_sale',

    start() {
        this._super(...arguments);
        this._setDefaultPackaging();
    },

    _setDefaultPackaging() {
        // Detecta los botones/radios del grupo de embalaje en la vista web
        const packagingRadios = this.el.querySelectorAll('input[type="radio"][name*="uom"], input[type="radio"][name*="packaging"]');

        // packagingRadios[0] es la unidad base ('Uni'), packagingRadios[1] es el primer embalaje ('X 12')
        if (packagingRadios.length > 1) {
            const firstPackagingOption = packagingRadios[1];

            if (!firstPackagingOption.checked) {
                // Desmarca la unidad base y activa el embalaje
                packagingRadios.forEach(input => input.closest('label')?.classList.remove('active'));
                firstPackagingOption.checked = true;
                firstPackagingOption.closest('label')?.classList.add('active');

                // Dispara el evento nativo para que Odoo actualice el precio en pantalla
                firstPackagingOption.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
    },
});