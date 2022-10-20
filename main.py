from PMC import *
from dataSimulator import *
from baseline import *
from PRESTO_simulation import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    model_path = "/Users/xinweifang/Documents/PRESTO/SEAM_example/Example.pm"
    prop1 = "P=?[F s=4]"
    prop2 = "R{\"totalTime\"}=?[F s=5]"
    prop3 = "R{\"totalCost\"}=?[F s=5]"
    R1 = 0.8
    R2 = 5
    R3 = 5
    application = "fruit-picking"

    # model_path = "/Users/xinweifang/Documents/PRESTO/simplifiedRAD/RAD_model_modified.pm"
    # prop1 = "P =? [F \"complete\" ]"
    # prop2 = "P=? [ !\"correction\" U \"complete\" ]"
    # prop3 = "R{\"totalTime\"}=? [ F \"end\" ]"
    # R1 = 0.75
    # R2 = 0.6
    # R3 = 38
    # application = "RAD"

    noise = 0

    prediction_horizon = 1000
    Updating_N = 400
    Line_fit_data_size = Updating_N
    Epsilon = 0
    psi_threshold = 100
    trigger_value = psi_threshold

    pmc_result = dict()
    requirement = dict()
    prop_name = [1, 2, 3]

    for i in prop_name:
        pmc_result[i] = parametric_model_checking(model_path, eval(f"prop{i}"))
        requirement[i] = eval(f"R{i}")


    # TP, FN, FP = PRESTOSimulation(43200, prediction_horizon, Updating_N, Line_fit_data_size, Epsilon, pmc_result,
    #                               application, noise, requirement, psi_threshold, trigger_value)
    # print(TP, FN, FP)



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
