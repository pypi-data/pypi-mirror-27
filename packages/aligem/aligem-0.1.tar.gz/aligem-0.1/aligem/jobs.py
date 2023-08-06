# Jobs handling suite

import subprocess
import argparse


def main() :
    print "Welcome to AliGEM | Jobs"

def exec_alien_cmd(process = [], verbose=False) :
    """
    Wrapper function to execude terminal commands within python based on subprocess package.
    Example of input process list ['alien_top','-all_status','-user',str(user)]
     - first element is the command
     - following arguments is parameter (& values) sequence
    TODO: ATM it is handled by try-except clause, a Popen might be more suitable (and stable?) solution
    """

    if not process :
        print 'Process list is empty. Nothing to execute!'
        return
    try :
        output = subprocess.check_output(process)
        return output
    except subprocess.CalledProcessError as error :
        if(verbose) :
            print("CalledProcessError exception caught!")
            print("Error return code:\n" + str(error.returncode))
            print("Error cmd:\n" + str(error.cmd))
            print("Error output:\n" + str(error.output))
        return error.output
    return

def fetch_jobs(user,verbose=False) :
    """ Returns list of job dicts from Grid query for a single user """
    job_string = exec_alien_cmd(['alien_top','-all_status','-user',str(user)],verbose=verbose)

    # stripping useless characters within jobs output
    job_string = job_string.replace(" ","") # removing whitespaces
    job_string = job_string.rstrip("\n\n") # stripping last \n\n to avoid empty entries
    jobs = job_string.split("\n\n")

    list_jobs = []
    for job in jobs :
        processed_job = process_single_job(job)
        if validate_single_job(processed_job) : list_jobs.append(processed_job)
    return list_jobs

def process_single_job(job='') :
    """ Returns a dict with a data from single job"""
    job = job.split("\t")

    if len(job) < 4 :
        return {}

    if job[4].startswith("pcapiserv") :
        job_type = 'master'
    else :
        job_type = 'subjob'

    single_job = { 'id':job[0], 'group':job_type, 'status':job[1], 'user':job[2], 'script':job[3], 'server':job[4] }
    return single_job

def validate_single_job(job,debug=False) :
    """ Returns True if job is valid, False otherwise """
    isOK = True
    if not job['id'].isdigit() :
        isOK = False
        if debug : print "job id '%s' not validated" % str(job['id'])

    if ( (job['group'] == 'master') and (not job['server'].startswith('pcapiserv')) ) :
        isOK = False
        if debug : print "job group '%s' not validated" % job['group']

    if (job['group'] == 'subjob') and (not job['server'].startswith('aliendb')) :
        isOK = False
        if debug : print "job group '%s' not validated" % job['group']

    if debug and (isOK == False) : print(job)
    return isOK

