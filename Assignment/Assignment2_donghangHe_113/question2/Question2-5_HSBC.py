import os
import traceback
from prettytable import PrettyTable
import matplotlib.pyplot as plt

# variables for read file
ticker = 'HSBC'
input_dir = r'../stock_data'
ticker_file = os.path.join(input_dir, 'new_' + ticker + '.csv')
# global variables
# predict label for the last two years
predict_label = []
# variable to get predict label from predict() function
temp_label = []
# list for data of last 2 years
last_data = []
# list for actual label
act_label = []
# calculate the '+' and '-' in the real stock
t_count = 0
f_count = 0
# global count list for save correct number
count = [[0, 0], [0, 0], [0, 0]]
# global count list for number of "+" and "-" which we predicted
p_count = [[0, 0], [0, 0], [0, 0]]
# global count list for save correct number
e_count = [0, 0]
# global count list for number of "+" and "-" which we predicted
ep_count = [0, 0]
# list for save ensemble label
ensemble_label = []


def main():
    global temp_label, last_data, t_count, f_count
    try:
        # load file
        with open(ticker_file) as f:
            lines = f.readlines()
        print('opened file for ticker: ', ticker)
        # save data in list
        data = []
        # list for data of first 3 years
        sub_data = []
        '''
        # list for data of last 2 years
        last_data = []
        '''
        # list for the last 4 days of 2017
        w_data = []
        # split each line to a list
        for row in lines:
            data.append(row.split(','))
        # append data to the three list above
        j = 0
        for line in data:
            if j == 0:
                j = 1
                continue
            # check the data for the first 3 years
            if int(line[1]) < 2018:
                sub_data.append(line)
                # check the data for the last 4 days of 2017
                if int(line[2]) == 12 and int(line[1]) == 2017:
                    if int(line[3]) > 25:
                        w_data.append(line)
            # check the data for the last 2 years
            else:
                last_data.append(line)
                act_label.append(line[14])
        t_count = act_label.count('+')
        f_count = act_label.count('-')
        # add the 4 days to the last 2 years make them a new list
        last_data_r = w_data + last_data
        # Question2.1
        for w in range(2, 5):
            # print("W = " + str(w) + ":")
            # according to the w get the label of each days in the last 2 years
            get_label(last_data_r, w, sub_data)
            # append each label list to the final predict label list
            predict_label.append(temp_label)
            temp_label = []

        # Question2.2
        correct_percentage(predict_label)

        # Question 3
        ensemble()

        # Question 4
        confusion_matrix()

        # Question 5
        chart()

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print('falied to read stock data for ticker: ', ticker)


def get_label(data, w, sub_data):
    # loop from 2017-12-29 to get the label for each day in 2018,2019
    for i in range(3, len(data) - 1):
        # list for save the  label
        label_temp = []
        # lop for different W
        for m in range(0, w):
            label_temp.append(data[i - m][14])

        predict(label_temp, sub_data, data[i + 1][0])


def predict(label_temp, sub_data, date):

    length = len(label_temp)
    label_temp.reverse()

    # int variables for save the '+' and '-'
    next_up = 0
    next_down = 0
    flag = 0
    # loop for search the same pattern in the first three year
    for i in range(0, len(sub_data) - length):
        for j in range(0, length):
            if str(sub_data[i + j][14]) != str(label_temp[j]):
                flag = 1
                break
        if flag == 1:
            flag = 0
            continue
        # calculate the up/down times
        if str(sub_data[i + length][14]) == '-':
            next_down += 1
        else:
            next_up += 1

    if next_up < next_down:
        # print(date + ': -')
        temp_label.append('-')
    else:
        # because of the p in the question1 is '+' > '-'
        # print(date + ': +')
        temp_label.append('+')


