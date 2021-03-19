import ccm
from ccm.lib.actr import *
import params


class MyAgent(ACTR):

    production_time = 0.05         # production parameter settings
    production_sd = 0.01
    production_threshold = -100

    goal = Buffer()
    DMbuffer = Buffer()  # create a buffer for the declarative memory
    DM = Memory(DMbuffer)  # create DM and connect it to its buffer

    #Sub symbolic system
    dm_n = DMNoise(DM, noise=params.e_chunk_activation_transitory_noise, baseNoise=0)
    dm_bl = DMBaseLevel(DM, decay=0.0, limit=None)

    dm_spread = DMSpreading(DM, goal)  # specify the buffer(s) to spread from
    dm_spread.strength = params.S_chunk_strength_of_association  # set strengh of activation for buffers
    # set weight to adjust for how many slots in the buffer
    # usually this is strength divided by number of slots
    dm_spread.weight[goal] = params.W

    #PARTIAL MATCHING OF CHUNKS, PARTIAL SIMILARITY TO CREATE COMMISSION ERRORS
    partial = Partial(DM, strength=params.Ps, limit=-1.0)  # turn on partial matching
    partial.similarity('the-kettle', 'the-mug', params.similarity)
    partial.similarity('the-teabag', 'the-water', params.similarity)

    #utility conflicts with noise using PMPGC
    pgc = PMPGC()
    pmnoise = PMNoise(noise=params.e_production_utility_transitory_noise)

    def init():

        DM.add('ingredient:the-teabag')
        DM.add('ingredient:the-water')

        DM.add('ustensile:the-kettle')
        DM.add('ustensile:the-mug')
        DM.add('ustensile:the-spoon')
        DM.add('ustensile:the-bowl')
        DM.add('ustensile:the-hotmitt')

        goal.set('ready-to-proceed')

## READY TO PROCEED

    def PRO_0_initiate(goal='ready-to-proceed'):
        print "Ready to start the task."
        goal.set('proceed')

    def PRO_0_proceed_CORRECT(goal='proceed', utility=params.utility_success):
        print "The subject has initiated the activity."
        goal.set('do water')

#BEHAVIOR INITIATION ERRORS

    def PRO_0_proceed_CONFLICT_INITIATION(goal='proceed', utility=params.utility_fail):  # this production competes with the other proceed production
        print "-------------------  INITIATION ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_0 error initiate help')

    def PRO_0_proceed_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_0 error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_0 error require verbal clues')

    def PRO_0_proceed_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_0 error require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('do water')

    def PRO_0_proceed_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_0 error require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_0 error require physical help to continue')

    def PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_0 error require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('do water')

    def PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_0 error require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAILED AND CONTINUE   ------------------------------------------"
        goal.set('pro_0 error require physical help incapable')

    def PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_0 error require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('do water')

