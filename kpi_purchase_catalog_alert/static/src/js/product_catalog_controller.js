import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

// En lugar de llamar a un ir.actions.act_window:
if (action && action.message) {
    this.env.services.dialog.add(ConfirmationDialog, {
        title: action.title,
        body: action.message,
        confirmLabel: "Entendido y Continuar",
        cancel: () => {},
        confirm: () => {},
    });
}