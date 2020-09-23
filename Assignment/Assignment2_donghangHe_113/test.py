
import os
import traceback

# variables for read file
ticker = 'HSBC'
input_dir = r'stock_data'
ticker_file = os.path.join(input_dir, 'new_' + ticker + '.csv')
# global variables
# predict label for the last two years
predict_label = []
# variable to get predict label from predict() function
temp_label = []
# list for data of last 2 years
last_data = []


def main():
    global temp_label, last_data
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
                sub_data.append(line[14])
        predict(sub_data)

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print('falied to read stock data for ticker: ', ticker)


def predict(sub_data):
    # print(label_temp)
    label_temp = ['+', '+', '+', '+', '-']
    length = len(label_temp)

    # print(label_temp)
    # int variables for save the '+' and '-'
    next_up = 0
    next_down = 0
    flag = 0
    count = 0
    # loop for search the same pattern in the first three year
    for i in range(0, len(sub_data) - length):
        for j in range(0, length):
            if str(sub_data[i + j]) != str(label_temp[j]):
                flag = 1
                break
        if flag == 1:
            flag = 0
            continue
        '''
        # calculate the up/down times
        if str(sub_data[i + length]) == '-':
            next_down += 1
        else:
            next_up += 1
        '''
        count += 1
    if next_up < next_down:
        # print(date + ': -')
        temp_label.append('-')
    else:
        # because of the p in the question1 is '+' > '-'
        # print(date + ': +')
        temp_label.append('+')
    print(next_down, next_up, count)


main()
