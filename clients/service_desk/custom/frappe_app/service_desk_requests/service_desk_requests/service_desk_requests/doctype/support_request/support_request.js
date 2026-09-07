frappe.ui.form.on("Support Request", {
  refresh(frm) {
    if (frm.is_new()) return;
    const call = (method, args = {}) => frappe.call({method: `service_desk_requests.api.${method}`, args: {name: frm.doc.name, ...args}, callback: () => frm.reload_doc()});
    if (frm.doc.status === "Assigned") frm.add_custom_button("Start Work", () => call("start_request"));
    if (frm.doc.status === "In Progress") frm.add_custom_button("Wait on Requester", () => call("wait_request"));
    if (frm.doc.status === "Waiting on Requester") frm.add_custom_button("Resume Work", () => call("resume_request"));
    if (["In Progress", "Waiting on Requester"].includes(frm.doc.status)) frm.add_custom_button("Resolve", () => frappe.prompt([{fieldname:"resolution", label:"Resolution", fieldtype:"Small Text", reqd:1}], values => call("resolve_request", values), "Resolve Support Request"));
    if (frm.doc.status === "Resolved") frm.add_custom_button("Close", () => call("close_request"));
  }
});
