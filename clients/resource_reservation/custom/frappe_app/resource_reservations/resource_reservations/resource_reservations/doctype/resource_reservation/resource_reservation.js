frappe.ui.form.on("Resource Reservation", {
  refresh(frm) {
    if (frm.is_new()) return;

    const call = (method, args = {}) => frappe.call({
      method: `resource_reservations.api.${method}`,
      args: {name: frm.doc.name, ...args},
      callback: () => frm.reload_doc(),
    });

    if (frm.doc.status === "Draft") {
      frm.add_custom_button("Reserve", () => call("reserve_request"));
    }

    if (frm.doc.status === "Reserved") {
      frm.add_custom_button("Reschedule", () => {
        frappe.prompt(
          [
            {fieldname: "start_time", label: "Start Time", fieldtype: "Datetime", reqd: 1, default: frm.doc.start_time},
            {fieldname: "duration_minutes", label: "Duration Minutes", fieldtype: "Int", reqd: 1, default: frm.doc.duration_minutes},
          ],
          values => call("reschedule_request", values),
          "Reschedule Reservation"
        );
      });
      frm.add_custom_button("Cancel", () => call("cancel_request"));
    }
  }
});
