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


from typing import final, TypeVar

from yutiriti.error import ReportError
from yutiriti.readonly import Readonly
from yutiriti.json import JSON
from yutiriti.common import typeof

Object = TypeVar( "Object" )
ObjectBuilder = TypeVar( "ObjectBuilder" )


#[yutiriti.object.Object]
class Object:
    
    #[Object( Dict|Object data, Any parent )]: None
    def __init__( self, data:dict|Object={}, parent:any=None ) -> None:

        """
        Construct method of class Object.

        :params Dict|List|Object data
        :params Any parent

        :return None
        """

        self.__dict__['__parent__'] = parent
        self.__dict__['__index__'] = 0
        self.__dict__['__data__'] = {}
        self.set( data )
    
    #[Object.__builder__( Object parent, Dict|Object data )]: ObjectBuilder
    @final
    @staticmethod
    def __builder__( parent:object, data:dict|Object ) -> ObjectBuilder:

        """
        Object builder for child

        :params Object parent
        :params Dict<Str, Str> data

        :return Object
        """

        class ObjectBuilder( parent ):
            def __init__( self, data:dict ) -> None:
                Object.__init__( self, data )
        return ObjectBuilder( data )

    #[Object.__contains__( Str name )]: Bool
    @final
    def __contains__( self, name ) -> bool: return f"{name}" in self.__data__

    #[Object.__delattr__( Int|Str key )]: None
    @final
    def __delattr__( self, key:int|str ) -> None:
        key = str( key )
        if key in self.__dict__:
            if key != "__data__" and \
                key != "__index__" and \
                key != "__parent__":
                del self.__dict__[key]
        elif key in self.__dict__['__data__']:
            del self.__dict__['__data__'][key]
    
    #[Object.__delitem__( Int|Str index )]: None
    @final
    def __delitem__( self, index:int|str ) -> None:
        index = str( index )
        if index in self.__dict__['__data__']:
            del self.__dict__['__data__'][index]
        elif index in self.__dict__:
            if index != "__data__" and \
                index != "__index__" and \
                index != "__parent__":
                del self.__dict__[index]
    
    #[Object.__getattr__( self, name )]: Any
    @final
    def __getattr__( self, name ):
        name = str( name )
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self.__dict__['__data__']:
            return self.__dict__['__data__'][name]
        raise AttributeError( "\"{}\" object has no attribute \"{}\"".format( typeof( self ), name ) )
    
    #[Object.__getitem__( Str key )]: Any
    @final
    def __getitem__( self, key ) -> any:
        if key in self.__dict__['__data__']:
            return self.__dict__['__data__'][key]
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError( "\"{}\" object has no item \"{}\"".format( typeof( self ), key ) )
    
    #[Object.__iter__()]: Object
    @final
    def __iter__( self ) -> Object: return self
    
    #[Object.__json__( Dict|List data )]: Dict
    @final
    def __json__( self, data:dict|list=None ) -> dict:
        if data == None:
            data = self.dict()
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
                for idx in range( len( data ) ):
                    if isinstance( data[idx], ( dict, list ) ):
                        data[idx] = self.__json__( data[idx] )
                    else:
                        if not JSON.isSerializable( data[idx] ):
                            data[idx] = self.__str( data[idx] )
        return data
    
    #[Object.__len__()]: Int
    @final
    def __len__( self ) -> int: return len( self.__dict__['__data__'] )
    
    #[Object.__next__()]: Any
    @final
    def __next__( self ) -> any:
        
        # Get current index iteration.
        index = self.__index__
        
        # Get object length.
        length = len( self )
        try:
            if index < length:
                self.__index__ += 1
                return self[self.keys( index )]
        except IndexError:
            pass
        raise StopIteration
    
    #[Object.__ref__()]: None
    @final
    def __ref__( self ) -> None:
        if "__parent__" in self.__dict__ and self.__dict__['__parent__'] is not None:
            for key in self.keys():
                self.__dict__['__parent__'].__dict__[key] = self.__dict__['__data__'][key]
        
    #[Object.__repr__()]: Str
    @final
    def __repr__( self ) -> str:

        """
        Return representation of Object.

        :return Str
        """

        def represent( data:dict|list|Object, indent=4 ) -> str:
            def normalize( string:str ) -> str: return string.replace( "\"", "\\\"" )
            def wrapper( data:dict|list|Object, indent=4 ) -> str:
                values = []
                length = len( data )
                spaces = "\x20" * indent
                if isinstance( data, ( dict, Object ) ):
                    define = "\"{}\""
                    indexs = data.keys()
                else:
                    define = "[{}]"
                    indexs = [ idx for idx in range( length ) ]
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
            else:
                return "{}(\n{})".format( typeof( data ), "\x20" * ( 0 if indent == 4 else indent -4 ) )
        return represent( self, indent=4 )
    
    #[Object.__setattr__( Str name, Any value )]: None
    @final
    def __setattr__( self, name, value ) -> None: self.set({ str( name ): value })

    #[Object.__setitem__( Str key, Any value )]: None
    @final
    def __setitem__( self, key, value ) -> None: self.set({ str( key ): value })

    #[Object.__str__()]: Str
    @final
    def __str__( self ) -> str: return self.json()
    
    #[Object.copy()]: Object
    @final
    def copy( self ) -> Object: return self.__builder__( type( self ), self.dict() )

    #[Object.delt( Int|Str index )]: None
    @final
    def delt( self, index:int|str ) -> None: self.__delitem__( index )
    
    #[Object.dict()]: Dict[str:any]
    @final
    def dict( self ) -> dict[str:any]:

        """
        Return Dictionary of Object

        :return Dict
        """

        data = {}
        copy = self.__dict__['__data__']
        for key in copy.keys():
            if isinstance( copy[key], Object ):
                data[key] = copy[key].dict()
            elif isinstance( copy[key], list ):
                data[key] = []
                for item in copy[key]:
                    if isinstance( item, Object ):
                        data[key].append( item.dict() )
                    else:
                        data[key].append( item )
            else:
                data[key] = copy[key]
        return data
    
    #[Object.dump()]: Str
    @final
    def dump( self ) -> str: return self.__repr__()

    #[Object.empty()]: Bool
    @final
    def empty( self ) -> bool: return self.__len__() == 0
    
    #[Object.json( Any *args, Any **kwargs )]: Str
    @final
    def json( self, *args, **kwargs ) -> str: return JSON.encode( self.__json__( self.dict() ), *args, **kwargs )
    
    #[Object.isset( Str key )]: Bool
    @final
    def isset( self, key ) -> bool: return self.__contains__( key )
    
    #[Object.idxs()]: List<Int>
    @final
    def idxs( self ) -> list[int]: return [ idx for idx in range( len( self ) ) ]
    
    #[Object.keys()]: List<Str>
    @final
    def keys( self, index=None ) -> list[str]: return self.keys()[index] if isinstance( index, int ) else list( self.__dict__['__data__'].keys() )
    
    #[Object.get()]: Any
    @final
    def get( self, key ) -> any: return self.__getitem__( key )
    
    #[Object.len()]: Int
    @final
    def len( self ) -> int: return self.__len__()

    #[Object.length()]: Int
    @final
    @property
    def length( self ) -> int: return self.__len__()
    
    #[Object.__set( Dict|List|Object data )]: None
    @final
    def set( self, data ) -> None:

        """
        Object setter.

        :params Dict|List|Object data

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
                key = str( key )
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
                        if name != "Object" and name != "ObjectBuilder" or \
                            diff != "Object" and diff != "ObjectBuilder" or \
                            name != diff:
                            self.__dict__['__data__'][key] = value
                        else:
                            self.__dict__['__data__'][key].set( value )
                    elif isinstance( self.__dict__['__data__'][key], list ) and isinstance( value, list ):
                        for i in range( len( value ) ):
                            if value[i] not in self.__dict__['__data__'][key]:
                                self.__dict__['__data__'][key].append( value[i] )
                    else:
                        self.__dict__['__data__'][key] = value
                else:
                    self.__dict__['__data__'][key] = value
        elif isinstance( data, list ):
            raise ReportError( "Functionality for set multiple value on class {} is deprecated".format( typeof( self ) ) )
        elif isinstance( data, Object ):
            for key in data.keys():
                self.set({ key: data[key] })
        else:
            raise ValueError( "Invalid \"data\" parameter, value must be type Dict|List|Object, {} passed".format( typeof( data ) ) )
        self.__ref__()

