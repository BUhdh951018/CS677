import os
import traceback

ticker = 'SPY'
input_dir = r'../stock_data'
ticker_file = os.path.join(input_dir, 'new_' + ticker + '.csv')

predict_label = []
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
        sub_data = []
        last_data = []
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
            else:
                last_data.append(line)
        # print(last_data)

        # Question2.1
        for w in range(2, 5):
            print("W = " + str(w) + ":")
            get_label(last_data, w, sub_data)
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
    j = w - 1
    for i in range(0, len(last_data) - 1):
        if j > 0:
            j -= 1
            continue
        label_temp = []
        for m in range(0, w):
            label_temp.append(last_data[i - m][14])
        # print(label_temp, last_data[i][0])
        predict(label_temp, sub_data, last_data[i][0])


def predict(label_temp, sub_data, date):
    label = ['-', '+']
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
        for i in range(j + 2, length):
            if label[j][i - 2 - j] == last_data[i][14]:
                count[j] += 1
        print(count[j] / len(last_data))
    print(count)


main()
