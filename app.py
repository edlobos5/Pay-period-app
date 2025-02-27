from flask import Flask, request, render_template_string
import datetime
from collections import defaultdict

app = Flask(__name__)
transactions = []

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        type_ = request.form.get('type')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        date = request.form.get('date') or str(datetime.date.today())
        pay_period = request.form.get('pay_period')
        transactions.append({'type': type_, 'amount': amount, 'category': category, 'date': date, 'pay_period': pay_period})

    pay_periods = defaultdict(lambda: {'income': 0, 'expenses': 0})
    for t in transactions:
        period = t['pay_period']
        if t['type'] == 'Income':
            pay_periods[period]['income'] += t['amount']
        else:
            pay_periods[period]['expenses'] += t['amount']
    dashboard_data = {period: {'income': data['income'], 'expenses': data['expenses'], 'balance': data['income'] - data['expenses']} for period, data in pay_periods.items()}

    html = '''
        <style>
            body { font-family: Arial, sans-serif; padding: 10px; max-width: 100%; overflow-x: hidden; }
            table { width: 100%; border-collapse: collapse; margin: 10px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            form { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
            input, select, button { padding: 5px; }
            button { background-color: #4CAF50; color: white; border: none; }
            @media (max-width: 600px) { form { flex-direction: column; } input, select, button { width: 100%; } }
        </style>
        <h1>Budget Dashboard</h1>
        <h2>Add Transaction</h2>
        <form method="post">
            <select name="type"><option value="Income">Income</option><option value="Expense">Expense</option></select>
            <input type="number" name="amount" placeholder="Amount" step="0.01" required>
            <input type="text" name="category" placeholder="Category" required>
            <input type="date" name="date">
            <input type="text" name="pay_period" placeholder="Pay Period (e.g., Feb 1-15)" required>
            <button type="submit">Add</button>
        </form>
        <h2>Pay Period Breakdown</h2>
        <table><tr><th>Pay Period</th><th>Income</th><th>Expenses</th><th>Balance</th></tr>
            {% for period, data in dashboard_data.items() %}
                <tr><td>{{ period }}</td><td>{{ data.income }}</td><td>{{ data.expenses }}</td><td>{{ data.balance }}</td></tr>
            {% endfor %}
        </table>
        <h2>All Transactions</h2>
        <table><tr><th>Type</th><th>Amount</th><th>Category</th><th>Date</th><th>Pay Period</th></tr>
            {% for t in transactions %}
                <tr><td>{{ t.type }}</td><td>{{ t.amount }}</td><td>{{ t.category }}</td><td>{{ t.date }}</td><td>{{ t.pay_period }}</td></tr>
            {% endfor %}
        </table>
    '''
    return render_template_string(html, dashboard_data=dashboard_data, transactions=transactions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)