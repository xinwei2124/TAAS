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
from baseline import *


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


def linear_updating(fitted_linear_model, data, datasize, model_parameters, Epsilon, Updating_N, idx, Line_fit_data_size):
    counter_positive = dict()
    counter_negative = dict()
    fitting_index = dict()
    flag = 0
    for i in model_parameters:
        counter_positive[i] = 0
        counter_negative[i] = 0
        fitting_index[i] = 0

    for i in model_parameters:
        a = max(data.get(i)[2])
        b = min(data.get(i)[2])
        value_diff = diff_value(a,b)
        for data_sample in range(idx[i], datasize):
            x = data.get(i)[0][data_sample]
            y = data.get(i)[1][data_sample]


            if fitted_linear_model[i].ndim < 2:
                linear_result = fitted_linear_model[i][0] * x + fitted_linear_model[i][1]
            else:
                linear_result = fitted_linear_model[i][-1][0] * x + fitted_linear_model[i][-1][1]

            if y > linear_result - value_diff*Epsilon:
                counter_positive[i] = counter_positive[i] + 1
                counter_negative[i] = 0
            if y < linear_result + value_diff*Epsilon:
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
        if new_fitting_origin[i] >=0:
            fitted_linear_model[i] = linear_analysis(
                data.get(i)[0][new_fitting_origin[i]:new_fitting_origin[i] + Line_fit_data_size],
                data.get(i)[1][new_fitting_origin[i]:new_fitting_origin[i] + Line_fit_data_size])
        temp_array = np.append(temp_array, new_fitting_origin[i] + Line_fit_data_size)
        param_idx[i] = new_fitting_origin[i] + Line_fit_data_size
    idx = int(max(temp_array))
    return param_idx, idx, fitted_linear_model


def multi_req_evaluation (model_parameters, fitted_linear_model, pmc_exp, req, data, PMC_result):
    var = [1, 2, 3]
    t = []
    data_length = []
    decision = []
    for i in var:
        temp= polynomial_evaluation_first_root(model_parameters, fitted_linear_model, pmc_exp[i], req[i])
        if (temp > 0):
            t.append(temp)
        data_length.append(system_level_prop_eval(data, req[i], PMC_result[i])[0])
        decision.append(system_level_prop_eval(data, req[i], PMC_result[i])[1])
    if not t:
        t = 500000
    else:
        t = min(t)
    data_length = min(data_length)
    if sum(decision)>0:
        decision = 1
    else:
        decision = 0
    return t, data_length, decision


def PRESTO(model_parameters, fitted_linear_model, pmc_exp, req, data, PMC_result, datasize, Epsilon, Updating_N, param_idx, Line_fit_data_size, value, trigger_value):
    idx = 0
    prediction_flag = 0
    counter = 0

    while counter < datasize:
        t, ref_t, decision = multi_req_evaluation(model_parameters, fitted_linear_model, pmc_exp, req, data, PMC_result)
        flag, new_fitting_origin = linear_updating(fitted_linear_model, data, datasize, model_parameters, Epsilon,
                                                   Updating_N, param_idx, Line_fit_data_size)
        if flag == 1:
            temp = []
            for i in new_fitting_origin:
                temp.append(new_fitting_origin[i])
            min_val = 0
            for i in temp:
                if min_val < i < ref_t:
                    min_val = i
            for i in new_fitting_origin:
                if new_fitting_origin[i] >= ref_t:
                    new_fitting_origin[i] = min_val
                    prediction_flag = 1
            if prediction_flag == 1:
                prediction_flag = 0
                param_idx, idx, fitted_linear_model = new_linear_model(model_parameters, fitted_linear_model, data, new_fitting_origin, Line_fit_data_size, param_idx)
                t, ref_t, decision = multi_req_evaluation(model_parameters, fitted_linear_model, pmc_exp, req, data, PMC_result)
                return t, ref_t, decision, idx
            else:
                param_idx, idx, fitted_linear_model = new_linear_model(model_parameters, fitted_linear_model, data,
                                                                       new_fitting_origin, Line_fit_data_size,
                                                                       param_idx)
                t, ref_t, decision = multi_req_evaluation(model_parameters, fitted_linear_model, pmc_exp, req, data,
                                                          PMC_result)
                if t - idx -counter < trigger_value:
                    return t, ref_t, decision, idx
                else:
                    counter +=idx
        else:
            param_idx, idx, fitted_linear_model = new_linear_model(model_parameters, fitted_linear_model, data,
                                                                   new_fitting_origin, Line_fit_data_size, param_idx)

            t, ref_t, decision = multi_req_evaluation(model_parameters, fitted_linear_model, pmc_exp, req, data,
                                                      PMC_result)
            return t, ref_t, decision, idx
    return t, ref_t, decision, idx

