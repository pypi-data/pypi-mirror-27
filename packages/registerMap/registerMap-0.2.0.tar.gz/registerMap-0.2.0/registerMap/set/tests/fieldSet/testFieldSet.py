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

import registerMap.elements.field as rmbf
import registerMap.elements.register as rmbr
import registerMap.set.fieldSet as rmesb

from registerMap.structure.memory.space import MemorySpace

from registerMap.set.tests.elementSet import testElementSet as rmstes


class TestConstructFieldSet( unittest.TestCase ) :
    def testDefaultConstructor( self ) :
        b = rmesb.FieldSet()

        self.assertEqual( len( b ), 0 )


class TestSetAdd( rmstes.TestElementSetAdd ) :
    def getTestType( self ) :
        return rmesb.FieldSet


    def generateElement( self,
                         name = None ) :
        f = rmbf.Field()

        return f


class TestSetDiscard( rmstes.TestElementSetDiscard ) :
    def getTestType( self ) :
        return rmesb.FieldSet


    def generateElement( self,
                         name = None ) :
        f = rmbf.Field()

        return f


class TestSetSingleElement( rmstes.TestElementSetSingleElement ) :
    def getTestType( self ) :
        return rmesb.FieldSet


    def generateElement( self,
                         name = None ) :
        f = rmbf.Field()
        f[ 'name' ] = name

        return f


class TestSetMultipleElements( rmstes.TestElementSetMultipleElements ) :
    memory = MemorySpace()
    registers = list()
    fieldSet = rmesb.FieldSet()


    def getTestType( self ) :
        return rmesb.FieldSet


    def generateElement( self,
                         name = None ) :
        self.registers.append( rmbr.Register( self.memory, self.fieldSet ) )
        f = rmbf.Field( parent = self.registers[ -1 ] )
        f[ 'name' ] = name

        return f


if __name__ == '__main__' :
    unittest.main()
