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
import unittest.mock

from registerMap.elements.field import Field
from registerMap.set.elementSet import ElementSet
from registerMap.structure.bitrange import BitRange

from .mocks import MockBitStore

from .. import \
    BitMap, \
    ConfigurationError, \
    ParseError


log = logging.getLogger( __name__ )


class TestDecodeYamlBitMap( unittest.TestCase ) :
    def setUp( self ) :
        self.destinationSet = ElementSet()
        self.sourceSet = ElementSet()

        self.mockSource = MockBitStore( 'module.register', 10 )
        self.bitMapUnderTest = BitMap( self.mockSource )

        self.mockSource.bitMap = self.bitMapUnderTest

        self.sourceSet.add( self.mockSource )


    def testDecodeEmptyBitMap( self ) :
        # An empty bitmap encodes only the source info

        encodedYamlData = self.bitMapUnderTest.to_yamlData()

        decodedBitMap = BitMap.from_yamlData( encodedYamlData, self.sourceSet, self.destinationSet )

        self.assertEqual( decodedBitMap.source, self.mockSource )
        self.assertEqual( len( decodedBitMap.destinations ), 0 )
        self.assertEqual( len( decodedBitMap.intervalMap ), 0 )


    def testSourceElementDoesNotExistRaises( self ) :
        # Decoding a bit map where the element set does not contain the specified source element raises.

        encodedYamlData = self.bitMapUnderTest.to_yamlData()

        emptySet = ElementSet()

        with self.assertRaisesRegex( ConfigurationError, '^Source object not found in element set' ) :
            BitMap.from_yamlData( encodedYamlData, emptySet, self.destinationSet )


    def testMissingYamlSourceIdRaises( self ) :
        yamlData = { 'bitmap' : { } }
        with self.assertRaisesRegex( ParseError, '^Source id not specified in YAML' ) :
            BitMap.from_yamlData( yamlData, self.sourceSet, self.destinationSet )


class TestDecodeYamlBitMapIntervals( unittest.TestCase ) :
    def setUp( self ) :
        self.destinationSet = ElementSet()
        self.sourceSet = ElementSet()


        def constructMockDestination() :
            nonlocal self

            self.destinationMockBitmap = unittest.mock.create_autospec( BitMap )

            self.mockDestination = unittest.mock.create_autospec( Field )

            idp = unittest.mock.PropertyMock( return_value = 'module.register.field' )
            type( self.mockDestination ).id = idp

            idbm = unittest.mock.PropertyMock( return_value = self.destinationMockBitmap )
            type( self.mockDestination ).bitMap = idbm


        self.mockSource = MockBitStore( 'module.register', 10 )
        self.bitMapUnderTest = BitMap( self.mockSource )

        self.mockSource.bitMap = self.bitMapUnderTest

        constructMockDestination()

        self.sourceSet.add( self.mockSource )
        self.destinationSet.add( self.mockDestination )


    def testDecodeIntervals( self ) :
        def checkDestinations() :
            nonlocal decodedBitMap, self

            self.assertEqual( len( decodedBitMap.destinations ), 1 )
            self.assertIn( self.mockDestination, decodedBitMap.destinations )


        def checkMapping() :
            nonlocal decodedBitMap, self

            self.assertEqual( len( decodedBitMap.intervalMap ), 1 )

            intervalData = decodedBitMap.intervalMap[ BitRange( [ 0, 3 ] ) ]
            self.assertEqual( intervalData[ 'interval' ], BitRange( [ 0, 3 ] ) )
            self.assertEqual( intervalData[ 'destination' ], self.mockDestination )


        with unittest.mock.patch.object( BitMap, '_BitMap__validateBitRange' ) :
            with unittest.mock.patch.object( BitMap, '_BitMap__validateSourceOverlaps' ) :
                self.bitMapUnderTest.mapBits( BitRange( [ 0, 3 ] ), BitRange( (0, 3) ), self.mockDestination )

                encodedYamlData = self.bitMapUnderTest.to_yamlData()

                decodedBitMap = BitMap.from_yamlData( encodedYamlData, self.sourceSet, self.destinationSet )

                self.assertEqual( decodedBitMap.source, self.mockSource )

                checkDestinations()
                checkMapping()


if __name__ == '__main__' :
    unittest.main()
