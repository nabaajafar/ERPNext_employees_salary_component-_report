# Copyright (c) 2022, zizo and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import flt

import erpnext


def execute(filters=None):
	if not filters: filters = {}
	salary_structure_assignments = get_salary_structure_assignment(filters)
	if not salary_structure_assignments: return [], []

	columns, earning_types, ded_types = get_columns(salary_structure_assignments)
	ssa_earning_map = get_ssa_earning_map(salary_structure_assignments)
	ssa_ded_map = get_ssa_earning_map(salary_structure_assignments)
	# doj_map = get_employee_doj_map()

	data = []
	for ssa in salary_structure_assignments:
		row = [ssa.name,ssa.salary_structure, ssa.employee, ssa.employee_name, ssa.branch, ssa.department, ssa.designation,
			ssa.company]

		if ssa.branch is not None: columns[3] = columns[3].replace('-1','120')
		if ssa.department is not None: columns[4] = columns[4].replace('-1','120')
		if ssa.designation is not None: columns[5] = columns[5].replace('-1','120')


		for e in earning_types:
			row.append(ssa_earning_map.get(ssa.salary_structure, {}).get(e))
			
		row += ["------"]

		for d in ded_types:
			row.append(ssa_ded_map.get(ssa.salary_structure, {}).get(d))
		
		data.append(row)

	for c in columns:
		if c.split(":")[0] in earning_types:
			s = c.split(":")[0]
			c = c.replace(s,' ')
			# frappe.msgprint(c)
	return columns, data


def get_columns(salary_structure_assignments):

	columns = [
		_("Salary Structure Assignment") + ":Link/Salary Structure Assignment:150",
		_("Salary Structure") + ":Link/Salary Structure:150",
		_("Employee") + ":Link/Employee:120",
		_("Employee Name") + "::160",
		_("Branch") + ":Link/Branch:-1",
		_("Department") + ":Link/Department:-1",
		_("Designation") + ":Link/Designation:120",
		_("Company") + ":Link/Company:120"
	]

	salary_structure_components = {_("Earning"): [], _("Deduction"): []}
	# salary_components = {_("Earning"): [], _("Deduction"): []}

	for component in frappe.db.sql("""select sd.salary_component, sc.type
		from `tabSalary Detail` sd, `tabSalary Component` sc
		where sc.name=sd.salary_component and sd.parent in (%s)""" %
		(', '.join(['%s']*len(salary_structure_assignments))),tuple([d.salary_structure for d in salary_structure_assignments]), as_dict=1):
		salary_structure_components[_(component.type)].append(component.salary_component)

	columns = columns + [(e + "::80") for e in salary_structure_components[_("Earning")]] + \
		[_("----") + "::80"] + \
		[(d + "::80") for d in salary_structure_components[_("Deduction")]] 

	return columns, salary_structure_components[_("Earning")], salary_structure_components[_("Deduction")]



def get_salary_structure_assignment(filters):
	conditions, filters = get_conditions(filters)
	salary_structure_assignment = frappe.db.sql(
	"""select ssa.name, ssa.salary_structure , ssa.employee , ssa.employee_name, emp.branch, emp.department, emp.designation, ssa.company
		from `tabSalary Structure Assignment` ssa, `tabEmployee` emp 
		where ssa.employee = emp.name  and ssa.docstatus = 1
		 %s
		""" % conditions, filters, as_dict=1)

	return salary_structure_assignment or []

def get_conditions(filters):
	conditions = ""
	if filters.get("company"): conditions += " and emp.company = %(company)s"
	if filters.get("branch"): conditions += " and emp.branch = %(branch)s"
	if filters.get("employment_type"): conditions += " and emp.employment_type = %(employment_type)s"
	if filters.get("employee"): conditions += " and ssa.employee = %(employee)s"

	return conditions, filters

def get_ssa_earning_map(salary_structure_assignments):
	ssa_earnings = frappe.db.sql("""select sd.parent, sd.salary_component, ss.name
		from `tabSalary Detail` sd, `tabSalary Structure` ss
		where sd.parent=ss.name and sd.parent in (%s)""" %
		(', '.join(['%s']*len(salary_structure_assignments))), tuple([d.salary_structure for d in salary_structure_assignments]), as_dict=1)

	ssa_earning_map = {}
	for d in ssa_earnings:
		ssa_earning_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, "")
		ssa_earning_map[d.parent][d.salary_component] += d.salary_component

	return ssa_earning_map



