# Payroll Management System

A complete payroll management system with both CLI and web interfaces.

## Project Structure

```
payroll-system/
├── payroll.sh         # CLI script (original)
├── employees.db       # SQLite database
├── sql/
│   └── schema.sql     # DB schema
├── reports/           # Generated payslip reports
├── app.py             # Flask web application
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── employees.html
│   ├── add_employee.html
│   └── payroll.html
├── requirements.txt   # Python dependencies
└── README.md
```

## Features

- **Employee Management**: Add and view employees
- **Payroll Generation**: Calculate net salary with deductions
- **Payslip Generation**: Generate text reports
- **Dual Interface**: Both CLI and web versions available

## Setup

### Prerequisites
- Python 3.x
- SQLite3
- bash (for CLI version)
- bc calculator (for CLI version)

### Installation

1. **Clone/Download the project**

2. **Initialize the database:**
   ```bash
   sqlite3 employees.db < sql/schema.sql
   ```

3. **For Web Version - Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### CLI Version (Original)

```bash
# Make executable (if needed)
chmod +x payroll.sh

# Run the CLI
./payroll.sh
```

The CLI provides a menu-driven interface:
1. Add Employee
2. View Employees
3. Generate Payroll
4. View Payroll Records
5. Generate Payslip
6. Exit

### Web Version

```bash
# Start the web server
python app.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

#### Web Interface Features:
- **Home Page**: Welcome and navigation
- **Employees**: View all employees
- **Add Employee**: Add new employees via form
- **Payroll**: Generate payroll and view records

## Database Schema

### Employees Table
- `emp_id` (INTEGER, Primary Key, Auto-increment)
- `name` (TEXT, NOT NULL)
- `department` (TEXT)
- `base_salary` (REAL, NOT NULL)

### Payroll Table
- `payroll_id` (INTEGER, Primary Key, Auto-increment)
- `emp_id` (INTEGER, Foreign Key)
- `month` (TEXT)
- `deductions` (REAL)
- `net_salary` (REAL)

## Sample Usage Flow

1. **Add Employees** using either CLI or web interface
2. **Generate Payroll** by specifying employee ID, month, and deductions
3. **View Records** to see all payroll history
4. **Generate Payslips** which are saved as text files in `reports/` folder

## Technical Details

- **Backend**: Flask (Python) for web, bash scripting for CLI
- **Database**: SQLite3
- **Frontend**: HTML templates with Jinja2 templating
- **Reports**: Text files generated in `reports/` directory

Both interfaces use the same SQLite database, so data is shared between CLI and web versions.