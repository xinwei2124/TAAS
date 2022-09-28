from PMC import *
from dataSimulator import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    model_path = "/Users/xinweifang/Documents/PRESTO/simplifiedRAD/RAD_model_modified.pm"
    prop = "R{\"totalTime\"}=? [ F \"end\" ]"

    pmc_exp, pmc_param_all, pmc_param_prob, pmc_param_reward = parametric_model_checking(model_path, prop)

    data = data_generator(pmc_param_prob, pmc_param_reward, "RAD", 1)

    print("xinwei")

    print("xinwei")
