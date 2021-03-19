from __future__ import division
import numpy as np
from statistics_parsers import get_statistics_dressing
import PySimpleGUI27 as sg
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

    # forg_problems_all = 0
    # conf_sim_problems_all = 0
    # conf_other_chunk_problems_all = 0

    # for 1 subject we also generate the KTA score
    ## KTA ##

    kta_init = 0
    kta_org  = 0
    kta_seq  = 0
    kta_saf  = 0
    kta_comp  = 0
    performance_all_steps = 0

    ## KTA SCORE ###

    execfile("dressing_model.py")
    result_one = get_statistics_dressing()

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


    # #plot the results
    # data = [
    #     [init_problems_all, init_problems_all_verbal_help, init_problems_all_physical_help, init_problems_all_incapable],
    #     [org_problems_all, org_problems_all_verbal_help, org_problems_all_physical_help, org_problems_all_incapable],
    #     [seq_problems_all, seq_problems_all_verbal_help, seq_problems_all_physical_help, seq_problems_all_incapable],
    #     [saf_problems_all, saf_problems_all_verbal_help, saf_problems_all_physical_help, saf_problems_all_incapable],
    #     [comp_problems_all, comp_problems_all_verbal_help, comp_problems_all_physical_help, comp_problems_all_incapable]
    # ]
    #
    # columns = ['All errors', 'Verbal help', 'Physical Help', 'Incapable']
    #
    # # Code to print to GUI the results
    # sg.change_look_and_feel('Topanga')  # Add some color to the window
    # layout = [sg.Table(values=data, headings=columns]
    #
    # window = sg.Window('Simulation of daily activities results', layout)
    # event, values = window.read()
    # window.close()
    # print(event)
    #


    # # Code to print to GUI the results
    #
    # sg.change_look_and_feel('Topanga')  # Add some color to the window
    # layout = [
    #     [sg.Text('Results:')],
    #     [sg.Text("Total initiation errors: " + str(init_problems_all))],
    #     [sg.Text("Total initiation errors verbal help: " + str(init_problems_all_verbal_help))],
    #     [sg.Text("Total initiation errors physical help: " + str(init_problems_all_physical_help))],
    #     [sg.Text("Total initiation errors incapable: " + str(init_problems_all_incapable))]
    # ]
    #
    # window = sg.Window('Simulation of daily activities results', layout)
    # event, values = window.read()
    # window.close()
    # print(event)





