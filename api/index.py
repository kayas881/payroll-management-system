from flask import Flask, render_template, request, redirect
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DB = os.path.join(PROJECT_ROOT, "employees.db")
REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")

# Ensure reports directory exists
os.makedirs(REPORT_DIR, exist_ok=True)

def init_db():
    """Initialize the database if it doesn't exist"""
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        # Create tables
        conn.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT,
                base_salary REAL NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS payroll (
                payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id INTEGER,
                month TEXT,
                deductions REAL,
                net_salary REAL,
                FOREIGN KEY(emp_id) REFERENCES employees(emp_id)
            )
        ''')
        conn.commit()
        conn.close()

def get_db():
    init_db()  # Ensure DB exists
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/employees")
def employees():
    conn = get_db()
    rows = conn.execute("SELECT * FROM employees").fetchall()
    conn.close()
    return render_template("employees.html", employees=rows)

@app.route("/add", methods=["GET","POST"])
def add_employee():
    if request.method == "POST":
        name = request.form["name"]
        dept = request.form["department"]
        salary = request.form["salary"]

        conn = get_db()
        conn.execute("INSERT INTO employees (name, department, base_salary) VALUES (?, ?, ?)",
                     (name, dept, salary))
        conn.commit()
        conn.close()
        return redirect("/employees")

    return render_template("add_employee.html")

@app.route("/payroll", methods=["GET","POST"])
def payroll():
    conn = get_db()
    if request.method == "POST":
        emp_id = request.form["emp_id"]
        month = request.form["month"]
        deductions = float(request.form["deductions"])

        salary = conn.execute("SELECT base_salary FROM employees WHERE emp_id=?",(emp_id,)).fetchone()
        if not salary:
            conn.close()
            return "❌ Employee not found!"

        net = salary["base_salary"] - deductions
        conn.execute("INSERT INTO payroll (emp_id, month, deductions, net_salary) VALUES (?,?,?,?)",
                     (emp_id, month, deductions, net))
        conn.commit()

        # save payslip file (just like CLI)
        slip_path = os.path.join(REPORT_DIR, f"payslip_{emp_id}_{month}.txt")
        try:
            with open(slip_path, "w") as f:
                f.write(f"Employee ID: {emp_id}\nMonth: {month}\nNet Salary: {net}\n")
        except:
            pass  # Handle file write issues in serverless environment

        conn.close()
        return redirect("/payroll")

    rows = conn.execute("""
        SELECT p.payroll_id, e.name, e.department, p.month, p.deductions, p.net_salary
        FROM payroll p
        JOIN employees e ON e.emp_id = p.emp_id
    """).fetchall()
    conn.close()
    return render_template("payroll.html", payroll=rows)

# For Vercel serverless function
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == "__main__":
    app.run(debug=True)