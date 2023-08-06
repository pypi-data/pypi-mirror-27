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
import registerMap.structure.memory.space as rmm

from registerMap.set import SetCollection

from registerMap.elements.tests.mockObserver import MockObserver
from .testRegister import MockPreviousRegister


log = logging.getLogger( __name__ )


class TestRegisterYamlLoadSave( unittest.TestCase ) :
    def setUp( self ) :
        self.sourceCollection = SetCollection()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.sourceCollection )

        self.observer = MockObserver()
        self.testRegister.sizeChangeNotifier.addObserver( self.observer )

        self.acquiredCollection = SetCollection()


    def testEncodeDecode( self ) :
        def checkFields() :
            """
            Test the register fields have been recovered correctly.
            """
            nonlocal self, decodedRegister

            self.assertEqual( decodedRegister[ 'fields' ][ 'f1' ][ 'name' ],
                              self.testRegister[ 'fields' ][ 'f1' ][ 'name' ] )
            self.assertEqual( decodedRegister[ 'fields' ][ 'f1' ][ 'size' ],
                              self.testRegister[ 'fields' ][ 'f1' ][ 'size' ] )
            self.assertEqual( decodedRegister[ 'fields' ][ 'f2' ][ 'name' ],
                              self.testRegister[ 'fields' ][ 'f2' ][ 'name' ] )
            self.assertEqual( decodedRegister[ 'fields' ][ 'f2' ][ 'size' ],
                              self.testRegister[ 'fields' ][ 'f2' ][ 'size' ] )

            self.assertEqual( len( self.acquiredCollection.registerSet ), 1 )

            # Ensure that acquired fields have been added to the field set.
            self.assertEqual( len( self.sourceCollection.fieldSet ), len( self.testRegister[ 'fields' ] ) )
            fieldSetIds = [ x.canonicalId for x in self.sourceCollection.fieldSet ]
            for thisField in decodedRegister[ 'fields' ].values() :
                self.assertIn( thisField.canonicalId, fieldSetIds )


        def checkParameters() :
            """
            Test the register parameters, other than 'fields', have been recovered correctly.
            """
            nonlocal self, decodedRegister

            self.assertEqual( decodedRegister[ 'constraints' ][ 'fixedAddress' ],
                              self.testRegister[ 'constraints' ][ 'fixedAddress' ] )
            self.assertEqual( decodedRegister[ 'description' ], self.testRegister[ 'description' ] )
            self.assertEqual( decodedRegister[ 'mode' ], self.testRegister[ 'mode' ] )
            self.assertEqual( decodedRegister[ 'name' ], self.testRegister[ 'name' ] )
            self.assertEqual( decodedRegister[ 'public' ], self.testRegister[ 'public' ] )
            self.assertEqual( decodedRegister[ 'summary' ], self.testRegister[ 'summary' ] )


        def checkBitMap() :
            nonlocal self, decodedRegister

            for thisField in self.acquiredCollection.fieldSet :
                # Assume that this test indicates the bitmap has acquired itself from YAML correctly;
                # other bit map specific tests will exhaustively test bit map YAML acquisition.
                self.assertIn( thisField, decodedRegister.bitMap.destinations )

                # Check that the reciprocal map has been established.
                self.assertIn( decodedRegister, thisField.bitMap.destinations )


        self.testRegister[ 'constraints' ][ 'fixedAddress' ] = 0x10
        self.testRegister[ 'description' ] = 'some description'
        self.testRegister[ 'mode' ] = 'ro'
        self.testRegister[ 'name' ] = 'registerName'
        self.testRegister[ 'public' ] = False
        self.testRegister[ 'summary' ] = 'a summary'

        self.testRegister.addField( 'f1', [ 3, 5 ], (0, 2) )
        self.testRegister.addField( 'f2', [ 7, 7 ], (0, 0) )

        self.assertEqual( self.testRegister.canonicalId, self.testRegister[ 'name' ] )

        encodedYamlData = self.testRegister.to_yamlData()
        log.debug( 'Encoded yaml data: ' + repr( encodedYamlData ) )
        decodedRegister = rmr.Register.from_yamlData( encodedYamlData, self.testSpace, self.acquiredCollection )

        checkFields()
        checkParameters()
        checkBitMap()


    def testDefaultEncodeDecode( self ) :
        encodedYamlData = self.testRegister.to_yamlData()
        log.debug( 'Encoded yaml data: ' + repr( encodedYamlData ) )
        decodedRegister = rmr.Register.from_yamlData( encodedYamlData, self.testSpace, self.sourceCollection )

        self.assertEqual( len( decodedRegister[ 'fields' ] ), 0 )
        self.assertEqual( len( decodedRegister[ 'constraints' ] ), 0 )
        self.assertEqual( decodedRegister[ 'description' ], '' )
        self.assertEqual( decodedRegister[ 'mode' ], 'rw' )
        self.assertIsNone( decodedRegister[ 'name' ] )
        self.assertEqual( decodedRegister[ 'public' ], True )
        self.assertEqual( decodedRegister[ 'summary' ], '' )


    def testBadYamlDataRaises( self ) :
        yamlData = { 'mode' : 'ro' }
        with self.assertRaisesRegex( rmr.ConfigurationError, '^Register is not defined in yaml data' ) :
            rmr.Register.from_yamlData( yamlData, self.testSpace, self.sourceCollection,
                                        optional = False )


    def testOptionalYamlData( self ) :
        yamlData = { 'mode' : 'ro' }
        decodedRegister = rmr.Register.from_yamlData( yamlData, self.testSpace, self.acquiredCollection,
                                                      optional = True )
        self.assertEqual( len( decodedRegister[ 'fields' ] ), 0 )
        self.assertEqual( len( decodedRegister[ 'constraints' ] ), 0 )
        self.assertEqual( decodedRegister[ 'description' ], '' )
        self.assertEqual( decodedRegister[ 'mode' ], 'rw' )
        self.assertIsNone( decodedRegister[ 'name' ] )
        self.assertEqual( decodedRegister[ 'public' ], True )
        self.assertEqual( decodedRegister[ 'summary' ], '' )


