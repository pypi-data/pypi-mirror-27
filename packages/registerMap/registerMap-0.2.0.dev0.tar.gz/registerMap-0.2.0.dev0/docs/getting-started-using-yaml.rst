Getting started using a YAML file
---------------------------------

Using a text editor you can define the YAML structure of your register map relatively easily. It gets a little easier
if you use an editor that understands YAML, such as `Notepad++ <https://notepad-plus-plus.org/>`_ or an IDE such as
`PyCharm <https://www.jetbrains.com/pycharm/>`_.

The example below shows a register map skeleton that defines some properties of the memory space, along with a summary
and description of the register map. The modules section is left blank for now.

In any register map you must have at least one module.

.. code-block:: yaml

   registerMap: {
     # A memorySpace is not optional
     memorySpace: {
       # but all the parameters are optional.
       # Default: 0x0
       baseAddress: 0x1000
       # Default: None
       pageSize: None
       # Default: 32
       addressBits: 48
       # Default: 8
       memoryUnitBits: 16
     }
     summary: 'A short summary of the register map'
     description: 'A longer description of the register map'
     modules: [
     ]
   }

When you are done and have saved your YAML data to a file, your YAML register map can be loaded into Python.

.. code-block:: python

   import registerMap
   myMap = registerMap.load( 'registermap.yml' )

Let's test that the register map properties are loaded as expected.

.. code-block:: python

   assert myMap.memory.addressBits == 48
   assert myMap.memory.memoryUnitBits == 16
   assert myMap.memory.baseAddress == 0x1000
