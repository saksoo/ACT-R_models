import os
from urllib2 import urlopen
from lxml.html import parse
from pandas.io.parsers import TextParser
from collections import defaultdict
import shutil
import sys

#output files to be saved here

if sys.platform == "darwin":  # check if on OSX
    directory = "mainGUI/"
else:  # check if on WINDOWS
    directory = "." + "/mainGUI"


def table_to_list(table):
    dct = table_to_2d_dict(table)
    return list(iter_2d_dict(dct))


def table_to_2d_dict(table):
    result = defaultdict(lambda : defaultdict(unicode))
    for row_i, row in enumerate(table.xpath('./tr')):
        for col_i, col in enumerate(row.xpath('./td|./th')):
            colspan = int(col.get('colspan', 1))
            rowspan = int(col.get('rowspan', 1))
            col_data = col.text_content()
            while row_i in result and col_i in result[row_i]:
                col_i += 1
            for i in range(row_i, row_i + rowspan):
                for j in range(col_i, col_i + colspan):
                    result[i][j] = col_data
    return result


def iter_2d_dict(dct):
    for i, row in sorted(dct.items()):
        cols = []
        for j, col in sorted(row.items()):
            cols.append(col)
        yield cols


def get_statistics_dressing():
    dir_path = directory
    html_log_filename = os.listdir(dir_path)[0]
    if sys.platform == "darwin":  # check if on OSX
        parsed = parse(urlopen("file:///" + os.path.abspath(dir_path) + "/" + html_log_filename))
    else:  # check if on WINDOWS
        parsed = parse(urlopen("file:/" + os.path.abspath(dir_path) + "/" + html_log_filename))

    #get the results in panda frame
    df = 0
    doc = parsed
    for table_el in doc.xpath('//table'):
        table = table_to_list(table_el)
        df = table
        break

    header = df[2]
    #print "The header has %d columns." % (len(header))
    if len(header) == 5:
        header = ['time', 'DM_busy', 'DMBuffer_Chunk', 'Goal_Chunk', 'Production']
    else:
        header = ['time', 'DM_busy', 'DM_error', 'DMBuffer_Chunk', 'Goal_Chunk', 'Production']

    df = df[3:]
    results = TextParser(df, names=header).get_chunk()

    conflict_initiation_verbal_help = 0
    conflict_initiation_physical_help = 0
    conflict_initiation_incapable = 0

    stage1_verbal_help = 0
    stage1_physical_help = 0
    stage1_incapable = 0

    safety_verbal_help1 = 0
    safety_physical_help1 = 0
    safety_incapable_help1 = 0

    completion_verbal_help1 = 0
    completion_physical_help1 = 0
    completion_incapable_help1 = 0

    completion_verbal_help2 = 0
    completion_physical_help2 = 0
    completion_incapable_help2 = 0

    #count stages conflict help needed
    if len(results[results['Production'].str.contains("PRO_0_proceed_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        conflict_initiation_verbal_help += 1
    if len(results[results['Production'].str.contains("PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        conflict_initiation_physical_help += 1
    if len(results[results['Production'].str.contains("PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        conflict_initiation_incapable += 1

    if len(results[results['Production'].str.contains("PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        stage1_verbal_help += 1
    if len(results[results['Production'].str.contains("PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        stage1_physical_help += 1
    if len(results[results['Production'].str.contains("PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        stage1_incapable += 1

    # count all stages sum
    all_stages_verbal_help = stage1_verbal_help
    all_stages_physical_help = stage1_physical_help
    all_stages_incapable = stage1_incapable

    #count safety help

    if len(results[results['Production'].str.contains("PRO_1_putshirtwrong_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        safety_verbal_help1 += 1
    if len(results[results['Production'].str.contains("PRO_1_putshirtwrong_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        safety_physical_help1 += 1
    if len(results[results['Production'].str.contains("PRO_1_putshirtwrong_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        safety_incapable_help1 += 1

    safety_verbal_help = safety_verbal_help1 
    safety_physical_help = safety_physical_help1 
    safety_incapable_help = safety_incapable_help1

    # count completion help
    if len(results[results['Production'].str.contains("PRO_1_put_head_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        completion_verbal_help1 += 1
    if len(results[results['Production'].str.contains("PRO_1_put_head_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        completion_physical_help1 += 1
    if len(results[results['Production'].str.contains("PRO_1_put_head_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        completion_incapable_help1 += 1

    if len(results[results['Production'].str.contains("PRO_2_pulltrousers_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        completion_verbal_help2 += 1
    if len(results[results['Production'].str.contains("PRO_2_pulltrousers_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        completion_physical_help2 += 1
    if len(results[results['Production'].str.contains("PRO_2_pulltrousers_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        completion_incapable_help2 += 1

    # count all COMPLETION 
    completion_verbal_help = completion_verbal_help1 + completion_verbal_help2
    completion_physical_help = completion_physical_help1 + completion_physical_help2
    completion_incapable_help = completion_incapable_help1 + completion_incapable_help2

    #                             !!!!!!!!!!     CHUNK ACTIVATION       !!!!!!!!!!!!!!
    organ_problems = 0

    #count each chunk statistics
    verbal_help_chunk1 = 0
    physical_help_chunk1 = 0
    incapable_chunk1 = 0
    chunk_act_help_mem1 = len(results[results['Production'].str.contains("PRO_1_GET_shirt_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem1 == 1:  verbal_help_chunk1 += 1
    if chunk_act_help_mem1 == 2:  physical_help_chunk1 += 1
    if chunk_act_help_mem1  > 2:  incapable_chunk1 += 1
    if chunk_act_help_mem1:       organ_problems += 1

    verbal_help_chunk2 = 0
    physical_help_chunk2 = 0
    incapable_chunk2 = 0
    chunk_act_help_mem2 = len(results[results['Production'].str.contains("PRO_2_GET_trousers_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem2 == 1:  verbal_help_chunk2 += 1
    if chunk_act_help_mem2 == 2:  physical_help_chunk2 += 1
    if chunk_act_help_mem2  > 2:  incapable_chunk2 += 1
    if chunk_act_help_mem2:       organ_problems += 1

    verbal_help_chunk_all = verbal_help_chunk1 + verbal_help_chunk2
    physical_help_chunk_all = physical_help_chunk1 + physical_help_chunk2
    incapable_all_chunks = incapable_chunk1 + incapable_chunk2

    #behavior problems
    init_problems = len(results[results['Production'].str.contains("_CONFLICT_INITIATION") == True])
    all_stages = len(results[results['Production'].str.contains("CONFLICT_ERROR_INIT") == True])
    comp_problems = len(results[results['Production'].str.contains("ERROR_COMPLETION_ERROR") == True])
    safe_problems = len(results[results['Production'].str.contains("CONFLICT_ERROR_SAFETY") == True])

    #calculate performance of all steps

    if conflict_initiation_verbal_help + verbal_help_chunk_all + all_stages_verbal_help\
        + safety_verbal_help + completion_verbal_help>0:
        performance_all_steps_verbal_help = True
    else:
        performance_all_steps_verbal_help = False

    if conflict_initiation_physical_help + physical_help_chunk_all + all_stages_physical_help\
        + safety_physical_help + completion_physical_help>0:
        performance_all_steps_physical_help = True
    else:
        performance_all_steps_physical_help = False

    if conflict_initiation_incapable + incapable_all_chunks + all_stages_incapable\
        + safety_incapable_help + completion_incapable_help>0:
        performance_all_steps_incapable = True
    else:
        performance_all_steps_incapable = False

    performance_all_steps = 0
    if performance_all_steps_incapable:
        performance_all_steps = 3
    elif performance_all_steps_physical_help:
        performance_all_steps = 2
    elif performance_all_steps_verbal_help:
        performance_all_steps = 1
    else:
        performance_all_steps = 0


    #output results
    res = {
        "Initiation problems": init_problems,
        "Initiation problems verbal help":  conflict_initiation_verbal_help,
        "Initiation problems physical help": conflict_initiation_physical_help,
        "Initiation problems incapable": conflict_initiation_incapable,

        "Organization problems": organ_problems,
        "Organization problems verbal help": verbal_help_chunk_all,
        "Organization problems physical help": physical_help_chunk_all,
        "Organization problems incapable": incapable_all_chunks,

        "Sequencing problems": all_stages,
        "Sequencing problems verbal help": all_stages_verbal_help,
        "Sequencing problems physical help": all_stages_physical_help,
        "Sequencing problems incapable": all_stages_incapable,

        "Safety problems": safe_problems,
        "Safety problems verbal help": safety_verbal_help,
        "Safety problems physical help": safety_physical_help,
        "Safety problems incapable": safety_incapable_help,

        "Completion problems": comp_problems,
        "Completion problems verbal help": completion_verbal_help,
        "Completion problems physical help": completion_physical_help,
        "Completion problems incapable": completion_incapable_help,

        "Performance all steps": performance_all_steps,

        "Forget": len(results[results['Production'].str.contains("_FORGET_RETRIEVAL") == True]),
        "Confused similarity": len(results[results['Production'].str.contains("_CONFUSED_RETRIEVAL") == True]),
        "Confused other": len(results[results['Production'].str.contains("_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL") == True])
    }

    #pprint(res)
    #delete the html files
    shutil.rmtree(dir_path)
    return res


def get_statistics_tea():
    dir_path = directory
    html_log_filename = os.listdir(dir_path)[0]
    if sys.platform == "darwin":  # check if on OSX
        parsed = parse(urlopen("file:///" + os.path.abspath(dir_path) + "/" + html_log_filename))
    else:  # check if on WINDOWS
        parsed = parse(urlopen("file:/" + os.path.abspath(dir_path) + "/" + html_log_filename))
 
    #get the results in panda frame
    df = 0
    doc = parsed
    for table_el in doc.xpath('//table'):
        table = table_to_list(table_el)
        df = table
        break

    header = df[2]
    #print "The header has %d columns." % (len(header))
    if len(header) == 5:
        header = ['time', 'DM_busy', 'DMBuffer_Chunk', 'Goal_Chunk', 'Production']
    else:
        header = ['time', 'DM_busy', 'DM_error', 'DMBuffer_Chunk', 'Goal_Chunk', 'Production']

    df = df[3:]
    results = TextParser(df, names=header).get_chunk()

    conflict_initiation_verbal_help = 0
    conflict_initiation_physical_help = 0
    conflict_initiation_incapable = 0

    stage1_verbal_help = 0
    stage1_physical_help = 0
    stage1_incapable = 0

    stage2_verbal_help = 0
    stage2_physical_help = 0
    stage2_incapable = 0

    stage3_verbal_help = 0
    stage3_physical_help = 0
    stage3_incapable = 0

    stage4_verbal_help = 0
    stage4_physical_help = 0
    stage4_incapable = 0

    safety_verbal_help1 = 0
    safety_physical_help1 = 0
    safety_incapable_help1 = 0

    safety_verbal_help2 = 0
    safety_physical_help2 = 0
    safety_incapable_help2 = 0

    safety_verbal_help3 = 0
    safety_physical_help3 = 0
    safety_incapable_help3 = 0

    completion_verbal_help = 0
    completion_physical_help = 0
    completion_incapable_help = 0

    #count stages conflict help needed
    if len(results[results['Production'].str.contains("PRO_0_proceed_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        conflict_initiation_verbal_help += 1
    if len(results[results['Production'].str.contains("PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        conflict_initiation_physical_help += 1
    if len(results[results['Production'].str.contains("PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        conflict_initiation_incapable += 1

    if len(results[results['Production'].str.contains("PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        stage1_verbal_help += 1
    if len(results[results['Production'].str.contains("PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        stage1_physical_help += 1
    if len(results[results['Production'].str.contains("PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        stage1_incapable += 1

    if len(results[results['Production'].str.contains("PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        stage2_verbal_help += 1
    if len(results[results['Production'].str.contains("PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        stage2_physical_help += 1
    if len(results[results['Production'].str.contains("PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        stage2_incapable += 1

    if len(results[results['Production'].str.contains("PRO_3_MOVETOSTAGE4_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        stage3_verbal_help += 1
    if len(results[results['Production'].str.contains("PRO_3_MOVETOSTAGE4_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        stage3_physical_help += 1
    if len(results[results['Production'].str.contains("PRO_3_MOVETOSTAGE4_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        stage3_incapable += 1

    if len(results[results['Production'].str.contains("PRO_4_MOVETOSTAGE5_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        stage4_verbal_help += 1
    if len(results[results['Production'].str.contains("PRO_4_MOVETOSTAGE5_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        stage4_physical_help += 1
    if len(results[results['Production'].str.contains("PRO_4_MOVETOSTAGE5_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        stage4_incapable += 1

    # count all stages sum
    all_stages_verbal_help = stage1_verbal_help + stage2_verbal_help + stage3_verbal_help + stage4_verbal_help
    all_stages_physical_help = stage1_physical_help + stage2_physical_help + stage3_physical_help + stage4_physical_help
    all_stages_incapable = stage1_incapable + stage2_incapable + stage3_incapable + stage4_incapable

    #count safety help

    if len(results[results['Production'].str.contains("PRO_1_turnonstove_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        safety_verbal_help1 += 1
    if len(results[results['Production'].str.contains("PRO_1_turnonstove_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        safety_physical_help1 += 1
    if len(results[results['Production'].str.contains("PRO_1_turnonstove_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        safety_incapable_help1 += 1

    if len(results[results['Production'].str.contains("PRO_3_turnoffstove_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        safety_verbal_help2 += 1
    if len(results[results['Production'].str.contains("PRO_3_turnoffstove_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        safety_physical_help2 += 1
    if len(results[results['Production'].str.contains("PRO_3_turnoffstove_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        safety_incapable_help2 += 1

    if len(results[results['Production'].str.contains("PRO_4_pour_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        safety_verbal_help3 += 1
    if len(results[results['Production'].str.contains("PRO_4_pour_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        safety_physical_help3 += 1
    if len(results[results['Production'].str.contains("PRO_4_pour_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        safety_incapable_help3 += 1

    safety_verbal_help = safety_verbal_help1 + safety_verbal_help2 + safety_verbal_help3
    safety_physical_help = safety_physical_help1 + safety_physical_help2 + safety_physical_help3
    safety_incapable_help = safety_incapable_help1 + safety_incapable_help2 + safety_incapable_help3

    # count completion help
    if len(results[results['Production'].str.contains("PRO_4_do_let34_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        completion_verbal_help += 1
    if len(results[results['Production'].str.contains("PRO_4_do_let34_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        completion_physical_help += 1
    if len(results[results['Production'].str.contains("PRO_4_do_let34_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        completion_incapable_help += 1

    #                             !!!!!!!!!!     CHUNK ACTIVATION       !!!!!!!!!!!!!!
    organ_problems = 0

    #count each chunk statistics
    verbal_help_chunk1 = 0
    physical_help_chunk1 = 0
    incapable_chunk1 = 0
    chunk_act_help_mem1 = len(results[results['Production'].str.contains("PRO_1_GET_water_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem1 == 1:  verbal_help_chunk1 += 1
    if chunk_act_help_mem1 == 2:  physical_help_chunk1 += 1
    if chunk_act_help_mem1  > 2:  incapable_chunk1 += 1
    if chunk_act_help_mem1:       organ_problems += 1

    verbal_help_chunk2 = 0
    physical_help_chunk2 = 0
    incapable_chunk2 = 0
    chunk_act_help_mem2 = len(results[results['Production'].str.contains("PRO_1_GET_kettle_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem2 == 1:  verbal_help_chunk2 += 1
    if chunk_act_help_mem2 == 2:  physical_help_chunk2 += 1
    if chunk_act_help_mem2  > 2:  incapable_chunk2 += 1
    if chunk_act_help_mem2:       organ_problems += 1

    verbal_help_chunk3 = 0
    physical_help_chunk3 = 0
    incapable_chunk3 = 0
    chunk_act_help_mem3 = len(results[results['Production'].str.contains("PRO_2_GET_mug_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem3 == 1:  verbal_help_chunk3 += 1
    if chunk_act_help_mem3 == 2:  physical_help_chunk3 += 1
    if chunk_act_help_mem3  > 2:  incapable_chunk3 += 1
    if chunk_act_help_mem3:       organ_problems += 1

    verbal_help_chunk4 = 0
    physical_help_chunk4 = 0
    incapable_chunk4 = 0
    chunk_act_help_mem4 = len(results[results['Production'].str.contains("PRO_2_GET_teabag_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem4 == 1:  verbal_help_chunk4 += 1
    if chunk_act_help_mem4 == 2:  physical_help_chunk4 += 1
    if chunk_act_help_mem4  > 2:  incapable_chunk4 += 1
    if chunk_act_help_mem4:       organ_problems += 1

    verbal_help_chunk5 = 0
    physical_help_chunk5 = 0
    incapable_chunk5 = 0
    chunk_act_help_mem5 = len(results[results['Production'].str.contains("PRO_3_GET_hotmitt_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem5 == 1:  verbal_help_chunk5 += 1
    if chunk_act_help_mem5 == 2:  physical_help_chunk5 += 1
    if chunk_act_help_mem5  > 2:  incapable_chunk5 += 1
    if chunk_act_help_mem5:       organ_problems += 1

    verbal_help_chunk6 = 0
    physical_help_chunk6 = 0
    incapable_chunk6 = 0
    chunk_act_help_mem6 = len(results[results['Production'].str.contains("PRO_4_GET_kettlewithwater_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem6 == 1:  verbal_help_chunk6 += 1
    if chunk_act_help_mem6 == 2:  physical_help_chunk6 += 1
    if chunk_act_help_mem6  > 2:  incapable_chunk6 += 1
    if chunk_act_help_mem6:       organ_problems += 1

    verbal_help_chunk7 = 0
    physical_help_chunk7 = 0
    incapable_chunk7 = 0
    chunk_act_help_mem7 = len(results[results['Production'].str.contains("PRO_4_GET_theteabagmug_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem7 == 1:  verbal_help_chunk7 += 1
    if chunk_act_help_mem7 == 2:  physical_help_chunk7 += 1
    if chunk_act_help_mem7  > 2:  incapable_chunk7 += 1
    if chunk_act_help_mem7:       organ_problems += 1

    verbal_help_chunk8 = 0
    physical_help_chunk8 = 0
    incapable_chunk8 = 0
    chunk_act_help_mem8 = len(results[results['Production'].str.contains("PRO_4_GET_bowl_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem8 == 1:  verbal_help_chunk8 += 1
    if chunk_act_help_mem8 == 2:  physical_help_chunk8 += 1
    if chunk_act_help_mem8  > 2:  incapable_chunk8 += 1
    if chunk_act_help_mem8:       organ_problems += 1

    verbal_help_chunk9 = 0
    physical_help_chunk9 = 0
    incapable_chunk9 = 0
    chunk_act_help_mem9 = len(results[results['Production'].str.contains("PRO_5_GET_thereadytea_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem9 == 1:  verbal_help_chunk9 += 1
    if chunk_act_help_mem9 == 2:  physical_help_chunk9 += 1
    if chunk_act_help_mem9  > 2:  incapable_chunk9 += 1
    if chunk_act_help_mem9:       organ_problems += 1

    verbal_help_chunk_all = verbal_help_chunk1 + verbal_help_chunk2 + verbal_help_chunk3 + verbal_help_chunk4 + verbal_help_chunk5 + verbal_help_chunk6 + verbal_help_chunk7 + verbal_help_chunk8 + verbal_help_chunk9
    physical_help_chunk_all = physical_help_chunk1 + physical_help_chunk2 + physical_help_chunk3 + physical_help_chunk4 + physical_help_chunk5 + physical_help_chunk6 + physical_help_chunk7 + physical_help_chunk8 + physical_help_chunk9
    incapable_all_chunks = incapable_chunk1 + incapable_chunk2 + incapable_chunk3 + incapable_chunk4 + incapable_chunk5 + incapable_chunk6 + incapable_chunk7 + incapable_chunk8 + incapable_chunk9

    #behavior problems
    init_problems = len(results[results['Production'].str.contains("_CONFLICT_INITIATION") == True])
    all_stages = len(results[results['Production'].str.contains("CONFLICT_ERROR_INIT") == True])
    comp_problems = len(results[results['Production'].str.contains("ERROR_COMPLETION_ERROR") == True])
    safe_problems = len(results[results['Production'].str.contains("CONFLICT_ERROR_SAFETY") == True])

    #calculate performance of all steps

    if conflict_initiation_verbal_help + verbal_help_chunk_all + all_stages_verbal_help\
        + safety_verbal_help + completion_verbal_help>0:
        performance_all_steps_verbal_help = True
    else:
        performance_all_steps_verbal_help = False

    if conflict_initiation_physical_help + physical_help_chunk_all + all_stages_physical_help\
        + safety_physical_help + completion_physical_help>0:
        performance_all_steps_physical_help = True
    else:
        performance_all_steps_physical_help = False

    if conflict_initiation_incapable + incapable_all_chunks + all_stages_incapable\
        + safety_incapable_help + completion_incapable_help>0:
        performance_all_steps_incapable = True
    else:
        performance_all_steps_incapable = False

    performance_all_steps = 0
    if performance_all_steps_incapable:
        performance_all_steps = 3
    elif performance_all_steps_physical_help:
        performance_all_steps = 2
    elif performance_all_steps_verbal_help:
        performance_all_steps = 1
    else:
        performance_all_steps = 0


    #output results
    res = {
        "Initiation problems": init_problems,
        "Initiation problems verbal help":  conflict_initiation_verbal_help,
        "Initiation problems physical help": conflict_initiation_physical_help,
        "Initiation problems incapable": conflict_initiation_incapable,

        "Organization problems": organ_problems,
        "Organization problems verbal help": verbal_help_chunk_all,
        "Organization problems physical help": physical_help_chunk_all,
        "Organization problems incapable": incapable_all_chunks,

        "Sequencing problems": all_stages,
        "Sequencing problems verbal help": all_stages_verbal_help,
        "Sequencing problems physical help": all_stages_physical_help,
        "Sequencing problems incapable": all_stages_incapable,

        "Safety problems": safe_problems,
        "Safety problems verbal help": safety_verbal_help,
        "Safety problems physical help": safety_physical_help,
        "Safety problems incapable": safety_incapable_help,

        "Completion problems": comp_problems,
        "Completion problems verbal help": completion_verbal_help,
        "Completion problems physical help": completion_physical_help,
        "Completion problems incapable": completion_incapable_help,

        "Performance all steps": performance_all_steps,

        "Forget": len(results[results['Production'].str.contains("_FORGET_RETRIEVAL") == True]),
        "Confused similarity": len(results[results['Production'].str.contains("_CONFUSED_RETRIEVAL") == True]),
        "Confused other": len(results[results['Production'].str.contains("_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL") == True])
    }

    #pprint(res)
    #delete the html files
    shutil.rmtree(dir_path)
    return res


def get_statistics_washing():
    dir_path = directory
    html_log_filename = os.listdir(dir_path)[0]
    if sys.platform == "darwin":  # check if on OSX
        parsed = parse(urlopen("file:///" + os.path.abspath(dir_path) + "/" + html_log_filename))
    else:  # check if on WINDOWS
        parsed = parse(urlopen("file:/" + os.path.abspath(dir_path) + "/" + html_log_filename))
    
    #get the results in panda frame
    df = 0
    doc = parsed
    for table_el in doc.xpath('//table'):
        table = table_to_list(table_el)
        df = table
        break

    header = df[2]
    #print "The header has %d columns." % (len(header))
    if len(header) == 5:
        header = ['time', 'DM_busy', 'DMBuffer_Chunk', 'Goal_Chunk', 'Production']
    else:
        header = ['time', 'DM_busy', 'DM_error', 'DMBuffer_Chunk', 'Goal_Chunk', 'Production']

    df = df[3:]
    results = TextParser(df, names=header).get_chunk()

    conflict_initiation_verbal_help = 0
    conflict_initiation_physical_help = 0
    conflict_initiation_incapable = 0

    stage1_verbal_help = 0
    stage1_physical_help = 0
    stage1_incapable = 0

    stage2_verbal_help = 0
    stage2_physical_help = 0
    stage2_incapable = 0

    safety_verbal_help1 = 0
    safety_physical_help1 = 0
    safety_incapable_help1 = 0

    completion_verbal_help1 = 0
    completion_physical_help1 = 0
    completion_incapable_help1 = 0

    completion_verbal_help2 = 0
    completion_physical_help2 = 0
    completion_incapable_help2 = 0

    #count stages conflict help needed
    if len(results[results['Production'].str.contains("PRO_0_proceed_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        conflict_initiation_verbal_help += 1
    if len(results[results['Production'].str.contains("PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        conflict_initiation_physical_help += 1
    if len(results[results['Production'].str.contains("PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        conflict_initiation_incapable += 1

    if len(results[results['Production'].str.contains("PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        stage1_verbal_help += 1
    if len(results[results['Production'].str.contains("PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        stage1_physical_help += 1
    if len(results[results['Production'].str.contains("PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        stage1_incapable += 1

    if len(results[results['Production'].str.contains("PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        stage2_verbal_help += 1
    if len(results[results['Production'].str.contains("PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        stage2_physical_help += 1
    if len(results[results['Production'].str.contains("PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        stage2_incapable += 1

    # count all stages sum
    all_stages_verbal_help = stage1_verbal_help + stage2_verbal_help
    all_stages_physical_help = stage1_physical_help + stage2_physical_help
    all_stages_incapable = stage1_incapable + stage2_incapable

    #count safety help

    if len(results[results['Production'].str.contains("PRO_1_applysoap_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        safety_verbal_help1 += 1
    if len(results[results['Production'].str.contains("PRO_1_applysoap_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        safety_physical_help1 += 1
    if len(results[results['Production'].str.contains("PRO_1_applysoap_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        safety_incapable_help1 += 1

    safety_verbal_help = safety_verbal_help1
    safety_physical_help = safety_physical_help1
    safety_incapable_help = safety_incapable_help1

    # count completion help
    if len(results[results['Production'].str.contains("PRO_1_do_washhands_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        completion_verbal_help1 += 1
    if len(results[results['Production'].str.contains("PRO_1_do_washhands_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        completion_physical_help1 += 1
    if len(results[results['Production'].str.contains("PRO_1_do_washhands_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        completion_incapable_help1 += 1

    if len(results[results['Production'].str.contains("PRO_3_do_dofinish_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS") == True]):
        completion_verbal_help2 += 1
    if len(results[results['Production'].str.contains("PRO_3_do_dofinish_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS") == True]):
        completion_physical_help2 += 1
    if len(results[results['Production'].str.contains("PRO_3_do_dofinish_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE") == True]):
        completion_incapable_help2 += 1

    # count all COMPLETION
    completion_verbal_help = completion_verbal_help1 + completion_verbal_help2
    completion_physical_help = completion_physical_help1 + completion_physical_help2
    completion_incapable_help = completion_incapable_help1 + completion_incapable_help2

    #                             !!!!!!!!!!     CHUNK ACTIVATION       !!!!!!!!!!!!!!
    organ_problems = 0

    #count each chunk statistics
    verbal_help_chunk1 = 0
    physical_help_chunk1 = 0
    incapable_chunk1 = 0
    chunk_act_help_mem1 = len(results[results['Production'].str.contains("PRO_1_GET_tapon_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem1 == 1:  verbal_help_chunk1 += 1
    if chunk_act_help_mem1 == 2:  physical_help_chunk1 += 1
    if chunk_act_help_mem1  > 2:  incapable_chunk1 += 1
    if chunk_act_help_mem1:       organ_problems += 1

    verbal_help_chunk2 = 0
    physical_help_chunk2 = 0
    incapable_chunk2 = 0
    chunk_act_help_mem2 = len(results[results['Production'].str.contains("PRO_1_GET_soap_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem2 == 1:  verbal_help_chunk2 += 1
    if chunk_act_help_mem2 == 2:  physical_help_chunk2 += 1
    if chunk_act_help_mem2  > 2:  incapable_chunk2 += 1
    if chunk_act_help_mem2:       organ_problems += 1

    verbal_help_chunk3 = 0
    physical_help_chunk3 = 0
    incapable_chunk3 = 0
    chunk_act_help_mem3 = len(results[results['Production'].str.contains("PRO_2_GET_towel_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem3 == 1:  verbal_help_chunk3 += 1
    if chunk_act_help_mem3 == 2:  physical_help_chunk3 += 1
    if chunk_act_help_mem3  > 2:  incapable_chunk3 += 1
    if chunk_act_help_mem3:       organ_problems += 1

    verbal_help_chunk4 = 0
    physical_help_chunk4 = 0
    incapable_chunk4 = 0
    chunk_act_help_mem4 = len(results[results['Production'].str.contains("PRO_3_GET_tapoff_ASK_CHUNK_HELP") == True])
    if chunk_act_help_mem4 == 1:  verbal_help_chunk4 += 1
    if chunk_act_help_mem4 == 2:  physical_help_chunk4 += 1
    if chunk_act_help_mem4  > 2:  incapable_chunk4 += 1
    if chunk_act_help_mem4:       organ_problems += 1

    verbal_help_chunk_all = verbal_help_chunk1 + verbal_help_chunk2 + verbal_help_chunk3 + verbal_help_chunk4
    physical_help_chunk_all = physical_help_chunk1 + physical_help_chunk2 + physical_help_chunk3 + physical_help_chunk4
    incapable_all_chunks = incapable_chunk1 + incapable_chunk2 + incapable_chunk3 + incapable_chunk4

    #behavior problems
    init_problems = len(results[results['Production'].str.contains("_CONFLICT_INITIATION") == True])
    all_stages = len(results[results['Production'].str.contains("CONFLICT_ERROR_INIT") == True])
    comp_problems = len(results[results['Production'].str.contains("ERROR_COMPLETION_ERROR") == True])
    safe_problems = len(results[results['Production'].str.contains("CONFLICT_ERROR_SAFETY") == True])

    #calculate performance of all steps

    if conflict_initiation_verbal_help + verbal_help_chunk_all + all_stages_verbal_help\
        + safety_verbal_help + completion_verbal_help>0:
        performance_all_steps_verbal_help = True
    else:
        performance_all_steps_verbal_help = False

    if conflict_initiation_physical_help + physical_help_chunk_all + all_stages_physical_help\
        + safety_physical_help + completion_physical_help>0:
        performance_all_steps_physical_help = True
    else:
        performance_all_steps_physical_help = False

    if conflict_initiation_incapable + incapable_all_chunks + all_stages_incapable\
        + safety_incapable_help + completion_incapable_help>0:
        performance_all_steps_incapable = True
    else:
        performance_all_steps_incapable = False

    performance_all_steps = 0
    if performance_all_steps_incapable:
        performance_all_steps = 3
    elif performance_all_steps_physical_help:
        performance_all_steps = 2
    elif performance_all_steps_verbal_help:
        performance_all_steps = 1
    else:
        performance_all_steps = 0


    #output results
    res = {
        "Initiation problems": init_problems,
        "Initiation problems verbal help":  conflict_initiation_verbal_help,
        "Initiation problems physical help": conflict_initiation_physical_help,
        "Initiation problems incapable": conflict_initiation_incapable,

        "Organization problems": organ_problems,
        "Organization problems verbal help": verbal_help_chunk_all,
        "Organization problems physical help": physical_help_chunk_all,
        "Organization problems incapable": incapable_all_chunks,

        "Sequencing problems": all_stages,
        "Sequencing problems verbal help": all_stages_verbal_help,
        "Sequencing problems physical help": all_stages_physical_help,
        "Sequencing problems incapable": all_stages_incapable,

        "Safety problems": safe_problems,
        "Safety problems verbal help": safety_verbal_help,
        "Safety problems physical help": safety_physical_help,
        "Safety problems incapable": safety_incapable_help,

        "Completion problems": comp_problems,
        "Completion problems verbal help": completion_verbal_help,
        "Completion problems physical help": completion_physical_help,
        "Completion problems incapable": completion_incapable_help,

        "Performance all steps": performance_all_steps,

        "Forget": len(results[results['Production'].str.contains("_FORGET_RETRIEVAL") == True]),
        "Confused similarity": len(results[results['Production'].str.contains("_CONFUSED_RETRIEVAL") == True]),
        "Confused other": len(results[results['Production'].str.contains("_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL") == True])
    }

    #pprint(res)
    #delete the html files
    shutil.rmtree(dir_path)
    return res






