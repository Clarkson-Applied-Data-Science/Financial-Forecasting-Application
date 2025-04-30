from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta
from user import user
from investments import investments
from transaction import transaction
from debt import debt
import time

app = Flask(__name__,static_url_path='')

app.config['SECRET_KEY'] = '5sdghsgRTg'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

@app.route('/')
def home():
    return redirect('/login')

@app.context_processor
def inject_user():
    return dict(me=session.get('user'))

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.form.get('name') is not None and request.form.get('password') is not None:
        u = user()
        if u.tryLogin(request.form.get('name'),request.form.get('password')):
            print("Login ok")
            session['user'] = u.data[0]
            session['active'] = time.time()
            return redirect('main')
        else:
            print("Login Failed")
            return render_template('login.html', title='Login', msg='Incorrect username or password.')
    else:   
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)    
    
@app.route('/logout',methods = ['GET','POST'])
def logout():
    if session.get('user') is not None:
        del session['user']
        del session['active']
    return render_template('login.html', title='Login', msg='You have logged out.')
@app.route('/main')
def main():
    if checkSession() == False: 
        return redirect('/login')
    
    if session['user']['role'] == 'admin':
        return render_template('main.html', title='Main menu') 
    else:
        return render_template('customer_main.html', title='Main menu') 

@app.route('/users/manage',methods=['GET','POST'])
def manage_user():
    if checkSession() == False or session['user']['role'] != 'admin': 
        return redirect('/login')
    o = user()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['fname'] = request.form.get('fname')
        d['email'] = request.form.get('email')
        d['role'] = request.form.get('role')
        d['password'] = request.form.get('password')
        d['password2'] = request.form.get('password2')
        o.set(d)
        if o.verify_new():
            #print(o.data)
            o.insert()
            return render_template('ok_dialog.html',msg= "User added.")
        else:
            return render_template('users/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['fname'] = request.form.get('fname')
        o.data[0]['email'] = request.form.get('email')
        o.data[0]['role'] = request.form.get('role')
        o.data[0]['password'] = request.form.get('password')
        o.data[0]['password2'] = request.form.get('password2')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "User updated. ")
        else:
            return render_template('users/manage.html',obj = o)
    if pkval is None:
        o.getAll()
        return render_template('users/list.html',obj = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('users/add.html',obj = o)
    else:
        print(pkval)
        o.getById(pkval)
        return render_template('users/manage.html',obj = o)

@app.route("/profile")
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))  # Still check if logged in

    uid = session['user']['uid']
    u = user()
    u.getById(uid)

    if not u.data:
        return "User not found", 404

    return render_template("profile.html", user=u.data[0])

@app.route('/debts/manage', methods=['GET', 'POST'])
def manage_debts():
    if checkSession() == False or session['user']['role'] != 'customer':
        return redirect('/login')

    d = debt()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            new_debt = {
                'debt_amount': request.form['debt_amount'],
                'debt_rate': request.form['debt_rate'],
                'debt_date': request.form['debt_date'],
                'debt_terms': request.form['debt_terms'],
                'user_id': session['user']['uid']
            }
            d.set(new_debt)
            d.insert()

        elif action == 'delete':
            d.deleteById(request.form['debt_id'])
        
        elif action == 'update':
            updated_debt = {
                'debt_id': request.form['debt_id'],
                'debt_amount': request.form['debt_amount'],
                'debt_rate': request.form['debt_rate'],
                'debt_date': request.form['debt_date'],
                'debt_terms': request.form['debt_terms'],
                'user_id': session['user']['uid']
            }
            d.set(updated_debt)
            d.update()

    d.getByField("user_id", session['user']['uid'])
    return render_template('customer_debts.html', debts=d.data)

@app.route('/investments/manage', methods=['GET', 'POST'])
def manage_investments():
    if checkSession() == False or session['user']['role'] != 'customer':
        return redirect('/login')

    inv = investments()
    error = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            stock_tic = request.form.get('stock_tic').upper()
            if not inv.is_valid_ticker(stock_tic):
                error = f"Ticker '{stock_tic}' is invalid. Please enter a valid stock ticker."
            else:
                new_inv = {
                    'inv_date': request.form['inv_date'],
                    'uid': session['user']['uid'],
                    'stock_tic': stock_tic,
                    'stock_shares': request.form.get('stock_shares'),
                    'stock_purchase_price': request.form.get('stock_purchase_price')
                }
                inv.set(new_inv)
                inv.insert()

        elif action == 'delete':
            inv.deleteById(request.form['inv_id'])

        elif action == 'update':
            updated_inv = {
                'inv_id': request.form['inv_id'],
                'inv_date': request.form['inv_date'],
                'uid': session['user']['uid'],
                'stock_tic': request.form.get('stock_tic'),
                'stock_shares': request.form.get('stock_shares'),
                'stock_purchase_price': request.form.get('stock_purchase_price')
            }
            inv.set(updated_inv)
            inv.update()

    inv.getByField("uid", session['user']['uid'])
    return render_template('customer_investments.html', investments=inv.data, error=error)