class TestRegisterYamlParameters( unittest.TestCase ) :
    def setUp( self ) :
        self.setCollection = SetCollection()
        self.testSpace = rmm.MemorySpace()
        self.testRegister = rmr.Register( self.testSpace, self.setCollection )

        self.previousRegister = MockPreviousRegister( endAddress = 0x3e7,
                                                      sizeMemoryUnits = 4 )
        self.testRegister.previousElement = self.previousRegister

        self.observer = MockObserver()
        self.testRegister.sizeChangeNotifier.addObserver( self.observer )


    def testYamlDataAddress( self ) :
        # The address data is automatically generated so it is prefixed by '_'.
        self.assertEqual( self.previousRegister.endAddress, 0x3e7 )

        expectedName = '_address'
        expectedValue = 0x3e8

        self.assertEqual( self.testRegister.address, expectedValue )

        yamlData = self.testRegister.to_yamlData()
        self.assertEqual( yamlData[ 'register' ][ expectedName ], expectedValue )


    def testYamlDataSpan( self ) :
        # The address data is automatically generated so it is prefixed by '_'.
        expectedName = '_sizeMemoryUnits'
        expectedValue = 1

        self.assertEqual( self.testRegister.sizeMemoryUnits, expectedValue )

        yamlData = self.testRegister.to_yamlData()
        self.assertEqual( yamlData[ 'register' ][ expectedName ], expectedValue )


class MockModule :
    def __init__( self, name ) :
        self.__name = name


    def __getitem__( self, item ) :
        assert item == 'name'

        return self.__name


class TestRegisterYamlLoadSaveCanonicalId( unittest.TestCase ) :
    def setUp( self ) :
        self.sourceCollection = SetCollection()
        self.space = rmm.MemorySpace()
        self.module = MockModule( 'module' )

        self.acquiredCollection = SetCollection()


    def testEncodeDecode( self ) :
        """
        The canonical ID of the decoded register much match that of the encoded register and is expected to include the
        module canonical ID.
        :return:
        """
        testRegister = rmr.Register( self.space, self.sourceCollection,
                                     parent = self.module )
        testRegister[ 'name' ] = 'register'

        self.sourceCollection.registerSet.add( testRegister )

        self.assertEqual( 'module.register', testRegister.canonicalId )

        encodedYamlData = testRegister.to_yamlData()
        log.debug( 'Encoded yaml data: ' + repr( encodedYamlData ) )
        decodedRegister = rmr.Register.from_yamlData( encodedYamlData, self.space, self.acquiredCollection,
                                                      parent = self.module )

        self.assertEqual( testRegister.canonicalId, decodedRegister.canonicalId )
        self.assertEqual( 'module.register', testRegister.canonicalId )


if __name__ == '__main__' :
    unittest.main()
