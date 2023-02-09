// Copyright (c) 2022, zizo and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employees Salary Components Report"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": "100px"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"width": "100px"
		},
		{
			"fieldname":"branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
			"width": "100px"
		},
		{
			"fieldname":"employment_type",
			"label": __("Employment Type"),
			"fieldtype": "Link",
			"options": "Employment Type",
			"width": "100px"
		},
		{
			"fieldname":"title",
			"label":__("Document Title"),
			"fieldtype":"Data",
			on_change: function() {
				
			}
		}
		
	]
};
