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

    def getCategoryTotalsAcrossUsers(self):
        sql = """
            SELECT 
                trans_category,
                COUNT(DISTINCT user_id) AS user_count,
                SUM(CASE 
                        WHEN trans_category = 'Income' THEN trans_amount 
                        ELSE -trans_amount 
                    END) AS total_amount,
                AVG(CASE 
                        WHEN trans_category = 'Income' THEN trans_amount 
                        ELSE -trans_amount 
                    END) AS avg_amount
            FROM `{0}`
            GROUP BY trans_category
            ORDER BY FIELD(trans_category, 'Income', 'Food', 'Gas', 'Housing', 'Loan Payment', 'Entertainment');
        """.format(self.tn)

        self.cur.execute(sql)
        results = self.cur.fetchall()

        report = {
            'categories': {},
            'total_in': 0.0,
            'total_out': 0.0,
            'net': 0.0
        }

        for row in results:
            cat = row['trans_category']
            total = float(row['total_amount'])
            avg = float(row['avg_amount'])

            # Store individual category stats
            report['categories'][cat] = {
                'total': total,
                'average': avg,
                'user_count': row['user_count']
            }

            # Aggregate income and spending
            if cat == 'Income':
                report['total_in'] += total
            else:
                report['total_out'] += abs(total)

        report['net'] = report['total_in'] - report['total_out']
        return report


