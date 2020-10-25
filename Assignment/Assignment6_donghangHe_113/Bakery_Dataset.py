import os
import pandas as pd
import math
import numpy as np
import datetime
import traceback

# show all row
pd.options.display.max_columns = None
pd.options.display.max_rows = None
np.set_printoptions(threshold=np.inf)

input_dir = r'dataset'
input_file = os.path.join(input_dir, 'BreadBasket_DMS_output.csv')

# my choice for drink and food
drink = ['Coffee', 'Tea', 'Hot chocolate', 'Juice']
food = ['Bread', 'Cake', 'Sandwich', 'Cookies', 'Brownie', 'Muffin']
# day name
day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def busiest(df):
    # count each hour, each day, each period
    df_hour = df.groupby(['Hour'])['Transaction'].nunique()
    df_day = df.groupby(['Weekday'])['Transaction'].nunique()
    df_period = df.groupby(['Period'])['Transaction'].nunique()
    # (a)
    print(df_hour)
    # (b)
    print(df_day)
    # (c)
    print(df_period)


def profitable(df):
    # get the total price of each hour, day, period
    df_hour = df.groupby(['Hour'])['Item_Price'].sum()
    df_day = df.groupby(['Weekday'])['Item_Price'].sum()
    df_period = df.groupby(['Period'])['Item_Price'].sum()
    # (a)
    print(df_hour)
    # (b)
    print(df_day)
    # (c)
    print(df_period)


def most_and_least(df):
    # sort by item
    df_item = df.groupby(['Item'])['Item'].count().sort_values()
    print(df_item)


def barista(df):
    # select the item which is coffee, because I search the word 'barista' means who make coffee
    df_coffee = df[(df['Item']) == 'Coffee']
    # get the year, month, day for calculate the week number
    year = df_coffee['Year'].tolist()
    month = df_coffee['Month'].tolist()
    day = df_coffee['Day'].tolist()
    # get the weekday for new table
    weekday = df_coffee['Weekday'].tolist()
    # calculate the week number
    week_number = []
    for i in range(len(df_coffee)):
        week_number.append(datetime.date(year[i], month[i], day[i]).isocalendar()[1])
    # make the new table
    df_new = pd.DataFrame({"week_number": week_number, "weekday": weekday})
    # search from Monday to Sunday
    for i in range(7):
        df_weekday = df_new[(df_new['weekday']) == day_name[i]]
        df = df_weekday.groupby(['week_number'])['weekday'].count().max()
        # get the most coffee selling day in all Monday to Sunday and calculate the barista shop need
        print(str(day_name[i]) + " need " + str(math.ceil(df / 50)) + " barista.")


def avg_drink_food(df):
    # divide the dataset to drink and food
    df_drink = df[(df['Item']).isin(drink)]
    df_food = df[(df['Item']).isin(food)]
    # get mean price of drink and food
    mean_drink = df_drink['Item_Price'].mean()
    mean_food = df_food['Item_Price'].mean()
    # average drink
    print("average drink")
    print(round(mean_drink, 2))
    # average food
    print("average food")
    print(round(mean_food, 2))


def sum_drink_food(df):
    df_drink = df[(df['Item']).isin(drink)]
    df_food = df[(df['Item']).isin(food)]
    # get the total income of drink and food
    sum_drink = df_drink['Item_Price'].sum()
    sum_food = df_food['Item_Price'].sum()
    # drink money
    print("money from drink")
    print(round(sum_drink, 2))
    # food money
    print("money from food")
    print(sum_food)


def top_5(df):
    # loop from Monday to Sunday
    for i in range(7):
        df_day = df[(df['Weekday']) == day_name[i]]
        # sort by selling item numbers
        df_top = df_day.groupby(['Item'])['Item'].count().sort_values()
        print(day_name[i], "top 5")
        # get the bottom 5 for top 5
        print(df_top[-5:])


def bottom_5(df):
    for i in range(7):
        df_day = df[(df['Weekday']) == day_name[i]]
        df_top = df_day.groupby(['Item'])['Item'].count().sort_values()
        print(day_name[i], "top 5")
        # get the top 5 for bottom 5
        print(df_top[:5])


def drink_per_trans(df):
    # total transaction number
    total_trans = df['Transaction'].nunique()
    # get drink and calculate then length
    df_drink = df[(df['Item']).isin(drink)]
    total_drink = len(df_drink)
    # drink per trans
    print("drink per trans")
    print(round(total_drink / total_trans, 2))


def main():
    try:
        df = pd.read_csv(input_file)

        # question 1
        busiest(df)
        print('\n')

        # question 2
        profitable(df)
        print('\n')

        # question 3
        most_and_least(df)
        print('\n')

        # question 4
        barista(df)
        print('\n')

        # question 5
        avg_drink_food(df)
        print('\n')

        # question 6
        sum_drink_food(df)
        print('\n')

        # question 7
        top_5(df)
        print('\n')

        # question 8
        bottom_5(df)
        print('\n')

        # question 9
        drink_per_trans(df)
        print('\n')

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
