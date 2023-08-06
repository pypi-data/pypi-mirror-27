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

import re

class SAAVpediaInputParser(object):
    def __init__(self):
        self.__its2dStringData = []
        self.__itsColOfRsID           = 'col6'
        self.__itsColOfCosmicID       = 'col6'
        self.__itsColOfENSP           = 'col43'
        self.__itsColOfENST           = 'col10'
        self.__itsColOfENSG           = 'col9'
        self.__itsColOfSAAVpeptideSeq = 'col14'
        self.__itsColOfUnitprot       = 'col8'
        self.__itsColOfNextprot       = 'col7'

        self.__itsUniprotMatcher = re.compile( \
            '[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}')
        pass

    def set(self, theStringInput):
        the2dStringData = []
        theSplitedLineList = theStringInput.replace('\r','').strip().split('\n')
        for ithLine in theSplitedLineList:
            the2dStringData.append(ithLine.split())
            pass
        self.__its2dStringData = the2dStringData
        pass


    def __aListToSqlString(self, theStringList):
        theList = []
        for i in theStringList:
            theList.append(self.__stringToQuery(i))
        return "("+" AND ".join(theList)+")"

    def __2dListToSqlString(self, the2dList):
        theQueryList = []
        for ithList in the2dList:
            theQueryList.append(self.__aListToSqlString(ithList))
            pass
        return "("+" OR ".join(theQueryList)+")"


    def __aListToQueryDict(self, theStringList):
        theQueryDict = {}
        for i in theStringList:
            self.__addQueryToQueryDict(theQueryDict, i)
        return theQueryDict

    def __2dListToQueryDictList(self, the2dList):
        theQueryDictList = []
        for ithList in the2dList:
            theQueryDictList.append(self.__aListToQueryDict(ithList))
            pass
        return theQueryDictList

    def __isDigitIncludingPrefix(self, theString, thePrefix):
        if (len(theString) < len(thePrefix)) :
            return False
        if not (thePrefix == str(theString[:len(thePrefix)]).upper()):
            return False
        if (str(theString[len(thePrefix):]).isdigit()):
            return True
        return False

    def __isENSP(self, theString):
        return self.__isDigitIncludingPrefix(theString, 'ENSP')

    def __isENST(self, theString):
        return self.__isDigitIncludingPrefix(theString, 'ENST')

    def __isENSG(self, theString):
        return self.__isDigitIncludingPrefix(theString, 'ENSG')

    def __isRsID(self, theString):
        return self.__isDigitIncludingPrefix(theString, 'rs')

    def __isCosmicID(self, theString):
        return self.__isDigitIncludingPrefix(theString, 'COSM')

    def __isUniprot(self, theString):
        return bool(self.__itsUniprotMatcher.match(theString))

    def __isNextprot(self, theString):
        thePrefix = 'NX_'
        if len(theString) < len(thePrefix):
            return False
        theTail = theString[len(thePrefix):].split('-')[0]
        return bool(self.__itsUniprotMatcher.match(theTail))


    def __stringToQuery(self, theString):
        if self.__isCosmicID(theString):
            return '({0} LIKE \"{1}\")'.format(self.__itsColOfCosmicID, theString)
        elif self.__isRsID(theString):
            return '({0} LIKE \"{1}\")'.format(self.__itsColOfRsID, theString)
        elif self.__isENSG(theString):
            return '({0} LIKE \"{1}\")'.format(self.__itsColOfENSG, theString)
        elif self.__isENST(theString):
            return '({0} LIKE \"{1}\")'.format(self.__itsColOfENST, theString)
        elif self.__isENSP(theString):
            return '({0} LIKE \"{1}\")'.format(self.__itsColOfENSP, theString)
        elif self.__isUniprot(theString):
            return '({0} LIKE \"{1}\")'.format(self.__itsColOfUnitprot, theString)
        elif self.__isNextprot(theString):
            return '({0} LIKE \"{1}\")'.format(self.__itsColOfNextprot, theString)
        elif str(theString).isalpha():
            return '({0} LIKE \"{1}\")'.format(self.__itsColOfSAAVpeptideSeq, theString)

    def __addQueryToQueryDict(self, theQueryDict, theString):
        theKey = None
        if self.__isCosmicID(theString):
            theKey = 'cosmic'
        elif self.__isRsID(theString):
            theKey = 'rs'
        elif self.__isENSG(theString):
            theKey = 'ensg'
        elif self.__isENST(theString):
            theKey = 'enst'
        elif self.__isENSP(theString):
            theKey = 'ensp'
        elif self.__isUniprot(theString):
            theKey = 'unitprot'
        elif self.__isNextprot(theString):
            theKey = 'nextprot'
        elif str(theString).isalpha():
            theKey = 'seq'
        if theKey != None:
            if theQueryDict.has_key(theKey):
                if type(theQueryDict[theKey]) == type(list()):
                    theSet = set(theQueryDict[theKey])
                    theSet.add(theString)
                    theQueryDict[theKey] = list(theSet)
                else:
                    theSet = set([theQueryDict[theKey], theString])
                    theQueryDict[theKey] = list(theSet)
            else :
                theQueryDict[theKey] = theString

    def toSqlCondition(self):
        return self.__2dListToSqlString(self.__its2dStringData)

    def __str__(self):
        return self.toString()

    def toQueryList(self):
        return self.__2dListToQueryDictList(self.__its2dStringData)

    def toString(self):
        return str(self.toQueryList())
    pass



if __name__ == '__main__':

    parser = SAAVpediaInputParser()
    parser.set("WLEAK\tQ7Z5L2\tNX_Q7Z5L2-3\nPLEAK\t\tQ7Z5L2\tNX_Q7Z5L2-3 ENSG00000166024\n")
    print parser.toSqlCondition()
    print parser

    pass

