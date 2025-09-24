-- Employees table
CREATE TABLE IF NOT EXISTS employees (
    emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT,
    base_salary REAL NOT NULL
);

-- Payroll table
CREATE TABLE IF NOT EXISTS payroll (
    payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id INTEGER,
    month TEXT,
    deductions REAL,
    net_salary REAL,
    FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
);