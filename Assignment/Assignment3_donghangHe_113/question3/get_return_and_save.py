import pandas as pd
import os
import traceback

ticker = ['HSBC', 'SPY']
input_dir = r'../stock_data'


def main():
    try:
        # read two file
        for i in range(0, 2):
            ticker_file = os.path.join(input_dir, ticker[i] + '.csv')
            df = pd.read_csv(ticker_file)
            df = pd.DataFrame(df)

            print('opened file for ticker: ', ticker[i])
            # get the weekday and return column in a new table
            df_new = pd.DataFrame(df['Weekday'])
            df_new.insert(1, 'Return', df['Return'])
            print(df_new)
            # save the table to csv file
            new_file = os.path.join(r'../stock_data', 'return_' + ticker[i] + '.csv')
            df_new.to_csv(new_file, index=False)

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
