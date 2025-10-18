from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# لیست موقت مشتریان در حافظه
customers = []
next_id = 1

# صفحه ورود
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == '1234':
            return redirect(url_for('dashboard'))
        else:
            return "نام کاربری یا رمز عبور اشتباه است"
    return render_template('login.html')

# صفحه داشبورد
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# صفحه لیست مشتریان
@app.route('/customers')
def customers_page():
    return render_template('customers.html', customers=customers)

# افزودن مشتری جدید
@app.route('/customers/new', methods=['GET', 'POST'])
def new_customer():
    global next_id
    if request.method == 'POST':
        customer = {
            'id': next_id,
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'phone': request.form['phone'],
            'address': request.form['address']
        }
        customers.append(customer)
        next_id += 1
        return redirect(url_for('customers_page'))
    return render_template('customer_form.html', customer=None)

# ویرایش مشتری
@app.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = next((c for c in customers if c['id'] == customer_id), None)
    if not customer:
        return "مشتری یافت نشد"
    if request.method == 'POST':
        customer['first_name'] = request.form['first_name']
        customer['last_name'] = request.form['last_name']
        customer['phone'] = request.form['phone']
        customer['address'] = request.form['address']
        return redirect(url_for('customers_page'))
    return render_template('customer_form.html', customer=customer)

# حذف مشتری
@app.route('/customers/delete/<int:customer_id>')
def delete_customer(customer_id):
    global customers
    customers = [c for c in customers if c['id'] != customer_id]
    return redirect(url_for('customers_page'))


if __name__ == '__main__':
    app.run(debug=True)
