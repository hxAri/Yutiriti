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


from datetime import datetime
from json import dumps, JSONDecodeError as JSONError, loads
from typing import final

import yutiriti


#[yutiriti.json.JSON]
class JSON:

    """
    Json utility
    """
    
    #[Json.decode( Str string, Any *args, Any **kwargs )]: Dict|List
    @staticmethod
    def decode( string, *args, **kwargs ) -> dict|list:
        return loads( string, *args, **kwargs )
        
    #[Json.encode( Any values, Any *args, Any **kwargs )]: Str
    @staticmethod
    def encode( values, *args, **kwargs ) -> str:
        kwargs['indent'] = kwargs.pop( "indent", 4 )
        return dumps( JSON.serializer( values ), *args, **kwargs )
        
    #[Json.isSerializable( Any values )]: Bool
    @staticmethod
    def isSerializable( values ) -> bool:
        
        """
        Return if value is serializable.
        
        :params Any values
        
        :return Bool
        """
        
        try:
            JSON.encode( values )
        except OverflowError:
            return False
        except TypeError:
            return False
        return True
    
    @final
    @staticmethod
    def serializer( values ) -> dict|list:
        if isinstance( values, ( dict, yutiriti.object.Object ) ):
            if isinstance( values, yutiriti.object.Object ):
                values = values.props()
            for key in values.keys():
                values[key] = JSON.serializer( values[key] )
        elif isinstance( values, list ):
            for index, value in enumerate( values ):
                values[index] = JSON.serializer( value )
        elif isinstance( values, datetime ):
            values = values.strftime( "%d-%m-%YT%H:%M:%S" )
        return values
    
