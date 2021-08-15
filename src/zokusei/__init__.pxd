
from ._general_methods cimport _add_methods, attributes


cdef class Attribute:

   cdef str name
   cdef object default
   cdef object order
