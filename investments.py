from baseObject import baseObject
import yfinance as yf
from datetime import datetime

class investments(baseObject):
    def __init__(self):
        self.setup()


    def is_valid_ticker(self, ticker):
        try:
            t = yf.Ticker(ticker)
            info = t.info
            return info and info.get('regularMarketPrice') is not None
        except Exception:
            return False
        
    def get_status_by_user(self, uid):
        self.getByField("uid", uid)
        enriched_data = []

        for inv in self.data:
            if not inv.get('stock_tic'):
                continue

            try:
                ticker = yf.Ticker(inv['stock_tic'])
                current_price = ticker.info.get('regularMarketPrice', None)

                if current_price is None:
                    raise ValueError("Price not found")

                purchase_price = float(inv['stock_purchase_price'])
                shares = float(inv['stock_shares'])

                total_value = shares * current_price
                purchase_value = shares * purchase_price
                gain_loss = total_value - purchase_value
                roi = ((current_price - purchase_price) / purchase_price) * 100

                # Get start-of-year price
                year_start = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%d')
                ytd_history = ticker.history(start=year_start, end=datetime.now().strftime('%Y-%m-%d'), interval='1d')

                if ytd_history.empty:
                    ytd_roi = 'Error'
                else:
                    start_price = ytd_history.iloc[0]['Close']
                    ytd_roi = ((current_price - start_price) / start_price) * 100

                enriched_data.append({
                    **inv,
                    'current_price': round(current_price, 2),
                    'total_value': round(total_value, 2),
                    'gain_loss': round(gain_loss, 2),
                    'roi': round(roi, 2),
                    'ytd_roi': round(ytd_roi, 2) if ytd_roi != 'Error' else 'Error'
                })

            except Exception as e:
                enriched_data.append({
                    **inv,
                    'current_price': 'Error',
                    'total_value': 'Error',
                    'gain_loss': 'Error',
                    'roi': 'Error',
                    'ytd_roi': 'Error'
                })

        return enriched_data

