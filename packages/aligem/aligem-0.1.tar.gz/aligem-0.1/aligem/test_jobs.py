from jobs import *

const_masterjob = "pcapiserv"
const_subjob = "aliendb"

user = 'yozhou'

get_status(user)


print "checking the filtering for job operations"

jobs_list = fetch_jobs(user)
if jobs_list : print len(jobs_list)

filtered = filter_jobs(jobs_list,group="master")

if filtered :
    print len(filtered)
    for job in filtered :
        print job
