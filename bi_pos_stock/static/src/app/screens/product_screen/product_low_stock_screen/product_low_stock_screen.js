/** @odoo-module */
import { registry } from "@web/core/registry";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { LowStockLine } from "@bi_pos_stock/app/screens/product_screen/product_low_stock_screen/low_stock_line/low_stock_line";

export class LowStockProducts extends Component {
    static components = { LowStockLine };
    static template = "bi_pos_stock.LowStockProducts";

    setup() {
        super.setup(...arguments);
        this.pos = usePos();
        this.ui = useState(useService("ui"));
    }

    back() {
        this.props.resolve({ confirmed: false, payload: false });
        this.pos.closeTempScreen();
    }
    get low_products(){
        return this.pos.low_stock_products
    }
}

registry.category("pos_screens").add("LowStockProducts", LowStockProducts);
