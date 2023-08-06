import jobs
import argparse

def main() :
    ### top-level group (L0)
    parser = argparse.ArgumentParser(description="Welcome to AliGEM - ALICE Grid Enviroment Manager - toolbox for handling Grid related operations")
    parser.add_argument("-v","--verbose", help="produce verbose output", action="store_true")
    parser.add_argument("-d","--debug", help="debugging mode (additional printout)", action="store_true")
    parser.add_argument("--version", action="version", version='0.1', help="print current version")
    subparsers = parser.add_subparsers(dest="command")

    ### sub-parsers
    # jobs parser (L1)
    parser_jobs = subparsers.add_parser("jobs", help="grid jobs operations")
    jobs_subparsers = parser_jobs.add_subparsers(dest="job_command")

    # jobs sub-parser (L2)
    jobs_subparser_status = jobs_subparsers.add_parser("status", help = "print overview of current grid jobs")
    jobs_subparser_status.add_argument("-u","--user", help="specify USER as CERN username")

    jobs_subparser_kill = jobs_subparsers.add_parser("kill", help = "kill grid job(s)")
    jobs_subparser_kill.add_argument("-u","--user", help="specify USER as CERN username")


    # token parser (L1)
    # NOTE: not implemented
    parser_token = subparsers.add_parser("token", help="token (not implemented yet)")



    args = parser.parse_args()

    debug = args.debug


    # if debug :
    if True :
        print "=== Arguments ================================="
        print args
        print "==============================================="

    if args.command == 'jobs' :
        if debug : print "inside jobs"

        if args.job_command == 'status' :
            if debug : print "inside status"
            user = args.user

            if user == None :
                jobs.get_status()
            else :
                jobs.get_status(user)

        if args.job_command == 'kill' :
            if debug : print "inside kill"
            user = args.user

            if user == None :
                jobs.kill_done(debug=debug)
            else :
                jobs.kill_done(user,debug=debug)

    if args.command == 'token' :
        print "token command not implemented (yet)"


    return
