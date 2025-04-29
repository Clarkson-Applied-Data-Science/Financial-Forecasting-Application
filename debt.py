from baseObject import baseObject
import numpy as np
from datetime import datetime

class debt(baseObject):
    def __init__(self):
        self.setup()

    @staticmethod
    def loan_forecast_data(loan_amount, annual_rate, num_terms, extra_payment=0):
        monthly_rate = annual_rate / 12 / 100

        if monthly_rate == 0:
            base_payment = loan_amount / num_terms
        else:
            base_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_terms) / ((1 + monthly_rate) ** num_terms - 1)

        monthly_payment = base_payment + extra_payment

        balance = loan_amount
        total_interest = 0
        principal_paid = []
        interest_paid = []
        months = 0

        while balance > 0 and months < 1000:
            interest = balance * monthly_rate
            principal = monthly_payment - interest

            if principal > balance:
                principal = balance
                monthly_payment = principal + interest

            balance -= principal
            total_interest += interest
            principal_paid.append(round(principal, 2))
            interest_paid.append(round(interest, 2))
            months += 1

        total_paid = sum(principal_paid) + sum(interest_paid)

        return {
            'base_payment': round(base_payment, 2),
            'monthly_payment': round(base_payment + extra_payment, 2),
            'total_interest': round(total_interest, 2),
            'total_paid': round(total_paid, 2),
            'principal_paid': principal_paid,
            'interest_paid': interest_paid,
            'months_to_payoff': months
        }

    def forecast_from_db(self, debt_id, extra_payment=0):
        self.getById(debt_id)
        if not self.data:
            return {'error': 'Debt not found'}

        debt_record = self.data[0]

        loan_amount = float(debt_record['debt_amount'])
        annual_rate = float(debt_record['debt_rate'])
        total_terms = int(debt_record['debt_terms'])
        start_date = datetime.strptime(str(debt_record['debt_date']), "%Y-%m-%d")

        today = datetime.today()
        months_passed = (today.year - start_date.year) * 12 + today.month - start_date.month
        months_remaining = max(total_terms - months_passed, 0)

        if months_remaining == 0:
            return {
                'message': 'Loan is fully paid or term has ended',
                'monthly_payment': 0,
                'remaining_balance': 0,
                'remaining_interest': 0,
                'remaining_terms': 0
            }

        forecast = self.loan_forecast_data(loan_amount, annual_rate, total_terms)
        paid_principal = sum(forecast['principal_paid'][:months_passed])
        remaining_balance = loan_amount - paid_principal

        adjusted_forecast = self.loan_forecast_data(remaining_balance, annual_rate, months_remaining, extra_payment)
        adjusted_forecast['months_remaining'] = months_remaining
        adjusted_forecast['remaining_balance'] = round(remaining_balance, 2)
        adjusted_forecast['extra_payment'] = extra_payment

        return adjusted_forecast



