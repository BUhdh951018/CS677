import math
import traceback
from sklearn.metrics import mean_squared_error

# for here I use the result of question1 for the real frequency
real_p = [0.377, 0.24, 0.094, 0.122, 0.054, 0.018, 0.038, 0.038, 0.019]
bernford = [0.301, 0.176, 0.125, 0.097, 0.079, 0.058, 0.058, 0.051, 0.046]
equal_weight = [0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111]


def main():
    try:
        # two variables for calculate the RMSE
        bernford_error = math.sqrt(mean_squared_error(real_p, bernford))
        equal_weight_error = math.sqrt(mean_squared_error(real_p, equal_weight))

        print("RMSE for model 1 is: " + str(equal_weight_error))
        print("RMSE for model 2 is: " + str(bernford_error))

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