### STAGE 1 ###

    def PRO_1_watering(goal="do water"):
        print "                 ### Stage 1 ###"
        print "The subject is looking for the water"
        goal.set('get ingredient:the-water')


    ##1 MEMORY RETRIEVAL
        
    def PRO_1_GET_water(goal="get ingredient:the-water"):
        print "The subject is requesting the water from the DM"
        DM.request('ingredient:the-water') # retrieve a chunk from DM into the DM buffer
        goal.set('find ingredient:the-water')

    def PRO_1_GET_water_SUCCESS_RETRIEVAL(goal="find ingredient:the-water",     DMbuffer='ingredient:the-water'):
        print "DM:  The subject found in the DM: WATER"
        DM.add('ingredient:the-water') # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get ustensile:the-kettle')

    def PRO_1_GET_water_FORGET_RETRIEVAL(goal="find ingredient:the-water",      DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM WITH WATER."
        goal.set('find ingredient-the-water ask chunk help')

    def PRO_1_GET_water_CONFUSED_RETRIEVAL(goal='find ingredient:the-water',    DMbuffer='ingredient:the-teabag'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED THE TEABAG"
        DMbuffer.clear()
        goal.set('find ingredient-the-water ask chunk help')

    def PRO_1_GET_water_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find ingredient:the-water', DMbuffer='ingredient:!the-water ingredient:!the-teabag'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE!!!"
        DMbuffer.clear()
        goal.set('find ingredient-the-water ask chunk help')

    # BOOST ACTIVATION CHUNK 1
    def PRO_1_GET_water_ASK_CHUNK_HELP(goal="find ingredient-the-water ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE WATER WITH CHUNK ACTIVATION"
        DM.add('ingredient:the-water') # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get ingredient:the-water')

    ##FINISHED 1 MEMORY RETRIEVAL

    ##2 MEMORY RETRIEVAL
        
    def PRO_1_GET_kettle(goal="get ustensile:the-kettle"):
        print "The subject is requesting the kettle from the DM"
        DM.request('ustensile:the-kettle') # retrieve a chunk from DM into the DM buffer
        goal.set('find ustensile:the-kettle')

    def PRO_1_GET_kettle_SUCCESS_RETRIEVAL(goal="find ustensile:the-kettle",        DMbuffer='ustensile:the-kettle'):
        print "DM:  The subject found in the DM: KETTLE"
        DM.add('ustensile:the-kettle')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()  # this is automatic in Lisp implementation
        goal.set('do fill-kettle')

    def PRO_1_GET_kettle_FORGET_RETRIEVAL(goal='find ustensile:the-kettle',         DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM IN KETTLE."
        goal.set('find ustensile-the-kettle ask chunk help')

    def PRO_1_GET_kettle_CONFUSED_RETRIEVAL(goal='find ustensile:the-kettle',       DMbuffer='ustensile:the-mug'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED THE MUG"
        DMbuffer.clear()
        goal.set('find ustensile-the-kettle ask chunk help')

    def PRO_1_GET_kettle_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find ustensile:the-kettle', DMbuffer='ustensile:!the-kettle ustensile:!the-mug'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE!!!"
        DMbuffer.clear()
        goal.set('find ustensile-the-kettle ask chunk help')

    # BOOST ACTIVATION CHUNK 2
    def PRO_1_GET_kettle_ASK_CHUNK_HELP(goal="find ustensile-the-kettle ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE KETTLE WITH CHUNK ACTIVATION"
        DM.add('ustensile:the-kettle')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get ustensile:the-kettle')

    ##FINISHED 2 MEMORY RETRIEVAL

    def PRO_1_fillkettle(goal="do fill-kettle"):
        print "The subject is filling the kettle with water."
        print "A new chuck created here with value - ingredient:the-kettlewithwater."
        DM.add('ingredient:the-kettlewithwater')
        DMbuffer.clear()
        goal.set('do turnonstove')

    def PRO_1_turnonstove(goal="do turnonstove", utility=params.utility_success):
        print "The subject is turning on the stove."
        goal.set('do fivemin')

    # 1st SAFETY BEHAVIOR DO TURN ON STOVE CONFLICT ERRORS -- SAFETY ERROR
    def PRO_1_turnonstove_CONFLICT_ERROR_SAFETY(goal='do turnonstove', utility=params.utility_fail):
        print "-------------------  TURN ON STOVE ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_1 turnonstove error initiate help')

    def PRO_1_turnonstove_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_1 turnonstove error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_1 turnonstove require verbal clues')

    def PRO_1_turnonstove_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_1 turnonstove require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('do fivemin')

    def PRO_1_turnonstove_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_1 turnonstove require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_1 turnonstove require physical help to continue')

    def PRO_1_turnonstove_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_1 turnonstove require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('do fivemin')

    def PRO_1_turnonstove_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_1 turnonstove require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAIL AND CONTINUE   ------------------------------------------"
        goal.set('pro_1 turnonstove require physical help incapable')

    def PRO_1_turnonstove_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_1 turnonstove require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('do fivemin')

    ## END OF 1st SAFETY BEHAVIOR DO TURN OFF STOVE CONFLICT ERRORS -- SAFERY ERROR

    def PRO_1_fivemin(goal="do fivemin"):
        print "The subject is leaving the kettle for 5 min boiling."
        goal.set('do moveawayfromkettle')

    def PRO_1_PRO_1_moveawayfromkettle(goal="do moveawayfromkettle", utility=params.utility_success):
        print "The subject is moving further away."
        goal.set('get ustensile:the-mug')

# BEHAVIOR 1 STAGE CONFLICT ERRORS

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_INIT(goal='do moveawayfromkettle', utility=params.utility_fail):
        print "-------------------  STAGE 1 TRANSITION ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_1 movestage2 error initiate help')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_1 movestage2 error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_1 movestage2 require verbal clues')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_1 movestage2 require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('get ustensile:the-mug')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_1 movestage2 require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_1 movestage2 require physical help to continue')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_1 movestage2 require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('get ustensile:the-mug')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_1 movestage2 require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAILED AND CONTINUE   ------------------------------------------"
        goal.set('pro_1 movestage2 require physical help incapable')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_1 movestage2 require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('get ustensile:the-mug')

## END OF TRANSITION END STAGE 1

    ### STAGE 2 ###

    ##3 MEMORY RETRIEVAL

    def PRO_2_GET_mug(goal="get ustensile:the-mug"):
        print "                 ### Stage 2 ###"
        print "The subject is requesting the mug from the DM"
        DM.request('ustensile:the-mug')  # retrieve a chunk from DM into the DM buffer
        goal.set('find ustensile:the-mug')

    def PRO_2_GET_mug_SUCCESS_RETRIEVAL(goal="find ustensile:the-mug",      DMbuffer='ustensile:the-mug'):
        print "DM:  The subject found in the DM: MUG"
        DM.add('ustensile:the-mug')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()  # this is automatic in Lisp implementation
        goal.set('get ingredient:the-teabag')

    def PRO_2_GET_mug_FORGET_RETRIEVAL(goal='find ustensile:the-mug',       DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM IN MUG."
        goal.set('find ustensile-the-mug ask chunk help')

    def PRO_2_GET_mug_CONFUSED_RETRIEVAL(goal='find ustensile:the-mug',     DMbuffer='ustensile:the-kettle'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED THE KETTLE"
        DMbuffer.clear()
        goal.set('find ustensile-the-mug ask chunk help')

    def PRO_2_GET_mug_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find ustensile:the-mug', DMbuffer='ustensile:!the-mug ustensile:!the-kettle'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE!!!"
        DMbuffer.clear()
        goal.set('find ustensile-the-mug ask chunk help')

    # BOOST ACTIVATION CHUNK 3
    def PRO_2_GET_mug_ASK_CHUNK_HELP(goal="find ustensile-the-mug ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE MUG WITH CHUNK ACTIVATION"
        DM.add('ustensile:the-mug')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get ustensile:the-mug')

    ##FINISHED 3 MEMORY RETRIEVAL

    ## 4 MEMORY RETRIEVAL
        
    def PRO_2_GET_teabag(goal="get ingredient:the-teabag"):
        print "The subject is requesting the teabag from the DM"
        DM.request('ingredient:the-teabag')  # retrieve a chunk from DM into the DM buffer
        goal.set('find ingredient:the-teabag')

    def PRO_2_GET_teabag_SUCCESS_RETRIEVAL(goal="find ingredient:the-teabag",       DMbuffer='ingredient:the-teabag'):
        print "DM:  The subject found in the DM: TEABAG"
        DM.add('ingredient:the-teabag')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()  # this is automatic in Lisp implementation
        goal.set('do stir')

    def PRO_2_GET_teabag_FORGET_RETRIEVAL(goal='find ingredient:the-teabag',        DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM IN TEABAG."
        goal.set('find ingredient-the-teabag ask chunk help')

    def PRO_2_GET_teabag_CONFUSED_RETRIEVAL(goal='find ingredient:the-teabag',      DMbuffer='ingredient:the-water'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED THE WATER"
        DMbuffer.clear()
        goal.set('find ingredient-the-teabag ask chunk help')

    def PRO_2_GET_teabag_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find ingredient:the-teabag', DMbuffer='ingredient:!the-teabag ingredient:!the-water'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE!!!"
        DMbuffer.clear()
        goal.set('find ingredient-the-teabag ask chunk help')

    # BOOST ACTIVATION CHUNK 4
    def PRO_2_GET_teabag_ASK_CHUNK_HELP(goal="find ingredient-the-teabag ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE TEABAG WITH CHUNK ACTIVATION"
        DM.add('ingredient:the-teabag')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get ingredient:the-teabag')

    ##FINISHED 4 MEMORY RETRIEVAL

    def PRO_2_dostir(goal="do stir", utility=params.utility_success):
        print "The subject is placing the teabag in the mug."
        print "A new chuck created here with value - ingredient:the-teabagmug."
        DM.add('ingredient:the-teabagmug')
        DMbuffer.clear()
        goal.set('do waitforwhistle')

#  2ND STAGE CONFLICT ERRORS

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_INIT(goal='do stir', utility=params.utility_fail):
        print "-------------------  STAGE 2 TRANSITION ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_2 movestage3 error initiate help')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_2 movestage3 error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_2 movestage3 require verbal clues')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_2 movestage3 require verbal clues', utility=params.utility_success + params.verbal_factor):
        DM.add('ingredient:the-teabagmug')
        DMbuffer.clear()
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('do waitforwhistle')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_2 movestage3 require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_2 movestage3 require physical help to continue')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_2 movestage3 require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        DM.add('ingredient:the-teabagmug')
        DMbuffer.clear()
        goal.set('do waitforwhistle')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_2 movestage3 require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAILED AND CONTINUE   ------------------------------------------"
        goal.set('pro_2 movestage3 require physical help incapable')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_2 movestage3 require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        DM.add('ingredient:the-teabagmug')
        DMbuffer.clear()
        goal.set('do waitforwhistle')

## END OF TRANSITION END STAGE 2

### STAGE 3 ###

    def PRO_3_waitforwhistle(goal="do waitforwhistle"):
        print "                 ### Stage 3 ###"
        print "The subject is waiting for the kettle to whistle."
        goal.set('do turnoffstove')

    def PRO_3_turnoffstove(goal="do turnoffstove", utility=params.utility_success):
        print "The subject is turning off the stove."
        goal.set('get ustensile:the-hotmitt')

    # 2nd SAFETY BEHAVIOR DO TURN OFF STOVE CONFLICT ERRORS
    def PRO_3_turnoffstove_CONFLICT_ERROR_SAFETY(goal='do turnoffstove', utility=params.utility_fail):
        print "-------------------  TURN OFF STOVE ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_3 turnoffstove error initiate help')

    def PRO_3_turnoffstove_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_3 turnoffstove error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_3 turnoffstove require verbal clues')

    def PRO_3_turnoffstove_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_3 turnoffstove require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('get ustensile:the-hotmitt')

    def PRO_3_turnoffstove_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_3 turnoffstove require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_3 turnoffstove require physical help to continue')

    def PRO_3_turnoffstove_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_3 turnoffstove require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('get ustensile:the-hotmitt')

    def PRO_3_turnoffstove_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_3 turnoffstove require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAILED AND CONTINUE   ------------------------------------------"
        goal.set('pro_3 turnoffstove require physical help incapable')

    def PRO_3_turnoffstove_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_3 turnoffstove require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('get ustensile:the-hotmitt')

    ## END OF 2nd SAFETY BEHAVIOR DO TURN OFF STOVE CONFLICT ERRORS

    ## 5 MEMORY RETRIEVAL

    def PRO_3_GET_hotmitt(goal="get ustensile:the-hotmitt"):
        print "The subject is requesting the hotmitt from the DM"
        DM.request('ustensile:the-hotmitt')  # retrieve a chunk from DM into the DM buffer
        goal.set('find ustensile:the-hotmitt')

    def PRO_3_GET_hotmitt_SUCCESS_RETRIEVAL(goal="find ustensile:the-hotmitt", DMbuffer='ustensile:the-hotmitt'):
        print "DM:  The subject found in the DM: HOT MITT"
        DM.add('ustensile:the-hotmitt')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()  # this is automatic in Lisp implementation
        goal.set('do wearhotmitt')

    def PRO_3_GET_hotmitt_FORGET_RETRIEVAL(goal='find ustensile:the-hotmitt', DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM IN HOT MITT."
        goal.set('find ustensile-the-hotmitt ask chunk help')

    def PRO_3_GET_hotmitt_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find ustensile:the-hotmitt', DMbuffer='ustensile:!the-hotmitt'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE!!!"
        DMbuffer.clear()
        goal.set('find ustensile-the-hotmitt ask chunk help')

    # BOOST ACTIVATION CHUNK 5
    def PRO_3_GET_hotmitt_ASK_CHUNK_HELP(goal="find ustensile-the-hotmitt ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE HOTMITT WITH CHUNK ACTIVATION"
        DM.add('ustensile:the-hotmitt')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get ustensile:the-hotmitt')

    ##FINISHED 5 MEMORY RETRIEVAL

    def PRO_3_wearhotmitt(goal="do wearhotmitt", utility=params.utility_success):
        print "The subject is wearing the hot mitt."
        goal.set('get ingredient:the-kettlewithwater')

# BEHAVIOR 3ND STAGE CONFLICT ERRORS

    def PRO_3_MOVETOSTAGE4_CONFLICT_ERROR_INIT(goal='do wearhotmitt', utility=params.utility_fail):
        print "-------------------  STAGE 3 TRANSITION ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_3 movestage4 error initiate help')

    def PRO_3_MOVETOSTAGE4_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_3 movestage4 error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_3 movestage4 require verbal clues')

    def PRO_3_MOVETOSTAGE4_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_3 movestage4 require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('get ingredient:the-kettlewithwater')

    def PRO_3_MOVETOSTAGE4_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_3 movestage4 require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_3 movestage4 require physical help to continue')

    def PRO_3_MOVETOSTAGE4_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_3 movestage4 require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('get ingredient:the-kettlewithwater')

    def PRO_3_MOVETOSTAGE4_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_3 movestage4 require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAILED AND CONTINUE   ------------------------------------------"
        goal.set('pro_3 movestage4 require physical help incapable')

    def PRO_3_MOVETOSTAGE4_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_3 movestage4 require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('get ingredient:the-kettlewithwater')

## END OF TRANSITION END STAGE 3

### STAGE 4 ###

    ## 6 MEMORY RETRIEVAL

    def PRO_4_GET_kettlewithwater(goal="get ingredient:the-kettlewithwater"):
        print "                 ### Stage 4 ###"
        print "The subject is requesting the kettlewithwater from the DM"
        DM.request('ingredient:the-kettlewithwater')  # retrieve a chunk from DM into the DM buffer
        goal.set('find ingredient:the-kettlewithwater')

    def PRO_4_GET_kettlewithwater_SUCCESS_RETRIEVAL(goal="find ingredient:the-kettlewithwater", DMbuffer='ingredient:the-kettlewithwater'):
        print "DM:  The subject found in the DM: KETTLEWITHWATER"
        DM.add('ingredient:the-kettlewithwater')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()  # this is automatic in Lisp implementation
        goal.set('get ingredient:the-teabagmug')

    def PRO_4_GET_kettlewithwater_FORGET_RETRIEVAL(goal="find ingredient:the-kettlewithwater", DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM IN KETTLE-WATER."
        goal.set('find ingredient-the-kettlewithwater ask chunk help')

    def PRO_4_GET_kettlewithwater_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find ingredient:the-kettlewithwater', DMbuffer='ingredient:!the-kettlewithwater'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE!!!"
        DMbuffer.clear()
        goal.set('find ingredient-the-kettlewithwater ask chunk help')

    # BOOST ACTIVATION CHUNK 6
    def PRO_4_GET_kettlewithwater_ASK_CHUNK_HELP(goal="find ingredient-the-kettlewithwater ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE KETTLEWITHWATER WITH CHUNK ACTIVATION"
        DM.add('ingredient:the-kettlewithwater')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get ingredient:the-kettlewithwater')

    ##  FINISHED 6 MEMORY RETRIEVAL

    ## 7 MEMORY RETRIEVAL

    def PRO_4_GET_theteabagmug(goal="get ingredient:the-teabagmug"):
        print "The subject is requesting the teabagmug from the DM"
        DM.request('ingredient:the-teabagmug')  # retrieve a chunk from DM into the DM buffer
        goal.set('find ingredient:the-teabagmug')

    def PRO_4_GET_theteabagmug_SUCCESS_RETRIEVAL(goal="find ingredient:the-teabagmug", DMbuffer='ingredient:the-teabagmug'):
        print "DM:  The subject found in the DM: TEABAGMUG"
        DM.add('ingredient:the-teabagmug')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()  # this is automatic in Lisp implementation
        goal.set('do pour')

    def PRO_4_GET_theteabagmug_FORGET_RETRIEVAL(goal='find ingredient:the-teabagmug', DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM IN TEABAGMUG."
        #DM = 'error:False'
        goal.set('find ingredient-the-teabagmug ask chunk help')

    def PRO_4_GET_theteabagmug_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find ingredient:the-teabagmug', DMbuffer='ingredient:!the-teabagmug'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE!!!"
        DMbuffer.clear()
        goal.set('find ingredient-the-teabagmug ask chunk help')

    # BOOST ACTIVATION CHUNK 7
    def PRO_4_GET_theteabagmug_ASK_CHUNK_HELP(goal="find ingredient-the-teabagmug ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE TEABAGMUG WITH CHUNK ACTIVATION"
        DM.add('ingredient:the-teabagmug')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get ingredient:the-teabagmug')

    ##  FINISHED 7 MEMORY RETRIEVAL

    def PRO_4_pour(goal="do pour", utility=params.utility_success):
        print "The subject is pouring water into the mug."
        goal.set('do let34')

    # 3rd SAFETY BEHAVIOR DO POUR ERROR CONFLICT ERRORS, THE SUBJECT DROPS THE WATER ON HIS HANDS

    def PRO_4_pour_CONFLICT_ERROR_SAFETY(goal='do pour', utility=params.utility_fail):
        print "-------------------  POUR WATER ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_4 pour error initiate help')

    def PRO_4_pour_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_4 pour error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_4 pour require verbal clues')

    def PRO_4_pour_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_4 pour require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('do let34')

    def PRO_4_pour_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_4 pour require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_4 pour require physical help to continue')

    def PRO_4_pour_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_4 pour require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('do let34')

    def PRO_4_pour_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_4 pour require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAIL AND CONTINUE   ------------------------------------------"
        goal.set('pro_4 pour require physical help to continue incapable')

    def PRO_4_pour_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_4 pour require physical help to continue incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('do let34')

    ## END OF 3rd SAFETY BEHAVIOR DO POUR ERROR CONFLICT ERRORS

    def PRO_4_let34(goal="do let34", utility=params.utility_success):
        print "The subject is letting 3-4 minutes for the tea to be ready."
        goal.set('do removeteabag')

    # BEHAVIOR COMPLETION ERROR, REPEAT ACTION OVER AND OVER

    def PRO_4_do_let34_CONFLICT_ERROR_COMPLETION_ERROR(goal='do let34', utility=params.utility_fail):
        print "-------------------  COMPLETION ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_4 let34 error initiate help')

    def PRO_4_do_let34_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_4 let34 error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_4 let34 require verbal clues')

    def PRO_4_do_let34_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_4 let34 require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('do removeteabag')

    def PRO_4_do_let34_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_4 let34 require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_4 let34 require physical help to continue')

    def PRO_4_do_let34_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_4 let34 require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('do removeteabag')

    def PRO_4_do_let34_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_4 let34 require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAIL AND CONTINUE   ------------------------------------------"
        goal.set('pro_4 let34 require physical help to continue incapable')

    def PRO_4_do_let34_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_4 let34 require physical help to continue incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('do removeteabag')

    ## END OF BEHAVIOR DO SAME ACTION

    def PRO_4_removeteabag(goal="do removeteabag"):
        print "The subject is about to remove the teabag."
        goal.set('get ustensile:the-bowl')

    ## 8 MEMORY RETRIEVAL

    def PRO_4_GET_bowl(goal="get ustensile:the-bowl"):
        print "The subject is requesting the bowl from the DM"
        DM.request('ustensile:the-bowl')  # retrieve a chunk from DM into the DM buffer
        goal.set('find ustensile:the-bowl')

    def PRO_4_GET_bowl_SUCCESS_RETRIEVAL(goal="find ustensile:the-bowl", DMbuffer='ustensile:the-bowl'):
        print "DM:  The subject found in the DM: BOWL"
        DM.add('ustensile:the-bowl')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()  # this is automatic in Lisp implementation
        goal.set('do movethebag')

    def PRO_4_GET_bowl_FORGET_RETRIEVAL(goal='find ustensile:the-bowl', DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM IN BOWL."
        goal.set('find ustensile-the-bowl ask chunk help')

    def PRO_4_GET_bowl_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find ustensile:the-bowl', DMbuffer='ustensile:!the-bowl'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE!!!"
        DMbuffer.clear()
        goal.set('find ustensile-the-bowl ask chunk help')

    # BOOST ACTIVATION CHUNK 8
    def PRO_4_GET_bowl_ASK_CHUNK_HELP(goal="find ustensile-the-bowl ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE BOWL WITH CHUNK ACTIVATION"
        DM.add('ustensile:the-bowl')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get ustensile:the-bowl')

    ##  FINISHED 8 MEMORY RETRIEVAL

    def PRO_4_movethebag(goal="do movethebag", utility=params.utility_success):
        print "The subject is placing the teabag to the bowl."
        print "A new chuck created here with value - ingredient:the-readytea."
        DM.add('ingredient:the-readytea')
        DMbuffer.clear()
        goal.set('do movetostage5')

    # BEHAVIOR 4ND STAGE CONFLICT ERRORS

    def PRO_4_MOVETOSTAGE5_CONFLICT_ERROR_INIT(goal='do movethebag', utility=params.utility_fail):
        print "-------------------  STAGE 4 TRANSITION ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_4 movestage5 error initiate help')

    def PRO_4_MOVETOSTAGE5_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_4 movestage5 error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_4 movestage5 require verbal clues')

    def PRO_4_MOVETOSTAGE5_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_4 movestage5 require verbal clues', utility=params.utility_success + params.verbal_factor):
        DM.add('ingredient:the-readytea')
        DMbuffer.clear()
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('do movetostage5')

    def PRO_4_MOVETOSTAGE5_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_4 movestage5 require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_4 movestage5 require physical help to continue')

    def PRO_4_MOVETOSTAGE5_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_4 movestage5 require physical help to continue', utility=params.utility_success + params.physical_factor):
        DM.add('ingredient:the-readytea')
        DMbuffer.clear()
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('do movetostage5')

    def PRO_4_MOVETOSTAGE5_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_4 movestage5 require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAILED AND CONTINUE   ------------------------------------------"
        goal.set('pro_4 movestage5 require physical help incapable')

    def PRO_4_MOVETOSTAGE5_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_4 movestage5 require physical help incapable'):
        DM.add('ingredient:the-readytea')
        DMbuffer.clear()
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('do movetostage5')

    ## END OF TRANSITION END STAGE 4


### STAGE 5 ###

    def PRO_5_clean(goal="do movetostage5"):
        print "                 ### Stage 5 ###"
        print "The subject is cleaning."
        goal.set('get ingredient:the-readytea')

    ## 9 MEMORY RETRIEVAL

    def PRO_5_GET_thereadytea(goal="get ingredient:the-readytea"):
        print "The subject is requesting the ready tea from the DM"
        DM.request('ingredient:the-readytea') # retrieve a chunk from DM into the DM buffer
        goal.set('find ingredient:the-readytea')

    def PRO_5_GET_thereadytea_SUCCESS_RETRIEVAL(goal="find ingredient:the-readytea", DMbuffer='ingredient:the-readytea'):
        print "DM:  The subject found in the DM: READYTEA"
        DM.add('ingredient:the-readytea')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()  # this is automatic in Lisp implementation
        print "Done"
        goal.set('stop')

    def PRO_5_GET_thereadytea_FORGET_RETRIEVAL(goal='find ingredient:the-readytea', DMbuffer=None, DM='error:True'):
        DMbuffer.clear()
        print "FORGET RETRIEVAL PROBLEM IN READY TEA."
        print "Done"
        goal.set('find ingredient-the-readytea ask chunk help')

    def PRO_5_GET_thereadytea_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find ingredient:the-readytea', DMbuffer='ingredient:!the-readytea'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE!!!"
        DMbuffer.clear()
        goal.set('find ingredient-the-readytea ask chunk help')

    # BOOST ACTIVATION CHUNK 9
    def PRO_5_GET_thereadytea_ASK_CHUNK_HELP(goal="find ingredient-the-readytea ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE READYTEA WITH CHUNK ACTIVATION"
        DM.add('ingredient:the-readytea')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get ingredient:the-readytea')

    ##  FINISHED 9 MEMORY RETRIEVAL

    def stop_production(goal='stop'):
        #print "I AM THE TEA FILE!!!"
        self.stop()


class MyEnvironment(ccm.Model):
    pass


dementia_user = MyAgent()  # name the agent
smart_home = MyEnvironment()  # name the environment
smart_home.agent = dementia_user  # put the agent in the environment
log = ccm.log(html=True)
ccm.log_everything(smart_home)  # print out what happens in the environment
smart_home.run()  # run the environment
#smarthome.run(1000)  # run the environment
ccm.finished()  # stop the environment
