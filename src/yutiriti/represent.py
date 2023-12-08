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


from typing import final

from yutiriti import object as module
from yutiriti.common import typeof

#[yutiriti.represent.Represent]
@final
class Represent:
    
    #[Represent.normalize( Str string )]: Str
    @staticmethod
    def normalize( string:str ) -> str:
        return string \
            .replace( "\"", "\\\"" ) \
            .replace( "\n", "\\n" ) \
            .replace( "\t", "\\t" )
        
    #[Represent.wrapper( Dict<Key, Value>|List<Value>|Object data, Int indent )]: Str
    @staticmethod
    def wrapper( data:dict|list|object, indent:int=4 ) -> str:
        values = []
        length = len( data )
        spaces = "\x20" * indent
        if isinstance( data, ( dict, module.Object ) ):
            define = "\"{}\""
            indexs = data.keys()
        else:
            define = "[{}]"
            indexs = list( idx for idx in range( length ) )
        for index in indexs:
            key = define.format( index )
            value = data[index]
            if isinstance( value, ( dict, module.Object ) ):
                if len( value ) >= 1:
                    values.append( "{}: {}".format( key, Represent.convert( value, indent +4 ) ) )
                else:
                    values.append( "{}: {}(\n{})".format( key, typeof( value ), spaces ) )
            elif isinstance( value, list ):
                length = len( value )
                lspace = indent + 4
                lspace = "\x20" * lspace
                if length >= 1:
                    array = []
                    for i in range( length ):
                        if isinstance( value[i], ( dict, list, module.Object ) ):
                            array.append( "[{}]: {}".format( i, Represent.convert( value[i], indent +8 ) ) )
                        else:
                            if isinstance( value[i], str ):
                                value[i] = f"\"{Represent.normalize(value[i])}\""
                            array.append( "[{}]: {}({})".format( i, typeof( value[i] ), value[i] ) )
                    values.append( "{0}: {1}(\n{2}{4}\n{3})".format( key, typeof( value ), lspace, spaces, f",\n{lspace}".join( array ) ) )
                else:
                    values.append( "{0}: {1}(\n{2})".format( key, typeof( value ), spaces ) )
            else:
                if isinstance( value, str ):
                    value = f"\"{Represent.normalize(value)}\""
                values.append( "{}: {}({})".format( key, typeof( value ), value ) )
        return f",\n{spaces}".join( values )
    
    #[Represent.convert( Dict<Key, Value>|List<Value>|object data, Int indent )]: Str
    @staticmethod
    def convert( data:dict|list|object, indent:int=4 ) -> str:
        
        """
        """
        
        if len( data ) >= 1:
            return "{}(\n{}{}\n{})".format( typeof( data ), "\x20" * indent, Represent.wrapper( data, indent=indent ), "\x20" * ( 0 if indent == 4 else indent -4 ) )
        return "{}(\n{})".format( typeof( data ), "\x20" * ( 0 if indent == 4 else indent -4 ) )
    