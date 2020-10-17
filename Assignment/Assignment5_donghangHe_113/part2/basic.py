from method import df_banknote


def main():
    df = df_banknote

    # question 1
    data = df['class'].tolist()
    # set the color
    color = []
    for row in data:
        if row == 0:
            color.append('green')
        else:
            color.append('red')
    # add color column
    df.insert(5, 'Color', color)

    # question 2
    result1 = df.groupby(['class'])[['variance', 'skewness']].agg(['mean', 'std'])
    result2 = df.groupby(['class'])[['curtosis', 'entropy']].agg(['mean', 'std'])
    f1 = df['variance'].agg(['mean', 'std'])
    f2 = df['skewness'].agg(['mean', 'std'])
    f3 = df['curtosis'].agg(['mean', 'std'])
    f4 = df['entropy'].agg(['mean', 'std'])
    print(result1)
    print(result2)
    print('\nmean and standard deviation for all')
    print(f1, '\n', f2, '\n', f3, '\n', f4)

    # save file
    df.to_csv('../datasets/data_banknote_color.csv', index=False)


main()
