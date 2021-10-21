from __future__ import division
import numpy as np
from statistics_parsers import get_statistics_tea
import params
import pandas as pd
import matplotlib.pyplot as plt


N = params.N

if N == 1:  #for 1 subject we count all the problems -- sum

    init_problems_all = 0
    init_problems_all_verbal_help = 0
    init_problems_all_physical_help = 0
    init_problems_all_incapable = 0

    org_problems_all = 0
    org_problems_all_verbal_help = 0
    org_problems_all_physical_help = 0
    org_problems_all_incapable = 0

    seq_problems_all = 0
    seq_problems_all_verbal_help = 0
    seq_problems_all_physical_help = 0
    seq_problems_all_incapable = 0

    saf_problems_all = 0
    saf_problems_all_verbal_help = 0
    saf_problems_all_physical_help = 0
    saf_problems_all_incapable = 0

    comp_problems_all = 0
    comp_problems_all_verbal_help = 0
    comp_problems_all_physical_help = 0
    comp_problems_all_incapable = 0

    # for 1 subject we also generate the KTA score
    ## KTA ##

    kta_init = 0
    kta_org  = 0
    kta_seq  = 0
    kta_saf  = 0
    kta_comp  = 0
    performance_all_steps = 0

    ## KTA ###

    execfile("tea_model.py")
    result_one = get_statistics_tea()

    # count ALL problems and print results

    init_problems_all += result_one['Initiation problems']
    init_problems_all_verbal_help += result_one['Initiation problems verbal help']
    init_problems_all_physical_help += result_one['Initiation problems physical help']
    init_problems_all_incapable += result_one['Initiation problems incapable']

    org_problems_all += result_one['Organization problems']
    org_problems_all_verbal_help += result_one['Organization problems verbal help']
    org_problems_all_physical_help += result_one['Organization problems physical help']
    org_problems_all_incapable += result_one['Organization problems incapable']

    seq_problems_all += result_one['Sequencing problems']
    seq_problems_all_verbal_help += result_one['Sequencing problems verbal help']
    seq_problems_all_physical_help += result_one['Sequencing problems physical help']
    seq_problems_all_incapable += result_one['Sequencing problems incapable']

    saf_problems_all += result_one['Safety problems']
    saf_problems_all_verbal_help += result_one['Safety problems verbal help']
    saf_problems_all_physical_help += result_one['Safety problems physical help']
    saf_problems_all_incapable += result_one['Safety problems incapable']

    comp_problems_all += result_one['Completion problems']
    comp_problems_all_verbal_help += result_one['Completion problems verbal help']
    comp_problems_all_physical_help += result_one['Completion problems physical help']
    comp_problems_all_incapable += result_one['Completion problems incapable']

    # count KTA score and print it
    # we count for each person how much help they got

    if result_one['Initiation problems incapable'] > 0:
        kta_init = 3
    elif result_one['Initiation problems physical help'] > 0:
        kta_init = 2
    elif result_one['Initiation problems verbal help'] > 0:
        kta_init = 1

    if result_one['Organization problems incapable'] > 0:
        kta_org = 3
    elif result_one['Organization problems physical help'] > 0:
        kta_org = 2
    elif result_one['Organization problems verbal help'] > 0:
        kta_org = 1

    if result_one['Sequencing problems incapable'] > 0:
        kta_seq = 3
    elif result_one['Sequencing problems physical help'] > 0:
        kta_seq = 2
    elif result_one['Sequencing problems verbal help'] > 0:
        kta_seq = 1

    if result_one['Safety problems incapable'] > 0:
        kta_saf = 3
    elif result_one['Safety problems physical help'] > 0:
        kta_saf = 2
    elif result_one['Safety problems verbal help'] > 0:
        kta_saf = 1

    if result_one['Completion problems incapable'] > 0:
        kta_comp = 3
    elif result_one['Completion problems physical help'] > 0:
        kta_comp = 2
    elif result_one['Completion problems verbal help'] > 0:
        kta_comp = 1

    performance_all_steps = result_one['Performance all steps']

    ## Extra memory statistics for 1 subject

    forget_problems_all = result_one['Forget']
    conf_sim_problems_all = result_one['Confused similarity']
    conf_other_chunk_problems_all = result_one['Confused other']
    ##################

    print "This experiment is run for 1 subject!"
    print "Total initiation errors: ", init_problems_all
    print "Total initiation errors verbal help: ", init_problems_all_verbal_help
    print "Total initiation errors physical help: ", init_problems_all_physical_help
    print "Total initiation errors incapable: ", init_problems_all_incapable

    print "Total Organization errors: ", org_problems_all
    print "Total Organization errors verbal help: ", org_problems_all_verbal_help
    print "Total Organization errors physical help: ",org_problems_all_physical_help
    print "Total Organization errors incapable: ", org_problems_all_incapable

    print "Total Sequencing errors: ", seq_problems_all
    print "Total Sequencing errors verbal help: ", seq_problems_all_verbal_help
    print "Total Sequencing errors physical help: ", seq_problems_all_physical_help
    print "Total Sequencing errors incapable: ", seq_problems_all_incapable

    print "Total Safety errors: ", saf_problems_all
    print "Total Safety errors verbal help: ", saf_problems_all_verbal_help
    print "Total Safety errors physical help: ", saf_problems_all_physical_help
    print "Total Safety errors incapable: ", saf_problems_all_incapable

    print "Total Completion errors: ", comp_problems_all
    print "Total Completion errors verbal help: ", comp_problems_all_verbal_help
    print "Total Completion errors physical help: ", comp_problems_all_physical_help
    print "Total Completion errors incapable: ", comp_problems_all_incapable

    print "#########         KTA test score: \n"

    print "KTA INITIATION: ", kta_init
    print "KTA ORGANIZATION: ", kta_org
    print "KTA ALL STEPS: ", performance_all_steps
    print "KTA SEQUENCE: ", kta_seq
    print "KTA SAFETY: ", kta_saf
    print "KTA COMPLETION: ", kta_comp

    print "KTA FINAL SCORE: ", kta_init + kta_org + performance_all_steps + kta_seq + kta_saf + kta_comp

    ## print extra memory statistics
    print "Total FORGET errors: ", forget_problems_all
    print "Total CONFUSION ERRORS WITH SIMILARITY: ", conf_sim_problems_all
    print "Total CONFUSION ERRORS WITH OTHERS: ", conf_other_chunk_problems_all


