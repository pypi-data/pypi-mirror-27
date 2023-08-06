Getting started using Python
----------------------------

You can start creating your register map directly in Python. You just need to import the ``registerMap`` library
and declare a ``RegisterMap`` instance. At this point you will have the default settings for the memory space and no
modules defined.

.. code-block:: python

   import registerMap
   myMap = registerMap.RegisterMap()

   assert myMap.memory.addressBits == 32
   assert myMap.memory.memoryUnitBits == 8
   assert myMap.memory.baseAddress == 0x0
   assert len( myMap[ 'modules' ] ) == 0

Now that the register map is defined, it can be saved.

.. code-block:: python

   myMap.save( myMap, 'mymap.yml' )

Creating a module
~~~~~~~~~~~~~~~~~

.. code-block:: python

   myMap.addModule()


Creating a register
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   myRegister = myMap[ 'mymodule' ].addRegister( 'myregister' )

A register may contain references to local or global fields. See below for details on local or global fields.

Creating a local field
~~~~~~~~~~~~~~~~~~~~~~

Local fields have no limitation on the name, but can only be used by a single register.

The following expression creates a field that is local to the parent register and explicitly maps bits from the register
to bits from the field. If the field 'my-local-field' does not exist, it is automatically created; in this case, since
the field bit range is (4, 6) a field of 7 bits is created.

.. code-block:: python

   myField = myRegister.addField( 'my-local-field', [2, 4], (4, 6) )

The above expresssion explicitly maps the bits from register to field. It is also possible to only specify the register
bits. It is not possible to use a default mapping with an existing field and an exception will be raised.

.. code-block:: python

   myField = myRegister.addField( 'my-local-field', [2, 4] )

The default above is implicitly the same as this operation.

.. code-block:: python

   myField = myRegister.addField( 'my-local-field', [2, 4], (0, 2) )

Creating a global field
~~~~~~~~~~~~~~~~~~~~~~~

Global fields can be shared by multiple registers and the name must be globally unique within the register map. There can
be no module, register or field with the same name as the global field.

For a global field, when adding a field to the register use the optional argument ``isGlobal = True``. If the field does
not exist then it will be created. If the field already exists, then the specified field bit interval will be tested for
interference with other intervals and an exception raised as necessary.

.. code-block:: python

   myField = myRegister.addField( 'my-global-field, [3,6], (3,6), isGlobal = True )
