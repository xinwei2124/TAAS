from PMC import *
from dataSimulator import *
from baseline import *
from PRESTO_simulation import *


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # model_path = "/Users/xinweifang/Documents/PRESTO/simplifiedRAD/RAD_model_modified.pm"
    # # prop = "R{\"totalTime\"}=? [ F \"end\" ]"
    # # prop = "P =? [F \"complete\" ]"
    # #
    # prop = "P=? [ !\"correction\" U \"complete\" ]"
    # # requirement = 0.75
    # requirement = 0.6
    # # requirement = 38
    # application = "RAD"

    model_path = "/Users/xinweifang/Documents/PRESTO/SEAM_example/Example.pm"
    prop ="P=?[F s=4]"
    # prop ="R{\"totalTime\"}=?[F s=5]"
    # prop = "R{\"totalCost\"}=?[F s=5]"
    requirement = 0.8
    # requirement = 5
    application = "fruit-picking"
    noise = 0

    prediction_horizon = 1000
    Updating_N = 400
    Line_fit_data_size = Updating_N
    Epsilon = 0.5
    psi_threshold = 500
    trigger_value = psi_threshold

    pmc_result = dict()


    # pmc_exp, pmc_param_all, pmc_param_prob, pmc_param_reward = parametric_model_checking(model_path, prop)
    pmc_result = parametric_model_checking(model_path, prop)
    # data = data_generator(pmc_result[2], pmc_result[3], "RAD", 1)

    TP, FN, FP = PRESTOSimulation(43200, prediction_horizon, Updating_N, Line_fit_data_size, Epsilon, pmc_result,
                     application, noise, requirement, psi_threshold, trigger_value)
    print(TP, FN, FP)

    number_of_maintenance = 1
    number_of_runs = 1

    Matrix = [[0 for x in range(number_of_runs)] for y in range(number_of_maintenance)]
    for n in range(0, number_of_maintenance):
        print(n)
        for repeat in range(0, number_of_runs):
            print(repeat)
            Matrix[n][repeat] = BaselineSimulation(43200, n, pmc_result, application, noise, requirement)

    print(Matrix)
    a = np.asarray(Matrix)


