# -*- coding: utf-8 -*-
import os
import re
import random
import dircache
import sys
import datetime

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ''


#===========================
# Input Variables
#===========================

eventsToRun = [
#                 { 'EventType': "Beam_Cosmics", 'EventsPerFile' : 10, 'Momentum':  [5], 'DetectorModel': 'ProtoDUNE-SP', 'Sample': 'mcc10', 'LArSoftVersion': 'larsoft_v06_63_00_triggered_mc_info', 'SpaceChargeEffect': False, 'AnalysisTag': 1 },
                 { 'EventType': "Beam_Cosmics", 'EventsPerFile' : 10, 'Momentum':  [5, -7, -5, -1, 1, 7], 'DetectorModel': 'ProtoDUNE-SP', 'Sample': 'mcc10', 'LArSoftVersion': 'larsoft_v06_63_00_triggered_mc_info', 'SpaceChargeEffect': True, 'AnalysisTag': 6 }
              ]

jobName = 'BdtBeamParticleId'

#===========================

now = datetime.datetime.now()
jobList = ''

for eventSelection in eventsToRun:
    eventType = eventSelection['EventType']
    detectorModel = eventSelection['DetectorModel']
    sample = eventSelection['Sample']
    larsoftVersion = eventSelection['LArSoftVersion']
    spaceChargeOn = eventSelection['SpaceChargeEffect']
    tag = eventSelection['AnalysisTag']
 
    for momenta in eventSelection['Momentum']:
        spaceChargeString = ''
        if spaceChargeOn:
            spaceChargeString = 'SpaceChargeEffectOn'
        else:
            spaceChargeString = 'SpaceChargeEffectOff'

        pndrPath = '/r05/dune/protoDUNE/' + sample + '_Pndr/' + detectorModel + '/LArSoft_Version_' + larsoftVersion + '/' + eventType + '/' + str(momenta) + 'GeV/' + spaceChargeString + '/'
        pndrFormat = sample + '_Pndr_' + detectorModel + '_LArSoft_Version_' + larsoftVersion + '_' + eventType + '_Momentum_' + str(momenta) + 'GeV_(.*?).pndr'

        baseFile = os.path.join(os.getcwd(), 'PandoraSettings_Master_ProtoDUNE.xml')
        settingsPath = '/r05/dune/sg568/LAr/Jobs/protoDUNE/' + str(now.year) + '/' + now.strftime("%B") + '/' + jobName + '/AnalysisTag' + str(tag) + '/' + str(momenta) + 'GeV/' + spaceChargeString + '/PandoraSettings'
        rootFilePath = '/r05/dune/sg568/LAr/Jobs/protoDUNE/' + str(now.year) + '/' + now.strftime("%B") + '/' + jobName + '/AnalysisTag' + str(tag) + '/' + str(momenta) + 'GeV/' + spaceChargeString + '/BdtTrainingFiles'

        if not os.path.exists(settingsPath):
            os.makedirs(settingsPath)

        if not os.path.exists(rootFilePath):
            os.makedirs(rootFilePath)

        base = open(baseFile,'r')
        baseContent = base.read()
        base.close()

        fileDirectory = pndrPath
        allFilesInDirectory = dircache.listdir(fileDirectory)
        inputFileExt = 'pndr'

        allFiles = []
        allFiles.extend(allFilesInDirectory)
        allFiles[:] = [ item for item in allFiles if re.match('.*\.'+inputFileExt+'$',item.lower()) ]
        allFiles.sort()

        nFiles = 0
        if allFiles:
            nFiles = len(allFiles)

        for idx in range (nFiles):
            newContent = baseContent
            nextFile = allFiles.pop(0)
            matchObj = re.match(pndrFormat, nextFile, re.M|re.I)
        
            if matchObj:
                identifier = matchObj.group(1)
                newSettingsName = 'PandoraSettings_Master_ProtoDUNE_' + jobName + '_Training_Job_Number_' + str(identifier) + '.xml'
                settingsFullPath = os.path.join(settingsPath, newSettingsName)
                rootFileFullPath = os.path.join(rootFilePath, jobName + '_Training_Job_Number_' + str(identifier) + '.txt')
                newContent = re.sub('AdaBoostDecisionTreeTrainingOutput.txt', rootFileFullPath, newContent)

                file = open(settingsFullPath,'w')
                file.write(newContent)
                file.close()

                jobList += settingsFullPath + ' ' + os.path.join(pndrPath,nextFile)
                jobList += '\n'
                del newContent

runFilePath = os.getcwd() 
file = open(runFilePath + '/CondorRunFile.txt','w')
file.write(jobList)
file.close()
