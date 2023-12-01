#!/usr/bin/env bash

#
# @author Ari Setiawan
# @create 15.10-2023 23:39
# @github https://github.com/hxAri/Yutiriti
#
# Yūtiriti Copyright (c) 2023 - Ari Setiawan <hxari@proton.me>
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


from typing import final, TypeVar

from yutiriti.error import ReportError
from yutiriti.readonly import Readonly
from yutiriti.json import JSON
from yutiriti.common import typeof


Key = TypeVar( "Key" )
Value = TypeVar( "Value" )
Object = TypeVar( "Object" )
ObjectBuilder = TypeVar( "ObjectBuilder" )

#[yutiriti.object.Object]
class Object:

    """
    A python Object utility to transform any dictionary structure into Object
    """
    
    #[Object( Dict|Object data )]: None
    def __init__( self, data:dict|Object|None=None ) -> None:

        """
        Construct method of class Object.

        :params Dict<Key, Value>|Object data
        :params Any parent

        :return None
        """

        self.__dict__['__index__'] = 0
        self.__dict__['__data__'] = {}
        self.__set__( data if isinstance( data, dict ) else {} )

    #[Object.__builder__( Object parent, Dict<Key, Value>|Object data )]: ObjectBuilder
    @final
    @staticmethod
    def __builder__( parent:Object, data:dict|Object ) -> ObjectBuilder:

        """
        Object builder for child, 

        :params Object parent
        :params Dict<Key, Value> data

        :return Object
        """

        #[Object.__builder__$.ObjectBuilder]
        class ObjectBuilder( parent ):

            """
            Children Object builder for avoid unhandled argument 
            when create new object for children value
            """

            #[ObjectBuilder( Dict<Key, Value>|Object data )]: None
            def __init__( self, data:dict|Object ) -> None:
                Object.__init__( self, data )
            
        return ObjectBuilder( data )
    
    #[Object.__contains__( Key name )]: Bool
    @final
    def __contains__( self, name:Key ) -> bool: return name in self.__data__

    #[Object.__delattr__( Key key )]: None
    @final
    def __delattr__( self, key:Key ) -> None:
        if key in self.__dict__:
            if key not in [ "__data__", "__index__", "__parent__" ]:
                del self.__dict__[key]
        elif key in self.__dict__['__data__']:
            del self.__dict__['__data__'][key]
    
    #[Object.__delitem__( Key index )]: None
    @final
    def __delitem__( self, index:Key ) -> None:
        if index in self.__dict__['__data__']:
            del self.__dict__['__data__'][index]
        elif index in self.__dict__:
            if index not in [ "__data__", "__index__", "__parent__" ]:
                del self.__dict__[index]
    
    #[Object.__getattr__( Key name )]: Any
    @final
    def __getattr__( self, name:Key ) -> any:
        if name in self.__dict__:
            return self.__dict__[name]
        if name in self.__dict__['__data__']:
            return self.__dict__['__data__'][name]
        raise AttributeError( "\"{}\" object has no attribute \"{}\"".format( typeof( self ), name ) )
    
    #[Object.__getitem__( Key key )]: Any
    @final
    def __getitem__( self, key:Key ) -> any:
        if key in self.__dict__['__data__']:
            return self.__dict__['__data__'][key]
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError( "\"{}\" object has no item \"{}\"".format( typeof( self ), key ) )

    #[Object.__index__]: Int
    @final
    @property
    def __index__( self ) -> int: return self.__dict__['__index__']
    
    #[Object.__iter__()]: Object
    @final
    def __iter__( self ) -> Object: return self

    #[Object.__json__( Any *args, Any **kwargs  )]: Str
    @final
    def __json__( self, *args:any, **kwargs:any ) -> str:

        #[Object.__json__$.iterator( Dict<key, Value>|List<Value> data )]: Dict
        def iterator( data:dict|list ) -> dict:
            match type( data ):
                case "dict":
                    for key in data:
                        match type( data[key] ).__name__:
                            case "dict" | "list":
                                data[key] = self.__json__( data[key] )
                            case _:
                                if not JSON.isSerializable( data[key] ):
                                    data[key] = self.__str( data[key] )
                case "list":
                    for idx, value in enumerate( data ):
                        if isinstance( value, ( dict, list ) ):
                            data[idx] = self.__json__( value )
                        else:
                            if not JSON.isSerializable( value ):
                                data[idx] = self.__str( value )
            return data
        
        return JSON.encode( iterator( self.__props__() ), *args, **kwargs )
    
    #[Object.__len__()]: Int
    @final
    def __len__( self ) -> int: return len( self.__dict__['__data__'] )

    #[Object.__keys__()]: List<Key>
    @final
    def __keys__( self ) -> list[Key]: return list( self.__dict__['__data__'].keys() )
    
    #[Object.__next__()]: Any
    @final
    def __next__( self ) -> any:
        
        # Get current index iteration.
        index = self.__index__
        
        keys = self.__keys__()
        length = len( keys )

        try:
            if index < length:
                self.__index__ += 1
                return self[keys[index]]
        except IndexError:
            pass
        raise StopIteration
    
    #[Object.__props__()]: Dict<Key, Value>
    @final
    def __props__( self ) -> dict:

        """
        Return Dictionary of Object

        :return Dict<Key, Value>
        """

        data = {}
        copy = self.__dict__['__data__']
        for key in copy.keys():
            if isinstance( copy[key], Object ):
                data[key] = copy[key].__props__()
            elif isinstance( copy[key], list ):
                data[key] = []
                for item in copy[key]:
                    if isinstance( item, Object ):
                        data[key].append( item.__props__() )
                    else:
                        data[key].append( item )
            else:
                data[key] = copy[key]
        return data
    
    #[Object.__repr__()]: Str
    @final
    def __repr__( self ) -> str:

        """
        Return representation of Object.

        :return Str
        """

        #[Object.__repr__$.represent( Dict<Key, Value>|List<Value>|Object data, Int indent )]: Str
        def represent( data:dict|list|Object, indent:int=4 ) -> str:

            #[Object.__repr__$.represent$.normalize( Str string )]: Str
            def normalize( string:str ) -> str:
                return string \
                    .replace( "\"", "\\\"" ) \
                    .replace( "\n", "\\n" ) \
                    .replace( "\t", "\\t" )

            #[Object.__repr__$.represent$.wrapper( Dict<Key, Value>|List<Value>|Object data, Int indent )]: Str
            def wrapper( data:dict|list|Object, indent:int=4 ) -> str:
                values = []
                length = len( data )
                spaces = "\x20" * indent
                if isinstance( data, ( dict, Object ) ):
                    define = "\"{}\""
                    indexs = data.keys()
                else:
                    define = "[{}]"
                    indexs = list( idx for idx in range( length ) )
                for index in indexs:
                    key = define.format( index )
                    value = data[index]
                    if isinstance( value, ( dict, Object ) ):
                        if len( value ) >= 1:
                            values.append( "{}: {}".format( key, represent( value, indent +4 ) ) )
                        else:
                            values.append( "{}: {}(\n{})".format( key, typeof( value ), spaces ) )
                    elif isinstance( value, list ):
                        length = len( value )
                        lspace = indent + 4
                        lspace = "\x20" * lspace
                        if length >= 1:
                            array = []
                            for i in range( length ):
                                if isinstance( value[i], ( dict, list, Object ) ):
                                    array.append( "[{}]: {}".format( i, represent( value[i], indent +8 ) ) )
                                else:
                                    if isinstance( value[i], str ):
                                        value[i] = f"\"{normalize(value[i])}\""
                                    array.append( "[{}]: {}({})".format( i, typeof( value[i] ), value[i] ) )
                            values.append( "{0}: {1}(\n{2}{4}\n{3})".format( key, typeof( value ), lspace, spaces, f",\n{lspace}".join( array ) ) )
                        else:
                            values.append( "{0}: {1}(\n{2})".format( key, typeof( value ), spaces ) )
                    else:
                        if isinstance( value, str ):
                            value = f"\"{normalize(value)}\""
                        values.append( "{}: {}({})".format( key, typeof( value ), value ) )
                return f",\n{spaces}".join( values )
            if len( data ) >= 1:
                return "{}(\n{}{}\n{})".format( typeof( data ), "\x20" * indent, wrapper( data, indent=indent ), "\x20" * ( 0 if indent == 4 else indent -4 ) )
            return "{}(\n{})".format( typeof( data ), "\x20" * ( 0 if indent == 4 else indent -4 ) )
        
        return represent( self, indent=4 )
    
    #[Object.__set__( Dict<Key, Value>|Object data )]: None
    @final
    def __set__( self, data:dict|Object ) -> None:
        
        """
        Object setter.

        :params Dict<Key, Value>|Object data

        :return None
        :raises TypeError
            When trying override value on Readonly Object
        :raises ValueError
            When the value type of parameter is invalid
        """

        if isinstance( data, dict ):
            excepts = []
            if isinstance( self, Readonly ):
                excepts = []
                if "__except__" in self.__dict__:
                    if isinstance( self.__dict__['__except__'], list ):
                        excepts = self.__dict__['__except__']
            else:
                for keyword in data.keys():
                    if keyword not in excepts:
                        excepts.append( keyword )
            if "__data__" in excepts:
                del excepts[excepts.index( "__data__" )]
            if "__parent__" in excepts:
                del excepts[excepts.index( "__parent__" )]
            if "__index__" not in excepts:
                excepts.append( "__index__" )
            for key in data.keys():
                value = data[key]
                if isinstance( value, dict ):
                    define = typeof( self )
                    if define != "Object" and define != "ObjectBuilder":
                        value = Object.__builder__( type( self ), value )
                    else:
                        value = Object( value )
                elif isinstance( value, list ):
                    for i in range( len( value ) ):
                        if isinstance( value[i], dict ):
                            value[i] = Object( value[i] )
                if key in self.__dict__:
                    if key == "__except__":
                        if isinstance( value, list ):
                            for val in value:
                                if not isinstance( val, str ):
                                    if key in self.__dict__:
                                        raise TypeError( f"Cannot override attribute \"{key}\", cannot override attribute that has been set in a class that extends the Readonly class" )
                                    self.__dict__['__except__'] = excepts
                                    break
                                else:
                                    self.__dict__['__except__'].append( val )
                            excepts = self.__dict__['__except__']
                            continue
                    if key not in excepts:
                        raise TypeError( f"Cannot override attribute \"{key}\", cannot override attribute that has been set in a class that extends the Readonly class" )
                    self.__dict__[key] = data[key]
                elif key in self.__dict__['__data__']:
                    if key not in excepts:
                        raise TypeError( f"Cannot override item \"{key}\", cannot override item that has been set in a class that extends the Readonly class" )
                    if isinstance( self.__dict__['__data__'][key], Object ) and isinstance( value, ( dict, Object ) ):
                        name = typeof( self.__dict__['__data__'][key] )
                        diff = typeof( value )
                        if name not in [ "Object", "ObjectBuilder", diff ]:
                            self.__dict__['__data__'][key] = value
                        else:
                            self.__dict__['__data__'][key].__set__( value )
                    elif isinstance( self.__dict__['__data__'][key], list ) and isinstance( value, list ):
                        for item in value:
                            if item not in self.__dict__['__data__'][key]:
                                self.__dict__['__data__'][key].append( item )
                    else:
                        self.__dict__['__data__'][key] = value
                else:
                    self.__dict__['__data__'][key] = value
        elif isinstance( data, list ):
            raise ReportError( "Functionality for set multiple value on class {} is deprecated".format( typeof( self ) ) )
        elif isinstance( data, Object ):
            for key in data.__keys__():
                self.__set__({
                    key: data[key]
                })
            ...
        else:
            raise ValueError( "Invalid \"data\" parameter, value must be type Dict|List|Object, {} passed".format( typeof( data ) ) )
    
    #[Object.__setattr__( Key name, Value value )]: None
    @final
    def __setattr__( self, name:Key, value:Value ) -> None:
        self.__set__({
            name: value
        })

    #[Object.__setitem__( Str key, Any value )]: None
    @final
    def __setitem__( self, key:Key, value:Value ) -> None:
        self.__set__({ key: value })
    
    #[Object.__str__()]: Str
    @final
    def __str__( self ) -> str: return self.__json__()

    #[Object.copy()]: Object
    def copy( self ) -> Object: return self.__builder__( type( self ), self.__props__() )

    #[Object.delt( Key index )]: None
    def delt( self, index:Key ) -> None: self.__delitem__( index )
    
    #[Object.dump()]: Str
    @final
    def dump( self ) -> str: return self.__repr__()

    #[Object.empty()]: Bool
    @final
    def empty( self ) -> bool: return self.__len__() == 0

    #[Object.get( Key key )]: Any
    @final
    def get( self, key:Key ) -> any: return self.__getitem__( key )
    
    #[Object.isset( Key key )]: Bool
    @final
    def has( self, key:Key ) -> bool: return self.__contains__( key )
    
    #[Object.idxs()]: List<Int>
    @final
    def idxs( self ) -> list[int]: return [ idx for idx in range( len( self ) ) ]
    
    #[Object.json( Any *args, Any **kwargs )]: Str
    @final
    def json( self, *args:any, **kwargs:any ) -> str: return self.__json__( *args, **kwargs )
    
    #[Object.keys()]: List<Key>
    def keys( self ) -> list[Key]: return self.__keys__()
    
    #[Object.len()]: Int
    @final
    def len( self ) -> int: return self.__len__()

    #[Object.length()]: Int
    @final
    @property
    def length( self ) -> int: return self.__len__()

    #[Object.props()]: Dict<key, Value>
    def props( self ) -> dict: return self.__props__()

    #[Object.set( Dict<Key, Value>|Object data )]: None
    @final
    def set( self, data:dict|Object ) -> None: self.__set__( data )
