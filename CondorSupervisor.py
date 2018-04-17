#!/usr/bin/python

import os, sys, getopt, re, subprocess

#-------------------------------------------------------------------------------------------------------------------------------------------
# && (Name == strcat("slot1@", Machine) || Name == strcat("slot3@", Machine) || Name == strcat("slot5@", Machine)) \n'

def GetJobString(scripts, idx):
    jobString  = 'executable              = ' + scripts + '                                                      \n'
    jobString += 'initial_dir             = ' + os.getcwd() + '                                                  \n'
    jobString += 'notification            = never                                                                \n'
    jobString += 'Requirements            = (OSTYPE == \"SLC6\")                                                 \n'
    jobString += 'request_memory          = 2048                                                                 \n'
    jobString += 'Rank                    = memory                                                               \n'
    jobString += 'output                  = ' + os.environ['HOME'] + '/CondorLogs/sliceanalysis' + str(idx) + '.out    \n'
    jobString += 'error                   = ' + os.environ['HOME'] + '/CondorLogs/sliceanalysis' + str(idx) + '.err    \n'
    jobString += 'log                     = ' + os.environ['HOME'] + '/CondorLogs/sliceanalysis' + str(idx) + '.log    \n'
    jobString += 'environment             = CONDOR_JOB=true                                                      \n'
    jobString += 'Universe                = vanilla                                                              \n'
    jobString += 'getenv                  = false                                                                \n'
    jobString += 'copy_to_spool           = true                                                                 \n'
    jobString += 'should_transfer_files   = yes                                                                  \n'
    jobString += 'when_to_transfer_output = on_exit_or_evict                                                     \n'
    return jobString

#-------------------------------------------------------------------------------------------------------------------------------------------

def GetJobArguments(firstLine):
    arguments = firstLine.split()

    if 2 != len(arguments):
        print 'Invalid arguments found in runlist.'
        sys.exit(3)

    pandoraSettings = arguments[0]
    eventFile = arguments[1]

    jobArguments = 'arguments = ' + pandoraSettings + ' ' + eventFile 
    jobArguments += '\n'
    return jobArguments

#-------------------------------------------------------------------------------------------------------------------------------------------

def main():
    scripts = sys.argv[1] # LArReco.sh
    runlist = sys.argv[2] # PandoraSettings EventFile 
    maxRuns = sys.argv[3]

    maxRuns = int(maxRuns)

    if not runlist or not os.path.isfile(runlist):
        print 'Invalid runlist specified'
        sys.exit(2)

    counter = 1

    while True:
        queueProcess = subprocess.Popen(['condor_q', '-nobatch'], stdout=subprocess.PIPE)
        queueOutput = queueProcess.communicate()[0]

        regex = re.compile('LArReco.sh')
        queueList = regex.findall(queueOutput)
        nQueued = len(queueList)

        if nQueued >= maxRuns:
            subprocess.call(["usleep", "500000"])
        else:
            with open(runlist, 'r') as file:
                firstLine = file.readline()
                fileContents = file.read().splitlines(True)

            nRemaining = len(fileContents)

            with open(runlist, 'w') as file:
                file.truncate()
                file.writelines(fileContents)

            with open('temp.job', 'w') as jobFile:
                jobFile.truncate()
                jobString  = GetJobString(scripts, counter)
                jobString += GetJobArguments(firstLine)
                jobString += 'queue 1 \n'
                jobFile.write(jobString)

            subprocess.call(['condor_submit', 'temp.job'])
            print 'Submitted job as there were only ' + str(nQueued) + ' jobs in the queue and ' + str(nRemaining) + ' jobs remaining.'
            subprocess.call(["usleep", "500000"])
            os.remove('temp.job')
            counter =  counter + 1

            if 0 == nRemaining:
                print 'Runlist empty'
                sys.exit(0)

#-------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
