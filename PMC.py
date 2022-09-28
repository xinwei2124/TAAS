import stormpy.info
import pycarl
import stormpy._config as config


def parametric_model_checking(path, formula_str):
    # Check support for parameters
    if not config.storm_with_pars:
        print("Support parameters is missing. Try building storm-pars.")
        return

    import stormpy.pars
    from pycarl.formula import FormulaType, Relation
    if stormpy.info.storm_ratfunc_use_cln():
        import pycarl.cln.formula
    else:
        import pycarl.gmp.formula

    prism_program = stormpy.parse_prism_program(path)
    properties = stormpy.parse_properties_for_prism_program(formula_str, prism_program)
    model = stormpy.build_parametric_model(prism_program, properties)

    initial_state = model.initial_states[0]
    result = stormpy.model_checking(model, properties[0])
    parameters = model.collect_all_parameters()
    return result.at(initial_state), parameters, model.collect_probability_parameters(), model.collect_reward_parameters()
