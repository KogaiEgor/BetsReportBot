import xlsxwriter
from db import queries


async def create_excel(stat: list, balance: list):
    workbook = xlsxwriter.Workbook('Report.xlsx')
    worksheet = workbook.add_worksheet("Sheet")
    accs = await queries.get_spain_accs()

    col = 0
    for i in accs:
        temp_stat = [d for d in stat if d[-1] == i[0]]
        temp_balance = [d for d in balance if d[-1] == i[0]]

        row = 0

        report = [
            ["Отчет по аккаунту", f"{i[1]}:"]
        ]
        for j in range(len(temp_stat)):
            start_balance, end_balance = temp_balance[j][1], temp_balance[j][2]
            count, rev = temp_stat[j][1], temp_stat[j][2]
            profit = end_balance - start_balance

            day = [f"{j + 1}-й день:", ""]
            start_balance_list = ["НАЧАЛЬНЫЙ БАЛАНС:", start_balance]
            bets_count_list = ["Кол-во ставок:", count]
            revenue_list = ["Сумма оборота:", rev]
            profit_list = ["Профит:", round(profit, 3)]
            roi_list = ["ROI:", round((profit / rev) * 100, 3)]
            end_balance_list = ["КОНЕЧНЫЙ БАЛАНС:", end_balance]
            report.extend([day, start_balance_list, bets_count_list, revenue_list, profit_list, roi_list, end_balance_list])

        for name, data in report:
            if "-й день:" in name:
                row += 1
            worksheet.write(row, col, name)
            worksheet.write(row, col+1, data)
            row += 1
            worksheet.set_column(col, col, 20)
            worksheet.set_column(col+1, col+1, 15)

        col += 3
    workbook.close()


# async def main():
#     stat = await queries.get_daily_stat_for_all()
#     balance = await queries.get_daily_balance_for_all()
#     await create_excel(stat, balance)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())