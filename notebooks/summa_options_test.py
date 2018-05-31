import summa_plot as sp
import pysumma.Simulation
import importlib
import time
importlib.reload(pysumma.Simulation)

sites = ['Amplero', 'Blodgett', 'Bugac', 'ElSaler', 'ElSaler2', 'Espirra', 'FortPeck', 
         'Harvard', 'Hesse', 'Howard', 'Howlandm', 'Hyytiala', 'Kruger', 'Loobos', 'Merbleue',
         'Mopane', 'Palang', 'Sylvania', 'Tumba', 'UniMich']
fman_template = "/pool0/data/tushark/PLUMBER_data/sites/{}/settings/summa_zFileManager_{}.txt"
fman_dict = {s: fman_template.format(s, s) for s in sites}

def run_summa(site, decision, option):
    s = pysumma.Simulation.Simulation(fman_dict[site])
    s.decision_obj.decision.value = option
    s.executable = '/opt/local/bin/summa.exe'
    s.library_path = '/opt/local/lib:/opt/local/lib64:$LD_LIBRARY_PATH'
    additional_args = ['export OMP_NUM_THREADS=8']
    return s.execute(decision + '_' + option, 'local', additional_args)

def monitor(proc):
    while proc.poll() is not None:
        time.sleep(1)
    return proc.stdout.read(), proc.stderr.read()
    
summa_options = {
    0: {'stomResist': ['value', 'BallBerry', 'Jarvis', 'simpleResistance', 'BallBerryFlex', 
                   'BallBerryTest']},
    'groundwatr': ['qTopmodl', 'bigBuckt', 'noXplict'],
    'hc_profile': ['constant', 'pow_prof'],
    'thCondSoil': ['funcSoilWet', 'mixConstit', 'hanssonVZ'],
    'canopySrad': ['noah_mp', 'CLM_2stream', 'UEB_2stream', 'NL_scatter', 'BeersLaw']
}

# this nested loop would test each of the options independently.
# I'm not sure whether there is a better way to do this using pysumma
for site in sites:
    for decision in summa_options:
        for options in summa_options[decision]:
            run_summa(site, decision, option)

'''
# this is a loop to run combinations of all decision. Again, there
# is probably a better way
for site in sites:
    for 

def run_options(summa_options)
    run_decisions = {}
    for decision in summa_options:
        run_decisions[decision:'']
        
    

# helper
def recursive_helper(run_decisions):
    s = pysumma.Simulation.Simulation(fman_dict[site])
    for decision in run_decisions:
        s.decision_obj.decision.value = run_decisions[decision]
    s.executable = '/opt/local/bin/summa.exe'
    s.library_path = '/opt/local/lib:/opt/local/lib64:$LD_LIBRARY_PATH'
    additional_args = ['export OMP_NUM_THREADS=8']
    return s.execute(NEED_NAMING_CONVENTION, 'local', additional_args)
    
'''

def run_combinations(dataframe, sites):
    '''
    This function takes a dataframe with summa
    decision points as column names, and with each
    row representing a summa run with the appropriate
    decision options
    It also takes an array_like object sites which just
    lists the names of the sites for which each summa
    combination should be run at.
    '''
    # assuming we want to run all sites
    # another option would be to have a column in the 
    # dataframe representing the site for each run
    for site in sites:
        
        # set up a simulation object for the site
        s = pysumma.Simulation.Simulation(fman_dict[site])
        s.executable = '/opt/local/bin/summa.exe'
        s.library_path = '/opt/local/lib:/opt/local/lib64:$LD_LIBRARY_PATH'
        additional_args = ['export OMP_NUM_THREADS=8']
        
        # for each option combination, set the appropriate
        # values in the decision object, then run
        for index in dataframe.index.values:
            for decision in dataframe.columns.values:
                s.decision_obj.decision.value = dataframe[decision][index]
                
                # need naming convention for output files
                s.execute('test_run_' + index, 'local', additional_args)
                

