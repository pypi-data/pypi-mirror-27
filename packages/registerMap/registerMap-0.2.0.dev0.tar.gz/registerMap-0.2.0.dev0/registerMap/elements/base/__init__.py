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

import abc
import collections


class IdentityElement( metaclass = abc.ABCMeta ) :
    __idCounter = 0


    def __init__( self ) :
        self.__id = IdentityElement.assignId()


    @property
    @abc.abstractmethod
    def canonicalId( self ) :
        pass


    @property
    def id( self ) :
        return self.__id


    @staticmethod
    def assignId() :
        IdentityElement.__idCounter += 1

        return IdentityElement.__idCounter


class AddressableElementInterface( metaclass = abc.ABCMeta ) :
    @property
    @abc.abstractmethod
    def startAddress( self ) :
        pass


    @property
    @abc.abstractmethod
    def endAddress( self ) :
        pass


    @property
    @abc.abstractmethod
    def sizeMemoryUnits( self ) :
        pass


class BitStoreInterface( metaclass = abc.ABCMeta ) :
    @property
    @abc.abstractmethod
    def bitMap( self ) :
        pass


    @property
    @abc.abstractmethod
    def id( self ) :
        pass


    @property
    @abc.abstractmethod
    def sizeBits( self ) :
        pass


class ElementList( collections.OrderedDict ) :
    def __init__( self, owner ) :
        super().__init__()
        self.__owner = owner


    def __setitem__( self, key, value ) :
        try :
            previousElementKey = next( reversed( self ) )
            previousElement = self[ previousElementKey ]
        except StopIteration as e :
            # This is the first register added.
            previousElement = self.__owner.firstElement

        super().__setitem__( key, value )

        value.previousElement = previousElement
        value.sizeChangeNotifier.addObserver( self.__owner.sizeObserver )
        # Address change of an element implies a potential size change to its owner.
        value[ 'constraints' ].addressChangeNotifier.addObserver( self.__owner.sizeObserver )
        value.reviewAddressChange()


class SizeObservableInterface( metaclass = abc.ABCMeta ) :
    @abc.abstractmethod
    def reviewSizeChange( self ) :
        pass


class AddressObservableInterface( metaclass = abc.ABCMeta ) :
    @abc.abstractmethod
    def reviewAddressChange( self ) :
        pass
