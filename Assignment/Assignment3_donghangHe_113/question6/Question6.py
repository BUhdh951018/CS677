import pandas as pd
import os
import traceback

ticker = ['return_HSBC', 'return_SPY']
input_dir = r'../stock_data'


def main():
    try:
        for i in range(0, 2):
            ticker_file = os.path.join(input_dir, ticker[i] + '.csv')
            # read file
            df = pd.read_csv(ticker_file)
            df = pd.DataFrame(df)

            print('opened file for ticker: ', ticker[i])
            df_new = pd.DataFrame(df['Return'])
            # add an index column to the table
            index = df.index.values
            df_new.insert(1, 'index', index)
            # sort by return column
            df_sort = df_new.sort_values(by=['Return'], ascending=[False])

            miss_10_best(df_sort)
            get_10_worst(df_sort)
            each_5(df_sort)
    except Exception as e:
        print(e)
        print(traceback.format_exc())


def miss_10_best(data):
    # let the biggest 10 value to 0
    data.iloc[:10, 0] = 0
    # select the return > 0
    data_new = data[(data['Return']) >= 0]
    # sort by index
    data_result = data_new.sort_values(by=['index'])
    data = list(data_result['Return'])
    # calculate the price
    price = 100
    for row in data:
        price = price * (1 + float(row))
    print("scenario a ", price)


def get_10_worst(data):
    # get the worst 10 return value
    temp = data[-10:]

    data_new = data[(data['Return']) >= 0]
    result = data_new.append(temp)
    result = result.sort_values(by=['index'])
    data = list(result['Return'])
    # calculate the price
    price = 100
    for row in data:
        price = price * (1 + float(row))
    print("scenario b ", price)


def each_5(data):
    # let the biggest 5 value to 0 and get the worst 5 return value
    data.iloc[:5, 0] = 0
    temp = data[-5:]

    data_new = data[(data['Return']) >= 0]
    result = data_new.append(temp)
    result = result.sort_values(by=['index'])
    data = list(result['Return'])
    # calculate the price
    price = 100
    for row in data:
        price = price * (1 + float(row))
    print("scenario c ", price)


main()