def PRESTOSimulation(RunningPeriod, number_of_maintenance, PMC_result, application_domain, noise_level, req, Epsilon, Updating_N, Line_fit_data_size, value, trigger_value,Random_seed_idx):

    TP =0
    FP = 0
    FN = 0
    service = 0

    maintenance_interval = int(RunningPeriod / (number_of_maintenance + 1))
    maintenance_idx_list = [0]
    no_service_flag = 0

    var = [1, 2, 3]
    pmc_exp = dict()
    model_parameters = set()
    model_parameter_rwd = set()
    model_parameter_prob = set()
    fitted_linear_model = dict()
    param_idx = dict()

    for i in var:
        pmc_exp[i] = PMC_result[i][0]
        model_parameter_rwd = model_parameter_rwd.union(PMC_result[i][3])
        model_parameters = model_parameters.union(PMC_result[i][1])
        model_parameter_prob = model_parameter_prob.union(PMC_result[i][2])

    for i in model_parameters:
        fitted_linear_model[i] = np.array([0, 0, 0, 0])
        param_idx[i] = 0

    if number_of_maintenance >= 1:
        for i in range(1, number_of_maintenance + 1):
            maintenance_idx_list.append(maintenance_interval * i)
        maintenance_idx_list.append(RunningPeriod)
    else:
        no_service_flag = 1
    counter = 0
    number_of_violation = 0
    data_reset_flag = 1
    tempx=0
    while counter < RunningPeriod:
        tempx+=1
        # print(counter)
        if data_reset_flag == 1:
            data, datasize = data_generator(model_parameter_prob, model_parameter_rwd, application_domain, noise_level, Random_seed_idx+counter)
        current_bound_idx = lower_bound(counter, maintenance_idx_list)

        if no_service_flag == 0 and counter + datasize > maintenance_idx_list[current_bound_idx]:
            data_before_fixed_service = maintenance_idx_list[current_bound_idx] - counter + 1
            resized_data = data_resize(data, data_before_fixed_service)
            t, ref_t, decision, idx = PRESTO(model_parameters, fitted_linear_model, pmc_exp, req, resized_data, PMC_result,
                                             data_before_fixed_service, Epsilon, Updating_N,
                                             param_idx, Line_fit_data_size, value, trigger_value)
            psi = ref_t - t
            if decision == 1:
                if abs(psi) <= value:
                    TP += 1
                    counter += ref_t
                elif abs(psi) > value and psi > 0:
                    FP += 1
                    counter += ref_t
                elif abs(psi) > value and psi <= 0:
                    FN += 1
                    counter += ref_t
            else:
                if psi < 0:
                    service += 1
                    counter += ref_t
                else:
                    if t-idx < trigger_value:
                        FP += 1
                        counter += ref_t
                    else:
                        service += 1
                        counter += ref_t
        else:  # when no fixed interval service
            t, ref_t, decision, idx = PRESTO(model_parameters, fitted_linear_model, pmc_exp, req, data, PMC_result, datasize, Epsilon, Updating_N,
                   param_idx, Line_fit_data_size, value, trigger_value)
            psi = ref_t - t
            if abs(psi) <= value:
                TP += 1
                counter += ref_t
            elif abs(psi) > value and psi > 0:
                FP += 1
                counter += ref_t
            elif abs(psi) > value and psi <= 0:
                FN += 1
                counter += ref_t


    return TP, FN, FP, service







