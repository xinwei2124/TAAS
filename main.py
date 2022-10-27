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
    gate = 10

    # model_path = "/Users/xinweifang/Documents/PRESTO/simplifiedRAD/RAD_model_modified.pm"
    # prop1 = "P =? [F \"complete\" ]"
    # prop2 = "P=? [ !\"correction\" U \"complete\" ]"
    # prop3 = "R{\"totalTime\"}=? [ F \"end\" ]"
    # R1 = 0.75
    # R2 = 0.6
    # R3 = 38
    # application = "RAD"
    # gate = 5

    noise = 0

    prediction_horizon = 1000

    # Epsilon_range = [1, 2, 3]
    # Updating_N_range = [400]
    # psi_threshold_range = [100]

    # Updating_N_range = [50, 100, 200, 400, 600, 800, 1000, 1200]
    # psi_threshold_range = [50, 100, 200, 400, 600, 800, 1000, 1200]

    Updating_N_range = [50]
    psi_threshold_range = [100]

    pmc_result = dict()
    requirement = dict()
    prop_name = [1, 2, 3]
    # for Epsilong_loop in Epsilon_range:
    #     if Epsilong_loop == 1:
    #         Epsilon = 0.01
    #     elif Epsilong_loop == 2:
    #         Epsilon = 0.05
    #     elif Epsilong_loop == 3:
    #         Epsilon = 0.1
    Epsilon = 0
    for Updating_N in Updating_N_range:
        for psi_threshold in psi_threshold_range:
            Line_fit_data_size = Updating_N
            trigger_value = psi_threshold
            for i in prop_name:
                pmc_result[i] = parametric_model_checking(model_path, eval(f"prop{i}"))
                requirement[i] = eval(f"R{i}")

            number_of_maintenance = 1
            number_of_runs = 20

            Matrix = [[0 for x in range(number_of_runs)] for y in range(number_of_maintenance)]
            PRESTO_low_cost = [[0 for x in range(number_of_runs)] for y in range(number_of_maintenance)]
            PRESTO_high_cost = [[0 for x in range(number_of_runs)] for y in range(number_of_maintenance)]

            for n in range(0, number_of_maintenance):
                number_service = n * gate
                for repeat in range(0, number_of_runs):
                    print(Epsilon, repeat)
                    # print(repeat)
                    Random_seed_idx = int(n + 1 * repeat + 1)
                    Matrix[n][repeat] = BaselineSimulation(43200, number_service, pmc_result, application, noise,
                                                           requirement, Random_seed_idx)
                    TP, FN, FP, service = PRESTOSimulation(43200, number_service, pmc_result, application, noise,
                                                           requirement, Epsilon, Updating_N, Line_fit_data_size,
                                                           psi_threshold, trigger_value, Random_seed_idx)
                    PRESTO_low_cost[n][repeat] = TP + FP + service
                    PRESTO_high_cost[n][repeat] = FN
            # print(Matrix, TP, FN, FP, service)
            a = np.asarray(Matrix)
            b = np.asarray(PRESTO_low_cost)
            c = np.asarray(PRESTO_high_cost)
            # np.savetxt(f"/Users/xinweifang/Documents/PRESTO/new_plot/RQ2/FruitPicking/refined/Matrix_noise1.csv", a,
            #            delimiter=",", fmt='%d')
            # np.savetxt(f"/Users/xinweifang/Documents/PRESTO/new_plot/RQ2/FruitPicking/refined/PRESTO_low_cost_noise1.csv", b,
            #            delimiter=",", fmt='%d')
            # np.savetxt(f"/Users/xinweifang/Documents/PRESTO/new_plot/RQ2/FruitPicking/refined/PRESTO_high_cost_noise1.csv", c,
            #            delimiter=",", fmt='%d')
            np.savetxt(
                f"/Users/xinweifang/Documents/PRESTO/new_plot/RQ3/FruitPicking/refined/test/Matrix_{Updating_N}_{psi_threshold}.csv",
                a,
                delimiter=",", fmt='%d')
            np.savetxt(
                f"/Users/xinweifang/Documents/PRESTO/new_plot/RQ3/FruitPicking/refined/test/PRESTO_low_cost_{Updating_N}_{psi_threshold}.csv",
                b,
                delimiter=",", fmt='%d')
            np.savetxt(
                f"/Users/xinweifang/Documents/PRESTO/new_plot/RQ3/FruitPicking/refined/test/PRESTO_high_cost_{Updating_N}_{psi_threshold}.csv",
                c,
                delimiter=",", fmt='%d')
    # model_path = "/Users/xinweifang/Documents/PRESTO/simplifiedRAD/RAD_model_modified.pm"
    # prop1 = "P =? [F \"complete\" ]"
    # prop2 = "P=? [ !\"correction\" U \"complete\" ]"
    # prop3 = "R{\"totalTime\"}=? [ F \"end\" ]"
    # R1 = 0.75
    # R2 = 0.6
    # R3 = 38
    # application = "RAD"
    # gate = 5
    #
    # noise = 0
    #
    # prediction_horizon = 1000
    #
    # Epsilon_range = [1, 2, 3]
    #
    # # Updating_N_range = [400]
    # # psi_threshold_range = [100]
    #
    # Updating_N_range = [50, 100, 200, 400, 600, 800, 1000, 1200]
    # psi_threshold_range = [50, 100, 200, 400, 600, 800, 1000, 1200]
    #
    # pmc_result = dict()
    # requirement = dict()
    # prop_name = [1, 2, 3]
    # for Epsilong_loop in Epsilon_range:
    #     if Epsilong_loop == 1:
    #         Epsilon = 0.1
    #     elif Epsilong_loop == 2:
    #         Epsilon = 0.2
    #     elif Epsilong_loop == 3:
    #         Epsilon = 0.3
    #     for Updating_N in Updating_N_range:
    #         for psi_threshold in psi_threshold_range:
    #             Line_fit_data_size = Updating_N
    #             trigger_value = psi_threshold
    #             for i in prop_name:
    #                 pmc_result[i] = parametric_model_checking(model_path, eval(f"prop{i}"))
    #                 requirement[i] = eval(f"R{i}")
    #
    #             number_of_maintenance = 1
    #             number_of_runs = 20
    #
    #             Matrix = [[0 for x in range(number_of_runs)] for y in range(number_of_maintenance)]
    #             PRESTO_low_cost = [[0 for x in range(number_of_runs)] for y in range(number_of_maintenance)]
    #             PRESTO_high_cost = [[0 for x in range(number_of_runs)] for y in range(number_of_maintenance)]
    #
    #             for n in range(0, number_of_maintenance):
    #                 number_service = n * gate
    #                 print(Epsilong_loop,Updating_N)
    #                 for repeat in range(0, number_of_runs):
    #                     # print(repeat)
    #                     Random_seed_idx = int(n + 1 * repeat + 1)
    #                     Matrix[n][repeat] = BaselineSimulation(43200, number_service, pmc_result, application, noise,
    #                                                            requirement, Random_seed_idx)
    #                     TP, FN, FP, service = PRESTOSimulation(43200, number_service, pmc_result, application, noise,
    #                                                            requirement, Epsilon, Updating_N, Line_fit_data_size,
    #                                                            psi_threshold, trigger_value, Random_seed_idx)
    #                     PRESTO_low_cost[n][repeat] = TP + FP + service
    #                     PRESTO_high_cost[n][repeat] = FN
    #             # print(Matrix, TP, FN, FP, service)
    #             a = np.asarray(Matrix)
    #             b = np.asarray(PRESTO_low_cost)
    #             c = np.asarray(PRESTO_high_cost)
    #             np.savetxt(
    #                 f"/Users/xinweifang/Documents/PRESTO/new_plot/RQ3/RAD/refined/Eps{Epsilong_loop}/Matrix_{Updating_N}_{psi_threshold}.csv",
    #                 a,
    #                 delimiter=",", fmt='%d')
    #             np.savetxt(
    #                 f"/Users/xinweifang/Documents/PRESTO/new_plot/RQ3/RAD/refined/Eps{Epsilong_loop}/PRESTO_low_cost_{Updating_N}_{psi_threshold}.csv",
    #                 b,
    #                 delimiter=",", fmt='%d')
    #             np.savetxt(
    #                 f"/Users/xinweifang/Documents/PRESTO/new_plot/RQ3/RAD/refined/Eps{Epsilong_loop}/PRESTO_high_cost_{Updating_N}_{psi_threshold}.csv",
    #                 c,
    #                 delimiter=",", fmt='%d')
