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


from json import (
    dumps,
    JSONDecodeError as JSONError, 
    loads, 
)

from yutiriti.common import typedef


#[yutiriti.json.JSON]
class JSON:
    
    #[Json.decode( Str string, Any *args, Any **kwargs )]
    @staticmethod
    def decode( string, *args, **kwargs ):
        return( loads( string, *args, **kwargs ) )
        
    #[Json.encode( Any values, Any *args, Any **kwargs )]
    @staticmethod
    def encode( values, *args, **kwargs ):
        if typedef( values, "Object" ):
            return values.json()
        kwargs['indent'] = kwargs.pop( "indent", 4 )
        return( dumps( values, *args, **kwargs ) )
        
    #[Json.isSerializable( Any values )]
    @staticmethod
    def isSerializable( values ):
        
        """
        Return if value is serializable.
        
        :params Any values
        
        :return Bool
        """
        
        try:
            JSON.encode( values )
        except OverflowError:
            return( False )
        except TypeError:
            return( False )
        return( True )
    
