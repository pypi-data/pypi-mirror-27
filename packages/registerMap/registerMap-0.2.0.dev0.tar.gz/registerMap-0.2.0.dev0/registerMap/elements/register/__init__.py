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
import math

import registerMap.elements.field as rmf
import registerMap.elements.parameter as rmp
import registerMap.structure.memory.element as rme
import registerMap.utility.io.yaml.parameters.encode as rye
import registerMap.utility.observer as rmo

from registerMap.elements.base import \
    BitStoreInterface, \
    IdentityElement, \
    AddressObservableInterface, \
    SizeObservableInterface

from registerMap.set.elementSet import ElementSet
from registerMap.structure.bitmap import BitMap
from registerMap.structure.bitrange import BitRange
from registerMap.utility.io import yaml

from registerMap.exceptions import ConfigurationError

from . import parameters as rmrp


log = logging.getLogger( __name__ )


class Register( IdentityElement,
                BitStoreInterface,
                AddressObservableInterface,
                SizeObservableInterface,
                yaml.Export,
                yaml.Import ) :
    __defaultSize = 1
    __yamlName = 'register'


    class SizeChangeObserver( rmo.Observer ) :
        def __init__( self, owner ) :
            self.__owner = owner


        def update( self, observable, arguments ) :
            self.__owner.reviewSizeChange()


    class AddressChangeObserver( rmo.Observer ) :
        def __init__( self, owner ) :
            self.__owner = owner


        def update( self, observable, arguments ) :
            # Register is only interested in the affect of address bits, memory unit bits or page size on its own
            # address from the memory space.
            # For constraints, Register is only interested in fixed address and alignment.
            # Ignore base address change which will be propagated from the previous register notification.
            if arguments not in [ 'baseAddress' ] :
                self.__owner.reviewAddressChange()


    def __init__( self, memorySpace, setCollection,
                  parent = None ) :
        super().__init__()

        self.addressChangeNotifier = rmo.Observable()
        self.sizeChangeNotifier = rmo.Observable()

        self.__addressObserver = Register.AddressChangeObserver( self )
        self.__setCollection = setCollection
        self.__bitMap = BitMap( self )
        self.__element = rme.AddressableMemoryElement()
        self.__memory = memorySpace
        self.__parentModule = parent
        self.__previousRegister = None
        self.__sizeObserver = Register.SizeChangeObserver( self )

        self.__data = {
            'fields' : rmrp.BitFieldsParameter(),
            'constraints' : rmp.ConstraintsParameter( self.__memory ),
            'description' : rmp.Parameter( 'description', '' ),
            'global' : rmrp.GlobalParameter( self ),
            'mode' : rmrp.ModeParameter( 'rw' ),
            'name' : rmp.Parameter( 'name', None ),
            'public' : rmrp.PublicParameter( True ),
            'summary' : rmp.Parameter( 'summary', '' )
        }

        self.__element.sizeMemoryUnits = 1
        self.__registerConstraintNotifiers()


    def __registerConstraintNotifiers( self ) :
        self.__memory.addressChangeNotifier.addObserver( self.__addressObserver )
        self.__data[ 'constraints' ].value.addressChangeNotifier.addObserver( self.__addressObserver )
        self.__data[ 'constraints' ].value.sizeChangeNotifier.addObserver( self.__sizeObserver )


    def reviewSizeChange( self ) :
        newSize = self.__calculateExtentMemoryUnits()
        if newSize != self.__element.sizeMemoryUnits :
            self.__element.sizeMemoryUnits = newSize
            self.sizeChangeNotifier.notifyObservers()


    def reviewAddressChange( self ) :
        newStartAddress = self.__calculateStartAddress()
        if newStartAddress != self.__element.startAddress :
            self.__element.startAddress = newStartAddress
            self.addressChangeNotifier.notifyObservers()


    @property
    def address( self ) :
        """
        The first memory unit (the smallest numerical address value) used by the register.
        """
        return self.__element.startAddress


    @property
    def bitMap( self ) :
        return self.__bitMap


    @property
    def canonicalId( self ) :
        if self.__parentModule is not None :
            canonicalName = '{0}.{1}'.format( self.__parentModule[ 'name' ],
                                              self.__data[ 'name' ].value )
        else :
            canonicalName = '{0}'.format( self.__data[ 'name' ].value )
        return canonicalName


    @property
    def endAddress( self ) :
        """
        The last memory unit (the largest numerical address value) used by the register.
        """
        return self.__element.endAddress


    @property
    def memory( self ) :
        return self.__memory


    @property
    def parent( self ) :
        return self.__parentModule


    @property
    def previousElement( self ) :
        """
        The previous register from which to derive the address of the current register.
        """
        return self.__previousRegister


    @previousElement.setter
    def previousElement( self, previousRegister ) :
        self.__previousRegister = previousRegister
        self.__previousRegister.sizeChangeNotifier.addObserver( self.__addressObserver )
        self.__previousRegister.addressChangeNotifier.addObserver( self.__addressObserver )

        # An address or size change in the previous register can affect the address of the current register, but the
        # previous register should have no effect on the size of the current register which is determined by
        # constraints and bit fields.
        self.reviewAddressChange()


    @property
    def sizeAllocatedFields( self ) :
        """
        The total number of bits in the field intervals allocated to this register.
        """
        allocatedBits = 0
        for thisInterval in self.__bitMap.sourceIntervals :
            allocatedBits += thisInterval.numberBits

        return allocatedBits


    @property
    def sizeBits( self ) :
        """
        The number of bits in the memory units used by the register.
        """
        numberBits = self.__element.sizeMemoryUnits * self.__memory.memoryUnitBits
        return numberBits


    @property
    def sizeMemoryUnits( self ) :
        """
        The integer number of memory units used by the register.
        """
        return self.__element.sizeMemoryUnits


    def addField( self, name, registerBitInterval,
                  fieldBitInterval = None,
                  isGlobal = False ) :
        """
        :param name: Name of new field. Must be unique to the register the field is a member of, except special
        names 'reserved' and 'unassigned'. If isGlobal is True then the name must be unique in the set of global
        fields, otherwise the specified ranges will be added to the existing global field definition.
        :param registerBitInterval: Range of register bits allocated to the new field.
        :param fieldBitInterval: Range of field bits allocated to the register.
        :param isGlobal: Is the new field referencing a global field definition?
        :return:
        """


        def createNewField() :
            nonlocal fieldBitInterval, isGlobal, name, registerBitInterval, self

            log.debug(
                'Creating new bit field, {0}.{1}, {2}<=>{3}'.format( self[ 'name' ],
                                                                     name,
                                                                     registerBitInterval,
                                                                     fieldBitInterval ) )
            if fieldBitInterval is None :
                fieldBitInterval = ((max( registerBitInterval ) - min( registerBitInterval )), 0)

            if not isGlobal :
                newField = rmf.Field( parent = self )
            else :
                newField = rmf.Field()

            newField[ 'name' ] = name
            newField[ 'size' ] = max( fieldBitInterval ) + 1

            # Need to consider the impact of the new field on register size now, otherwise mapping bits can raise.
            self.__reviewRegisterSize( registerBitInterval )

            self.__bitMap.mapBits( BitRange( registerBitInterval ), BitRange( fieldBitInterval ), newField )

            self.__setCollection.fieldSet.add( newField )
            self.__data[ 'fields' ].value[ newField[ 'name' ] ] = newField

            return newField


        def addToGlobal() :
            nonlocal existingFields, fieldBitInterval, name, registerBitInterval, self

            log.debug( 'Modifying the existing global field, {0}'.format( name ) )
            globalField = [ x for x in existingFields if x[ 'global' ] ]

            # If there's 0, or >1 then something has gone wrong in the function above.
            assert len( globalField ) == 1

            revisedField = addToField( globalField[ 0 ] )

            return revisedField


        def addToField( thisField ) :
            nonlocal fieldBitInterval, registerBitInterval, self

            assert fieldBitInterval is not None

            # Need to consider the impact of the new field on register and field size now, otherwise mapping bits can raise.
            self.__reviewRegisterSize( registerBitInterval )
            self.__reviewFieldSize( thisField, fieldBitInterval )

            self.__bitMap.mapBits( BitRange( registerBitInterval ), BitRange( fieldBitInterval ), thisField )

            return thisField


        def addToLocal( localField ) :
            nonlocal name, self

            log.debug( 'Modifying the existing local field, {0}'.format( name ) )

            revisedField = addToField( localField )

            return revisedField


        existingFields = self.__setCollection.fieldSet.find( name )
        existingFieldsThisRegister = [ x for x in existingFields if
                                       (not x[ 'global' ]) and all( [ y == self for y in x.bitMap.destinations ] ) ]
        if existingFields \
                and (not isGlobal) \
                and any( existingFieldsThisRegister ) :
            # User has requested a local field

            # If there's 0, or >1 then something has gone wrong; there can be only one local field with a given name
            # in a register.
            assert len( existingFieldsThisRegister ) == 1

            field = addToLocal( existingFieldsThisRegister[ 0 ] )
        elif existingFields \
                and isGlobal \
                and any( [ x[ 'global' ] for x in existingFields ] ) :
            # User has requested a global field and one already exists.
            field = addToGlobal()
        else :
            # Create a new field.
            field = createNewField()

        log.debug( 'Subscribing to field changes, {0}, for {1}'.format(
            field[ 'name' ],
            self.__data[ 'name' ] ) )
        field.sizeChangeNotifier.addObserver( self.__sizeObserver )

        return field


    def __reviewRegisterSize( self, registerInterval ) :
        # Register size only needs to be increased by the size of the interval being allocated to the register.
        # The field size could be larger even though it is new, for various reasons.
        #   eg. register[2:4] <=> field[5:7] => field size = 8, interval size = 3
        #       therefore the register potentially only needs to increase by 3 bits (interval size)
        proposedRegisterExtent = max( registerInterval ) + 1

        if proposedRegisterExtent > self.sizeBits :
            # Increase the size of the register to accomodate.
            log.debug( 'Register size increasing from adding new field, {0}'.format( self[ 'name' ] ) )

            newSizeChangeMemoryUnits = math.ceil(
                float( proposedRegisterExtent - self.sizeBits ) / self.__memory.memoryUnitBits )
            newSizeMemoryUnits = self.__element.sizeMemoryUnits + newSizeChangeMemoryUnits
            finalSize = self.__data[ 'constraints' ].value.applySizeConstraints( newSizeMemoryUnits )
            self.__element.sizeMemoryUnits = finalSize

            self.sizeChangeNotifier.notifyObservers()


    def __reviewFieldSize( self, existingField, fieldInterval ) :
        # A field interval defines the bits in the field being assigned.
        # The max of the interval indicates the extent of the field.
        # If the extent from the interval is greater than the current field size (extent) then the field must be resized.
        proposedFieldExtent = max( fieldInterval ) + 1
        if proposedFieldExtent > existingField.sizeBits :
            log.debug( 'Existing field size increasing with new interval, {0}'.format( existingField[ 'name' ] ) )
            existingField[ 'size' ] = proposedFieldExtent

            existingField.sizeChangeNotifier.notifyObservers()


    def __calculateStartAddress( self ) :
        if (self.__previousRegister is not None) and (self.__previousRegister.endAddress is not None) :
            # Page register impact is calculate before application of constraints. This means that constraints could
            # still affect the address. eg. if address alignment modified the affect of page register on the address.
            proposedAddress = self.__previousRegister.endAddress + 1
            initialAddress = self.__memory.calculatePageRegisterImpact( proposedAddress )
        else :
            initialAddress = None

        newAddress = self.__data[ 'constraints' ].value.applyAddressConstraints( initialAddress )

        return newAddress


    def __calculateExtentMemoryUnits( self ) :
        """
        The total number of memory units in the register after any constraints have been applied.

        Since the number of memory units is quantized to the memory unit size, then the result of this function
        implicitly includes both assigned and unassigned bits.
        """
        allBits = self.sizeAllocatedFields

        sizeMemoryUnits = math.ceil( float( allBits ) / self.__memory.memoryUnitBits )

        finalSize = self.__data[ 'constraints' ].value.applySizeConstraints( sizeMemoryUnits )
        if finalSize != sizeMemoryUnits :
            log.info( 'Constraint applied in calculating register size, {0}'.format( self[ 'name' ] ) )

        return finalSize


    def fieldExists( self, name ) :
        fieldInData = name in self.__data[ 'fields' ].value

        return fieldInData


    def __getitem__( self, item ) :
        return self.__data[ item ].value


    def __setitem__( self, key, value ) :
        self.__data[ key ].validate( value )

        self.__data[ key ].value = value
        # Assume that any change events in bit fields or constraints will be taken care of using registered observers
        # of the relevant objects.


    @classmethod
    def from_yamlData( cls, yamlData, memorySpace, setCollection,
                       optional = False,
                       parent = None ) :
        def acquireFields( thisData ) :
            nonlocal register
            register.__data[ 'fields' ] = rmrp.BitFieldsParameter.from_yamlData( thisData,
                                                                                 optional = True,
                                                                                 parent = register )

            for field in register.__data[ 'fields' ].value.values() :
                setCollection.fieldSet.add( field )


        def acquireBitMap( thisData ) :
            nonlocal setCollection, register

            register.__bitMap = BitMap.from_yamlData( thisData,
                                                      setCollection.registerSet,
                                                      setCollection.fieldSet )


        def acquireConstraints( thisData ) :
            nonlocal cls, memorySpace, register
            register.__data[ 'constraints' ] = rmp.ConstraintsParameter.from_yamlData( thisData, memorySpace,
                                                                                       optional = True )
            register.__registerConstraintNotifiers()


        def acquireDescription( thisData ) :
            nonlocal register
            register.__data[ 'description' ] = rmp.Parameter.from_yamlData( thisData, 'description',
                                                                            optional = True )


        def acquireMode( thisData ) :
            nonlocal register
            register.__data[ 'mode' ] = rmrp.ModeParameter.from_yamlData( thisData,
                                                                          optional = True )


        def acquireName( thisData ) :
            nonlocal register
            register.__data[ 'name' ] = rmp.Parameter.from_yamlData( thisData, 'name',
                                                                     optional = False )


        def acquirePublic( thisData ) :
            nonlocal register
            register.__data[ 'public' ] = rmrp.PublicParameter.from_yamlData( thisData,
                                                                              optional = True )


        def acquireSummary( thisData ) :
            nonlocal register
            register.__data[ 'summary' ] = rmp.Parameter.from_yamlData( thisData, 'summary',
                                                                        optional = True )


        register = cls( memorySpace, setCollection,
                        parent = parent )
        setCollection.registerSet.add( register )

        if (not optional) and (cls.__yamlName not in yamlData.keys()) :
            raise ConfigurationError( 'Register is not defined in yaml data' )
        elif cls.__yamlName in yamlData.keys() :
            acquireConstraints( yamlData[ cls.__yamlName ] )
            acquireDescription( yamlData[ cls.__yamlName ] )
            acquireMode( yamlData[ cls.__yamlName ] )
            acquireName( yamlData[ cls.__yamlName ] )
            acquirePublic( yamlData[ cls.__yamlName ] )
            acquireSummary( yamlData[ cls.__yamlName ] )

            # Field acquisition must be done after the basic register data is acquired.
            acquireFields( yamlData[ cls.__yamlName ] )

            # BitMap acquisition must come after the other parameters because it uses those parameters as part of the set up.
            acquireBitMap( yamlData[ cls.__yamlName ] )

        return register


    def to_yamlData( self ) :
        yamlData = { self.__yamlName : { } }

        parameters = list()
        parameters.append( rye.parameter( '_address', self.address ) )
        parameters.append( rye.parameter( '_sizeMemoryUnits', self.sizeMemoryUnits ) )

        for parameterData in self.__data.values() :
            parameterYamlData = parameterData.to_yamlData()
            parameters.append( parameterYamlData )

        parameters.append( self.__bitMap.to_yamlData() )

        for thisParameter in parameters :
            yamlData[ self.__yamlName ].update( thisParameter )

        return yamlData
