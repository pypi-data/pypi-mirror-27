#
# Copyright 2017 Russell Smiley
#
# This file is part of registerMap.
#
# registerMap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# registerMap is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with registerMap.  If not, see <http://www.gnu.org/licenses/>.
#

import copy
import logging

from registerMap.exceptions import ConfigurationError
from registerMap.structure import interval as rmbi
from registerMap.structure import bitrange as rmbr


log = logging.getLogger( __name__ )


class BitOffset :
    """
    Collection of intervals used for defining a bit field.
    """


    def __init__( self,
                  numberBits = 0 ) :
        self.__intervals = dict()
        self.__validateNumberBits( numberBits )
        self.__numberBits = numberBits

        self.__assembleDefaultIntervalAssignment()


    def __assembleDefaultIntervalAssignment( self ) :
        if self.__numberBits > 0 :
            self.__intervals[ rmbi.ClosedIntegerInterval( value = { 0, (self.__numberBits - 1) } ) ] = \
                {
                    'register' : None,
                }


    def __validateNumberBits( self, value ) :
        if (isinstance( value, int ) and (value < 0)) \
                or ((not isinstance( value, int )) and (value is not None)) :
            raise ConfigurationError( 'Number bits must be integer greater than zero, {0}'.format( value ) )

        if value < self.__numberBitsFromIntervals() :
            raise ConfigurationError( 'Remove intervals to reduce number of bits' )


    @property
    def isContiguousIntervals( self ) :
        def extractIntervalCoverage() :
            nonlocal self

            coverage = set()
            for interval in self.__intervals.keys() :
                coverage |= set( range( min( interval.value ), (max( interval.value ) + 1) ) )

            return coverage


        endpointList = set( self.__generateEndpointList( self.__intervals ) )
        if len( endpointList ) != 0 :
            intervalCoverage = extractIntervalCoverage()
            expectedIndices = set( range( 0, self.__numberBits ) )

            setDiff = expectedIndices - intervalCoverage

            result = setDiff == set()
        else :
            result = True

        return result


    @property
    def maxValue( self ) :
        maxValue = pow( 2, self.numberBits ) - 1

        return maxValue


    @property
    def numberBits( self ) :
        return self.__numberBits


    @numberBits.setter
    def numberBits( self, value ) :
        self.__validateNumberBits( value )

        self.__numberBits = value

        if self.__intervals :
            # Intervals have already been assigned so just validate those intervals against the new size.
            pass
        else :
            # No intervals assigned so assign the default interval.
            self.__assembleDefaultIntervalAssignment()


    @property
    def range( self ) :
        if self.__numberBits == 0 :
            thisRange = rmbr.BitRange( value = None )
        else :
            thisRange = rmbr.BitRange( value = (0, self.__numberBits) )

        return thisRange


    def assignInterval( self, interval ) :
        """
        
        :param interval: set, list or tuple of mathematically closed interval of the bit indices being assigned.
        :param offset: 
        """
        intervalContainer = rmbi.ClosedIntegerInterval( value = interval )
        self.__validate( intervalContainer )
        self.__intervals[ intervalContainer ] = { 'register' : None, }

        self.__reviewNumberBits()


    def __numberBitsFromIntervals( self ) :
        m = 0
        for interval in self.__intervals.keys() :
            if max( interval.value ) > m :
                m = max( interval.value ) + 1

        return m


    def __reviewNumberBits( self ) :
        numberBitsFromIntervals = self.__numberBitsFromIntervals()

        # If added intervals have exceeded the specified number of bits then grow the number of bits, otherwise do nothing.
        if numberBitsFromIntervals > self.__numberBits :
            self.__numberBits = numberBitsFromIntervals


    def isIntervalIn( self, interval ) :
        """
        Determine if an interval is already in the BitOffset interval collection.
        
        :param interval: `set`, `list` or `tuple` of interval to be examined
        :return: True if interval is in BitOffset interval collection.
        """
        return rmbi.ClosedIntegerInterval( value = interval ) in self.__intervals.keys()


    def removeInterval( self, interval ) :
        """
        Remove specified interval from BitOffset interval collectio dronen.
        
        :param interval: set, list or tuple of interval to be removed.
        """
        try :
            self.__intervals.pop( rmbi.ClosedIntegerInterval( value = interval ) )
            self.__numberBits = 0
        except KeyError as e :
            raise ConfigurationError(
                'Specified interval cannot be removed because it does not exist, {0}'.format( interval ) ) from e


    def __validate( self, interval ) :
        intervalList = copy.deepcopy( self.__intervals )
        intervalList[ interval ] = { 'offset' : 0 }

        listEndpoints = self.__generateEndpointList( intervalList )
        setEndpoints = set( listEndpoints )

        # Intervals can't overlap.
        if len( listEndpoints ) != len( setEndpoints ) :
            raise ConfigurationError( 'Interval overlaps with existing intervals' )


    def __generateEndpointList( self, intervalList ) :
        endpointList = [ n for thisInterval in intervalList.keys() for n in thisInterval.value ]

        return endpointList
