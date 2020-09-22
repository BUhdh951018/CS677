import os
import traceback
# variables for read file
ticker = 'HSBC'
input_dir = r'../stock_data'
ticker_file = os.path.join(input_dir, 'new_' + ticker + '.csv')
# global variables
# predict label for the last two years
predict_label = []
# variable to get predict label from predict() function
temp_label = []


def main():
    global temp_label
    try:
        # load file
        with open(ticker_file) as f:
            lines = f.readlines()
        print('opened file for ticker: ', ticker)
        # save data in list
        data = []
        # list for data of first 3 years
        sub_data = []
        # list for data of last 2 years
        last_data = []
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
        # add the 4 days to the last 2 years make them a new list
        last_data_r = w_data + last_data
        # Question2.1
        for w in range(2, 5):
            print("W = " + str(w) + ":")
            # according to the w get the label of each days in the last 2 years
            get_label(last_data_r, w, sub_data)
            # append each label list to the final predict label list
            predict_label.append(temp_label)
            temp_label = []
        # print(predict_label)
        # Question2.2
        correct_percentage(predict_label, last_data)

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print('falied to read stock data for ticker: ', ticker)


def get_label(last_data, w, sub_data):

    # print(last_data)
    for i in range(3, len(last_data) - 1):
        label_temp = []

        for m in range(0, w):
            label_temp.append(last_data[i - m][14])
        # print(label_temp, last_data[i + 1][0])
        predict(label_temp, sub_data, last_data[i + 1][0])


def predict(label_temp, sub_data, date):

    length = len(label_temp)
    label_temp.reverse()
    # print(label_temp)
    next_up = 0
    next_down = 0
    flag = 0

    for i in range(0, len(sub_data) - length):

        for j in range(0, length):

            if str(sub_data[i + j][14]) != str(label_temp[j]):
                flag = 1
                break
        if flag == 1:
            flag = 0
            continue

        if str(sub_data[i + length][14]) == '-':
            next_down += 1
        else:
            next_up += 1
    if next_up < next_down:
        print(date + ': -')
        temp_label.append('-')
    else:
        print(date + ': +')
        temp_label.append('+')


def correct_percentage(label, last_data):
    count = [0, 0, 0]
    length = len(last_data)

    for j in range(0, 3):
        for i in range(0, length - 1):
            if label[j][i] == last_data[i][14]:
                count[j] += 1
        print(count[j] / (len(last_data)))
    print(count)


main()