def correct_percentage(label):
    global count
    length = len(last_data)
    # loop for check the correct percentage
    for j in range(0, 3):
        # save the data for question 4
        p_count[j][0] = label[j].count('+')
        p_count[j][1] = label[j].count('-')

        for i in range(0, length):
            if label[j][i] == act_label[i]:
                if act_label[i] == '+':
                    count[j][0] += 1
                else:
                    count[j][1] += 1
        # print("true positive      true negative")
        # print(count[j][0] / t_count, count[j][1] / f_count)
    # print(count)


def ensemble():
    # get the predict label from question2
    label = predict_label
    # print(len(label))

    # list for save each days 3 predict label
    temp_ensemble_label = []

    length = int(len(label[0]))
    # get the pattern of each day
    for i in range(0, length):
        temp = [label[0][i], label[1][i], label[2][i]]
        temp_ensemble_label.append(temp)

    # calculate the major of three label
    for i in range(0, length):
        temp = max(temp_ensemble_label[i], key=temp_ensemble_label[i].count)
        ensemble_label.append(temp)

    # get the data of the last two years
    data = last_data
    # Question3.1
    '''
    for i in range(0, length):
        print("The ensemble labels of " + data[i][0] + " is " + ensemble_label[i])
    '''
    ep_count[0] = ensemble_label.count('+')
    ep_count[1] = ensemble_label.count('-')
    # Question3.2
    correct_percentage_e(ensemble_label, data)


def correct_percentage_e(e_label, data):
    global e_count, ensemble_label
    length = len(data)

    # calculate the percentage of correct label
    for i in range(0, length):
        if e_label[i] == data[i][14]:
            if data[i][14] == '+':
                e_count[0] += 1
            else:
                e_count[1] += 1
        else:
            continue


def confusion_matrix():
    # all correct label use ensemble learning
    e_total = e_count[0] + e_count[1]
    # total label numbers
    total = t_count + f_count
    # correct numbers of each W
    w_total = [(count[0][0] + count[0][1]), (count[1][0] + count[1][1]), (count[2][0] + count[2][1])]
    temp = ['W', 'ticker', 'TP', 'FP', 'TN', 'FN', 'accuracy', 'TPR', 'TNR']
    table = PrettyTable(temp)

    for i in range(0, 3):
        table.add_row([i + 2, 'HSBC Holdings', count[i][0], p_count[i][0] - count[i][0], count[i][1],
                       p_count[i][1] - count[i][1], round(w_total[i] / total, 4),
                       round(count[i][0] / (count[i][0] + p_count[i][1] - count[i][1]), 4),
                       round(count[i][1] / (count[i][1] + p_count[i][0] - count[i][0]), 4)
                       ])
    table.add_row(['ensemble', 'HSBC Holdings', e_count[0], ep_count[0] - e_count[0], e_count[1],
                   ep_count[1] - e_count[1], round(e_total / total, 4),
                   round(e_count[0] / (e_count[0] + ep_count[1] - e_count[1]), 4),
                   round(e_count[1] / (e_count[1] + ep_count[0] - e_count[0]), 4)
                   ])
    print(table)


def chart():
    # the best W is W=4 so save it label to a new list
    label = predict_label[2]
    # calculate the price for each days use W=4 label
    show = [100.00]
    for i in range(0, len(label)):
        if label[i] == '+':
            show.append(round(show[i] * (1 + float(last_data[i][13])), 4))
        else:
            show.append(round(show[i], 4))
    # calculate the price for each days use ensemble label
    show_s = [100]
    for i in range(0, len(ensemble_label)):
        if ensemble_label[i] == '+':
            show_s.append(show_s[i] * (1 + float(last_data[i][13])))
        else:
            show_s.append(show_s[i] * 1)
    # for i in range(0, 503):
    # real.append(real[i] * (1 + float(last_data[i][13])))
    # print the graph
    plt.plot(show, color='green', label='W')
    plt.plot(show_s, color='blue', label='ensemble')
    # plt.plot(real, color='red', label='real')
    plt.legend()
    plt.show()


main()
