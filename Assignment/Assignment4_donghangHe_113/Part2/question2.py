import math
import traceback
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# for here I use the result of question1 for the real frequency
real_p = [0.377, 0.24, 0.094, 0.122, 0.054, 0.018, 0.038, 0.038, 0.019]
bernford = [0.301, 0.176, 0.125, 0.097, 0.079, 0.058, 0.058, 0.051, 0.046]
equal_weight = [0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111]


# method to change the y axis from 0.01 to 1%
def to_percent(y, position):
    return str(100 * y) + "%"


def main():
    try:
        # three list for calculate the relative error
        real_error = []
        bernford_error = []
        equal_weight_error = []

        # calculate the relative error
        for i in range(0, 9):
            real_error.append(0.00)
            bernford_error.append(round(abs(real_p[i] - bernford[i]) / real_p[i], 3))
            equal_weight_error.append(round(abs(real_p[i] - equal_weight[i]) / real_p[i], 3))

        # print(real_error, equal_weight_error, bernford_error)

        # x axis label
        label = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # draw the plot
        plt.figure()

        # first sub plot for the real relative error, of cause the error will be 0, so the plot is empty
        plt.subplot(311)
        plt.bar(range(1, 10), real_error, color='blue', tick_label=label)
        plt.title('real distribution')
        plt.ylabel('relative error')

        # second sub plot for the Model 1 relative error
        plt.subplot(312)
        plt.bar(range(1, 10), equal_weight_error, color='red', tick_label=label)
        formatter = FuncFormatter(to_percent)
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.title('Model 1')
        plt.ylabel('relative error')

        # third sub plot for the Model 2 relative error
        plt.subplot(313)
        plt.bar(range(1, 10), bernford_error, color='green', tick_label=label)
        formatter = FuncFormatter(to_percent)
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.title('Model 2')
        plt.xlabel('leading digit')
        plt.ylabel('relative error')

        plt.show()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