else:

    kta_list_all_subjects = list()

    init_problems_all_at_least_one = 0
    init_problems_all_at_least_one_verbal = 0
    init_problems_all_at_least_one_physical = 0
    init_problems_all_at_least_one_incapable = 0

    org_problems_all_at_least_one = 0
    org_problems_all_at_least_one_verbal = 0
    org_problems_all_at_least_one_physical = 0
    org_problems_all_at_least_one_incapable = 0

    seq_problems_all_at_least_one = 0  #if the subject made at least 1 error we count it as 1
    seq_problems_all_at_least_one_verbal = 0
    seq_problems_all_at_least_one_physical = 0
    seq_problems_all_at_least_one_incapable = 0

    saf_problems_all_at_least_one = 0
    saf_problems_all_at_least_one_verbal = 0
    saf_problems_all_at_least_one_physical = 0
    saf_problems_all_at_least_one_incapable = 0

    comp_problems_all_at_least_one = 0
    comp_problems_all_at_least_one_verbal = 0
    comp_problems_all_at_least_one_physical = 0
    comp_problems_all_at_least_one_incapable = 0

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

        execfile("dressing_model.py")
        result_one = get_statistics_dressing()

        # we count for each person how much help they got
        if result_one['Initiation problems'] > 0:
            init_problems_all_at_least_one += 1
        if result_one['Initiation problems incapable'] > 0:
            init_problems_all_at_least_one_incapable += 1
            kta_init = 3
        elif result_one['Initiation problems physical help'] > 0:
            init_problems_all_at_least_one_physical += 1
            kta_init = 2
        elif result_one['Initiation problems verbal help'] > 0:
            init_problems_all_at_least_one_verbal += 1
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
            comp_problems_all_at_least_one += 1
        if result_one['Completion problems incapable'] > 0:
            comp_problems_all_at_least_one_incapable += 1
            kta_comp = 3
        elif result_one['Completion problems physical help'] > 0:
            comp_problems_all_at_least_one_physical += 1
            kta_comp = 2
        elif result_one['Completion problems verbal help'] > 0:
            comp_problems_all_at_least_one_verbal += 1
            kta_comp = 1

        performance_all_steps = result_one['Performance all steps']
        kta_score = kta_init + kta_org + performance_all_steps + kta_seq + kta_saf + kta_comp
        kta_list_all_subjects.append(kta_score)

    print "This experiment run for: ", N, "people!\n"
    print "Initiation: Independent  people are: ", N - init_problems_all_at_least_one
    print "Total initiation errors by ", N, "people are: ", init_problems_all_at_least_one
    print "Total initiation errors verbal help by ", N, "people are: ", init_problems_all_at_least_one_verbal
    print "Total initiation errors physical help by ", N, "people are: ", init_problems_all_at_least_one_physical
    print "Total initiation errors incapable by ", N, "people are: ", init_problems_all_at_least_one_incapable

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

    print "Completion: Independent  people are: ", N - comp_problems_all_at_least_one
    print "Total Completion errors by ", N, "people are: ", comp_problems_all_at_least_one
    print "Total Completion errors verbal help by ", N, "people are: ", comp_problems_all_at_least_one_verbal
    print "Total Completion errors physical help by ", N, "people are: ", comp_problems_all_at_least_one_physical
    print "Total Completion errors incapable by ", N, "people are: ", comp_problems_all_at_least_one_incapable

    print "The mean KTA by ", N, "people is: ", np.mean(kta_list_all_subjects)
    print "The SD KTA by ", N, "people is: ",   np.std(kta_list_all_subjects, ddof=0)

    #plot the results
    data = [
        ['Initiation', N - init_problems_all_at_least_one, init_problems_all_at_least_one_verbal, init_problems_all_at_least_one_physical, init_problems_all_at_least_one_incapable],
        ['Organization',  N - org_problems_all_at_least_one, org_problems_all_at_least_one_verbal, org_problems_all_at_least_one_physical, org_problems_all_at_least_one_incapable],
        ['Sequencing',  N - seq_problems_all_at_least_one, seq_problems_all_at_least_one_verbal, seq_problems_all_at_least_one_physical, seq_problems_all_at_least_one_incapable],
        ['Safety',  N - saf_problems_all_at_least_one, saf_problems_all_at_least_one_verbal, saf_problems_all_at_least_one_physical, saf_problems_all_at_least_one_incapable],
        ['Completion',  N - comp_problems_all_at_least_one, comp_problems_all_at_least_one_verbal, comp_problems_all_at_least_one_physical, comp_problems_all_at_least_one_incapable]
    ]
    df = pd.DataFrame(data, columns=['Criteria', 'Independent', 'Verbal help', 'Physical Help', 'Incapable'])
    df.plot.bar()
    plt.bar(df['Independent'], df['Verbal help'])
    plt.xlabel("Categories")
    plt.ylabel("#Subjects")
    texttodisplay = 'MEAN KTA: ' + str(np.mean(kta_list_all_subjects)) + '\n' + 'SD: ' + str(np.std(kta_list_all_subjects, ddof=0))
    plt.text(0.5, N + 1, texttodisplay)    # Create names
    xbars = ('Initiation', 'Organization', 'Sequencing', 'Safety', 'Completion')
    x_pos = np.arange(len(xbars))
    plt.xticks(x_pos, xbars, rotation='horizontal')
    plt.ylim([0, N])
    plt.show()

    #save the results to excel file.
    # workbook = xlsxwriter.Workbook('kta100.xlsx')
    # worksheet = workbook.add_worksheet()
    # row, column = 0, 0
    # for kta in kta_list_all_subjects:
    #     worksheet.write(row, column, kta)
    #     row += 1
    # workbook.close()




