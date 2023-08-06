Introduction
============

In this framework a register map is an ordered list of modules. A module is an ordered list of registers and a register
is made up of fields.

A memory space defines the fundamental properties of the register map such as the number of bits in addresses, the base
address of the register map and the number of bits in memory units. This is also where memory paging can be defined.

The order of the modules defines how module addresses are generated. So the first module in the list would probably get
assigned the base address of the register map memory space and the next module might get the next available address.
The words 'probably' and 'might' are used here because there are other factors such as the total span of the module,
page registers and constraints applied to modules and registers that can change what addresses are available for
assignment. More on that later.

A module is a way of grouping registers together. When there is more than one module, the groups will probably have
some functional association of the registers, for example, a set of registers associated with a particular output, or a
set of read only registers for reporting status.

A register is made up of fields. The order of fields is not defined because the register bits to which each field
is assigned must be explicitly defined. A register, or perhaps more accurately, the total span of its fields may
also span multiple memory units. This enables support for data that is larger than the bit size of a single memory unit;
eg. If the memory unit size is 8 bits, then it may still be desirable to store a 16, 32 or 64 bit number for the
function of the integrated circuit.

The primary source format of the register map is YAML, so one way to get started is by defining your register map
directly in a YAML text file. The other way is to import the Python library and start working on the register map
dataset directly in a Python terminal or script.
