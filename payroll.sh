#!/bin/bash
DB="employees.db"
REPORT_DIR="reports"

mkdir -p "$REPORT_DIR"

show_menu() {
  echo "==============================="
  echo " Payroll Management System"
  echo "==============================="
  echo "1. Add Employee"
  echo "2. View Employees"
  echo "3. Generate Payroll"
  echo "4. View Payroll Records"
  echo "5. Generate Payslip"
  echo "6. Exit"
  echo "==============================="
}

add_employee() {
  read -p "Enter Name: " name
  read -p "Enter Department: " dept
  read -p "Enter Base Salary: " salary

  sqlite3 $DB "INSERT INTO employees (name, department, base_salary) VALUES ('$name', '$dept', $salary);"
  echo "✅ Employee added successfully."
}

view_employees() {
  echo "---- Employee List ----"
  sqlite3 -header -column $DB "SELECT * FROM employees;"
}

generate_payroll() {
  read -p "Enter Employee ID: " id
  read -p "Enter Month (e.g. 2025-09): " month
  read -p "Enter Deductions: " ded

  salary=$(sqlite3 $DB "SELECT base_salary FROM employees WHERE emp_id=$id;")
  if [ -z "$salary" ]; then
    echo "❌ Employee not found!"
    return
  fi

  net=$(echo "$salary - $ded" | bc)

  sqlite3 $DB "INSERT INTO payroll (emp_id, month, deductions, net_salary) VALUES ($id, '$month', $ded, $net);"
  echo "✅ Payroll generated for Employee $id (Net Salary: $net)"
}

view_payroll() {
  echo "---- Payroll Records ----"
  sqlite3 -header -column $DB "SELECT * FROM payroll;"
}

generate_payslip() {
  read -p "Enter Employee ID: " id
  read -p "Enter Month (e.g. 2025-09): " month

  slip="$REPORT_DIR/payslip_${id}_${month}.txt"

  sqlite3 -header -column $DB "SELECT e.name, e.department, e.base_salary, p.month, p.deductions, p.net_salary 
                               FROM employees e 
                               JOIN payroll p ON e.emp_id=p.emp_id
                               WHERE e.emp_id=$id AND p.month='$month';" > "$slip"

  echo "✅ Payslip generated: $slip"
}

while true; do
  show_menu
  read -p "Choose option: " choice
  case $choice in
    1) add_employee ;;
    2) view_employees ;;
    3) generate_payroll ;;
    4) view_payroll ;;
    5) generate_payslip ;;
    6) echo "👋 Exiting..."; exit 0 ;;
    *) echo "❌ Invalid option!" ;;
  esac
done