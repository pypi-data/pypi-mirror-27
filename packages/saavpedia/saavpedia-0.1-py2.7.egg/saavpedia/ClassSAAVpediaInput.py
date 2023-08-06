#!/usr/bin/env python

################################################################################
# "SAAVpedia Annotation Javascript Library"
# Copyright (C) 2017 Young-Mook Kang <ymkang@thylove.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
################################################################################

import urllib
import uuid
from datetime import datetime

class SAAVpediaInput(object) :
    def __init__(self):
        self.__itsInputDataDict = dict()

        self.__itsKeyOfSAAVpeptideSequence = 'SAAVpeptideSequence'
        self.__itsKeyOfENSP                = 'ensp'
        self.__itsKeyOfENST                = 'enst'
        self.__itsKeyOfENSG                = 'ensg'
        self.__itsKeyOfUnitprot            = 'unitprot'
        self.__itsKeyOfNextprot            = 'nextprot'
        self.__itsKeyOfGenomicPosition     = 'genomicPosition'
        self.__itsKeyOfdbSNP               = 'dbSNP'
        self.__itsKeyOfCosmic              = 'cosmic'
        self.__itsKeyOfDatasetName         = 'datasetName'

        self.__itsInputDataDict[self.__itsKeyOfDatasetName] = \
            datetime.now().strftime("%Y%m%d-%Hh%Mm%S.%f")[:-3] + 's-' \
            + str(uuid.uuid4())[:8]
        pass

    def __getDataDict(self):
        return self.__itsInputDataDict

    def __setDataDict(self, theKey, theValue):
        self.__itsInputDataDict[theKey] = str(theValue)


    ################################################################################
    # ENSP input
    ################################################################################
    @property
    def ENSP(self):
        theKey = self.__itsKeyOfENSP
        return self.__getValueFromData(theKey)

    @ENSP.setter
    def ENSP(self, theENSP):
        theKey = self.__itsKeyOfENSP
        self.__setDataDict(theKey, theENSP)
        pass

    @property
    def ensp(self):
        return self.ENSP

    @ensp.setter
    def ensp(self, theENSP):
        self.ENSP = theENSP
        pass

    ################################################################################
    # ENST input
    ################################################################################
    @property
    def ENST(self):
        theKey = self.__itsKeyOfENST
        return self.__getValueFromData(theKey)

    @ENST.setter
    def ENST(self, theENST):
        theKey = self.__itsKeyOfENST
        self.__setDataDict(theKey, theENST)
        pass

    @property
    def enst(self):
        return self.ENST

    @enst.setter
    def enst(self, theENST):
        self.ENST = theENST
        pass

    ################################################################################
    # ENSG input
    ################################################################################

    @property
    def ENSG(self):
        theKey = self.__itsKeyOfENSG
        return self.__getValueFromData(theKey)

    @ENSG.setter
    def ENSG(self, theENSG):
        theKey = self.__itsKeyOfENSG
        self.__setDataDict(theKey, theENSG)
        pass

    @property
    def ensg(self):
        return self.ENSG

    @ensg.setter
    def ensg(self, theENSG):
        self.ENSG = theENSG
        pass

    ################################################################################
    # Uniprot input
    ################################################################################

    @property
    def unitprot(self):
        theKey = self.__itsKeyOfUnitprot
        return self.__getValueFromData(theKey)

    @unitprot.setter
    def unitprot(self, theUnitprot):
        theKey = self.__itsKeyOfUnitprot
        self.__setDataDict(theKey, theUnitprot)
        pass


    ################################################################################
    # Nextprot input
    ################################################################################
    @property
    def nextprot(self):
        theKey = self.__itsKeyOfNextprot
        return self.__getValueFromData(theKey)

    @nextprot.setter
    def nextprot(self, theNextprot):
        theKey = self.__itsKeyOfNextprot
        self.__setDataDict(theKey, theNextprot)
        pass

    ################################################################################
    # SAAV peptide sequence input
    ################################################################################

    @property
    def saavPeptideSequence(self):
        theKey = self.__itsKeyOfSAAVpeptideSequence
        return self.__getValueFromData(theKey)

    @saavPeptideSequence.setter
    def saavPeptideSequence(self, theSAAVpeptideSequence):
        theKey = self.__itsKeyOfSAAVpeptideSequence
        self.__setDataDict(theKey, theSAAVpeptideSequence)
        pass

    ################################################################################
    # dbSNP input
    ################################################################################

    @property
    def dbSNP(self):
        theKey = self.__itsKeyOfdbSNP
        return self.__getValueFromData(theKey)

    @dbSNP.setter
    def dbSNP(self, theDbSNP):
        theKey = self.__itsKeyOfdbSNP
        self.__setDataDict(theKey, theDbSNP)
        pass


    ################################################################################
    # Cosmic input
    ################################################################################

    @property
    def cosmic(self):
        theKey = self.__itsKeyOfCosmic
        return self.__getValueFromData(theKey)

    @cosmic.setter
    def cosmic(self, theCosmic):
        theKey = self.__itsKeyOfCosmic
        self.__setDataDict(theKey, theCosmic)
        pass

    ################################################################################
    # Genomic position input
    ################################################################################

    @property
    def genomicPosition(self):
        theKey = self.__itsKeyOfGenomicPosition
        return self.__getValueFromData(theKey)

    @genomicPosition.setter
    def genomicPosition(self, thePosition):
        theKey = self.__itsKeyOfGenomicPosition
        self.__setDataDict(theKey, thePosition)
        pass


    ################################################################################
    # Genomic position input
    ################################################################################

    @property
    def datasetName(self):
        theKey = self.__itsKeyOfDatasetName
        return self.__getValueFromData(theKey)

    @datasetName.setter
    def datasetName(self, theName):
        theKey = self.__itsKeyOfDatasetName
        self.__setDataDict(theKey, theName)
        pass


    ################################################################################
    # Internal functions
    ################################################################################

    def __getValueFromData(self, theKey):
        try:
            if self.__getDataDict().has_key(theKey):
                return self.__getDataDict()[theKey]
            pass
        except Exception:
            print Exception
        return None

    def toString(self):
        return str(self.__itsInputDataDict)

    def toQueryString(self):
        return urllib.urlencode(self.__itsInputDataDict)

    def __str__(self):
        return self.toString()


if __name__ == '__main__':

    i = SAAVpediaInput()
    i.saavPeptideSequence = 'LEAK'
    i.nextprot = 'NextprotID'
    i.unitprot = 'UnitprotID'
    i.dbSNP = 'dbSNP'
    i.genomicPosition = 10000
    i.ensg = 'ensg'
    i.enst = 'enst'
    i.ensg = 'ensg'
    i.cosmic = 'cosmic'

    print i
    print i.toQueryString()
    pass


