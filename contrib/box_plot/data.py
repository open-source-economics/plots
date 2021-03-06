from taxcalc import Policy, Records, Calculator
from taxcalc.utils import *
from taxcalc.records import Records
from taxcalc import Policy, Records, Calculator, Behavior, behavior, Growth

CURRENT_YEAR = 2017


def run_reform(name, reform, behave):

        puf = pd.read_csv("../tax-calculator/puf.csv")
        policy_base = Policy(start_year=2013)
        records_base = Records(puf)
        policy_reform = Policy()
        records_reform = Records(puf)
        bhv = Behavior()
        calcbase = Calculator(policy = policy_base, records = records_base)
        calcreform = Calculator(policy = policy_reform, records = records_reform, behavior = bhv)
        policy_reform.implement_reform(reform)
        calcbase.advance_to_year(CURRENT_YEAR)
        calcreform.advance_to_year(CURRENT_YEAR)
        calcbase.calc_all()
        calcreform.calc_all()
        bhv.update_behavior(behave)
        calc_behav = Behavior.response(calcbase, calcreform)
        calc_behav.calc_all()
        base_list = multiyear_diagnostic_table(calcbase, 10)
        reform_list = multiyear_diagnostic_table(calc_behav, 10)
        difflist = (reform_list.iloc[18] - base_list.iloc[18])

        return difflist


def get_source_data():
        behavioral_values = (0, -3.49)
        behavioral_inc_values = (0, 0.25,0.4, 0.55, 1.09)
        groups_ref = {}
        groups_grow = {}
        groups_beha = {}
        for j in range(5):
            for k in range(2):
                reform_be = {CURRENT_YEAR: {'_BE_cg': [behavioral_values[k]],
                                             '_BE_sub': [behavioral_inc_values[j]]}}
                groups_beha[''.join([str(k), str(j)])] = reform_be
        dataframes = {}
        for name, behave in groups_beha.items():
            data = run_reform(name, reform, behave)
            dataframes[name] = data
        return dataframes

reform = {CURRENT_YEAR: {
                        '_AGI_surtax_thd': [[5000000, 5000000, 5000000, 5000000, 5000000, 5000000]],
                        '_AGI_surtax_trt': [0.04]}}

dumm = get_source_data()
df = pd.DataFrame.from_dict(dumm, orient='columns', dtype=None)
df.to_csv('data.csv')