import sys
import params


if len(sys.argv) > 1:
    activity = int(sys.argv[1])
    CDR = float(sys.argv[2])
    N = int(sys.argv[3])

#adjust parameters

if CDR == 0:
    params.W = 3
    params.Ps = 0
    params.similarity = -1
    params.utility_success = 1
    params.utility_fail = 0
elif CDR == 0.5:  ## MCI
    params.W = 1.45
    params.Ps = 1
    params.similarity = -0.1
    params.utility_success = 0.8
    params.utility_fail = 1 - params.utility_success
elif CDR == 1:  ## MILD DEMENTIA
    params.W = 1.285
    params.Ps = 1
    params.similarity = -0.1
    params.utility_success = 0.62
    params.utility_fail = 1 - params.utility_success
elif CDR == 2:  ## MODERATE DEMENTIA
    params.W = 1.08
    params.Ps = 1
    params.similarity = -0.1
    params.utility_success = 0.475
    params.utility_fail = 1 - params.utility_success
elif CDR == 3:
    params.W = 1.035
    params.Ps = 1
    params.similarity = -0.1
    params.utility_success = 0.3
    params.utility_fail = 1 - params.utility_success


if activity == 1:
    params.CDR = CDR
    params.N = N

    print "Activity chosen: TEA PREPARATION"
    print "Level of dementia: CDR-%.1f" % CDR
    print "Run for", N, "people."

    execfile('tea_experiment.py')

elif activity == 2:
    params.CDR = CDR
    params.N = N

    print "Activity chosen: WASHING HANDS"
    print "Level of dementia: CDR-%.1f" % CDR
    print "Run for", N, "people."

    execfile('washing_experiment.py')

elif activity == 3:
    params.CDR = CDR
    params.N = N

    print "Activity chosen: DRESSING"
    print "Level of dementia: CDR-%.1f" % CDR
    print "Run for", N, "people."

    execfile('dressing_experiment.py')
