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

import logging

import registerMap.utility.io.yaml.parameters.encode as rye
import registerMap.utility.io.yaml.parameters.parse as ryp
import registerMap.utility.observer as rmo

from registerMap.structure.bitmap import BitMap
from registerMap.utility.io import yaml

from registerMap.exceptions import ConfigurationError, ParseError

from ..base import BitStoreInterface, IdentityElement
from . import parameters as rmbp


log = logging.getLogger( __name__ )


class Field( IdentityElement,
             BitStoreInterface,
             yaml.Export,
             yaml.Import ) :
    """
    Representation of a bit field in a register.

    The following parameters are available for every BitField:

    # description (str) - Expanded description of the BitField object.
    # global (bool) - Assert whether or not the BitField object is global.
    # name (str) - Alphanumeric name of the BitField object.
    # public (bool) - Assert whether or not the BitField object is public.
    # resetValue (int) - Reset (default) value of the BitField object.
    # size (int) - The number of bits in the BitField object.
    # summary (str) - Short description of the BitField object.
    """
    __defaultName = 'unassigned'
    __keyName = 'field'

    """
    __nonParameters do not conform to the registerMap.elements.bitfield.parameters.BitFieldParameter interface.
    """
    __nonParameters = list()


    class SizeChangeObserver( rmo.Observer ) :
        def __init__( self, owner ) :
            self.__owner = owner


        def update( self, observable, arguments ) :
            # Cascade the size change
            self.__owner.sizeChangeNotifier.notifyObservers()


    def __init__( self,
                  parent = None ) :
        super().__init__()

        self.sizeChangeNotifier = rmo.Observable()

        self.__bitMap = BitMap( self )
        self.__parentRegister = parent
        self.__sizeChangeObserver = Field.SizeChangeObserver( self )

        self.__data = {
            'description' : rmbp.StringParameter( value = '' ),
            'global' : rmbp.GlobalParameter( self ),
            'name' : rmbp.NameParameter( value = self.__defaultName ),
            'resetValue' : rmbp.ResetValueParameter( value = 0,
                                                     size = 0 ),
            'summary' : rmbp.StringParameter( value = '' ),
        }
        self.__data[ 'size' ] = rmbp.SizeParameter( self.__data[ 'resetValue' ] )


    def __getitem__( self, item ) :
        if item not in self.__nonParameters :
            value = self.__data[ item ].value
        else :
            value = self.__data[ item ]

        return value


    def __setitem__( self, key, value ) :
        if key not in self.__nonParameters :
            self.__data[ key ].value = value
        else :
            self.__data[ key ] = value

        if key == 'size' :
            log.debug( 'Notifying on field size change, {0}: {1}'.format( self.__data[ 'name' ].value,
                                                                          value ) )
            self.sizeChangeNotifier.notifyObservers()


    @property
    def bitMap( self ) :
        return self.__bitMap


    @property
    def canonicalId( self ) :
        if self.__parentRegister is not None :
            canonicalName = '{0}.{1}'.format( self.__parentRegister.canonicalId,
                                              self.__data[ 'name' ].value )
        else :
            canonicalName = '{0}'.format( self.__data[ 'name' ].value )

        return canonicalName


    @property
    def parent( self ) :
        return self.__parentRegister


    @property
    def sizeBits( self ) :
        return self.__data[ 'size' ].value


    @classmethod
    def from_yamlData( cls, yamlData,
                       parentRegister = None ) :
        field = cls()
        goodResult = field.__decodeField( yamlData, parentRegister )

        if not goodResult :
            raise ParseError( 'Processing field data failed. Check log for details. ' + repr( yamlData ) )

        return field


    def __decodeField( self, yamlData, parentRegister ) :
        def recordDescription( value ) :
            nonlocal self
            self.__data[ 'description' ].value = value


        def recordParent( value ) :
            nonlocal parentRegister

            assert value is not None

            if parentRegister is None :
                # Must specify a parent register for local fields.
                raise ParseError( 'Parent register not specified for YAML acquisition of a local field' )
            elif parentRegister.canonicalId != value :
                raise ParseError( 'Parent register does not match YAML specification, spec({0}), yaml({1})'.format(
                    parentRegister.canonicalId,
                    value ) )

            self.__parentRegister = parentRegister


        def recordName( value ) :
            nonlocal self
            self.__data[ 'name' ].value = value


        def recordResetValue( value ) :
            nonlocal self
            self.__data[ 'resetValue' ].value = value


        def recordSize( value ) :
            nonlocal self
            self.__data[ 'size' ].value = value


        def recordSummary( value ) :
            nonlocal self
            self.__data[ 'summary' ].value = value


        def getParameters( thisData ) :
            nonlocal self

            thisGoodResult = ryp.stringParameter( thisData, 'name', recordName )
            thisGoodResult &= ryp.integerParameter( thisData, 'size', recordSize )
            thisGoodResult &= ryp.integerParameter( thisData, 'resetValue', recordResetValue )
            # Make sure that we subscribe to notification of bit range size changes.
            self.__data[ 'size' ].sizeChangeNotifier.addObserver( self.__sizeChangeObserver )

            ryp.stringParameter( thisData, 'description', recordDescription,
                                 optional = True )
            ryp.stringParameter( thisData, 'summary', recordSummary,
                                 optional = True )

            ryp.stringParameter( thisData, 'parent', recordParent,
                                 optional = True )

            return thisGoodResult


        return ryp.complexParameter( yamlData, Field.__keyName, getParameters )


    def convertToLocal( self, parentRegister,
                        removeOthers = False ) :
        """
        Convert field to non-global, that is, dedicated bit maps to a single register.
        """


        def removeOtherRegisters() :
            nonlocal parentRegister

            otherRegisters = [ x for x in self.__bitMap.destinations if x != parentRegister ]

            assert len( otherRegisters ) == (len( self.__bitMap.destinations ) - 1)

            for thisRegister in otherRegisters :
                self.__bitMap.removeDestination( thisRegister )


        if parentRegister not in self.__bitMap.destinations :
            raise ConfigurationError( 'Field does not map to the register selected for parent' )
        if not removeOthers :
            if (parentRegister in self.__bitMap.destinations) \
                    and (len( self.__bitMap.destinations ) > 1) :
                raise ConfigurationError( 'Field maps to multiple registers' )
        else :
            removeOtherRegisters()

        self.__parentRegister = parentRegister


    def convertToGlobal( self ) :
        """
        Convert field to global, that is, allowing bit maps to multiple registers.
        """
        self.__parentRegister = None


    def to_yamlData( self ) :
        parameters = [ rye.parameter( 'size', self.__data[ 'size' ].value ),
                       rye.parameter( 'name', self.__data[ 'name' ].value ),
                       rye.parameter( 'resetValue', rye.HexInt( self.__data[ 'resetValue' ].value ) ) ]

        if self.__data[ 'description' ] != '' :
            parameters.append( rye.parameter( 'description', self.__data[ 'description' ].value ) )
        if self.__data[ 'summary' ] != '' :
            parameters.append( rye.parameter( 'summary', self.__data[ 'summary' ].value ) )

        if not self.__data[ 'global' ].value :
            assert self.__parentRegister.canonicalId is not None

            parameters.append( rye.parameter( 'parent', self.__parentRegister.canonicalId ) )

        yamlData = { Field.__keyName : { } }

        for thisParameter in parameters :
            yamlData[ Field.__keyName ].update( thisParameter )

        return yamlData
