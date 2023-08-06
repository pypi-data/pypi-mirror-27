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


import re

import registerMap.utility.observer as rmo

from registerMap.exceptions import ConfigurationError


class BitfieldParameter :
    def __init__( self, value = None ) :
        self.validate( value )
        self.__value = value


    @property
    def value( self ) :
        return self.__value


    @value.setter
    def value( self, v ) :
        self.validate( v )
        self.__value = v


class BooleanParameter( BitfieldParameter ) :
    def __init__( self, value = True ) :
        super().__init__( value )


    @staticmethod
    def validate( value ) :
        if not isinstance( value, bool ) :
            raise ConfigurationError( 'Must be specified as boolean' )


class GlobalParameter( BitfieldParameter ) :
    def __init__( self, element ) :
        super().__init__( element )

        self.__element = element


    @staticmethod
    def validate( value ) :
        pass


    @property
    def value( self ) :
        isGlobal = False
        if self.__element.parent is None :
            isGlobal = True

        return isGlobal


    @value.setter
    def value( self, v ) :
        # This method cannot be used, but need to override the behaviour from parent class.
        assert False


class IntParameter( BitfieldParameter ) :
    def __init__( self, value = 0 ) :
        super().__init__( value )


    @staticmethod
    def validate( value ) :
        if not isinstance( value, int ) :
            raise ConfigurationError( 'Must be an int, not {0}'.format( value ) )


class NameParameter( BitfieldParameter ) :
    def __init__( self,
                  value = 'unassigned' ) :
        super().__init__( value )


    @staticmethod
    def validate( value ) :
        if not isinstance( value, str ) :
            raise ConfigurationError( 'Must be a string, not {0}'.format( type( value ) ) )


class PositiveIntParameter( BitfieldParameter ) :
    def __init__( self, value = 0 ) :
        super().__init__( value )


    @staticmethod
    def validate( value ) :
        IntParameter.validate( value )

        if value < 0 :
            raise ConfigurationError( 'Must be a positive int, not {0}'.format( value ) )


class StringParameter( BitfieldParameter ) :
    def __init__( self, value = '' ) :
        super().__init__( value )


    @staticmethod
    def validate( value ) :
        if not isinstance( value, str ) :
            raise ConfigurationError( 'Must be a string, not {0}'.format( type( value ) ) )


class ResetValueParameter( PositiveIntParameter ) :
    def __init__( self,
                  value = 0,
                  size = 0 ) :
        """

        :type value: int
        :type size: int
        """
        self.__validateSize( size )
        self.__numberBits = size

        super().__init__( value )


    @property
    def maxValue( self ) :
        thisMax = pow( 2, self.__numberBits ) - 1

        return thisMax


    @property
    def size( self ) :
        return self.__numberBits


    def __validateSize( self, value ) :
        if (not isinstance( value, int )) \
                or (value < 0) :
            raise ConfigurationError( 'Size must be positive int, {0}'.format( value ) )


    @size.setter
    def size( self, value ) :
        self.__validateSize( value )
        self.__numberBits = value


    def validate( self, value ) :
        PositiveIntParameter.validate( value )

        maxValue = self.maxValue
        if value > maxValue :
            raise ConfigurationError(
                'Reset value cannot exceed number of bits of field, {0} maximum, {1} specified'.format( maxValue,
                                                                                                        value ) )


class SizeParameter :
    class SizeChangeObserver( rmo.Observer ) :
        def __init__( self, owner ) :
            self.__owner = owner


        def update( self, observable, arguments ) :
            # Cascade the size change
            self.__owner.sizeChangeNotifier.notifyObservers()


    def __init__( self, sizeResetParameter ) :
        assert isinstance( sizeResetParameter, ResetValueParameter )

        self.__sizeChangeObserver = SizeParameter.SizeChangeObserver( self )
        self.__sizeResetParameter = sizeResetParameter

        self.sizeChangeNotifier = rmo.Observable()


    @property
    def value( self ) :
        return self.__sizeResetParameter.size


    @value.setter
    def value( self, v ) :
        self.__sizeResetParameter.size = v
