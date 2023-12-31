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


from re import split
from sys import stdout
from time import sleep
from typing import final, TypeVar

from yutiriti.common import typeof
from yutiriti.readonly import Readonly
from yutiriti.thread import Thread
from yutiriti.yutiriti import puts, Yutiriti


Self = TypeVar( "Self" )

#[yutiriti.tester.Tester]
@final
class Tester( Readonly ):

    """ ... """
    
    #[Tester()]: None
    def __init__( self:Self ) -> None: ...

    #[Tester.testing( Self@Tester )]: None
    def testing( bind:Self=None ) -> None:

        """ ... """

        def callback( value:any ) -> None:
            parts = split( r"\x0a", value if isinstance( value, str ) else repr( value ) )
            if len( parts[0] ) <= 16:
                parts[0] += "\x20" *20
            puts( "\r\x7b\x7d\x7b\x7d".format( "\x20" *6, "\x0a\x7b\x7d".format( "\x20" *6 ).join( parts ), end="\x0a" + ( "\x20" *5 ) ) )

        if bind is None:
            bind = Tester()

        count = 1
        passed = []
        yutiriti = Yutiriti()
        yutiriti.output( Tester.testing, "Testing" )
        instance = type( bind )
        methods = instance.__dict__
        for method in list( methods.keys() ):
            string = yutiriti.colorize( "{}Testing case {}".format( "\x20" * 6, count ) )
            if methods[method] is Tester.testing:
                continue
            if not callable( methods[method] ):
                continue
            puts( "{}@{}".format( "\x20" *4, method ) )
            for part in string:
                stdout.write( part )
                stdout.flush()
                if part != "\x20":
                    sleep( 00000.1 )
            try:
                task = methods[method]
                thread = Thread( target=lambda: task( callback ) )
                thread.start()
                while thread.is_alive():
                    for u in "\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x20":
                        print( f"\r{string} \x1b[1;33m{u}\x1b[0m", end="" )
                        sleep( 00000.1 )
                    print( f"\r{string}", end="" )
                thrown = thread.getExcept()
                if thrown is not None:
                    print( "\x20\x1b[1;31mFailed", end="" )
                    print( yutiriti.colorize( "\x20{} {}".format( typeof( thread.getExcept() ), thread.getExcept() ) ) )
                    passed.append( False )
                else:
                    print( "\x20\x1b[1;32mSuccess" )
                    passed.append( True )
            except EOFError:
                puts( f"\r{string}\x20\x1b[1;38;5;149mCanceled" )
            except KeyboardInterrupt:
                puts( f"\r{string}\x20\x1b[1;38;5;160mCanceled" )
            count += 1
        print( "\n{}".format( "\x20" *4 ), end="" )
        if len( passed ) >= 1:
            if False in passed:
                puts( "\x1b[1;31mFailed!" )
            else:
                puts( "\x1b[1;38;5;190mPassed!" )
        else:
            puts( "\x1b[1;38;5;214mNothing!" )
        puts( "" )
    
