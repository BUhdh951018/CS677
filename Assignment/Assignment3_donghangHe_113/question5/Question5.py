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

            data = list(df['Return'])

            price = 100

            for row in data:
                price = price * (1 + float(row))
            print(price)

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