else:

    kta_list_all_subjects = list()

    init_problems_all = 0  #only 1 initiation problem so we use the same variable
    init_problems_all_verbal_help = 0
    init_problems_all_physical_help = 0
    init_problems_all_incapable = 0

    org_problems_all_at_least_one = 0  #if the subject made at least 1 error we count it as 1
    org_problems_all_at_least_one_verbal = 0
    org_problems_all_at_least_one_physical = 0
    org_problems_all_at_least_one_incapable = 0

    seq_problems_all_at_least_one = 0  #if the subject made at least 1 error we count it as 1
    seq_problems_all_at_least_one_verbal = 0
    seq_problems_all_at_least_one_physical = 0
    seq_problems_all_at_least_one_incapable = 0

    saf_problems_all_at_least_one = 0  #if the subject made at least 1 error we count it as 1
    saf_problems_all_at_least_one_verbal = 0
    saf_problems_all_at_least_one_physical = 0
    saf_problems_all_at_least_one_incapable = 0

    comp_problems_all = 0  #only 1 completion problem so we use the same variable
    comp_problems_all_verbal_help = 0
    comp_problems_all_physical_help = 0
    comp_problems_all_incapable = 0

    #keep real number of maximun and minimum number of help required:
    all_problems = np.zeros((0, 20), dtype=int)
    # print (all_problems)

    for i in range(0, N):

        ## KTA ##
        kta_init = 0
        kta_org = 0
        kta_seq = 0
        kta_saf = 0
        kta_comp = 0
        performance_all_steps = 0
        kta_score = 0
        ## KTA ###

        execfile("tea_model.py")
        result_one = get_statistics_tea()

        #create a numpy table to keep all info about each problem category
        row = [result_one['Initiation problems'], result_one['Initiation problems verbal help'], result_one['Initiation problems physical help'], result_one['Initiation problems incapable'],
               result_one['Organization problems'], result_one['Organization problems verbal help'], result_one['Organization problems physical help'], result_one['Organization problems incapable'],
               result_one['Sequencing problems'], result_one['Sequencing problems verbal help'], result_one['Sequencing problems physical help'], result_one['Sequencing problems incapable'],
               result_one['Safety problems'], result_one['Safety problems verbal help'], result_one['Safety problems physical help'], result_one['Safety problems incapable'], result_one['Completion problems'],
               result_one['Completion problems verbal help'], result_one['Completion problems physical help'], result_one['Completion problems incapable']]
        all_problems = np.vstack([all_problems, row])

        # we count for each person how much help they got
        if result_one['Initiation problems'] > 0:
            init_problems_all += 1
        if result_one['Initiation problems incapable'] > 0:
            init_problems_all_incapable += 1
            kta_init = 3
        elif result_one['Initiation problems physical help'] > 0:
            init_problems_all_physical_help += 1
            kta_init = 2
        elif result_one['Initiation problems verbal help'] > 0:
            init_problems_all_verbal_help += 1
            kta_init = 1

        # we count for each person how much help they got
        if result_one['Organization problems'] > 0:
            org_problems_all_at_least_one += 1
        if result_one['Organization problems incapable'] > 0:
            org_problems_all_at_least_one_incapable += 1
            kta_org = 3
        elif result_one['Organization problems physical help'] > 0:
            org_problems_all_at_least_one_physical += 1
            kta_org = 2
        elif result_one['Organization problems verbal help'] > 0:
            org_problems_all_at_least_one_verbal += 1
            kta_org = 1

        if result_one['Sequencing problems'] > 0: ## an kapoios pire polles voithies metrame mono tis megaluteres.
            seq_problems_all_at_least_one += 1
        if result_one['Sequencing problems incapable'] > 0:
            seq_problems_all_at_least_one_incapable += 1
            kta_seq = 3
        elif result_one['Sequencing problems physical help'] > 0:
            seq_problems_all_at_least_one_physical += 1
            kta_seq = 2
        elif result_one['Sequencing problems verbal help'] > 0:
            seq_problems_all_at_least_one_verbal += 1
            kta_seq = 1

        if result_one['Safety problems'] > 0:  ## an kapoios pire polles voithies metrame mono tis megaluteres.
            saf_problems_all_at_least_one += 1
        if result_one['Safety problems incapable'] > 0:
            saf_problems_all_at_least_one_incapable += 1
            kta_saf = 3
        elif result_one['Safety problems physical help'] > 0:
            saf_problems_all_at_least_one_physical += 1
            kta_saf = 2
        elif result_one['Safety problems verbal help'] > 0:
            saf_problems_all_at_least_one_verbal += 1
            kta_saf = 1

        if result_one['Completion problems'] > 0:  ## an kapoios pire polles voithies metrame mono tis megaluteres.
            comp_problems_all += 1
        if result_one['Completion problems incapable'] > 0:
            comp_problems_all_incapable += 1
            kta_comp = 3
        elif result_one['Completion problems physical help'] > 0:
            comp_problems_all_physical_help += 1
            kta_comp = 2
        elif result_one['Completion problems verbal help'] > 0:
            comp_problems_all_verbal_help += 1
            kta_comp = 1

        performance_all_steps = result_one['Performance all steps']
        kta_score = kta_init + kta_org + performance_all_steps + kta_seq + kta_saf + kta_comp
        kta_list_all_subjects.append(kta_score)

    print "This experiment run for: ", N, "people!\n"
    print "Initiation: Independent  people are: ", N - init_problems_all
    print "Total initiation errors by ", N, "people are: ", init_problems_all
    print "Total initiation errors verbal help by ", N, "people are: ", init_problems_all_verbal_help
    print "Total initiation errors physical help by ", N, "people are: ", init_problems_all_physical_help
    print "Total initiation errors incapable by ", N, "people are: ", init_problems_all_incapable

    print "Organization: Independent people are: ", N - org_problems_all_at_least_one
    print "Total Organization errors by ", N, "people are: ",  org_problems_all_at_least_one
    print "Total Organization errors verbal help by ", N, "people are: ",  org_problems_all_at_least_one_verbal
    print "Total Organization errors physical help by ", N, "people are: ",  org_problems_all_at_least_one_physical
    print "Total Organization errors incapable by ", N, "people are: ",  org_problems_all_at_least_one_incapable

    print "Sequencing: Independent people are: ", N - seq_problems_all_at_least_one
    print "Total Sequencing errors by ", N, "people are: ", seq_problems_all_at_least_one
    print "Total Sequencing errors verbal help by ", N, "people are: ", seq_problems_all_at_least_one_verbal
    print "Total Sequencing errors physical help by ", N, "people are: ", seq_problems_all_at_least_one_physical
    print "Total Sequencing errors incapable by ", N, "people are: ", seq_problems_all_at_least_one_incapable

    print "Safety: Independent people are: ", N - saf_problems_all_at_least_one
    print "Total Safety errors by ", N, "people are: ", saf_problems_all_at_least_one
    print "Total Safety errors verbal help by ", N, "people are: ", saf_problems_all_at_least_one_verbal
    print "Total Safety errors physical help by ", N, "people are: ", saf_problems_all_at_least_one_physical
    print "Total Safety errors incapable by ", N, "people are: ", saf_problems_all_at_least_one_incapable

    print "Completion: Independent  people are: ", N - comp_problems_all
    print "Total Completion errors by ", N, "people are: ", comp_problems_all
    print "Total Completion errors verbal help by ", N, "people are: ", comp_problems_all_verbal_help
    print "Total Completion errors physical help by ", N, "people are: ", comp_problems_all_physical_help
    print "Total Completion errors incapable by ", N, "people are: ", comp_problems_all_incapable

    print "The mean KTA by ", N, "people is: ", np.mean(kta_list_all_subjects)
    print "The SD KTA by ", N, "people is: ",   np.std(kta_list_all_subjects, ddof=0)

    #plot the results
    data = [
        ['Initiation', N - init_problems_all, init_problems_all_verbal_help, init_problems_all_physical_help, init_problems_all_incapable],
        ['Organization',  N - org_problems_all_at_least_one, org_problems_all_at_least_one_verbal, org_problems_all_at_least_one_physical, org_problems_all_at_least_one_incapable],
        ['Sequencing',  N - seq_problems_all_at_least_one, seq_problems_all_at_least_one_verbal, seq_problems_all_at_least_one_physical, seq_problems_all_at_least_one_incapable],
        ['Safety',  N - saf_problems_all_at_least_one, saf_problems_all_at_least_one_verbal, saf_problems_all_at_least_one_physical, saf_problems_all_at_least_one_incapable],
        ['Completion',  N - comp_problems_all, comp_problems_all_verbal_help, comp_problems_all_physical_help, comp_problems_all_incapable]
    ]

    #Parameters for the font of the figure
    plt.rcParams["figure.figsize"] = (15, 9)
    plt.rcParams.update({'font.size': 30})
    #plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"] # use this to default the settings

    df = pd.DataFrame(data, columns=['Criteria', 'Independent', 'Verbal help', 'Physical Help', 'Incapable'])
    ### When the SD of the KTA is > 2 we add a N=2 error in the Y bar. We want the score to be as accurate as possible
    if np.std(kta_list_all_subjects, ddof=0) >= 2:
        error_factor = 2
    else:
        error_factor = 0
    ###

    df.plot(kind='bar', yerr=error_factor)
    plt.xlabel("")
    plt.ylabel("#Subjects")

    # Text above the figure
    texttodisplay = 'MEAN KTA: ' + str(np.mean(kta_list_all_subjects)) + '\n' + 'SD KTA: ' + str(np.std(kta_list_all_subjects, ddof=0))
    plt.text(0.6, error_factor+N+3, texttodisplay)    # Create names # second parameter moves the text above


    xbars = ('Initiation', 'Organization', 'Sequencing', 'Safety', 'Completion')
    x_pos = np.arange(len(xbars))
    plt.xticks(x_pos, xbars, rotation='horizontal')

    plt.ylim([0, N+error_factor])  #Limit of the Y in the graph. use this if we go with error bars to show the error

    # print(all_problems)
    # for i in range(0, N):
    #     print all_problems[i][4]
    #
    # print np.max(all_problems, axis=0)
    # print np.min(all_problems, axis=0)
    # print np.mean(all_problems, axis=0)
    plt.show()