@app.route('/transactions/manage', methods=['GET', 'POST'])
def manage_transactions():
    if not checkSession() or session['user']['role'] != 'customer':
        return redirect('/login')

    t = transaction()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            new_txn = {
                'trans_category': request.form.get('trans_category'),
                'trans_amount': request.form.get('trans_amount'),
                'trans_date': request.form.get('trans_date'),
                'user_id': session['user']['uid']
            }
            t.set(new_txn)
            t.insert()

        elif action == 'delete':
            t.deleteById(request.form.get('tid'))

        elif action == 'update':
            updated_txn = {
                'tid': request.form.get('tid'),
                'trans_category': request.form.get('trans_category'),
                'trans_amount': request.form.get('trans_amount'),
                'trans_date': request.form.get('trans_date'),
                'user_id': session['user']['uid']
            }
            t.set(updated_txn)
            t.update()

    t.getByField("user_id", session['user']['uid'])
    return render_template('customer_transactions.html', transactions=t.data)



# endpoint route for static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

#standalone function to be called when we need to check if a user is logged in.
def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        #print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False   

@app.route('/debt/forecast', methods=['GET', 'POST'])
def debt_forecast():
    if checkSession() == False or session['user']['role'] != 'customer':
        return redirect('/login')

    forecast_result = None
    from debt import debt
    debt_obj = debt()
    debt_obj.getAll()
    debts = debt_obj.data

    if request.method == 'POST':
        action = request.form['action']
        extra_payment = float(request.form.get('extra_payment', 0) or 0)

        if action == 'forecast_existing':
            selected_id = request.form['debt_id']
            forecast_result = debt_obj.forecast_from_db(selected_id, extra_payment=extra_payment)

        elif action == 'forecast_future':
            amount = float(request.form['amount'])
            rate = float(request.form['rate'])
            terms = int(request.form['terms'])
            forecast_result = debt.loan_forecast_data(amount, rate, terms, extra_payment=extra_payment)
            forecast_result['extra_payment'] = extra_payment  # To display it in the template

    return render_template('loan_forecast_combined.html', result=forecast_result, debts=debts)

@app.route('/investments/status')
def investment_status():
    if checkSession() == False or session['user']['role'] != 'customer':
        return redirect('/login')

    user_id = session['user']['uid']
    inv = investments()
    enriched_investments = inv.get_status_by_user(user_id)

    # Calculate portfolio-level ROI averages
    roi_values = [i['roi'] for i in enriched_investments if isinstance(i['roi'], (int, float))]
    ytd_values = [i['ytd_roi'] for i in enriched_investments if isinstance(i['ytd_roi'], (int, float))]

    avg_roi = round(sum(roi_values) / len(roi_values), 2) if roi_values else 'N/A'
    avg_ytd = round(sum(ytd_values) / len(ytd_values), 2) if ytd_values else 'N/A'

    return render_template(
        'investment_status.html',
        investments=enriched_investments,
        all_time_roi=avg_roi,
        ytd_roi=avg_ytd
    )

@app.route('/budgeting')
def budgeting():
    if checkSession() == False or session['user']['role'] != 'customer':
        return redirect('/login')

    t = transaction()
    budget_data = t.getMonthlyTotalsByCategory(session['user']['uid'])

    # Sort the dictionary keys (month strings) in descending order
    sorted_data = dict(sorted(budget_data.items(), reverse=True))

    return render_template('budgeting.html', budget_data=sorted_data)

@app.route('/reports/user_spending')
def user_spending_report():
    if checkSession() == False or session['user']['role'] != 'admin':
        return redirect('/login')

    trans = transaction()
    report = trans.getCategoryTotalsAcrossUsers()

    return render_template('user_spending_report.html', report=report)

if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)   

