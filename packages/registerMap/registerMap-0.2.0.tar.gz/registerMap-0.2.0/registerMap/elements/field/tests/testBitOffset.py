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

import registerMap.elements.field.bitOffset as rmbo


class TestBitOffsetAssignInterval( unittest.TestCase ) :
    def setUp( self ) :
        self.bitOffset = rmbo.BitOffset()


    def testAddInterval( self ) :
        self.assertEqual( self.bitOffset.numberBits, 0 )

        interval = (2, 6)

        self.bitOffset.assignInterval( interval )

        self.assertTrue( self.bitOffset.isIntervalIn( interval ) )
        self.assertEqual( self.bitOffset.numberBits, 7 )


    def testAddContiguousInterval( self ) :
        self.assertEqual( self.bitOffset.numberBits, 0 )

        intervals = [ (2, 4), (5, 8) ]
        self.bitOffset.assignInterval( intervals[ 0 ] )
        self.bitOffset.assignInterval( intervals[ 1 ] )

        for interval in intervals :
            self.assertTrue( self.bitOffset.isIntervalIn( interval ) )

        self.assertEqual( self.bitOffset.numberBits, 9 )


    def testAddDisjointInterval( self ) :
        self.assertEqual( self.bitOffset.numberBits, 0 )

        intervals = [ (2, 4), (6, 8) ]
        for interval in intervals :
            self.bitOffset.assignInterval( interval )

        for interval in intervals :
            self.assertTrue( self.bitOffset.isIntervalIn( interval ) )

        self.assertEqual( self.bitOffset.numberBits, 9 )


    def testAddDuplicateIntervalNoEffect( self ) :
        interval = (2, 6)
        self.bitOffset.assignInterval( interval )
        # No effect from adding a duplicate interval
        self.bitOffset.assignInterval( interval )


class TestBitOffsetDefaultConstructor( unittest.TestCase ) :
    def testDefaultInterval( self ) :
        o = rmbo.BitOffset()

        self.assertEqual( o.numberBits, 0 )
        self.assertTrue( o.isContiguousIntervals )


    def testSetNumberBits( self ) :
        expectedNumberBits = 10
        o = rmbo.BitOffset( numberBits = expectedNumberBits )

        self.assertEqual( o.numberBits, expectedNumberBits )
        self.assertTrue( o.isContiguousIntervals )


class TestBitOffsetIsContiguousIntervals( unittest.TestCase ) :
    def setUp( self ) :
        self.bitOffset = rmbo.BitOffset()


    def testEmptyEqualsTrue( self ) :
        self.assertTrue( self.bitOffset.isContiguousIntervals )


    def testSingleContiguousInterval( self ) :
        self.bitOffset.assignInterval( (0, 2) )

        self.assertTrue( self.bitOffset.isContiguousIntervals )


    def testMultipleContiguousIntervals( self ) :
        self.bitOffset.assignInterval( (0, 2) )
        self.bitOffset.assignInterval( (3, 8) )
        self.bitOffset.assignInterval( (9, 12) )

        self.assertTrue( self.bitOffset.isContiguousIntervals )


    def testSingleDisjointInterval( self ) :
        self.bitOffset.assignInterval( (2, 4) )

        self.assertFalse( self.bitOffset.isContiguousIntervals )


    def testMultipleDisjointIntervals( self ) :
        self.bitOffset.assignInterval( (0, 4) )
        self.bitOffset.assignInterval( (8, 10) )

        self.assertFalse( self.bitOffset.isContiguousIntervals )


class TestBitOffsetRange( unittest.TestCase ) :
    def setUp( self ) :
        self.bitOffset = rmbo.BitOffset()


    def testDefaultRange( self ) :
        r = self.bitOffset.range

        self.assertEqual( r.numberBits, 0 )


class TestBitOffsetRemoveInterval( unittest.TestCase ) :
    def setUp( self ) :
        numberBitsForTest = 4
        self.bitOffset = rmbo.BitOffset( numberBits = numberBitsForTest )

        self.assertEqual( self.bitOffset.numberBits, numberBitsForTest )


    def testRemoveDefaultInterval( self ) :
        self.assertTrue( self.bitOffset.isIntervalIn( (0, 3) ) )

        self.bitOffset.removeInterval( (0, 3) )

        self.assertEqual( self.bitOffset.numberBits, 0 )


class TestBitOffsetValidateInterval( unittest.TestCase ) :
    def setUp( self ) :
        self.testBitOffset = rmbo.BitOffset()


    def testCompliantIntervalPasses( self ) :
        self.testBitOffset.assignInterval( (4, 5) )


    def testZeroElementPasses( self ) :
        self.testBitOffset.assignInterval( (0, 5) )


    def testNotTwoElementsRaises( self ) :
        with self.assertRaisesRegex( rmbo.ConfigurationError,
                                     '^Interval must be a set of one or two positive integers' ) :
            self.testBitOffset.assignInterval( (4, 5, 4) )

        with self.assertRaisesRegex( rmbo.ConfigurationError,
                                     '^Interval must be a set of one or two positive integers' ) :
            self.testBitOffset.assignInterval( tuple() )


    def testNonIntElementRaises( self ) :
        with self.assertRaisesRegex( rmbo.ConfigurationError,
                                     '^Interval must be a set of one or two positive integers' ) :
            self.testBitOffset.assignInterval( (4, '5') )


    def testNegativeElementRaises( self ) :
        with self.assertRaisesRegex( rmbo.ConfigurationError,
                                     '^Interval must be a set of one or two positive integers' ) :
            self.testBitOffset.assignInterval( (-4, 5) )


    def testOverlappingIntervalsRaises( self ) :
        self.testBitOffset.assignInterval( (2, 6) )

        with self.assertRaisesRegex( rmbo.ConfigurationError, '^Interval overlaps with existing intervals' ) :
            self.testBitOffset.assignInterval( (6, 8) )


class TestBitOffsetNumberBits( unittest.TestCase ) :
    def setUp( self ) :
        self.bitOffset = rmbo.BitOffset()

        self.assertEqual( self.bitOffset.numberBits, 0 )


    def testSingleInterval( self ) :
        self.bitOffset.numberBits = 4

        self.assertEqual( self.bitOffset.numberBits, 4 )


    def testContiguousIntervals( self ) :
        self.bitOffset.assignInterval( (2, 4) )
        self.assertEqual( self.bitOffset.numberBits, 5 )

        self.bitOffset.assignInterval( (5, 8) )

        self.assertEqual( self.bitOffset.numberBits, 9 )


    def testDisjointIntervals( self ) :
        self.bitOffset.assignInterval( (2, 3) )
        self.assertEqual( self.bitOffset.numberBits, 4 )

        self.bitOffset.assignInterval( (6, 8) )

        self.assertEqual( self.bitOffset.numberBits, 9 )


    def testSetNumberBitsBelowMaxInterval( self ) :
        self.bitOffset.assignInterval( (2, 3) )
        self.assertEqual( self.bitOffset.numberBits, 4 )

        with self.assertRaisesRegex( rmbo.ConfigurationError, '^Remove intervals to reduce number of bits' ) :
            self.bitOffset.numberBits = 2


if __name__ == '__main__' :
    unittest.main()
