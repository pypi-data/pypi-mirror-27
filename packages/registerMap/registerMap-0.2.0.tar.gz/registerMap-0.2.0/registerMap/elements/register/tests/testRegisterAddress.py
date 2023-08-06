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
import unittest

import registerMap.elements.register as rmr
import registerMap.exceptions as rme
import registerMap.set.elementSet as rmese
import registerMap.structure.memory.space as rmm

from registerMap.elements.tests.mockObserver import MockObserver
from .testRegister import MockPreviousRegister


log = logging.getLogger( __name__ )


class TestRegisterAddressPreviousNoneAddress( unittest.TestCase ) :
    """
    Test register address when the previous address has no defined address or size.
    """


    def setUp( self ) :
        self.observer = MockObserver()
        self.previousRegister = MockPreviousRegister()
        self.testBitFieldSet = rmese.ElementSet()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.testBitFieldSet )

        self.testRegister.previousElement = self.previousRegister

        self.testRegister.sizeChangeNotifier.addObserver( self.observer )
        self.testRegister.addressChangeNotifier.addObserver( self.observer )


    def testDefaultValue( self ) :
        self.assertIsNone( self.testRegister.address )
        self.assertIsNone( self.testRegister.endAddress )


    def testFixedAddress( self ) :
        expectedValue = 0x15

        self.assertNotEqual( self.testRegister.address, expectedValue )

        self.testRegister[ 'constraints' ][ 'fixedAddress' ] = expectedValue

        self.assertEqual( self.testRegister.address, expectedValue )
        self.assertEqual( self.observer.updateCount, 1 )


    def testAlignedAddress( self ) :
        alignmentValue = 2

        self.testRegister[ 'constraints' ][ 'alignmentMemoryUnits' ] = alignmentValue

        # Attempt to constrain alignment with no concrete addresses does nothing
        self.assertIsNone( self.testRegister.address )
        self.assertIsNone( self.testRegister.endAddress )
        self.assertEqual( self.observer.updateCount, 0 )


class TestRegisterAddressPreviousConcreteAddress( unittest.TestCase ) :
    """
    Test register address when the previous register has concrete address and size.
    """


    def setUp( self ) :
        self.observer = MockObserver()
        self.previousRegister = MockPreviousRegister( startAddress = 0x10,
                                                      sizeMemoryUnits = 5 )
        self.testBitFieldSet = rmese.ElementSet()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.testBitFieldSet )

        self.testRegister.previousElement = self.previousRegister

        self.testRegister.sizeChangeNotifier.addObserver( self.observer )
        self.testRegister.addressChangeNotifier.addObserver( self.observer )


    def testFixedAddress( self ) :
        expectedValue = 0x16

        self.assertNotEqual( self.testRegister.address, expectedValue )

        self.testRegister[ 'constraints' ][ 'fixedAddress' ] = expectedValue

        self.assertEqual( self.testRegister.address, expectedValue )
        self.assertEqual( self.observer.updateCount, 1 )


    def testFixedAddressOnPreviousRaises( self ) :
        expectedValue = self.previousRegister.endAddress

        with self.assertRaisesRegex( rme.ConstraintError, '^Fixed address exceeded' ) :
            self.testRegister[ 'constraints' ][ 'fixedAddress' ] = expectedValue


    def testAlignedAddress( self ) :
        alignmentValue = 2
        expectedValue = self.previousRegister.endAddress + 2

        self.assertEqual( (expectedValue % alignmentValue), 0 )
        self.assertLess( self.testRegister.address, expectedValue )

        self.testRegister[ 'constraints' ][ 'alignmentMemoryUnits' ] = alignmentValue

        self.assertEqual( self.testRegister.address, expectedValue )
        self.assertEqual( self.observer.updateCount, 1 )


class TestRegisterPageRegisterInteraction( unittest.TestCase ) :
    def setUp( self ) :
        self.testBitFieldSet = rmese.ElementSet()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.testBitFieldSet )

        self.previousRegister = MockPreviousRegister( startAddress = 0,
                                                      sizeMemoryUnits = 4 )
        self.testRegister.previousElement = self.previousRegister


    def testPageSize( self ) :
        self.assertEqual( self.testSpace.addressBits, 32 )
        self.assertEqual( self.testSpace.memoryUnitBits, 8 )

        self.previousRegister.address = 0x278

        log.debug( 'Mock previous register start address: ' + hex( self.previousRegister.address ) )
        log.debug( 'Mock previous register end address: ' + hex( self.previousRegister.endAddress ) )
        self.assertEqual( self.previousRegister.address, 0x278 )
        log.debug( 'Test register start address no page size: ' + hex( self.testRegister.address ) )
        log.debug( 'Test register end address no page size: ' + hex( self.testRegister.endAddress ) )
        self.assertEqual( self.testRegister.address, 0x27c )

        self.testSpace.pageSize = 0x80
        log.debug( 'Test register start address page size '
                   + hex( self.testSpace.pageSize ) + ': '
                   + hex( self.testRegister.address ) )
        log.debug( 'Test register end address page size '
                   + hex( self.testSpace.pageSize ) + ': '
                   + hex( self.testRegister.endAddress ) )
        self.assertEqual( self.testRegister.address, 0x280 )


class TestRegisterPreviousRegister( unittest.TestCase ) :
    def setUp( self ) :
        self.observer = MockObserver()
        self.testBitFieldSet = rmese.ElementSet()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.testBitFieldSet )

        self.testRegister.sizeChangeNotifier.addObserver( self.observer )


    def testDefaultValue( self ) :
        self.assertIsNone( self.testRegister.previousElement )


    def testPreviousRegisterAssign( self ) :
        expectedValue = 0x10
        self.testRegister.previousElement = MockPreviousRegister( startAddress = 0x5,
                                                                  endAddress = (expectedValue - 1) )

        self.assertEqual( self.testRegister.address, expectedValue )


    def testUnassignedPreviousRegisterNoneAddress( self ) :
        fixedAddress = 0x10
        self.testRegister[ 'constraints' ][ 'fixedAddress' ] = fixedAddress

        self.assertEqual( self.testRegister.address, fixedAddress )


    def testUnassignedEndAddress( self ) :
        self.testRegister.previousElement = MockPreviousRegister()

        actualAddress = self.testRegister.address
        self.assertIsNone( actualAddress )


    def testAssignPreviousRegisterEndAddress( self ) :
        self.testRegister.previousElement = MockPreviousRegister( startAddress = 0x5 )

        self.assertIsNone( self.testRegister.address )

        expectedAddress = 0x10
        self.testRegister.previousElement.endAddress = expectedAddress - 1

        actualAddress = self.testRegister.address
        self.assertEqual( actualAddress, expectedAddress )


if __name__ == '__main__' :
    unittest.main()
