frappe.ui.form.on("Service Intake", {
  refresh(frm) {
    if (!frm.is_new() && frm.doc.status === "Pending Approval" && frm.doc.appointment) {
      frm.add_custom_button(__("Approve & Book"), () => {
        frappe.call({
          method: "intake_booking.api.approve_intake",
          args: { intake_name: frm.doc.name },
          freeze: true,
          freeze_message: __("Approving consultation..."),
          callback: () => frm.reload_doc(),
        });
      });
    }
  },
});
