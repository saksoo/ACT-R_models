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
    partial.similarity('item:shirt', 'item:trousers', params.similarity) # very similar
    #
    # #utility conflicts with noise using PMPGC
    pgc = PMPGC()
    pmnoise = PMNoise(noise=params.e_production_utility_transitory_noise)

    def init():

        DM.add('item:sock1')
        DM.add('item:sock2')
        DM.add('item:shirt')
        DM.add('item:trousers')
        DM.add('item:shoe1')
        DM.add('item:shoe2')

        goal.set('ready-to-proceed')

## READY TO PROCEED

    def PRO_0_initiate(goal='ready-to-proceed'):
        print "Ready to start the task."
        goal.set('proceed')

    def PRO_0_proceed_CORRECT(goal='proceed', utility=params.utility_success):
        print "The subject has initiated the activity."
        goal.set('get clothes shirt')

#BEHAVIOR INITIATION ERRORS

    def PRO_0_proceed_CONFLICT_INITIATION(goal='proceed', utility=params.utility_fail):  # this production competes with the other proceed production
        print "-------------------  INITIATION ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_0 error initiate help')

    def PRO_0_proceed_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_0 error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_0 error require verbal clues')

    def PRO_0_proceed_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_0 error require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('get clothes shirt')

    def PRO_0_proceed_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_0 error require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_0 error require physical help to continue')

    def PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_0 error require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('get clothes shirt')

    def PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_0 error require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAILED AND CONTINUE   ------------------------------------------"
        goal.set('pro_0 error require physical help incapable')

    def PRO_0_proceed_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_0 error require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('get clothes shirt')

