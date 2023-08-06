Canonical names
===============

Each element in the register map has a "canonical name" reflecting the hierarchy of the element. Global elements have
no hiearchy and their canonical name is exactly the same as the element name.

.. code-block:: python

   myMap = RegisterMap()
   myModule = myMap.addModule( 'myModule' )

   assert myModule.canonicalId == 'myModule'

   myRegister = myModule.addRegister( 'myRegister' )

   assert myRegister.canonicalId == 'myModule.myRegister'

   myLocalField = myRegister.addField( 'myField', [0,4] )

   assert myField.canonicalId == 'myModule.myRegister.myField'

   myGlobalField = myRegister.addField( 'myGlobalField', [6, 9] )

   assert myGlobalField.canonicalId == 'myGlobalField'

Canonical names are unique within the register map so they can be used to index elements.

.. code-block:: python

   assert myMap[ 'element' ][ 'myModule.myRegister' ] == myRegister

   assert myMap[ 'element' ][ 'myGlobalField' ] == myGlobalField

Note that modules and global fields are all at the top of the hierarchy. The names are searched in order of fields
first, then modules, so care must be taken when selecting global names.

.. code-block:: python

   newModule = myMap.addModule( 'myGlobalName' )

   newGlobalField = myRegister.addField( 'myGlobalName', [0, 5], isGlobal = True )

   assert myMap[ 'element' ][ 'myGlobalName' ] == newGlobalField
   assert myMap[ 'element' ][ 'myGlobalName' ] != newModule