# def PRESTOSimulation(RunningPeriod, prediction_horizon, Updating_N, Line_fit_data_size, Epsilon, PMC_result,
#                      application_domain, noise_level, req, value, trigger_value):
#     TP = 0
#     FP = 0
#     FN = 0
#
#     pmc_exp = dict()
#     fitted_linear_model = dict()
#     param_idx = dict()
#
#     var = [1, 2, 3]
#     model_parameters = set()
#     model_parameter_rwd = set()
#     model_parameter_prob = set()
#     for i in var:
#         pmc_exp[i] = PMC_result[i][0]
#         model_parameter_rwd = model_parameter_rwd.union(PMC_result[i][3])
#         model_parameters = model_parameters.union(PMC_result[i][1])
#         model_parameter_prob = model_parameter_prob.union(PMC_result[i][2])
#
#     counter = 0
#     fitting_origin = 0
#     idx = 0
#     loop_counter = 0
#     for i in model_parameters:
#         fitted_linear_model[i] = np.array([0, 0, 0, 0])
#         param_idx[i] = 0
#
#     data, datasize = data_generator(model_parameter_prob, model_parameter_rwd, application_domain, noise_level, counter)
#     while counter < RunningPeriod:
#         t, data_length, decision = multi_req_evaluation(model_parameters, fitted_linear_model, pmc_exp, req, data,
#                                                         PMC_result)
#         flag, new_fitting_origin = linear_updating(fitted_linear_model, data, datasize, model_parameters, Epsilon, Updating_N,
#                                                    param_idx, Line_fit_data_size)
#         temp = []
#         for i in new_fitting_origin:
#             temp.append(new_fitting_origin[i])
#         min_val=0
#         for i in temp:
#             if min_val < i < data_length:
#                 min_val = i
#
#         for i in new_fitting_origin:
#             if new_fitting_origin[i] >= data_length:
#                 new_fitting_origin[i] = min_val
#
#         if flag == 1:
#             param_idx, idx, fitted_linear_model = new_linear_model(model_parameters, fitted_linear_model, data, new_fitting_origin, Line_fit_data_size,
#                              param_idx)
#             # t = polynomial_evaluation_first_root(model_parameters, fitted_linear_model, pmc_exp[2],
#             #                                      req[2]) + counter - Line_fit_data_size
#             # print(PMC_result[1][0])
#             # data_length, decision = system_level_prop_eval(data, req[1], PMC_result[1])
#             # print(PMC_result[2][0])
#             # data_length, decision = system_level_prop_eval(data, req[2], PMC_result[2])
#             t, data_length, decision = multi_req_evaluation(model_parameters, fitted_linear_model, pmc_exp, req, data, PMC_result)
#             t = t + counter
#             data_length = data_length + counter
#
#             # t = polynomial_evaluation_first_root(model_parameters, fitted_linear_model, pmc_exp,
#             #                                      req) + counter - Line_fit_data_size
#             # data_length, decision = system_level_prop_eval(data, req, PMC_result)
#             # if t < counter or all(value == 0 for value in new_fitting_origin.values()):
#             if t < counter or data_length - counter < loop_counter:
#                 print(counter)
#                 FN += 1
#                 counter = data_length
#                 data, datasize = data_generator(model_parameter_prob, model_parameter_rwd, application_domain,
#                                                 noise_level, counter)
#                 loop_counter = 0
#             elif t - idx - loop_counter - counter < trigger_value:
#                 print(counter)
#                 psi = data_length - t
#                 if abs(psi) <= value:
#                     TP += 1
#                     counter = counter + idx
#                 elif abs(psi) > value and psi > 0:
#                     FP += 1
#                     counter = t
#                 elif abs(psi) > value and psi <= 0:
#                     FN += 1
#                     counter = data_length
#                 for i in model_parameters:
#                     fitted_linear_model[i] = np.array([0, 0, 0, 0])
#                     param_idx[i] = 0
#                 data, datasize = data_generator(model_parameter_prob, model_parameter_rwd, application_domain, noise_level, counter)
#                 loop_counter = 0
#         else:
#             t, data_length, decision = multi_req_evaluation(model_parameters, fitted_linear_model, pmc_exp, req, data, PMC_result)
#             t = t + counter
#             data_length = data_length + counter
#             if decision == 0:
#                 if t < datasize:
#                     FP += 1
#                 counter += datasize
#                 print(counter)
#             else:
#                 psi = data_length - t
#                 if t < counter:
#                     print(counter)
#                     FN += 1
#                     counter = data_length
#                 else:
#                     if abs(psi) <= value:
#                         print(counter)
#                         TP += 1
#                         counter = t - trigger_value
#                     elif abs(psi) > value and psi > 0:
#                         print(counter)
#                         FP += 1
#                         counter = t
#                     elif abs(psi) > value and psi <= 0:
#                         print(counter)
#                         FN += 1
#                         counter = data_length
#                 for i in model_parameters:
#                     fitted_linear_model[i] = np.array([0, 0, 0, 0])
#                     param_idx[i] = 0
#             data, datasize = data_generator(model_parameter_prob, model_parameter_rwd, application_domain, noise_level, counter)
#             loop_counter = 0
#         loop_counter += idx
#     return TP, FN, FP