# END OF BEHAVIOR INITIATION ERRORS

    ######## STAGE 1 ################

    def PRO_1_getshirt(goal="get clothes shirt"):
        print "                 ### Stage 1 ###"
        print "The subject is looking moving forward to find and put the shirt on."
        goal.set('get item:shirt')

    ##1 MEMORY RETRIEVAL

    def PRO_1_GET_shirt(goal="get item:shirt"):
        print "The subject is requesting the shirt location from the DM."
        DM.request('item:shirt') # retrieve a chunk from DM into the DM buffer
        goal.set('find item:shirt')

    def PRO_1_GET_shirt_SUCCESS_RETRIEVAL(goal="find item:shirt", DMbuffer='item:shirt'):
        print "DM:  The subject found in the DM: SHIRT."
        DM.add('item:shirt') # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('action:start_shirt')

    def PRO_1_GET_shirt_FORGET_RETRIEVAL(goal="find item:shirt", DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM WITH SHIRT."
        goal.set('find item-shirt ask chunk help')

    def PRO_1_GET_shirt_CONFUSED_RETRIEVAL(goal='find item:shirt', DMbuffer='item:trousers'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED THE TROUSERS."
        DMbuffer.clear()
        goal.set('find item-shirt ask chunk help')

    def PRO_1_GET_shirt_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find item:shirt', DMbuffer='item:!shirt item:!trousers'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE."
        DMbuffer.clear()
        goal.set('find item-shirt ask chunk help')

    # BOOST ACTIVATION CHUNK 1
    def PRO_1_GET_shirt_ASK_CHUNK_HELP(goal="find item-shirt ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE SHIRT WITH CHUNK ACTIVATION."
        DM.add('item:shirt') # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get item:shirt')

    ## FINISHED 1 MEMORY RETRIEVAL

    def PRO_1_put_shirt(goal='action:start_shirt'):
        print "Start putting the shirt."
        goal.set('action:puthand1')

    def PRO_1_put_hand1(goal='action:puthand1'):
        print "I have put one hand in."
        goal.set('action:puthead')

    def PRO_1_put_head(goal='action:puthead', utility=params.utility_success):
        print "I have put the head in."
        goal.set('action:puthand2')

    # 1 BEHAVIOR COMPLETION ERROR, REPEAT ACTION OVER AND OVER

    def PRO_1_put_head_CONFLICT_ERROR_COMPLETION_ERROR(goal='action:puthead', utility=params.utility_fail):
        print "-------------------  COMPLETION ERROR PUT HEAD, NEED HELP    ------------------------------------------"
        goal.set('pro_1 puthead error initiate help')

    def PRO_1_put_head_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_1 puthead error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_1 puthead require verbal clues')

    def PRO_1_put_head_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_1 puthead require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('action:puthand2')

    def PRO_1_put_head_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_1 puthead require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_1 puthead require physical help to continue')

    def PRO_1_put_head_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_1 puthead require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('action:puthand2')

    def PRO_1_put_head_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_1 puthead require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAIL AND CONTINUE   ------------------------------------------"
        goal.set('pro_1 puthead require physical help by caregiver')

    def PRO_1_put_head_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_1 puthead require physical help by caregiver'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('action:puthand2')

    ## END OF 1 BEHAVIOR DO SAME ACTION

    def PRO_1_put_hand2(goal='action:puthand2', utility=params.utility_success):
        print "I have put two hands in."
        goal.set('action:putshirtplacein')

    # 1st SAFETY BEHAVIOR CONFLICT ERRORS -- SAFETY ERROR

    def PRO_1_putshirtwrong_CONFLICT_ERROR_SAFETY(goal='action:puthand2', utility=params.utility_fail):
        print "-------------------  SAFETY ERROR PUT SHIRT INCORRECTLY, NEED HELP    ------------------------------------------"
        goal.set('pro_1 putshirtwrong error initiate help')

    def PRO_1_putshirtwrong_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_1 putshirtwrong error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_1 putshirtwrong require verbal clues')

    def PRO_1_putshirtwrong_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_1 putshirtwrong require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('action:putshirtplacein')

    def PRO_1_putshirtwrong_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_1 putshirtwrong require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_1 putshirtwrong require physical help to continue')

    def PRO_1_putshirtwrong_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_1 putshirtwrong require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('action:putshirtplacein')

    def PRO_1_putshirtwrong_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_1 putshirtwrong require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAIL AND CONTINUE   ------------------------------------------"
        goal.set('pro_1 putshirtwrong require physical help incapable')

    def PRO_1_putshirtwrong_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_1 putshirtwrong require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('action:putshirtplacein')

    ## END OF 1st SAFETY BEHAVIOR CONFLICT ERRORS -- SAFERY ERROR

    def PRO_1_put_shirt_place_in(goal='action:putshirtplacein'):
        print "I have put the shirt."
        goal.set('action:stop_shirt')

    def PRO_1_MOVETOSTAGE2(goal='action:stop_shirt', utility=params.utility_success):
        print "I am moving to stage 2."
        goal.set('movetostage2')

    # BEHAVIOR 1 STAGE CONFLICT ERRORS

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_INIT(goal='action:stop_shirt', utility=params.utility_fail):
        print "-------------------  STAGE 1 TRANSITION ERROR, NEED HELP    ------------------------------------------"
        goal.set('pro_1 movestage2 error initiate help')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_1 movestage2 error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_1 movestage2 require verbal clues')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_1 movestage2 require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('movetostage2')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_1 movestage2 require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_1 movestage2 require physical help to continue')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_1 movestage2 require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('movetostage2')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_1 movestage2 require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAILED AND CONTINUE   ------------------------------------------"
        goal.set('pro_1 movestage2 require physical help incapable')

    def PRO_1_MOVETOSTAGE2_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_1 movestage2 require physical help incapable'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('movetostage2')

    ## END OF TRANSITION END STAGE 1

    ######## STAGE 2 ################

    def PRO_2_stage2initiate(goal='movetostage2'):
        print "                 ### Stage 2 ###"
        print "I am looking to find the trousers."
        goal.set('get item:trousers')

    ##  2  MEMORY RETRIEVAL  ########

    def PRO_2_GET_trousers(goal="get item:trousers"):
        print "The subject is requesting the trousers location from the DM."
        DM.request('item:trousers')  # retrieve a chunk from DM into the DM buffer
        goal.set('find item:trousers')

    def PRO_2_GET_trousers_SUCCESS_RETRIEVAL(goal="find item:trousers", DMbuffer='item:trousers'):
        print "DM:  The subject found in the DM: TROUSERS."
        DM.add('item:trousers')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('action:start_trousers')

    def PRO_2_GET_trousers_FORGET_RETRIEVAL(goal="find item:trousers", DMbuffer=None, DM='error:True'):
        print "FORGET RETRIEVAL PROBLEM WITH TROUSERS."
        goal.set('find item-trousers ask chunk help')

    def PRO_2_GET_trousers_CONFUSED_RETRIEVAL(goal='find item:trousers', DMbuffer='item:shirt'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED THE SHIRT."
        DMbuffer.clear()
        goal.set('find item-trousers ask chunk help')

    def PRO_2_GET_trousers_CONFUSED_WITH_OTHER_CHUNK_RETRIEVAL(goal='find item:trousers', DMbuffer='item:!shirt item:!trousers'):
        print "CONFUSED RETRIEVAL PROBLEM I RETRIEVED SOMETHING ELSE."
        DMbuffer.clear()
        goal.set('find item-trousers ask chunk help')

    # BOOST ACTIVATION CHUNK 2

    def PRO_2_GET_trousers_ASK_CHUNK_HELP(goal="find item-trousers ask chunk help"):
        print "DM: I AM HELPING THE SUBJECT TO REMEMBER THE SHIRT WITH CHUNK ACTIVATION."
        DM.add('item:trousers')  # each time you put something in memory (DM.add) it increases
        DMbuffer.clear()
        goal.set('get item:trousers')

    ## FINISHED 2 MEMORY RETRIEVAL

    def PRO_2_put_trousers(goal='action:start_trousers'):
        print "Start putting the trousers."
        goal.set('action:putweakleg')

    def PRO_2_put_weakleg(goal='action:putweakleg'):
        print "I have put the weak leg in."
        goal.set('action:putotherleg')

    def PRO_2_put_otherleg(goal='action:putotherleg'):
        print "I have put the two legs in."
        goal.set('action:pulltrousers')

    def PRO_2_pull_trousers(goal='action:pulltrousers', utility=params.utility_success):
        print "I have pulled the trousers in."
        goal.set('action:puttrousersplacein')

    # 2 BEHAVIOR COMPLETION ERROR, REPEAT ACTION OVER AND OVER

    def PRO_2_pulltrousers_CONFLICT_ERROR_COMPLETION_ERROR(goal='action:pulltrousers', utility=params.utility_fail):
        print "-------------------  COMPLETION ERROR PULL TROUSERS, NEED HELP    ------------------------------------------"
        goal.set('pro_1 pulltrousers error initiate help')

    def PRO_2_pulltrousers_CONFLICT_ERROR_ASK_VERBAL_HELP(goal='pro_1 pulltrousers error initiate help'):
        print "-------------------  REQUIRE VERBAL HELP ------------------------------------------"
        goal.set('pro_1 pulltrousers require verbal clues')

    def PRO_2_pulltrousers_CONFLICT_ERROR_ASK_VERBAL_HELP_SUCCESS(goal='pro_1 pulltrousers require verbal clues', utility=params.utility_success + params.verbal_factor):
        print "-------------------  VERBAL HELP SUCCESS ------------------------------------------"
        goal.set('action:puttrousersplacein')

    def PRO_2_pulltrousers_CONFLICT_ERROR_ASK_VERBAL_HELP_FAIL(goal='pro_1 pulltrousers require verbal clues', utility=params.utility_fail):
        print "-------------------  VERBAL HELP FAILED  ------------------------------------------"
        goal.set('pro_1 pulltrousers require physical help to continue')

    def PRO_2_pulltrousers_CONFLICT_ERROR_PHYSICAL_HELP_SUCCESS(goal='pro_1 pulltrousers require physical help to continue', utility=params.utility_success + params.physical_factor):
        print "-------------------  REQUIRE PHYSICAL HELP SUCCESS AND CONTINUE   ------------------------------------------"
        goal.set('action:puttrousersplacein')

    def PRO_2_pulltrousers_CONFLICT_ERROR_PHYSICAL_HELP_FAIL(goal='pro_1 pulltrousers require physical help to continue', utility=params.utility_fail):
        print "-------------------  REQUIRE PHYSICAL HELP FAIL AND CONTINUE   ------------------------------------------"
        goal.set('pro_1 pulltrousers require physical help by caregiver')

    def PRO_2_pulltrousers_CONFLICT_ERROR_PHYSICAL_HELP_INCAPABLE(goal='pro_1 pulltrousers require physical help by caregiver'):
        print "-------------------  INCAPABLE AND CONTINUE   ------------------------------------------"
        goal.set('action:puttrousersplacein')

    ## END OF 2 BEHAVIOR DO SAME ACTION

    def PRO_2_put_trousers_place_in(goal='action:puttrousersplacein'):
        print "I have put the trousers in."
        goal.set('action:stop_trousers')

    def PRO_2_stop_trousers(goal='action:stop_trousers'):
        print "I have completed the activity."
        goal.set('stop')

    ######## STAGE 3 ################

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
