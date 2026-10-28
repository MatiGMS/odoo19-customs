/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
// En mrp_workorder el componente base suele ser Workorder o Shopfloor
import { Workorder } from "@mrp_workorder/mrp_display/workorder";

patch(Workorder.prototype, {
    setup() {
        super.setup(...arguments);
    },

    get productionTags() {
        // Accede a las etiquetas serializadas desde Python
        const tags = this.props.record.data?.production_tags || this.props.record.production_tags || [];
        return tags;
    },

    get cardAccentClass() {
        const tags = this.productionTags;
        if (tags && tags.length > 0) {
            return `o_has_tag_accent o_tag_color_${tags[0].color || 0}`;
        }
        return "";
    }
});