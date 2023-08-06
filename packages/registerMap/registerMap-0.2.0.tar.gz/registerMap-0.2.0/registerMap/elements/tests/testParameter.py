#
# Copyright 2017 Russell Smiley
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

import unittest

import registerMap.elements.parameter as rmp
import registerMap.structure.memory.space as rmm


class TestParameter( unittest.TestCase ) :
    def testInitialization( self ) :
        expectedName = 'someName'
        expectedValue = 31415
        p = rmp.Parameter( expectedName, expectedValue )

        self.assertEqual( p.name, expectedName )
        self.assertEqual( p.value, expectedValue )


    def testToYamlData( self ) :
        expectedName = 'someName'
        expectedValue = 31415
        p = rmp.Parameter( expectedName, expectedValue )

        expectedYamlData = { expectedName : expectedValue }
        actualYamlData = p.to_yamlData( )

        self.assertEqual( actualYamlData, expectedYamlData )


    def testFromGoodYamlData( self ) :
        expectedName = 'someName'
        expectedValue = 31415
        yamlData = { expectedName : expectedValue }

        actualParameter = rmp.Parameter.from_yamlData( yamlData, expectedName )

        self.assertEqual( actualParameter.name, expectedName )
        self.assertEqual( actualParameter.value, expectedValue )


    def testFromBadYamlDataRaises( self ) :
        expectedName = 'someName'
        expectedValue = 31415
        yamlData = { 'badname' : expectedValue }

        with self.assertRaisesRegex( rmp.ParseError, '^Parameter is not in yaml data' ) :
            rmp.Parameter.from_yamlData( yamlData, expectedName )


    def testOptionalFromYamlDataNoRaise( self ) :
        expectedName = 'someName'
        expectedValue = 31415
        yamlData = { 'othername' : expectedValue }

        actualParameter = rmp.Parameter.from_yamlData( yamlData, expectedName,
                                                       optional = True )

        self.assertEqual( actualParameter.name, expectedName )
        self.assertIsNone( actualParameter.value )


class TestConstraintsParameter( unittest.TestCase ) :
    def setUp( self ) :
        self.testMemory = rmm.MemorySpace( )


    def testInitialization( self ) :
        p = rmp.ConstraintsParameter( self.testMemory )

        self.assertEqual( p.name, 'constraints' )
        self.assertTrue( isinstance( p.value, rmp.rmc.ConstraintTable ) )


    def testToYamlData( self ) :
        p = rmp.ConstraintsParameter( self.testMemory )

        p.value[ 'fixedAddress' ] = 0x10
        p.value[ 'fixedSizeMemoryUnits' ] = 5
        p.value[ 'alignmentMemoryUnits' ] = 2
        expectedYamlData = { 'constraints' : { 'fixedAddress' : 0x10,
                                               'fixedSize' : 5,
                                               'alignment' : 2 } }
        actualYamlData = p.to_yamlData( )

        self.assertEqual( actualYamlData, expectedYamlData )


    def testFromGoodYamlData( self ) :
        p = rmp.ConstraintsParameter( self.testMemory )

        p.value[ 'fixedAddress' ] = 0x10
        p.value[ 'fixedSizeMemoryUnits' ] = 5
        p.value[ 'alignmentMemoryUnits' ] = 2

        yamlData = p.to_yamlData( )
        generatedParameter = rmp.ConstraintsParameter.from_yamlData( yamlData, self.testMemory )

        self.assertEqual( p.value[ 'fixedAddress' ], generatedParameter.value[ 'fixedAddress' ] )
        self.assertEqual( p.value[ 'fixedSizeMemoryUnits' ], generatedParameter.value[ 'fixedSizeMemoryUnits' ] )
        self.assertEqual( p.value[ 'alignmentMemoryUnits' ], generatedParameter.value[ 'alignmentMemoryUnits' ] )


    def testGoodDataWithOtherParameter( self ) :
        p = rmp.ConstraintsParameter( self.testMemory )

        p.value[ 'fixedAddress' ] = 0x10
        p.value[ 'fixedSizeMemoryUnits' ] = 5
        p.value[ 'alignmentMemoryUnits' ] = 2

        yamlData = p.to_yamlData( )
        yamlData[ 'mode' ] = 'ro'
        generatedParameter = rmp.ConstraintsParameter.from_yamlData( yamlData, self.testMemory )

        self.assertEqual( p.value[ 'fixedAddress' ], generatedParameter.value[ 'fixedAddress' ] )
        self.assertEqual( p.value[ 'fixedSizeMemoryUnits' ], generatedParameter.value[ 'fixedSizeMemoryUnits' ] )
        self.assertEqual( p.value[ 'alignmentMemoryUnits' ], generatedParameter.value[ 'alignmentMemoryUnits' ] )


    def testBadYamlDataRaises( self ) :
        yamlData = { 'mode' : 'ro' }

        with self.assertRaisesRegex( rmp.ParseError, '^Yaml data does not specify constraints' ) :
            rmp.ConstraintsParameter.from_yamlData( yamlData, self.testMemory )


    def testOptionalYamlData( self ) :
        yamlData = { 'mode' : 'ro' }
        generatedParameter = rmp.ConstraintsParameter.from_yamlData( yamlData, self.testMemory,
                                                                     optional = True )
        self.assertEqual( len( generatedParameter.value ), 0 )
