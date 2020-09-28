from prettytable import PrettyTable
import traceback
from question3.Question3_HSBC import e_count, ep_count
from question2.Question2_HSBC import t_count, f_count, count, p_count
from question2.Question2_SPY import t_count_s, f_count_s, count_s, p_count_s
from question3.Question3_SPY import e_count_s, ep_count_s
# all correct label use ensemble learning
e_total = e_count[0] + e_count[1]
# total label numbers
total = t_count + f_count
# correct numbers of each W
w_total = [(count[0][0] + count[0][1]), (count[1][0] + count[1][1]), (count[2][0] + count[2][1])]
# _s means the data is from S&P-500
e_total_s = e_count_s[0] + e_count_s[1]
total_s = t_count_s + f_count_s
w_total_s = [(count_s[0][0] + count_s[0][1]), (count_s[1][0] + count_s[1][1]), (count_s[2][0] + count_s[2][1])]


def main():
    try:
        temp = ['W', 'ticker', 'TP', 'FP', 'TN', 'FN', 'accuracy', 'TPR', 'TNR']
        table = PrettyTable(temp)
        for i in range(0, 3):
            table.add_row([i + 2, 'S&P-500', count_s[i][0], p_count_s[i][0] - count_s[i][0], count_s[i][1],
                           p_count_s[i][1] - count_s[i][1], round(w_total_s[i] / total_s, 4),
                           round(count_s[i][0] / (count_s[i][0] + p_count_s[i][1] - count_s[i][1]), 4),
                           round(count_s[i][1] / (count_s[i][1] + p_count_s[i][0] - count_s[i][0]), 4)
                           ])
        table.add_row(['ensemble', 'S&P-500', e_count_s[0], ep_count_s[0] - e_count_s[0], e_count_s[1],
                       ep_count_s[1] - e_count_s[1], round(e_total_s/total_s, 4),
                       round(e_count_s[0]/(e_count_s[0] + ep_count_s[1] - e_count_s[1]), 4),
                       round(e_count_s[1]/(e_count_s[1] + ep_count_s[0] - e_count_s[0]), 4)
                       ])
        for i in range(0, 3):
            table.add_row([i + 2, 'HSBC Holdings', count[i][0], p_count[i][0] - count[i][0], count[i][1],
                           p_count[i][1] - count[i][1], round(w_total[i] / total, 4),
                           round(count[i][0] / (count[i][0] + p_count[i][1] - count[i][1]), 4),
                           round(count[i][1] / (count[i][1] + p_count[i][0] - count[i][0]), 4)
                           ])
        table.add_row(['ensemble', 'HSBC Holdings', e_count[0], ep_count[0] - e_count[0], e_count[1],
                       ep_count[1] - e_count[1], round(e_total/total, 4),
                       round(e_count[0]/(e_count[0] + ep_count[1] - e_count[1]), 4),
                       round(e_count[1]/(e_count[1] + ep_count[0] - e_count[0]), 4)
                       ])
        print(table)
    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
