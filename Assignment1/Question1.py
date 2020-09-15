import os

ticker = 'diamonds'
input_dir = r'/Users/donghanghe/study/Assignment1'
ticker_file = os.path.join(input_dir, ticker + '.csv')

try:
    with open(ticker_file) as f:
        lines = f.readlines()
    print('opened file for ticker: ', ticker)
    data = []
    sub_data = []
    for row in lines:
        data.append(row.split(','))
    for line in data:
        if line[2] == 'Good':
            sub_data.append(line)

    # Question 1.2
    print(len(sub_data))
    total = 0
    for carat in sub_data:
        total += float(carat[1])
    # Question 1.3
    print(round((total / len(sub_data)), 4))
    avg_price = 0
    for price in sub_data:
        avg_price += int(price[7])
    # Question 1.4
    print(round((avg_price / len(sub_data)), 4))

    pw1 = 0.00
    pw = []
    for diamond in sub_data:
        pw1 += (int(diamond[7]) / float(diamond[1]))
        pw.append(int(diamond[7]) / float(diamond[1]))

    # Question 2.1
    print(pw1 / len(sub_data))
    print(avg_price / total)

    # Question 2.3
    print(max(pw))
    # Question 2.4
    print(min(pw))
    pw.sort()
    mid = len(pw) // 2
    # Question 2.5
    print((pw[mid] + pw[~mid]) / 2)

except Exception as e:
    print(e)
    print('falied to read stock data for ticker: ', ticker)
