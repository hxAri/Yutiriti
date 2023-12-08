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


from yutiriti.text import Text


ITP = "\u00b7"
STR_LINE = "\u2502\x20\x20\x20"
MID_LINE = "\u251c\u2500\u2500\x20"
END_LINE = "\u2514\u2500\u2500\x20"
SPC_LINE = "\x20\x20\x20\x20"


#[yutiriti.tree$.builder( Any data, Int indent, Str space, Bool capitalize )]: Str
def builder( data:any, indent:int, space:str, capitalize:bool=False ) -> str:

    """ A tree builder """

    if isinstance( data, ( dict, list, set, tuple ) ):
        return looping( data=data, indent=indent if indent >= 4 else 4, space=space, capitalize=capitalize )
    return f"{space}{END_LINE}{data}\x0a"
    

#[yutiriti.tree$.looping( Dict|List[Any]|Set|Tuple data, Int indent, Str space, Bool capitalize )]: Str
def looping( data:dict|list|set|tuple, indent:int, space:str, capitalize:bool=False ) -> str:

    """ A Tree looping iteration handler """
    
    result = ""
    if isinstance( data, dict ):
        length = len( data )
        if length >= 1:
            keys = list( data.keys() )
            length -= 1
            for index, keyset in enumerate( keys ):
                value = data[keyset]
                if index != length:
                    result += space
                    result += MID_LINE
                    result += normalize( keyset, capitalize=capitalize )
                    result += "\x0a"
                    if isinstance( value, ( dict, list, set, tuple ) ):
                        result += builder( data=value, indent=indent, space=space + STR_LINE, capitalize=capitalize )
                    else:
                        result += space
                        result += STR_LINE
                        result += END_LINE
                        result += str( value )
                        result += "\x0a"
                else:
                    result += space
                    result += END_LINE
                    result += normalize( keyset, capitalize=capitalize )
                    result += "\x0a"
                    if isinstance( value, dict ):
                        result += builder( data=value, indent=indent, space=space + SPC_LINE, capitalize=capitalize )
                    elif isinstance( value, ( list, set, tuple ) ):
                        result += builder( data=value, indent=indent, space=space + SPC_LINE, capitalize=capitalize )
                        # result += looping( data=value, indent=indent, space=space + SPC_LINE )
                    else:
                        result += space
                        result += SPC_LINE
                        result += END_LINE
                        result += str( value )
                        result += "\x0a"
        else:
            result += space
            result += END_LINE
            result += "{}\x0a"
    else:
        length = len( data )
        if length >= 1:
            data = list( data )
            length -= 1
            for index, value in enumerate( data ):
                if index != length:
                    if isinstance( value, dict ):
                        if value:
                            key = list( value.keys() )[0]
                            val = value.pop( key )
                            result += space
                            result += MID_LINE
                            result += normalize( key, capitalize=capitalize )
                            result += "\x0a"
                            if len( value ) >= 1:
                                if isinstance( val, ( dict, list, set, tuple ) ):
                                    result += space
                                    result += STR_LINE
                                    result += MID_LINE
                                    result += "+\x0a"
                                    result += builder( data=val, indent=indent, space=space + STR_LINE + STR_LINE, capitalize=capitalize )
                                else:
                                    result += space
                                    result += STR_LINE
                                    result += MID_LINE
                                    result += str( val )
                                    result += "\x0a"
                                result += builder( data=value, indent=indent, space=space + STR_LINE, capitalize=capitalize )
                            else:
                                if isinstance( val, ( dict, list, set, tuple ) ):
                                    result += space
                                    result += STR_LINE
                                    result += MID_LINE
                                    result += "+\x0a"
                                    result += builder( data=val, indent=indent, space=space + STR_LINE + STR_LINE, capitalize=capitalize )
                                else:
                                    result += space
                                    result += STR_LINE
                                    result += END_LINE
                                    result += str( val )
                                    result += "\n"
                        else:
                            result += space
                            result += MID_LINE
                            result += "{}\x0a"
                    elif isinstance( value, ( list, set, tuple ) ):
                        if value:
                            result += "!=list<list>"
                        else:
                            result += space
                            result += MID_LINE
                            result += "[]\x0a"
                    else:
                        result += space
                        result += MID_LINE
                        result += str( value )
                        result += "\x0a"
                else:
                    if isinstance( value, dict ):
                        if value:
                            key = list( value.keys() )[0]
                            val = value.pop( key )
                            if len( value ) >= 1:
                                result += space
                                result += END_LINE
                                result += normalize( key, capitalize=capitalize )
                                result += "\x0a"
                                if isinstance( val, ( dict, list, set, tuple ) ):
                                    result += space
                                    result += SPC_LINE
                                    result += MID_LINE
                                    result += "+\x0a"
                                    result += builder( data=val, indent=indent, space=space + SPC_LINE + STR_LINE, capitalize=capitalize )
                                else:
                                    result += space
                                    result += SPC_LINE
                                    result += MID_LINE
                                    result += str( val )
                                    result += "\x0a"
                                result += builder( data=value, indent=indent, space=space + ( "\x20" * indent ), capitalize=capitalize )
                            else:
                                result += space
                                result += END_LINE
                                result += normalize( key, capitalize=capitalize )
                                result += "\x0a"
                        else:
                            result += space
                            result += END_LINE
                            result += "{}\x0a"
                    elif isinstance( value, ( list, set, tuple ) ):
                        if value:
                            result += "==list<list>"
                        else:
                            result += space
                            result += END_LINE
                            result += "[]\x0a"
                    else:
                        result += space
                        result += END_LINE
                        result += str( value )
                        result += "\n"
        else:
            result += space
            result += END_LINE
            result += "[]\n"
    return result
    

#[yutiriti.tree.tree$.normalize( Str keyset, Bool capitalize )]: Str
def normalize( keyset:str, capitalize:bool=False ) -> str:

    """ Normalize sey set of value """

    keyset = str( keyset )
    return Text.fromSnakeToTitle( keyset ) if capitalize else keyset


#[yutiriti.tree( Any data, Int indent, Bool capitalize )]: Str
def tree( data:any, indent:int=0, capitalize:bool=False ) -> str:
    
    """
    Convert data into the tree structure.
    
    :params Any data
    :params Int indent
        Indentation prefix
    :params Bool capitalize
        Capitalize dictionary key
    
    :return String
    """
    
    return "\x7b\x7d\x0a\x7b\x7d".format( ITP, builder( data=data, indent=indent, space="\x20" * indent, capitalize=capitalize ) )
    
