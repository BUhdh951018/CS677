import pandas as pd
import os
import traceback

ticker = ['return_SPY', 'return_HSBC']
input_dir = r'../stock_data'


def main():
    try:
        for i in range(0, 2):
            # read file
            ticker_file = os.path.join(input_dir, ticker[i] + '.csv')
            df = pd.read_csv(ticker_file)
            df = pd.DataFrame(df)

            print('opened file for ticker: ', ticker[i])

            for j in range(0, 3):
                df_temp = df
                if j == 1:
                    df_temp = df[(df['Return']) >= 0]
                    print("positive")
                elif j == 2:
                    df_temp = df[(df['Return']) < 0]
                    print("negative")
                # calculate the mean and std for each set, and count the number for each set
                calculator(df_temp)

                print()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


def calculator(df):
    result = df.groupby(['Weekday'])['Return'].agg(['mean', 'std', 'count'])
    print(result)


main()
