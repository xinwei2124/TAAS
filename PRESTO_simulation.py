import numpy as np
from scipy.optimize import *
from numpy import log, log2

from baseline import system_level_prop_eval
from dataSimulator import *
from PMC import *
from scipy import optimize
from sympy import *
from sympy.abc import t
import pycarl


def linear_fit(x, a, b):
    return a * x + b


def linear_analysis(x, y):
    popt, pcov = optimize.curve_fit(linear_fit, x, y)
    fit_a, fit_b = popt[0], popt[1]
    line_fitting_error = np.mean(np.diag(pcov))
    return np.array([fit_a, fit_b, x[0], line_fitting_error])


def find_positive(lst):
    for x in lst:
        if x > 0:
            return x


def polynomial_evaluation_first_root(model_parameters, fitted_linear_model, str, requirement):
    str = f"{str}-{requirement}"
    str = str.replace("^", "**")
    for i in model_parameters:
        if fitted_linear_model[i].ndim < 2:
            var = f"({fitted_linear_model[i][0]}*t+{fitted_linear_model[i][1]})"
        else:
            var = f"({fitted_linear_model[i][-1][0]}*t+{fitted_linear_model[i][-1][1]})"
        str = str.replace(i.name, var)
    try:
        sol = int(nsolve(eval(str), t, 1))
        return sol
    except ValueError:
        return 50000


def linear_updating(fitted_linear_model, data, datasize, PMC_result, Epsilon, Updating_N, idx, Line_fit_data_size):
    model_parameters = PMC_result[1]
    counter_positive = dict()
    counter_negative = dict()
    fitting_index = dict()
    flag = 0
    for i in model_parameters:
        counter_positive[i] = 0
        counter_negative[i] = 0
        fitting_index[i] = 0

    for i in model_parameters:
        for data_sample in range(idx[i], datasize):
            x = data.get(i)[0][data_sample]
            y = data.get(i)[1][data_sample]

            if fitted_linear_model[i].ndim < 2:
                linear_result = fitted_linear_model[i][0] * x + fitted_linear_model[i][1]
            else:
                linear_result = fitted_linear_model[i][-1][0] * x + fitted_linear_model[i][-1][1]

            if y > linear_result:
                counter_positive[i] = counter_positive[i] + 1
                counter_negative[i] = 0
            if y < linear_result:
                counter_negative[i] = counter_negative[i] + 1
                counter_positive[i] = 0
            if y == linear_result:
                counter_negative[i] = 0
                counter_positive[i] = 0

            if counter_negative[i] >= Updating_N:
                fitting_index[i] = data_sample - counter_negative[i] + 1
                flag = 1
                break
            if counter_positive[i] >= Updating_N:
                fitting_index[i] = data_sample - counter_positive[i] + 1
                flag = 1
                break
    return flag, fitting_index


def new_linear_model(model_parameters, fitted_linear_model, data, new_fitting_origin, Line_fit_data_size, param_idx):
    temp_array = np.array(0)

    for i in model_parameters:
        fitted_linear_model[i] = linear_analysis(
            data.get(i)[0][new_fitting_origin[i]:new_fitting_origin[i] + Line_fit_data_size],
            data.get(i)[1][new_fitting_origin[i]:new_fitting_origin[i] + Line_fit_data_size])
        temp_array = np.append(temp_array, new_fitting_origin[i] + Line_fit_data_size)
        param_idx[i] = new_fitting_origin[i] + Line_fit_data_size
    idx = int(max(temp_array))
    return param_idx, idx, fitted_linear_model

def PRESTOSimulation(RunningPeriod, prediction_horizon, Updating_N, Line_fit_data_size, Epsilon, PMC_result,
                     application_domain, noise_level, req, value, trigger_value):
    TP = 0
    FP = 0
    FN = 0

    counter = 0
    fitting_origin = 0
    model_parameters = PMC_result[1]
    pmc_exp = PMC_result[0]
    idx = 0
    param_idx = dict()

    fitted_linear_model = dict()
    for i in model_parameters:
        fitted_linear_model[i] = np.array([0, 0, 0, 0])
        param_idx[i] = 0

    data, datasize = data_generator(PMC_result[2], PMC_result[3], application_domain, noise_level, counter)

    while counter < RunningPeriod:
        flag, new_fitting_origin = linear_updating(fitted_linear_model, data, datasize, PMC_result, Epsilon, Updating_N,
                                                   param_idx, Line_fit_data_size)
        if flag == 1:
            param_idx, idx, fitted_linear_model = new_linear_model(model_parameters, fitted_linear_model, data, new_fitting_origin, Line_fit_data_size,
                             param_idx)
            t = polynomial_evaluation_first_root(model_parameters, fitted_linear_model, pmc_exp,
                                                 req) + counter - Line_fit_data_size
            data_length, decision = system_level_prop_eval(data, req, PMC_result)
            data_length = data_length + counter

            if t < counter:
                FN += 1
                counter = data_length
            elif t - idx - counter < trigger_value:
                print(counter)
                psi = data_length - t
                if abs(psi) <= value:
                    TP += 1
                    counter = counter + idx
                elif abs(psi) > value and psi > 0:
                    FP += 1
                    counter = t
                elif abs(psi) > value and psi <= 0:
                    FN += 1
                    counter = data_length
                for i in model_parameters:
                    fitted_linear_model[i] = np.array([0, 0, 0, 0])
                    param_idx[i] = 0
                data, datasize = data_generator(PMC_result[2], PMC_result[3], application_domain, noise_level, counter)

        else:
            counter += datasize
            data, datasize = data_generator(PMC_result[2], PMC_result[3], application_domain, noise_level, counter)

    return TP, FN, FP

    # if fitting_origin <= idx < fitting_origin+datasize:
    #
    #
    #
    #     if idx>=Line_fit_data_size + fitting_origin:
    #        for i in model_parameters:
    #            fitted_linear_model[i] = linear_analysis(data.get(i)[0][idx:Line_fit_data_size + idx],
    #                                                     data.get(i)[1][idx:Line_fit_data_size + idx])
    #        prediction_origin = fitting_origin + Line_fit_data_size
    #        t = polynomial_evaluation_first_root(model_parameters, fitted_linear_model, pmc_exp, req)
    #        if (t<0):
    #            # reset
    #        else:
    #            print("predicted violation wrt prediction_oritgin is %d", t-Line_fit_data_size)
