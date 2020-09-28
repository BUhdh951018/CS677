import question2.Question2_SPY
import traceback
from question2.Question2_SPY import act_label, t_count_s, f_count_s

# global count list for save correct number
e_count_s = [0, 0]
# global count list for number of "+" and "-" which we predicted
ep_count_s = [0, 0]


def correct_percentage(e_label, last_data):
    global e_count_s
    length = len(last_data)
    # print(e_label)
    # calculate the percentage of correct label
    for i in range(0, length):
        if e_label[i] == last_data[i][14]:
            if last_data[i][14] == '+':
                e_count_s[0] += 1
            else:
                e_count_s[1] += 1
        else:
            continue
    # print((e_count_s[0] + e_count_s[1]) / length)
    # print(e_count_s[0] / t_count_s, e_count_s[1] / f_count_s)


def main():
    try:
        # get the predict label from question2
        label = question2.Question2_SPY.predict_label
        # print(len(label))

        # list for save each days 3 predict label
        temp_ensemble_label = []
        # list for save ensemble label
        ensemble_label = []
        length = int(len(label[0]))
        # get the pattern of each day
        for i in range(0, length):
            temp = [label[0][i], label[1][i], label[2][i]]
            temp_ensemble_label.append(temp)
        
        # calculate the major of three label
        for i in range(0, length):
            temp = max(temp_ensemble_label[i], key=temp_ensemble_label[i].count)
            ensemble_label.append(temp)

        # get the data of the last two years
        data = question2.Question2_SPY.last_data
        # Question3.1
        '''
        for i in range(0, length):
            print("The ensemble labels of " + data[i][0] + " is " + ensemble_label[i])
        '''
        ep_count_s[0] = ensemble_label.count('+')
        ep_count_s[1] = ensemble_label.count('-')
        # Question3.2
        correct_percentage(ensemble_label, data)

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
