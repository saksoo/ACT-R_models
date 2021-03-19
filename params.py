# configuration parameters of the experiment
# run the experiment for N people and for d level of dementia

CDR = 1
N = 1


# common parameters for all levels of AD
e_chunk_activation_transitory_noise = 0.4
S_chunk_strength_of_association = 2
e_production_utility_transitory_noise = 0.15

#initiate parameters
W = 3
Ps = 0
similarity = -1
utility_success = 1
utility_fail = 0

physical_factor = 0.0
verbal_factor = 0.0

# for different dementia levels

if CDR == 0:
    W = 3
    Ps = 0
    similarity = -1
    utility_success = 1
    utility_fail = 0

elif CDR == 0.5: ## MCI
    W = 1.45
    Ps = 1
    similarity = -0.1
    utility_success = 0.8
    utility_fail = 1 - utility_success

elif CDR == 1:  ## MILD DEMENTIA
    W = 1.285
    Ps = 1
    similarity = -0.1
    utility_success = 0.62
    utility_fail = 1 - utility_success

elif CDR == 2: ## MODERATE DEMENTIA
    W = 1.08
    Ps = 1
    similarity = -0.1
    utility_success = 0.475
    utility_fail = 1 - utility_success

elif CDR == 3:
    W = 1.035
    Ps = 1
    similarity = -0.1
    utility_success = 0.3
    utility_fail = 1 - utility_success

