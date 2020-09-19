import os

ticker = 'diamonds'
input_dir = r'/Users/donghanghe/study/Assignment1'
ticker_file = os.path.join(input_dir, ticker + '.csv')

try:
    # load file
    with open(ticker_file) as f:
        lines = f.readlines()
    print('opened file for ticker: ', ticker)
    data = []
    sub_data = []
    # split each line to a list
    for row in lines:
        data.append(row.split(','))
    # subset for Good diamond
    for line in data:
        if line[2] == 'Good':
            sub_data.append(line)

    # Question 1.2 entries number
    print(len(sub_data))
    # compute total weight
    total = 0.00
    for carat in sub_data:
        total += float(carat[1])
    total = round(total, 2)
    # Question 1.3 average weight
    print(round((total / len(sub_data)), 4), (total / len(sub_data)))
    # compute total price
    avg_price = 0
    for price in sub_data:
        avg_price += int(price[7])
    # Question 1.4 average price
    print(round((avg_price / len(sub_data)), 4))

    pw1 = 0.00
    pw = []
    for diamond in sub_data:
        pw1 += (int(diamond[7]) / float(diamond[1]))
        pw.append(int(diamond[7]) / float(diamond[1]))

    # Question 2.1
    # Method a
    print(pw1 / len(sub_data))
    # Method b
    print(avg_price / total)

    # Question 2.3
    max_diamond = 0.00
    max_no = 0
    temp_no = 0
    for row in sub_data:
        temp = (int(row[7]) / float(row[1]))
        temp_no += 1
        if temp > max_diamond:
            max_diamond = temp
            max_no = temp_no
    # use two method to calculate the max one(don't know the max() function if it can be used)
    print(max(pw), max_diamond)
    # Question 2.4
    min_diamond = 100000.00
    min_no = 0
    temp_no = 0
    for row in sub_data:
        temp = (int(row[7]) / float(row[1]))
        temp_no += 1
        if temp < min_diamond:
            min_diamond = temp
            min_no = temp_no
    # use two method to calculate the min one(don't know the min() function if it can be used)
    print(min(pw), min_diamond)
    # calculate the median using sort()
    pw.sort()
    mid = len(pw) // 2
    # Question 2.5 median
    print((pw[mid] + pw[~mid]) / 2)

    # Question 4.1
    print("Highest value diamond, color: " + sub_data[max_no-1][3] + " clarity: " + sub_data[max_no-1][4] + " depth: " +
          sub_data[max_no-1][5] + " table: " + sub_data[max_no-1][6])
    # Question 4.2
    print("Lowest value diamond, color: " + sub_data[min_no - 1][3] + " clarity: " + sub_data[min_no - 1][4] +
          " depth: " + sub_data[min_no - 1][5] + " table: " + sub_data[min_no - 1][6])

    # Question 5
    print(avg_price / total * 102)

except Exception as e:
    print(e)
    print('falied to read stock data for ticker: ', ticker)
