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

    # #PARTIAL MATCHING OF CHUNKS, PARTIAL SIMILARITY TO CREATE COMMISSION ERRORS
    partial = Partial(DM, strength=params.Ps, limit=-1.0)  # turn on partial matching
    partial.similarity('the-towel', 'the-soap', params.similarity) # very similar

    # #utility conflicts with noise using PMPGC
    pgc = PMPGC()
    pmnoise = PMNoise(noise=params.e_production_utility_transitory_noise)

    def init():

        DM.add('item:the-soap')
        DM.add('item:the-towel')
        DM.add('item:the-tapon')
        DM.add('item:the-tapoff')

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

# END OF BEHAVIOR INITIATION ERRORS

### STAGE 1 ###

    def PRO_1_watering(goal="do water"):
        print "                 ### Stage 1 ###"
        print "The subject is looking moving forward to tap the water on."
        goal.set('get item:the-tapon')

    ##1 MEMORY RETRIEVAL

    def PRO_1_GET_tapon(goal="get item:the-tapon"):
        print "The subject is requesting the tapon location from the DM."
        DM.request('item:the-tapon') # retrieve a chunk from DM into the DM buffer
        goal.set('find item:the-tapon')

    def PRO_1_GET_tapon_SUCCESS_RETRIEVAL(goal="find item:the-tapon",     DMbuffer='item:the-tapon'):
        print "DM:  The subject found in the DM: TAPON LOCATION."
        DM.add('item:the-tapon') # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('wateron')

    def PRO_1_GET_tapon_FORGET_RETRIEVAL(goal="find item:the-tapon",      DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM WITH TAPON."
        goal.set('find item-the-tapon ask chunk help')

    def PRO_1_GET_tapon_CONFUSED_RETRIEVAL(goal='find item:the-tapon',    DMbuffer='item:the-XXX'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED THE XXX."
        DMbuffer.clear()
        goal.set('find item-the-tapon ask chunk help')

    def PRO_1_GET_tapon_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find item:the-tapon', DMbuffer='item:!the-tapon item:!XXX'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE."
        DMbuffer.clear()
        goal.set('find item-the-tapon ask chunk help')

    # BOOST ACTIVATION CHUNK 1
    def PRO_1_GET_tapon_ASK_CHUNK_HELP(goal="find item-the-tapon ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE TAP WATER ON WITH CHUNK ACTIVATION."
        DM.add('item:the-tapon') # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get item:the-tapon')

    ## FINISHED 1 MEMORY RETRIEVAL

    def PRO_1_wateron(goal="wateron"):
        print "The subject is turning on the tap water. "
        goal.set('get item:the-soap')

    ## 2  MEMORY RETRIEVAL

    def PRO_1_GET_soap(goal="get item:the-soap"):
        print "The subject is requesting the soap from the DM."
        DM.request('item:the-soap')  # retrieve a chunk from DM into the DM buffer
        goal.set('find item:the-soap')

    def PRO_1_GET_soap_SUCCESS_RETRIEVAL(goal="find item:the-soap", DMbuffer='item:the-soap'):
        print "DM:  The subject found in the DM: SOAP."
        DM.add('item:the-soap')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('applysoap')

    def PRO_1_GET_soap_FORGET_RETRIEVAL(goal="find item:the-soap", DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM WITH TAP."
        goal.set('find item-the-soap ask chunk help')

    def PRO_1_GET_soap_CONFUSED_RETRIEVAL(goal='find item:the-soap', DMbuffer='item:the-towel'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED THE TOWEL."
        DMbuffer.clear()
        goal.set('find item-the-soap ask chunk help')

    def PRO_1_GET_soap_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find item:the-soap', DMbuffer='item:!the-soap item:!towel'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE."
        DMbuffer.clear()
        goal.set('find item-the-soap ask chunk help')

    # BOOST ACTIVATION CHUNK 2

    def PRO_1_GET_soap_ASK_CHUNK_HELP(goal="find item-the-soap ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE SOAP WITH CHUNK ACTIVATION."
        DM.add('item:the-soap')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get item:the-soap')

    ## FINISHED 2 MEMORY RETRIEVAL

    # 1st SAFETY BEHAVIOR DO TURN ON STOVE CONFLICT ERRORS -- SAFETY ERROR

    def PRO_1_applysoap(goal="applysoap", utility=params.utility_success):
        print "The subject is applying soap to the hands."
        goal.set('do washhands')

    def PRO_1_applysoap_CONFLICT_ERROR_SAFETY(goal='applysoap', utility=params.utility_fail):
        print "-------------------  SAFETY ERROR APPLY SOAP ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_1 applysoap error initiate help')

    def PRO_1_applysoap_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_1 applysoap error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_1 applysoap require verbal clues')

    def PRO_1_applysoap_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_1 applysoap require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('do washhands')

    def PRO_1_applysoap_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_1 applysoap require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_1 applysoap require physical help to continue')

    def PRO_1_applysoap_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_1 applysoap require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('do washhands')

    def PRO_1_applysoap_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_1 applysoap require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAIL AND CONTINUE   ------------------------------------------"
        goal.set('pro_1 applysoap require physical help incapable')

    def PRO_1_applysoap_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_1 applysoap require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('do washhands')

    ## END OF 1st SAFETY BEHAVIOR DO TURN OFF STOVE CONFLICT ERRORS -- SAFERY ERROR

    def PRO_1_washhands(goal="do washhands", utility=params.utility_success):
        print "The subject is washing the hands."
        goal.set('movestage2')

    # 1 BEHAVIOR COMPLETION ERROR, REPEAT ACTION OVER AND OVER

    def PRO_1_do_washhands_CONFLICT_ERROR_COMPLETION_ERROR(goal='do washhands', utility=params.utility_fail):
        print "-------------------  COMPLETION ERROR WASHING HANDS, NEED HELP    ------------------------------------------"
        goal.set('pro_1 washhands error initiate help')

    def PRO_1_do_washhands_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_1 washhands error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_1 washhands require verbal clues')

    def PRO_1_do_washhands_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_1 washhands require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('movestage2')

    def PRO_1_do_washhands_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_1 washhands require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_1 washhands require physical help to continue')

    def PRO_1_do_washhands_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_1 washhands require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('movestage2')

    def PRO_1_do_washhands_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_1 washhands require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAIL AND CONTINUE   ------------------------------------------"
        goal.set('pro_1 washhands require physical help by caregiver')

    def PRO_1_do_washhands_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_1 washhands require physical help by caregiver'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('movestage2')

    ## END OF 1 BEHAVIOR DO SAME ACTION

    def PRO_1_movestage2(goal="movestage2", utility=params.utility_success):
        print "The subject is moving to stage 2."
        goal.set('rinsehands')

    # BEHAVIOR 1 STAGE CONFLICT ERRORS

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_INIT(goal='movestage2', utility=params.utility_fail):
        print "-------------------  STAGE 1 TRANSITION ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_1 movestage2 error initiate help')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_1 movestage2 error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_1 movestage2 require verbal clues')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_1 movestage2 require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('rinsehands')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_1 movestage2 require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_1 movestage2 require physical help to continue')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_1 movestage2 require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('rinsehands')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_1 movestage2 require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAILED AND CONTINUE   ------------------------------------------"
        goal.set('pro_1 movestage2 require physical help incapable')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE( goal='pro_1 movestage2 require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('rinsehands')

    ## END OF TRANSITION END STAGE 1

    ### STAGE 2 ###

    def PRO_2_rinsehands( goal='rinsehands'):
        print "                 ### Stage 2 ###"
        print "The subject is rinsing the hands."
        goal.set('get item:the-towel')

    ## 3  MEMORY RETRIEVAL

    def PRO_2_GET_towel(goal="get item:the-towel"):
        print "The subject is requesting the towel from the DM."
        DM.request('item:the-towel')  # retrieve a chunk from DM into the DM buffer
        goal.set('find item:the-towel')

    def PRO_2_GET_towel_SUCCESS_RETRIEVAL(goal="find item:the-towel", DMbuffer='item:the-towel'):
        print "DM:  The subject found in the DM: TOWEL."
        DM.add('item:the-towel')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('dryhands')

    def PRO_2_GET_towel_FORGET_RETRIEVAL(goal="find item:the-towel", DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM WITH TOWEL."
        goal.set('find item-the-towel ask chunk help')

    def PRO_2_GET_towel_CONFUSED_RETRIEVAL(goal='find item:the-towel', DMbuffer='item:the-soap'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED THE SOAP."
        DMbuffer.clear()
        goal.set('find item-the-towel ask chunk help')

    def PRO_2_GET_towel_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find item:the-towel', DMbuffer='item:!the-towel item:!soap'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE."
        DMbuffer.clear()
        goal.set('find item-the-towel ask chunk help')

    # BOOST ACTIVATION CHUNK 3

    def PRO_2_GET_towel_ASK_CHUNK_HELP(goal="find item-the-towel ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE TOWEL WITH CHUNK ACTIVATION."
        DM.add('item:the-towel')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get item:the-towel')

    ## FINISHED 3 MEMORY RETRIEVAL

    def PRO_2_dryhands( goal='dryhands'):
        print "The subject is drying the hands with the towel."
        goal.set('movetostage3')

    def PRO_2_movetostage3(goal="movetostage3", utility=params.utility_success):
        print "The subject is moving to stage 3."
        goal.set('tapwateroff')

    #  2ND STAGE CONFLICT ERRORS

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_INIT(goal='movetostage3', utility=params.utility_fail):
        print "-------------------  STAGE 2 TRANSITION ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_2 movestage3 error initiate help')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_2 movestage3 error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_2 movestage3 require verbal clues')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_2 movestage3 require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('tapwateroff')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_2 movestage3 require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_2 movestage3 require physical help to continue')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_2 movestage3 require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('tapwateroff')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_2 movestage3 require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAILED AND CONTINUE   ------------------------------------------"
        goal.set('pro_2 movestage3 require physical help incapable')

    def PRO_2_MOVETOSTAGE3_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_2 movestage3 require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('tapwateroff')

    ## END OF TRANSITION END STAGE 2

    ### STAGE 3 ###

    def PRO_3_tapwateroff(goal='tapwateroff'):
        print "                 ### Stage 3 -- LAST ONE ###"
        print "The subject is in stage 3 and looking for the tap off to stop the watering."
        goal.set('get item:the-tapoff')

    ## 4 MEMORY RETRIEVAL

    def PRO_3_GET_tapoff(goal="get item:the-tapoff"):
        print "The subject is requesting the tapoff location from the DM."
        DM.request('item:the-tapoff') # retrieve a chunk from DM into the DM buffer
        goal.set('find item:the-tapoff')

    def PRO_3_GET_tapoff_SUCCESS_RETRIEVAL(goal="find item:the-tapoff",     DMbuffer='item:the-tapoff'):
        print "DM:  The subject found in the DM: TAPOFF LOCATION."
        DM.add('item:the-tapoff') # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('waterofffinish')

    def PRO_3_GET_tapoff_FORGET_RETRIEVAL(goal="find item:the-tapoff",      DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM WITH TAPOFF."
        goal.set('find item-the-tapoff ask chunk help')

    def PRO_3_GET_tapoff_CONFUSED_RETRIEVAL(goal='find item:the-tapoff',    DMbuffer='item:the-XXX'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED THE XXX."
        DMbuffer.clear()
        goal.set('find item-the-tapoff ask chunk help')

    def PRO_3_GET_tapoff_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find item:the-tapoff', DMbuffer='item:!the-tapoff item:!XXX'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE."
        DMbuffer.clear()
        goal.set('find item-the-tapoff ask chunk help')

    # BOOST ACTIVATION CHUNK 4
    def PRO_3_GET_tapoff_ASK_CHUNK_HELP(goal="find item-the-tapoff ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE TAP WATER OFF WITH CHUNK ACTIVATION."
        DM.add('item:the-tapoff') # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get item:the-tapoff')

    ## FINISHED 4 MEMORY RETRIEVAL

    def PRO_3_waterofffinish(goal='waterofffinish'):
        print "The subject is in stage 3 and finishing turning off the water to finish the activity."
        goal.set('finish')

    # 2 BEHAVIOR COMPLETION ERROR, REPEAT ACTION OVER AND OVER

    def PRO_3_dofinish(goal='finish', utility=params.utility_success):
        print "The subject is finishing the activity."
        goal.set('stop')

    def PRO_3_do_dofinish_CONFLICT_ERROR_COMPLETION_ERROR(goal='finish', utility=params.utility_fail):
        print "-------------------  COMPLETION ERROR FINISHING ACTIVITY, NEED HELP    ------------------------------------------"
        goal.set('pro_3 dofinish error initiate help')

    def PRO_3_do_dofinish_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_3 dofinish error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_3 dofinish require verbal clues')

    def PRO_3_do_dofinish_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_3 dofinish require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('stop')

    def PRO_3_do_dofinish_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_3 dofinish require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_3 dofinish require physical help to continue')

    def PRO_3_do_dofinish_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_3 dofinish require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('stop')

    def PRO_3_do_dofinish_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_3 dofinish require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAIL AND CONTINUE   ------------------------------------------"
        goal.set('pro_3 dofinish require physical help by caregiver')

    def PRO_3_do_dofinish_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_3 dofinish require physical help by caregiver'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('stop')

    ## END OF 2 BEHAVIOR DO SAME ACTION

    def stop_production(goal='stop'):
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
