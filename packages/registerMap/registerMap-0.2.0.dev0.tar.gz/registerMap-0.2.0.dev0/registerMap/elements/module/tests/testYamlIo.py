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

from registerMap.elements.module import \
    Module, \
    ParseError
from registerMap.structure.memory.space import MemorySpace
from registerMap.set import SetCollection

from registerMap.elements.tests.mockObserver import MockObserver

from .mocks import MockPreviousModule


log = logging.getLogger( __name__ )


class TestModuleYamlLoadSave( unittest.TestCase ) :
    def setUp( self ) :
        self.observer = MockObserver()
        self.previousModule = MockPreviousModule( endAddress = 0x0 )
        self.setCollection = SetCollection()
        self.testSpace = MemorySpace()
        self.testModule = Module( self.testSpace, self.setCollection )

        self.testModule.previousElement = self.previousModule
        self.testModule[ 'name' ] = 'module'
        self.testModule.sizeChangeNotifier.addObserver( self.observer )

        self.setCollection.moduleSet.add( self.testModule )

        self.acquiredSetCollection = SetCollection()


    def testEncodeDecode( self ) :
        self.testModule[ 'constraints' ][ 'fixedAddress' ] = 0x10
        self.createRegister( 'r1' )

        encodedYamlData = self.testModule.to_yamlData()
        log.debug( 'Encoded yaml data: ' + repr( encodedYamlData ) )
        decodedModule = Module.from_yamlData( encodedYamlData, self.testSpace, self.acquiredSetCollection )

        self.assertEqual( decodedModule[ 'constraints' ][ 'fixedAddress' ],
                          self.testModule[ 'constraints' ][ 'fixedAddress' ] )
        self.assertEqual( decodedModule[ 'description' ], self.testModule[ 'description' ] )
        self.assertEqual( decodedModule[ 'summary' ], self.testModule[ 'summary' ] )

        self.assertEqual( len( self.acquiredSetCollection.moduleSet ), 1 )

        decodedModule.previousElement = self.previousModule
        # No exceptions should be thrown
        decodedModule.reviewAddressChange()


    def createRegister( self, name ) :
        self.testModule.addRegister( name )

        self.testModule[ 'registers' ][ name ][ 'constraints' ][ 'fixedAddress' ] = 0x10
        self.testModule[ 'registers' ][ name ][ 'description' ] = 'some description'
        self.testModule[ 'registers' ][ name ][ 'mode' ] = 'ro'
        self.testModule[ 'registers' ][ name ][ 'public' ] = False
        self.testModule[ 'registers' ][ name ][ 'summary' ] = 'a summary'

        self.testModule[ 'registers' ][ name ].addField( 'f1', [ 3, 5 ], (3, 5) )
        self.testModule[ 'registers' ][ name ].addField( 'f2', [ 7, 7 ], (7, 7) )


    def testFromBadYamlData( self ) :
        yamlData = { 'mode' : 'ro' }

        with self.assertRaisesRegex( ParseError, '^Module is not defined in yaml data' ) :
            Module.from_yamlData( yamlData, self.testSpace, self.acquiredSetCollection )


    def testFromOptionalYamlData( self ) :
        yamlData = { 'mode' : 'ro' }

        decodedModule = Module.from_yamlData( yamlData, self.testSpace, self.acquiredSetCollection,
                                              optional = True )

        self.assertEqual( len( decodedModule[ 'constraints' ] ), 0 )
        self.assertEqual( decodedModule[ 'description' ], '' )
        self.assertIsNone( decodedModule[ 'name' ] )
        self.assertEqual( len( decodedModule[ 'registers' ] ), 0 )
        self.assertEqual( decodedModule[ 'summary' ], '' )


class TestModuleYamlParameters( unittest.TestCase ) :
    def setUp( self ) :
        self.previousModule = MockPreviousModule( endAddress = 0x215 )
        self.setCollection = SetCollection()
        self.testSpace = MemorySpace()
        self.testModule = Module( self.testSpace, self.setCollection )

        self.testModule.previousElement = self.previousModule


    def testYamlDataAddress( self ) :
        # The address data is automatically generated so it is prefixed by '_'.
        self.assertEqual( self.previousModule.endAddress, 0x215 )

        expectedName = '_address'
        expectedValue = 0x216

        self.assertEqual( self.testModule.baseAddress, expectedValue )

        yamlData = self.testModule.to_yamlData()
        self.assertEqual( yamlData[ 'module' ][ expectedName ], expectedValue )


    def testYamlDataSpan( self ) :
        # The address data is automatically generated so it is prefixed by '_'.
        expectedName = '_spanMemoryUnits'
        expectedValue = 0

        self.assertEqual( self.testModule.spanMemoryUnits, expectedValue )

        yamlData = self.testModule.to_yamlData()
        self.assertEqual( yamlData[ 'module' ][ expectedName ], expectedValue )


    def testYamlDataNoneAddress( self ) :
        testModule = Module( self.testSpace, self.setCollection )

        yamlData = testModule.to_yamlData()
        self.assertIsNone( yamlData[ 'module' ][ '_address' ] )


if __name__ == '__main__' :
    unittest.main()
