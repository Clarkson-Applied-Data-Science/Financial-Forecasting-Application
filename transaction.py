from baseObject import baseObject

class transaction(baseObject):
    def __init__(self):
        self.setup()
    def getMonthlyTotalsByCategory(self, user_id):
        sql = f"""
            SELECT 
                DATE_FORMAT(trans_date, '%%Y-%%m') AS month,
                trans_category,
                SUM(
                    CASE 
                        WHEN trans_category = 'Income' THEN trans_amount
                        ELSE -trans_amount
                    END
                ) AS net_total
            FROM `{self.tn}`
            WHERE user_id = %s
            GROUP BY month, trans_category
            ORDER BY month ASC, trans_category ASC;
        """

        self.cur.execute(sql, [user_id])
        results = self.cur.fetchall()

        monthly_data = {}

        for row in results:
            month = row['month']
            category = row['trans_category']
            total = float(row['net_total'])

            if month not in monthly_data:
                monthly_data[month] = {
                    'categories': {},
                    'in': 0.0,
                    'out': 0.0,
                    'net': 0.0
                }

            # Store category-wise total
            monthly_data[month]['categories'][category] = total

            # Add to in/out/net
            if category == 'Income':
                monthly_data[month]['in'] += total
            else:
                monthly_data[month]['out'] += abs(total)  # make sure out is positive

            monthly_data[month]['net'] = monthly_data[month]['in'] - monthly_data[month]['out']

        return monthly_data

