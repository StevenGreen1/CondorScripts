#!/bin/bash

source /cvmfs/uboone.opensciencegrid.org/products/setup_uboone.sh

setup gcc v4_9_3 -f Linux64bit+2.6-2.12
setup git v2_4_6 -f Linux64bit+2.6-2.12
setup python v2_7_13d -f Linux64bit+2.6-2.12

setup eigen v3_3_3
setup root v6_06_08 -f Linux64bit+2.6-2.12 -q e10:nu:prof

export FW_SEARCH_PATH=${FW_SEARCH_PATH}:"/usera/sg568/LAr/Jobs/protoDUNE/2018/April/ProtoDUNE_BdtBeamParticleId/Condor/LArReco/settings/"
export PD_GEOEMTRY="/usera/sg568/LAr/Jobs/protoDUNE/2018/April/ProtoDUNE_BdtBeamParticleId/Condor/LArReco/geometry/PandoraGeometry_ProtoDUNE.xml"

/usera/sg568/LAr/Jobs/protoDUNE/2018/April/ProtoDUNE_BdtBeamParticleId/Condor/LArReco/bin/PandoraInterface -r Full -i $1 -e $2 -g ${PD_GEOEMTRY} -n 10