def get_status(user='vpacik',debug=True) :
    """
    Fetching jobs from Grid servers, sorting them according to their status and prints brief overview
    """

    if user == None :
        print 'User not specified. This might take long time. Aborted!'
        return

    jobs = fetch_jobs(str(user))

    master = []
    master_done = []
    master_split = []
    master_error = []
    master_inserting = []
    master_rest = []

    subjobs = []
    subjobs_done = []
    subjobs_running = []
    subjobs_waiting = []
    subjobs_assigned = []
    subjobs_started = []
    subjobs_saving = []
    subjobs_saved = []
    subjobs_errors = []
    subjobs_expired = []
    subjobs_zombie = []
    subjobs_rest = []

    print '######################################'
    print '  Jobs status for user "%s"' % user
    for job in jobs:

        if job['group'] == 'master' :
            # masterjob
            master.append(job)

            if job['status'].startswith('DONE') : master_done.append(job)
            elif job['status'] == 'SPLIT' : master_split.append(job)
            elif job['status'] == 'INSERTING' : master_inserting.append(job)
            elif job['status'].startswith('ERROR') : master_error.append(job)
            else : master_rest.append(job)

        elif job['group'] == 'subjob' :
            # subjobs
            subjobs.append(job)

            if job['status'] == 'RUNNING' : subjobs_running.append(job)
            elif job['status'].startswith('DONE') : subjobs_done.append(job)
            elif job['status'] == 'WAITING' : subjobs_waiting.append(job)
            elif job['status'] == 'ASSIGNED' : subjobs_assigned.append(job)
            elif job['status'] == 'STARTED' : subjobs_started.append(job)
            elif job['status'] == 'SAVING' : subjobs_saving.append(job)
            elif job['status'] == 'SAVED' : subjobs_saved.append(job)
            elif job['status'].startswith('ERROR') : subjobs_errors.append(job)
            elif job['status'] == 'EXPIRED' : subjobs_expired.append(job)
            elif job['status'] == 'ZOMBIE' : subjobs_zombie.append(job)
            else : subjobs_rest.append(job)

        else :
            print('Unknown job group : '+str(job['group']))



    num_masjob_all = len(master)
    num_masjob_done = len(master_done)
    num_masjob_split = len(master_split)
    num_masjob_inserting = len(master_inserting)
    num_masjob_error = len(master_error)
    num_masjob_rest = len(master_rest)

    num_subjob_all = len(subjobs)
    num_subjob_done = len(subjobs_done)
    num_subjob_run = len(subjobs_running)
    num_subjob_wait = len(subjobs_waiting)
    num_subjob_assign = len(subjobs_assigned)
    num_subjob_start = len(subjobs_started)
    num_subjob_saving = len(subjobs_saving)
    num_subjob_saved = len(subjobs_saved)
    num_subjob_error = len(subjobs_errors)
    num_subjob_expire = len(subjobs_expired)
    num_subjob_zombie = len(subjobs_zombie)
    num_subjob_rest = len(subjobs_rest)

    def printStatusLine(label, num, num_all) :
        perc = -1.0
        if num_all > 0.0 : perc = 100*float(num)/num_all
        print '%10s:  %4d/%d  %5.1f%%' % (label, num, num_all, perc)
        return

    print '======= Masterjobs (%d) ==============' % (num_masjob_all)
    printStatusLine("Done", num_masjob_done, num_masjob_all)
    printStatusLine("Split", num_masjob_split, num_masjob_all)
    printStatusLine("Inserting", num_masjob_inserting, num_masjob_all)
    printStatusLine("Error", num_masjob_error, num_masjob_all)
    printStatusLine("Rest", num_masjob_rest, num_masjob_all)
    print '======= Subjobs (%d) ===============' % (num_subjob_all)
    printStatusLine("Done", num_subjob_done, num_subjob_all)
    printStatusLine("Running", num_subjob_run, num_subjob_all)
    printStatusLine("Waiting", num_subjob_wait, num_subjob_all)
    printStatusLine("Assigned", num_subjob_assign, num_subjob_all)
    printStatusLine("Starting", num_subjob_start, num_subjob_all)
    printStatusLine("Saving", num_subjob_saving, num_subjob_all)
    printStatusLine("Saved", num_subjob_saved, num_subjob_all)
    printStatusLine("Error", num_subjob_error, num_subjob_all)
    printStatusLine("Expired", num_subjob_expire, num_subjob_all)
    printStatusLine("Zombie", num_subjob_zombie, num_subjob_all)
    printStatusLine("Rest", num_subjob_rest, num_subjob_all)
    print '######################################'

    if debug :
        if master_rest :
            print '========= Remaining (not-sorted) MASTER jobs ==========='
            for job in master_rest :
                print job

        if subjobs_rest :
            print '========= Remaining (not-sorted) SUBjobs ==========='
            for job in subjobs_rest :
                print job
    return

def kill_job_id(job_id, verbose=False) :
    """ Kill a single job based on input id """
    print exec_alien_cmd(['alien_kill',str(job_id)],verbose=verbose)

def kill_jobs(jobs_list,verbose=False,debug=True) :
    """ Kill ALL jobs based on provided list with (filtered) jobs. """
    if not jobs_list :
        print 'List of jobs is empty. Nothing to kill'
        return

    for job in jobs_list :
        job_id = job['id']

        if debug :
            print 'Job ID to kill %s (would be killed, running in debug mode)' % (job_id)
            print job
        else :
            kill_job_id(job_id,verbose=verbose)
    return

def filter_jobs(list_jobs, group=None, status=None, server=None, user=None) :
    """ Returns a list with jobs passing filtering criteria """

    if not list_jobs : # check if list is empty
        print 'Input job list is empty. Nothing to filter'
        return

    filtered_jobs = list_jobs

    if user != None :
        filtered_jobs = [ job for job in filtered_jobs if job['user'] == str(user) ]

    if group != None :
        filtered_jobs = [ job for job in filtered_jobs if job['group'] == str(group) ]

    if server != None :
        filtered_jobs = [ job for job in filtered_jobs if job['server'].startswith(str(server)) ]

    if status != None :
        filtered_jobs = [ job for job in filtered_jobs if job['status'].startswith(str(status)) ]

    return filtered_jobs

def kill_done(user="vpacik", verbose=False, debug=False) :
    filtered = filter_jobs(fetch_jobs(user), status="DONE")
    if verbose : print "Number of jobs to be deleted: %d " % len(filtered)
    kill_jobs(filtered, debug=debug)
    return

# ==============================================================================
