function access_call(frm, method, args = {}) {
  return frappe.call({
    method,
    args: { name: frm.doc.name, ...args },
    freeze: true,
    callback: () => frm.reload_doc(),
  });
}

frappe.ui.form.on("Access Request", {
  refresh(frm) {
    if (frm.is_new()) return;

    const roles = new Set(frappe.user_roles || []);

    if (frm.doc.status === "Draft") {
      frm.add_custom_button(__("Submit Request"), () =>
        access_call(frm, "access_requests.api.submit_access_request")
      );
    }

    if (frm.doc.status === "Pending Manager Approval" && roles.has("Access Manager")) {
      frm.add_custom_button(__("Approve"), () =>
        access_call(frm, "access_requests.api.manager_approve")
      );
      frm.add_custom_button(__("Reject"), () => {
        frappe.prompt(
          [{ fieldname: "reason", fieldtype: "Small Text", label: __("Reason"), reqd: 1 }],
          (values) => access_call(frm, "access_requests.api.manager_reject", values),
          __("Reject Access Request")
        );
      });
    }

    if (frm.doc.status === "Pending Security Approval" && roles.has("Security Approver")) {
      frm.add_custom_button(__("Approve"), () =>
        access_call(frm, "access_requests.api.security_approve")
      );
      frm.add_custom_button(__("Reject"), () => {
        frappe.prompt(
          [{ fieldname: "reason", fieldtype: "Small Text", label: __("Reason"), reqd: 1 }],
          (values) => access_call(frm, "access_requests.api.security_reject", values),
          __("Reject Access Request")
        );
      });
    }

    if (roles.has("Access Provisioner")) {
      if (frm.doc.status === "Ready to Provision") {
        frm.add_custom_button(__("Mark Provisioned"), () =>
          access_call(frm, "access_requests.api.mark_provisioned")
        );
      } else if (frm.doc.status === "Provisioned") {
        frm.add_custom_button(__("Revoke Access"), () =>
          access_call(frm, "access_requests.api.revoke_access")
        );
      }
    }
  },
});
