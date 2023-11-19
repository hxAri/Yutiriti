#!/usr/bin/env python

#
# @author Ari Setiawan
# @create 15.10-2023 23:39
# @github https://github.com/hxAri/Yutiriti
#
# Yūtiriti Copyright (c) 2022 - Ari Setiawan <hxari@proton.me>
# Yūtiriti Licence under GNU General Public Licence v3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#


from re import match
from typing import final

from yutiriti.common import droper, typeof
from yutiriti.object import Object
from yutiriti.readonly import Readonly


#[yutiriti.typing.typing.Typing]
class Typing( Object ):

    """
    The Typing class works in almost the same way as the
    Object class from Yutiriti, but Typing will only pass
    items returned by the __items__ method to its parent
    class, namely Object from Yutiriti, the aim is to avoid
    errors when checking response data and so on because
    Yutiriti treats dictionaries.
    
    And also lists as objects, and for example it can be very
    confusing when it comes to managing response data as
    Instagram usually provides quite large responses to process and,
    when the JSON response is passed to a class that extends the
    Typing class it will only take time and also set the value
    returned by previous __items__ method, but we can also set
    incompatible items from outside the class or from inside except
    the instance, and this is not always intended for things like
    those previously mentioned.

    Apart from that, Typing also normalizes strings to int values
    if the value only contains numbers.
    """

    #[Typing( Dict|List|Object data, Object parent )]: None
    @final
    def __init__( self, data:dict|Object, parent:object=None ) -> None:
        if not isinstance( data, ( dict, Object ) ):
            raise TypeError( "Invalid \"data\" parameter, value must be type Dict|Object, {} passed".format( typeof( data ) ) )
        parent = super()
        parent.__init__(
            self.__resolver__(
                self.__mapper__( 
                    self.__mapping__, 
                    droper( 
                        items=data, 
                        search=self.__items__, 
                        nested=self.__nested__ 
                    ) 
                )
            )
        )
    
    #[Typing.__items__]: Dict<Str, Str>|List<Str>
    @property
    def __items__( self ) -> dict[str:str]|list[str]:
        raise NotImplementedError( "Property {} is not initialize or implemented".format( self.__allows__ ) )
    
    #[Typing.__mapper__( Dict|Object properties, Any values )]: Any
    @final
    def __mapper__( self, properties:dict|Object, values:any ) -> any:
        if not isinstance( values, ( dict, list, Object ) ): return values 
        for key in list( properties.keys() ):
            if key in values:
                if isinstance( properties[key], type ):
                    if isinstance( values[key], properties[key] ):
                        continue
                    elif isinstance( values[key], ( dict, Object ) ):
                        values[key] = properties[key]( values[key] )
                    elif isinstance( values[key], list ):
                        for i in range( len( values[key] ) ):
                            if isinstance( values[key][i], properties[key] ):
                                continue
                            values[key][i] = properties[key]( values[key][i] )
                        ...
                    ...
                elif isinstance( properties[key], ( dict, Object ) ):
                    if isinstance( properties[key], type ):
                        if isinstance( values[key], properties[key] ):
                            continue
                    if isinstance( values[key], ( dict, Object ) ):
                        values[key] = self.__mapper__( properties[key], values[key] )
                    elif isinstance( values[key], list ):
                        for i in range( len( values[key] ) ):
                            if isinstance( values[key][i], properties[key] ):
                                continue
                            if isinstance( values[key][i], ( dict, Object ) ):
                                values[key][i] = self.__mapper__( properties[key], values[key][i] )
                        ...
            ...
        return values
    
    #[Typing.__mapping__]: Dict|Object
    @property
    def __mapping__( self ) -> dict|Object: return {}
    
    #[Typing.__nested__]: Bool
    @property
    def __nested__( self ) -> bool: return True

    #[Typing.__resolver__( Any value )]: Any
    @final
    def __resolver__( self, value:any ) -> any:
        if isinstance( value, Readonly ):
            return value
        if isinstance( value, ( dict, list, Object ) ):
            if isinstance( value, dict ):
                indexs = list( value.keys() )
            elif isinstance( value, Object ):
                indexs = value.keys()
            else:
                indexs = [ idx for idx in range( len( value ) ) ]
            for i in range( len( indexs ) ):
                index = indexs[i]
                value[index] = self.__resolver__( value[index] )
        elif isinstance( value, str ):
            if match( r"^\d+$", value ):
                value = int( value )
        return value
