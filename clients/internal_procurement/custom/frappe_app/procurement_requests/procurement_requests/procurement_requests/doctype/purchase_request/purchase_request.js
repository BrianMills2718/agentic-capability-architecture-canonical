function procurement_call(frm, method, args = {}) {
  return frappe.call({
    method,
    args: { name: frm.doc.name, ...args },
    freeze: true,
    callback: () => frm.reload_doc(),
  });
}

frappe.ui.form.on("Purchase Request", {
  refresh(frm) {
    if (frm.is_new()) return;

    const roles = new Set(frappe.user_roles || []);

    if (frm.doc.status === "Draft") {
      frm.add_custom_button(__("Submit Request"), () =>
        procurement_call(frm, "procurement_requests.api.submit_purchase_request")
      );
    }

    if (frm.doc.status === "Pending Manager Approval" && roles.has("Procurement Manager")) {
      frm.add_custom_button(__("Approve"), () =>
        procurement_call(frm, "procurement_requests.api.manager_approve")
      );
      frm.add_custom_button(__("Reject"), () => {
        frappe.prompt(
          [{ fieldname: "reason", fieldtype: "Small Text", label: __("Reason"), reqd: 1 }],
          (values) => procurement_call(frm, "procurement_requests.api.manager_reject", values),
          __("Reject Purchase Request")
        );
      });
    }

    if (frm.doc.status === "Pending Finance Approval" && roles.has("Procurement Finance")) {
      frm.add_custom_button(__("Approve"), () =>
        procurement_call(frm, "procurement_requests.api.finance_approve")
      );
      frm.add_custom_button(__("Reject"), () => {
        frappe.prompt(
          [{ fieldname: "reason", fieldtype: "Small Text", label: __("Reason"), reqd: 1 }],
          (values) => procurement_call(frm, "procurement_requests.api.finance_reject", values),
          __("Reject Purchase Request")
        );
      });
    }

    if (roles.has("Procurement Officer")) {
      if (frm.doc.status === "Ready to Purchase") {
        frm.add_custom_button(__("Mark Purchased"), () =>
          procurement_call(frm, "procurement_requests.api.mark_purchased")
        );
      } else if (frm.doc.status === "Purchased") {
        frm.add_custom_button(__("Mark Received"), () =>
          procurement_call(frm, "procurement_requests.api.mark_received")
        );
      } else if (frm.doc.status === "Received") {
        frm.add_custom_button(__("Close Request"), () =>
          procurement_call(frm, "procurement_requests.api.close_purchase_request")
        );
      }
    }
  },
});
