from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB = "employees.db"
REPORT_DIR = "reports"

os.makedirs(REPORT_DIR, exist_ok=True)

def get_db():
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
        with open(slip_path, "w") as f:
            f.write(f"Employee ID: {emp_id}\nMonth: {month}\nNet Salary: {net}\n")

        conn.close()
        return redirect("/payroll")

    rows = conn.execute("""
        SELECT p.payroll_id, e.name, e.department, p.month, p.deductions, p.net_salary
        FROM payroll p
        JOIN employees e ON e.emp_id = p.emp_id
    """).fetchall()
    conn.close()
    return render_template("payroll.html", payroll=rows)

if __name__ == "__main__":
    app.run(debug=True)