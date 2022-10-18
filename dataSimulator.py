import numpy as np
import random
import matplotlib.pyplot as plt


def linear_fit(x, a, b):
    return a * x + b


def diff_value(num1, num2):
    if num1 > num2:
        diff = num1 - num2
    else:
        diff = num2 - num1
    return diff


def normalise_in_range(x, a, b):
    return (b - a) * (x - np.min(x)) / (np.max(x) - np.min(x)) + a


def linear_data_generator(xrange, sign, high, low):
    rate = linear_slope_generator(sign)
    y = xrange * rate
    a = normalise_in_range(y, low, high)
    return a


def moving_avarage_function(arr, window_size):
    i = 0
    # Initialize an empty list to store moving averages
    moving_averages = []

    # Loop through the array to consider
    # every window of size 3
    while i < len(arr) - window_size + 1:
        # Store elements from i to i+window_size
        # in list to get the current window
        window = arr[i: i + window_size]

        # Calculate the average of current window
        window_average = round(sum(window) / window_size, 2)

        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)

        # Shift window to right by one position
        i += 1
    return moving_averages


def exp_data_generator(xrange, sign, high, low):
    random.seed(len(xrange))
    tau = random.randint(round(len(xrange) * 0.5), round(len(xrange)) * 2)
    if sign == "decrease":
        random.seed(int(len(xrange) / 10))
        if round(random.random()) == 0:
            return normalise_in_range(np.exp(-xrange / tau), low, high)
        else:
            return normalise_in_range(1 - np.exp(xrange / tau) / np.sum(np.exp(xrange / tau)), low, high)
    elif sign == "increase":
        random.seed(int(len(xrange) / 10))
        if round(random.random()) == 0:
            return normalise_in_range(-np.exp(-xrange / tau), low, high)
        else:
            return normalise_in_range(np.exp(xrange / tau) / np.sum(np.exp(xrange / tau)), low, high)


def linear_slope_generator(trend):
    if trend == "increase":
        random.seed(20)
        return np.random.exponential(scale=1.0, size=None)
    elif trend == "decrease":
        random.seed(30)
        return -np.random.exponential(scale=1.0, size=None)


def new_data(type, noise, default_trend, data_size, max_value, min_value, counter):
    trend = default_trend

    if type == "linear":
        y_reading_ref = np.array(linear_data_generator(np.linspace(1, data_size,
                                                                   data_size), trend, max_value, min_value))
    elif type == "non-linear":
        y_reading_ref = np.array(exp_data_generator(np.linspace(1, data_size,
                                                                data_size), trend, max_value, min_value))
    elif type == "non-mono":
        y_reading_ref = np.array(exp_data_generator(np.linspace(1, data_size,
                                                                data_size), trend, max_value, min_value))
        # plt.figure()
        # plt.plot(np.arange(0, y_reading_ref.size, 1, dtype=int), y_reading_ref)
        np.random.seed(int(counter + 1 / 100))
        y_reading_ref = y_reading_ref + np.random.normal(0, diff_value(min_value, max_value), y_reading_ref.shape)
        x = np.arange(0, y_reading_ref.size, 1, dtype=int)
        pfit = np.poly1d(np.polyfit(x, y_reading_ref, 5))
        y_reading_ref = pfit(x)
        y_reading_ref = normalise_in_range(y_reading_ref, min_value, max_value)
    y_reading = y_reading_ref
    a = diff_value(min_value, max_value)
    if noise == 1:
        np.random.seed(int(counter / 100 + 2))
        y_reading = y_reading + np.random.normal(0, a * 0.25, y_reading.shape)
    elif noise == 2:
        np.random.seed(int(counter / 100 + 3))
        y_reading = y_reading + np.random.normal(0, a * 0.5, y_reading.shape)
    elif noise == 3:
        np.random.seed(int(counter / 100 + 4))
        y_reading = y_reading + np.random.normal(0, a * 0.75, y_reading.shape)

    # y_reading = y_reading_ref[0:-prediction_horizon]
    x_generating = np.arange(0, y_reading.size, 1, dtype=int)

    # plt.figure()
    # plt.plot(x_generating, y_reading)
    # np.savetxt("/Users/xinweifang/Desktop/y1.csv", y_reading, delimiter=",", fmt='%0.6f')
    return x_generating, y_reading, y_reading_ref


def data_generator(prob_parameters, rwd_parameters, application, noise_level, global_t):
    data = dict()
    data_formatted = dict()
    data_size_temp = np.array(0)
    temp_couter = 0
    if application == "fruit-picking":
        for i in prob_parameters:
            # fruit picking
            temp_couter += 1
            random.seed(global_t / 100 + temp_couter)
            data[i] = new_data("non-mono", noise=noise_level, default_trend="decrease",
                               data_size=random.randint(7200, 10080),
                               max_value=1,
                               min_value=0.6, counter=global_t / 100 + temp_couter)
            # plt.figure()
            # plt.plot(data[i][0], data[i][1], "o")
            # print(len(data.get(i)[0]))
            data_size_temp = np.vstack((data_size_temp, len(data.get(i)[0])))
        if len(rwd_parameters) > 0:
            for i in rwd_parameters:
                temp_couter += 1
                # fruit picking
                random.seed(global_t / 100 + temp_couter)
                data[i] = new_data("non-mono", noise=noise_level, default_trend="increase",
                                   data_size=random.randint(7200, 10080),
                                   max_value=10,
                                   min_value=1, counter=global_t / 100 + temp_couter)
                data_size_temp = np.vstack((data_size_temp, len(data.get(i)[0])))
        data_size_temp = np.delete(data_size_temp, 0, 0)
        datasize = np.min(data_size_temp)
    elif application == "RAD":
        for i in prob_parameters:
            temp_couter += 1
            random.seed(global_t / 100 + temp_couter)
            data[i] = new_data("non-mono", noise=noise_level, default_trend="decrease",
                               data_size=random.randint(7200, 10080),
                               max_value=0.6,
                               min_value=0.3, counter=global_t / 100 + temp_couter)
            # plt.figure()
            # plt.plot(data[i][0], data[i][1], "o")
            # print(len(data.get(i)[0]))
            data_size_temp = np.vstack((data_size_temp, len(data.get(i)[0])))
        if len(rwd_parameters) > 0:
            for i in rwd_parameters:
                # RAD
                temp_couter += 1
                random.seed(global_t / 100 + temp_couter)
                data[i] = new_data("non-mono", noise=noise_level, default_trend="increase",
                                   data_size=random.randint(7200, 10080),
                                   max_value=10,
                                   min_value=1, counter=global_t / 100 + temp_couter)
                # plt.figure()
                # plt.plot(data[i][0], data[i][1], "o")
                # print(len(data.get(i)[0]))
                data_size_temp = np.vstack((data_size_temp, len(data.get(i)[0])))
        data_size_temp = np.delete(data_size_temp, 0, 0)
        datasize = np.min(data_size_temp)
    for i in data:
        temp = data[i]
        data_formatted[i] = [temp[0][0:datasize], temp[1][0:datasize], temp[2][0:datasize]]
    #    X, y_reading, y_refernce
    return data_formatted, datasize
