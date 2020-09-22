import os
import pandas as pd

ticker = 'HSBC'
input_dir = r'../stock_data'
ticker_file = os.path.join(input_dir, 'new_' + ticker + '.csv')


def main():
    try:
        # load file
        with open(ticker_file) as f:
            lines = f.readlines()
        print('opened file for ticker: ', ticker)
        # save data in list
        data = []
        sub_data = []
        # split each line to a list
        for row in lines:
            data.append(row.split(','))
        # select the data of first three years
        j = 0
        for line in data:
            if j == 0:
                j = 1
                continue
            if int(line[1]) < 2018:
                sub_data.append(line)
        # Question1.2
        l_days = upday(sub_data)
        # Question1.3
        k_downday(sub_data, l_days)
        # Question1.4
        k_upday(sub_data, l_days)

    except Exception as e:
        print(e)
        print('falied to read stock data for ticker: ', ticker)


def upday(sub_data):
    # get the 'True Label' column to string type
    label_data = []
    for row in sub_data:
        label_data.append(str(row[14]))
    label_data = ''.join(label_data)
    # print(label_data)
    # Question 1.2
    l_days = len(label_data)
    l_down = label_data.count('-')
    l_up = label_data.count('+')
    print(l_days, l_down, l_up)
    # probability that the next day is a "up" day
    print("the default probability p that the next day is a up day is " + str(l_up / l_days))
    return l_days


def k_downday(sub_data, l_days):
    # Question 1.3
    temp = search_all_same(sub_data, l_days, '-')
    k_days = search_change(sub_data, '-')

    print(temp, k_days)
    print("down days")
    print("For k=1 the probability is %.4f, for k=2 the probability is %.4f, for k=3 the probability is %.4f" %
          (k_days[0] / (temp[0] + k_days[0]), k_days[1] / (temp[1] + k_days[1]), k_days[2] / (temp[2] + k_days[2])))


def k_upday(sub_data, l_days):
    # Question 1.4
    temp = search_all_same(sub_data, l_days, '+')
    k_days = search_change(sub_data, '+')

    print(temp, k_days)
    print("up days")
    print("For k=1 the probability is %.4f, for k=2 the probability is %.4f, for k=3 the probability is %.4f" %
          (temp[0] / (temp[0] + k_days[0]), temp[1] / (temp[1] + k_days[1]), temp[2] / (temp[2] + k_days[2])))


def search_all_same(sub_data, l_days, label):
    temp = [0, 0, 0]
    # loop each row int the data list
    for i in range(0, l_days - 3):
        # if the 'return' column >= 0 check the follow three row
        if sub_data[i][14] == label:
            # loop 3 times for check the follow three row
            for m in range(1, 4):
                # if the 'return' column >= 0 add 1 in the calculate list
                if sub_data[i + m][14] == label:
                    temp[m - 1] += 1
                # if < 0 break out this loop
                else:
                    break
    return temp


def search_change(sub_data, label):
    # a int list for calculate the three situation
    k_days = [0, 0, 0]
    # int variable for counting the "up" days
    count = 0
    for row in sub_data:

        if row[14] == label:
            count += 1
            continue
        else:
            if count == 1:
                k_days[count - 1] += 1
                count = 0
            elif count == 2:
                k_days[count - 1] += 1
                count = 0
            elif count == 3:
                k_days[count - 1] += 1
                count = 0
            else:
                count = 0
                continue
    return k_days


main()
