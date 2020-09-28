from typing import List, Any, Union

import numpy as np
import matplotlib.pyplot as plt
from question2.Question2_HSBC import predict_label, last_data
from question3.Question3_HSBC import ensemble_label
# real = [100]
# the best W is W=4 so save it label to a new list
predict_label = predict_label[2]
# calculate the price for each days use W=4 label
show = [100.00]
for i in range(0, len(predict_label)):
    if predict_label[i] == '+':
        show.append(round(show[i] * (1 + float(last_data[i][13])), 4))
    else:
        show.append(round(show[i], 4))
# calculate the price for each days use ensemble label
show_s = [100]
for i in range(0, len(ensemble_label)):
    if ensemble_label[i] == '+':
        show_s.append(show_s[i] * (1 + float(last_data[i][13])))
    else:
        show_s.append(show_s[i] * 1)
# for i in range(0, 503):
    # real.append(real[i] * (1 + float(last_data[i][13])))
# print the graph
plt.plot(show, color='green', label='W')
plt.plot(show_s, color='blue', label='ensemble')
# plt.plot(real, color='red', label='real')
plt.legend()
plt.show()
