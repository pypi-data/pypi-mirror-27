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

import unittest

import registerMap.elements.register as rmr
import registerMap.exceptions as rme
import registerMap.structure.memory.space as rmm

from registerMap.set import SetCollection

from registerMap.elements.tests.mockObserver import MockObserver


class TestRegisterSizeBits( unittest.TestCase ) :
    def setUp( self ) :
        self.observer = MockObserver()
        self.setCollection = SetCollection()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.setCollection )

        self.testRegister.sizeChangeNotifier.addObserver( self.observer )


    def testCorrectSizeForFieldsAdded( self ) :
        self.assertEqual( self.observer.updateCount, 0 )

        memoryUnitsSizeBits = self.testSpace.memoryUnitBits

        self.testRegister.addField( 'f1', [ 0, 7 ], (0, 7) )
        self.assertEqual( self.testRegister.sizeBits, memoryUnitsSizeBits )

        self.testRegister.addField( 'f2', [ 8, 10 ], (0, 2) )
        self.assertEqual( self.testRegister.sizeBits, (2 * memoryUnitsSizeBits) )


class TestRegisterSize( unittest.TestCase ) :
    def setUp( self ) :
        self.observer = MockObserver()
        self.setCollection = SetCollection()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.setCollection )

        self.testRegister.sizeChangeNotifier.addObserver( self.observer )


    def testDefaultValue( self ) :
        # A register with no bit fields must allocate one memory unit for itself.
        self.assertEqual( self.testRegister.sizeMemoryUnits, 1 )


    def testCorrectSizeForBitFieldsAdded1( self ) :
        # Adding two intervals to a register increases the register size:
        #  - from different fields
        #  - the second register interval exceeds the existing register size
        self.assertEqual( self.testSpace.memoryUnitBits, 8 )
        self.assertEqual( self.observer.updateCount, 0 )

        self.testRegister.addField( 'f1', [ 0, 7 ], (0, 7) )
        self.assertEqual( self.testRegister.sizeMemoryUnits, 1 )
        # No notifications because the field addition didn't change the register size.
        self.assertEqual( self.observer.updateCount, 0 )

        self.testRegister.addField( 'f2', [ 8, 10 ], (0, 2) )
        self.assertEqual( self.testRegister.sizeMemoryUnits, 2 )
        self.assertEqual( self.observer.updateCount, 1 )
        self.assertEqual( self.testRegister[ 'fields' ][ 'f1' ][ 'size' ], 8 )
        self.assertEqual( self.testRegister[ 'fields' ][ 'f2' ][ 'size' ], 3 )


    def testCorrectSizeForBitFieldsAdded2( self ) :
        # Adding two intervals to a register increases the register size:
        #  - from different fields
        #  - the first register interval does not exceed the register size, but the second interval does
        self.assertEqual( self.testSpace.memoryUnitBits, 8 )
        self.assertEqual( self.observer.updateCount, 0 )

        self.testRegister.addField( 'f1', [ 0, 3 ], (0, 3) )
        self.assertEqual( self.testRegister.sizeMemoryUnits, 1 )
        self.assertEqual( self.observer.updateCount, 0 )

        self.testRegister.addField( 'f2', [ 8, 10 ], (0, 2) )
        self.assertEqual( self.testRegister.sizeMemoryUnits, 2 )
        self.assertEqual( self.observer.updateCount, 1 )
        self.assertEqual( self.testRegister[ 'fields' ][ 'f1' ][ 'size' ], 4 )
        self.assertEqual( self.testRegister[ 'fields' ][ 'f2' ][ 'size' ], 3 )


    def testCorrectSizeForBitFieldsAdded3( self ) :
        # Adding two intervals to a register does not increase the register size:
        #  - from the same field
        #  - the extent of the new register intervals is less than the size of the register
        #  - the extent of the second field interval changes the size of the field
        #  - the FieldSet does not change size
        self.assertEqual( self.testSpace.memoryUnitBits, 8 )
        self.assertEqual( self.observer.updateCount, 0 )

        self.testRegister.addField( 'f1', [ 0, 3 ], (0, 3) )
        self.assertEqual( self.testRegister.sizeMemoryUnits, 1 )
        self.assertEqual( self.testRegister[ 'fields' ][ 'f1' ][ 'size' ], 4 )
        # No notifications because the field addition didn't change the register size.
        self.assertEqual( self.observer.updateCount, 0 )
        self.testRegister.addField( 'f1', [ 6, 7 ], (5, 6) )

        self.assertEqual( self.testRegister.sizeMemoryUnits, 1 )
        self.assertEqual( self.observer.updateCount, 0 )
        self.assertEqual( self.testRegister[ 'fields' ][ 'f1' ][ 'size' ], 7 )
        self.assertEqual( len( self.setCollection.fieldSet ), 1 )
        self.assertEqual( len( self.testRegister.bitMap.sourceIntervals ), 2 )


    def testFixedSizeExceededAddBitfieldRaises( self ) :
        self.assertEqual( self.testSpace.memoryUnitBits, 8 )

        self.testRegister[ 'constraints' ][ 'fixedSizeMemoryUnits' ] = 1
        self.testRegister.addField( 'f1', [ 0, 6 ], [ 0, 6 ] )
        with self.assertRaisesRegex( rme.ConstraintError, '^Fixed size exceeded' ) :
            self.testRegister.addField( 'f2', [ 8, 10 ], (0, 2) )


    def testFixedSizeConstraintReportsAsSize( self ) :
        self.assertEqual( self.testSpace.memoryUnitBits, 8 )

        expectedSize = 2
        self.testRegister[ 'constraints' ][ 'fixedSizeMemoryUnits' ] = expectedSize

        self.assertEqual( self.testRegister.sizeMemoryUnits, expectedSize )
        self.assertEqual( self.observer.updateCount, 1 )


if __name__ == '__main__' :
    unittest.main()
