from dataSimulator import *
from PMC import *


def convert(s):
    try:
        return float(s)
    except ValueError:
        num, denom = s.split('/')
        return float(num) / float(denom)


def evaluateExpression(exp, Varlist):
    EvaResult = pycarl.cln.FactorizedRationalFunction.evaluate(exp, Varlist)
    return convert(EvaResult)


def compareValue(v1, v2):
    if v1 <= v2:
        return v1, v2
    else:
        return v2, v1


def Storm_evaluation_parameter_set(data, idx):
    data_instance = dict()
    for i in data:
        data_instance[i] = stormpy.RationalRF(data.get(i)[2][idx])
    return data_instance


def getClosest(val1, idx1, val2, idx2, target):
    if target - val1 >= val2 - target:
        return idx2
    else:
        return idx1


def system_level_prop_eval(data, req, PMC_result):
    data_length = len(data.get((list(data.keys())[0]))[2]) - 1
    result_first = evaluateExpression(PMC_result[0], Storm_evaluation_parameter_set(data, 0))
    result_last = evaluateExpression(PMC_result[0], Storm_evaluation_parameter_set(data, -1))
    small_result, large_result = compareValue(result_last, result_first)
    if small_result >= req or req >= large_result:
        # print(data_length, req, small_result, large_result)
        return data_length, 0
    else:
        if large_result == result_last:
            i = 0
            j = data_length
            mid = 0
            while i < j:
                mid = (i + j) // 2
                # print(data_length, mid)
                if diff_value(mid, data_length) <= 1:
                    return mid, 1
                temp_var = evaluateExpression(PMC_result[0], Storm_evaluation_parameter_set(data, mid))
                if temp_var == req:
                    return mid, 1
                if req < temp_var:
                    if mid > 0 and req > evaluateExpression(PMC_result[0],
                                                            Storm_evaluation_parameter_set(data, mid - 1)):
                        return getClosest(
                            evaluateExpression(PMC_result[0], Storm_evaluation_parameter_set(data, mid - 1)), mid - 1,
                            temp_var, mid, req), 1
                    j = mid
                else:
                    if mid < data_length - 1 and req < evaluateExpression(PMC_result[0],
                                                                          Storm_evaluation_parameter_set(data,
                                                                                                         mid + 1)):
                        return getClosest(temp_var, mid, evaluateExpression(PMC_result[0],
                                                                            Storm_evaluation_parameter_set(data,
                                                                                                           mid + 1)),
                                          mid + 1, req), 1
                    i = mid + 1
        elif small_result == result_last:
            i = 0
            j = data_length
            mid = 0
            while i < j:
                mid = (i + j) // 2
                # print(data_length, mid)
                if diff_value(mid, data_length) <= 1:
                    return mid, 1
                temp_var = evaluateExpression(PMC_result[0], Storm_evaluation_parameter_set(data, mid))
                if temp_var == req:
                    return mid, 1
                if req > temp_var:
                    var1 = evaluateExpression(PMC_result[0], Storm_evaluation_parameter_set(data, mid - 1))
                    if mid > 0 and req < var1:
                        return getClosest(
                            evaluateExpression(PMC_result[0], Storm_evaluation_parameter_set(data, mid - 1)), mid - 1,
                            temp_var, mid, req), 1
                    j = mid
                else:
                    var2 = evaluateExpression(PMC_result[0], Storm_evaluation_parameter_set(data, mid + 1))
                    if mid < data_length - 1 and req > var2:
                        return getClosest(temp_var, mid, evaluateExpression(PMC_result[0],
                                                                            Storm_evaluation_parameter_set(data,
                                                                                                           mid + 1)),
                                          mid + 1, req), 1
                    i = mid + 1


def data_resize(data, idx):
    data_instance = dict()
    for i in data:
        temp = data[i]
        data_instance[i] = [temp[0][0:idx], temp[1][0:idx], temp[2][0:idx]]
    return data_instance


def lower_bound(x, l):
    if l[0] > x:
        return 0
    for i, y in enumerate(l):
        if y > x:
            return i


def system_level_eval_multiple(req, data, PMC_result):
    var = [1, 2, 3]
    data_length = []
    decision = []
    for i in var:
        data_length.append(system_level_prop_eval(data, req[i], PMC_result[i])[0])
        decision.append(system_level_prop_eval(data, req[i], PMC_result[i])[1])
    data_length = min(data_length)
    if sum(decision)>0:
        decision = 1
    else:
        decision = 0
    return data_length, decision


def BaselineSimulation(RunningPeriod, number_of_maintenance, PMC_result, application_domain, noise_level, req):
    maintenance_interval = int(RunningPeriod / (number_of_maintenance + 1))
    maintenance_idx_list = [0]
    no_service_flag = 0

    var = [1, 2, 3]
    pmc_exp = dict()
    model_parameters = set()
    model_parameter_rwd = set()
    model_parameter_prob = set()
    for i in var:
        pmc_exp[i] = PMC_result[i][0]
        model_parameter_rwd = model_parameter_rwd.union(PMC_result[i][3])
        model_parameters = model_parameters.union(PMC_result[i][1])
        model_parameter_prob = model_parameter_prob.union(PMC_result[i][2])

    if number_of_maintenance >= 1:
        for i in range(1, number_of_maintenance + 1):
            maintenance_idx_list.append(maintenance_interval * i)
        maintenance_idx_list.append(RunningPeriod)
    else:
        no_service_flag = 1
    counter = 0
    number_of_violation = 0
    while counter < RunningPeriod:
        print(counter)
        data, datasize = data_generator(model_parameter_prob, model_parameter_rwd, application_domain, noise_level, counter)
        # data, datasize = data_generator(PMC_result[2], PMC_result[3], application_domain, noise_level, counter)
        current_bound_idx = lower_bound(counter, maintenance_idx_list)

        if no_service_flag == 0 and counter + datasize > maintenance_idx_list[current_bound_idx]:
            data_before_fixed_service = maintenance_idx_list[current_bound_idx] - counter + 1
            resized_data = data_resize(data, data_before_fixed_service)
            data_length, decision = system_level_eval_multiple(req, resized_data, PMC_result)
            # data_length, decision = system_level_prop_eval(resized_data, req,PMC_result)
            if decision == 0:
                counter = counter + data_length
            else:
                counter = counter + data_length
                number_of_violation += 1
        else:
            # data_length, decision = system_level_prop_eval(data, req, PMC_result)
            data_length, decision = system_level_eval_multiple(req, data, PMC_result)
            if decision == 0:
                counter = counter + data_length
            else:
                counter = counter + data_length
                number_of_violation += 1
    return number_of_violation

