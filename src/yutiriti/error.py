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


#[yutiriti.error.Throwable]
class Throwable( Exception ):
    
    #[Throwable( String message, Int code, Context throw, BaseException prev, List group, Function|Method callback, **data )]: None
    def __init__( self, message, code=0, throw=None, prev=None, group=[], callback=None, **data ) -> None:
        
        # Exception message.
        self.message = message
        
        # Exception code.
        self.code = code
        
        # Exception thrown.
        self.throw = throw
        
        # Exception previous.
        self.prev = prev
        
        # Sxception groups.
        self.group = group
        
        # Exception callback.
        self.callback = callback
        
        # Exception data passed.
        self.data = data
        
        # Call parent constructor.
        super().__init__( message, code )
    

#[yutiriti.error.Alert]
class Alert( Throwable, Warning ): ...

#[yutiriti.erorr.Error]
class Error( Throwable, RuntimeError ): ...

#[yutiriti.error.AuthError]
class AuthError( Error ): ...

#[yutiriti.error.RequestError]
class RequestError( Error ): ...

#[yutiriti.error.RequestAuthError]
class RequestAuthError( AuthError ): ...

#[yutiriti.error.RequestDownloadError]
class RequestDownloadError( RequestError ): ...

#[yutiriti.error.ReportError]
class ReportError( Error ): ...
