"""
Unit tests for Register
"""
#
# Copyright 2016 Russell Smiley
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import unittest

import registerMap.elements.register as rmr
import registerMap.utility.observer as rmo
import registerMap.structure.memory.space as rmm

from registerMap.set import SetCollection

from registerMap.elements.tests.mockObserver import MockObserver


log = logging.getLogger( __name__ )


class MockPreviousRegister :
    def __init__( self,
                  startAddress = None,
                  endAddress = None,
                  sizeMemoryUnits = None ) :
        self.sizeChangeNotifier = rmo.Observable()
        self.addressChangeNotifier = rmo.Observable()

        self.__address = startAddress
        if (endAddress is not None) and (startAddress is not None) :
            self.__endAddress = endAddress
            self.__sizeMemoryUnits = self.__endAddress - self.__address + 1
        elif (sizeMemoryUnits is not None) and (startAddress is not None) :
            self.__sizeMemoryUnits = sizeMemoryUnits
            self.__endAddress = self.__address + self.__sizeMemoryUnits - 1
        elif (sizeMemoryUnits is not None) and (endAddress is not None) :
            self.__endAddress = endAddress
            self.__sizeMemoryUnits = sizeMemoryUnits
            self.__address = self.__endAddress - self.__sizeMemoryUnits + 1
        elif (startAddress is None) and (sizeMemoryUnits is not None or endAddress is not None) :
            raise RuntimeError( 'Must specify address if specifying end address or size' )
        else :
            self.__sizeMemoryUnits = None
            self.__endAddress = None


    @property
    def address( self ) :
        return self.__address


    @address.setter
    def address( self, value ) :
        if self.__address is not None :
            addressChange = value - self.__address
            self.__address = value
            self.__endAddress += addressChange
        else :
            self.__address = value
            self.__endAddress = self.__address + self.__sizeMemoryUnits - 1

        self.addressChangeNotifier.notifyObservers()


    @property
    def endAddress( self ) :
        return self.__endAddress


    @endAddress.setter
    def endAddress( self, value ) :
        self.__endAddress = value
        # For the purpose of testing, assume that a change in end address always signals a size change.
        self.__sizeMemoryUnits = self.__endAddress - self.__address + 1
        self.sizeChangeNotifier.notifyObservers()


    @property
    def sizeMemoryUnits( self ) :
        return self.__sizeMemoryUnits


    @sizeMemoryUnits.setter
    def sizeMemoryUnits( self, value ) :
        self.__sizeMemoryUnits = value
        self.__endAddress = self.__address + self.__sizeMemoryUnits - 1
        self.sizeChangeNotifier.notifyObservers()


class TestRegisterDescription( unittest.TestCase ) :
    def setUp( self ) :
        self.observer = MockObserver()
        self.setCollection = SetCollection()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.setCollection )

        self.testRegister.sizeChangeNotifier.addObserver( self.observer )


    def testDefaultValue( self ) :
        expectedValue = ''
        self.assertEqual( self.testRegister[ 'description' ], expectedValue )


    def testDataAssignmet( self ) :
        expectedValue = 'register description'

        self.assertNotEqual( expectedValue, self.testRegister[ 'description' ] )

        self.testRegister[ 'description' ] = expectedValue

        self.assertEqual( self.testRegister[ 'description' ], expectedValue )
        self.assertEqual( self.observer.updateCount, 0 )


class TestRegisterMode( unittest.TestCase ) :
    def setUp( self ) :
        self.observer = MockObserver()
        self.setCollection = SetCollection()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.setCollection )

        self.testRegister.sizeChangeNotifier.addObserver( self.observer )


    def testDefaultValue( self ) :
        expectedValue = 'rw'
        self.assertEqual( self.testRegister[ 'mode' ], expectedValue )


    def testDataAssignment( self ) :
        expectedValue = 'ro'
        self.assertNotEqual( expectedValue, self.testRegister[ 'mode' ] )

        self.testRegister[ 'mode' ] = expectedValue

        self.assertEqual( self.testRegister[ 'mode' ], expectedValue )
        self.assertEqual( self.observer.updateCount, 0 )


    def testInvalidValueRaises( self ) :
        with self.assertRaisesRegex( rmr.ConfigurationError, '^Invalid value' ) :
            self.testRegister[ 'mode' ] = 'r'


class TestRegisterName( unittest.TestCase ) :
    def setUp( self ) :
        self.observer = MockObserver()
        self.setCollection = SetCollection()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.setCollection )

        self.testRegister.sizeChangeNotifier.addObserver( self.observer )


    def testDefaultValue( self ) :
        self.assertIsNone( self.testRegister[ 'name' ] )


    def testDataAssignment( self ) :
        expectedValue = 'register name'
        self.assertNotEqual( expectedValue, self.testRegister[ 'name' ] )

        self.testRegister[ 'name' ] = expectedValue

        self.assertEqual( self.testRegister[ 'name' ], expectedValue )
        self.assertEqual( self.observer.updateCount, 0 )


class TestRegisterPublic( unittest.TestCase ) :
    def setUp( self ) :
        self.observer = MockObserver()
        self.setCollection = SetCollection()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.setCollection )

        self.testRegister.sizeChangeNotifier.addObserver( self.observer )


    def testDefaultValue( self ) :
        expectedValue = True
        self.assertEqual( self.testRegister[ 'public' ], expectedValue )


    def testDataAssignment( self ) :
        self.assertTrue( self.testRegister[ 'public' ] )

        self.testRegister[ 'public' ] = False

        self.assertFalse( self.testRegister[ 'public' ] )
        self.assertEqual( self.observer.updateCount, 0 )


    def testNonBoolRaises( self ) :
        with self.assertRaisesRegex( rmr.ConfigurationError, '^Public must be specified as boolean' ) :
            self.testRegister[ 'public' ] = 'true'


class TestRegisterSummary( unittest.TestCase ) :
    def setUp( self ) :
        self.observer = MockObserver()
        self.setCollection = SetCollection()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.setCollection )

        self.testRegister.sizeChangeNotifier.addObserver( self.observer )


    def testDefaultValue( self ) :
        expectedValue = ''
        self.assertEqual( self.testRegister[ 'summary' ], expectedValue )


    def testDataAssignment( self ) :
        expectedValue = 'register summary'
        self.assertNotEqual( expectedValue, self.testRegister[ 'summary' ] )

        self.testRegister[ 'summary' ] = expectedValue

        self.assertEqual( self.testRegister[ 'summary' ], expectedValue )
        self.assertEqual( self.observer.updateCount, 0 )


if __name__ == '__main__' :
    unittest.main()
