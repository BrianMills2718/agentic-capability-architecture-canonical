frappe.ui.form.on("Maintenance Request", {
  refresh(frm) {
    if (frm.is_new()) return;

    const call = (method, args = {}) => frappe.call({
      method: `maintenance_requests.api.${method}`,
      args: {name: frm.doc.name, ...args},
      callback: () => frm.reload_doc(),
    });

    if (frm.doc.status === "Assigned") {
      frm.add_custom_button("Start Work", () => call("start_request"));
    }

    if (frm.doc.status === "In Progress") {
      frm.add_custom_button("Complete Work", () => {
        frappe.prompt(
          [{fieldname: "resolution", label: "Resolution", fieldtype: "Small Text", reqd: 1}],
          (values) => call("complete_request", values),
          "Complete Maintenance Request"
        );
      });
    }

    if (frm.doc.status === "Completed") {
      frm.add_custom_button("Close Request", () => call("close_request"));
    }
  }
});
