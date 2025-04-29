"""from flask import Flask, request, render_template_string
import yfinance as yf
from datetime import datetime

app = Flask(__name__)

html =
<!doctype html>
<title>Stock Info Lookup</title>
<h2>Enter a Stock Ticker</h2>
<form method="get">
  <input name="ticker" placeholder="e.g., AAPL" required>
  <input type="submit" value="Get Info">
</form>

{% if price %}
  <h3>{{ ticker.upper() }}'s latest closing price: ${{ price }}</h3>
  <h3>Dividend Rate: {{ dividend_rate if dividend_rate is not none else 'N/A' }}</h3>
  <h3>Dividend Frequency: {{ dividend_frequency if dividend_frequency else 'N/A' }}</h3>
{% elif error %}
  <h3 style="color:red;">{{ error }}</h3>
{% endif %}


@app.route('/', methods=['GET'])
def index():
    ticker = request.args.get('ticker')
    price = None
    dividend_rate = None
    dividend_frequency = None
    error = None

    if ticker:
        try:
            stock = yf.Ticker(ticker.upper())

            # Get latest closing price
            data = stock.history(period="1d")
            price = round(data["Close"].iloc[-1], 2)

            # Get dividend rate
            info = stock.info
            dividend_rate = info.get('dividendRate', None)

            # Try to determine dividend frequency from history
            divs = stock.dividends
            if len(divs) >= 2:
                # Get last 2 dividend dates
                last_dates = divs.index[-2:]
                delta = (last_dates[-1] - last_dates[-2]).days
                if 80 < delta < 100:
                    dividend_frequency = "Quarterly"
                elif 170 < delta < 200:
                    dividend_frequency = "Semi-Annually"
                elif 350 < delta < 380:
                    dividend_frequency = "Annually"
                else:
                    dividend_frequency = f"Every {delta} days"
            elif len(divs) == 1:
                dividend_frequency = "Only one dividend recorded"
            else:
                dividend_frequency = "No dividend history available"

        except Exception as e:
            error = f"Error fetching data for '{ticker.upper()}'."

    return render_template_string(html, ticker=ticker, price=price,
                                  dividend_rate=dividend_rate,
                                  dividend_frequency=dividend_frequency,
                                  error=error)

if __name__ == '__main__':
    app.run(debug=True)
"""

def loan_forecast_data(loan_amount, annual_rate, num_terms):
    monthly_rate = annual_rate / 12 / 100
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_terms) / ((1 + monthly_rate) ** num_terms - 1)
    
    balance = loan_amount
    total_interest = 0
    principal_paid = []
    interest_paid = []

    for _ in range(num_terms):
        interest = balance * monthly_rate
        principal = monthly_payment - interest
        balance -= principal
        total_interest += interest
        principal_paid.append(round(principal, 2))
        interest_paid.append(round(interest, 2))

    return {
        'monthly_payment': round(monthly_payment, 2),
        'total_interest': round(total_interest, 2),
        'total_paid': round(monthly_payment * num_terms, 2),
        'principal_paid': principal_paid,
        'interest_paid': interest_paid
    }

print(loan_forecast_data(10000, 5.3, 60))