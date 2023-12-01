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


#[yutiriti.common.classmethods( Object obj, Bool wrapper )]: Dict<Str, Callable>
def classmethods( obj:object, wrapper:bool=False ) -> dict[str,callable]:

    """
    Return dictionary method of class.

    :params Object obj
    :params Bool wrapper
        Include wrapper methods e.g __(init|repr)__
    
    :return Dict<Str, Callable>
    """

    methods = {}
    for method in dir( obj ):
        if not wrapper:
            if  method.startswith( "__" ) and \
                method.endswith( "__" ):
                continue
        methods[method] = getattr( obj, method )
    return methods
    

#[yutiriti.common.droper( Dict|List|Object items, List<Dict|List|Object|Dict> search, Bool nested )]: Dict
def droper( items:dict[str, object]|list[object|str], search:list[object|str], nested:bool=False ) -> dict[str, object]:
    
    """
    Drops item based keys given.
    
    :params Dict|List|Object items
    :params List<Dict|List|Object|Str> search
    :params Bool nested

    :return Dict
        Droped items
    
    :raises TypeError
        When the value type if parameter is invalid
    """
    
    if isinstance( search, ( dict, str ) ):
        search:list[dict[str, object]|str] = [search]
    if not isinstance( search, list ):
        raise TypeError( "Invalid keys parameter, value must be type List<Dict|List|Object|Str>, {} passed".format( typeof( search ) ) )
    drops = {}
    for index in search:
        if isinstance( index, dict ) or \
            typedef( index, [ "Collection", "Object" ] ):
            for key in index.keys():
                if key not in items: continue
                droping = droper( items[key], index[key], nested=nested )
                if nested is True:
                    drops[key] = droping
                else:
                    drops = { **drops, **droping }
        elif isinstance( index, list ):
            drops = { **drops, **droper( items[key], index[key], nested=nested ) }
        elif isinstance( index, str ):
            if index in items:
                drops[index] = items[index]
        else:
            raise TypeError( "Invalid keys parameter, value must be type List<Dict|List|Object|Str>, {} passed in items".format( typeof( key ) ) )
    return drops


#[yutiriti.itility.common.typedef( Object instance, Object|Str of, Bool opt )]: Bool
def typedef( instance:object, off:object|str|None=None, opt:bool|None=None ) -> bool:
    
    """
    Returns if instance is instance of instead.
    
    :params Any instance
    :params Any off
    :params Bool opt
        Negative check
    
    :return Bool
    """
    
    if isinstance( opt, bool ):
        return typedef( instance, off ) == opt
    try:
        off:str = off.__name__
    except AttributeError:
        if  not isinstance( off, str ):
            off = type( off ).__name__
    instance = type( instance ).__name__
    if  instance == off:
        return True
    return False
    

#[yutiriti.common.typeof( Object instance )]: Str
def typeof( instance:object ) -> str:
    
    """
    Return object instance name.
    
    :params Any instance
    
    :return Str
        Instance name
    """
    
    return type( instance ).__name__
    
