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
            # get the return > 0 values to a new file
            df_new = df[(df['Return']) > 0]
            data = list(df_new['Return'])
            # print(data)
            price = 100
            for row in data:
                price = price * (1 + float(row))
            print(price)

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
