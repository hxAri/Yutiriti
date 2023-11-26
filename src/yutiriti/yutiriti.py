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


import re
import sys

from getpass import getpass
from os import system
from re import findall
from time import sleep
from typing import final

from yutiriti.error import Error
from yutiriti.thread import Thread
from yutiriti.common import typeof


#[yutiriti.Yutiriti]
class Yutiriti:

    #[Yutiriti.banner]: Str
    @property
    def banner( self ) -> str:

        """
        Return string of Yutiriti Banner/ Logo.
        I hope you does not replace this bro!

        :return Str
        """

        return "\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▒▒▒\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▒▒▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20███▒\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▒▒███▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20███▒\x20\x20\x20\x20\x20\x20\x20\x20\x20▓\x20\x20▓▓▓███▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20███▒\x20\x20\x20\x20\x20▒▓▓████▒\x20▒███▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20███▒\x20▓▓▓\x20▒▓▓▒▒████████▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▒▓▓▓█▒\x20███▒▒▓▓▒\x20▓▓██████▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▒▓▓██▒░████████▓▓▓▓▒▓████▒▒▓\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▒▓███▓▓███▒▒▓███▓▓▓░▒██████▓▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20████████\x20▒█▓▓▓▓▓▓\x20▒███▒▒██▓\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20████████▓▓██▓▓▓▓▓\x20▒▓▓█▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▓███▓▒▓▓█▓███▓▒▓▓▓\x20\x20\x20▒▓▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20▒█████▒\x20███▓████▓▓▓▓\x20▒▓██▒\x0a\x20\x20\x20\x20\x20\x20\x20▒███████▒▒███\x20▒███▓▓▓▓░▒███▒\x0a\x20\x20\x20\x20\x20\x20▓███\x20\x20███▓▒███▒███▓▓▓▓▓▓▓███▒\x0a\x20\x20\x20\x20▓███▒\x20\x20\x20███▓▒███\x20▓██▒\x20▓▓▓▓████▒\x0a\x20\x20\x20\x20\x20▓▓\x20\x20\x20\x20▒███▒\x20▓▓▓\x20▒▓▓▒\x20▒▒▒▒▓███▓▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▓███▒\x20\x20\x20\x20\x20▒▓▓▒\x20\x20▓█▓▒████▓▓▓\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20███▒\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▒\x20▒███▓▓▓▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20███▒\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▒███▒\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▒▒▒\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20▒▒▒\x0a"

    #[Yutiriti.clear]: None
    @final
    @property
    def clear( self ) -> None:

        """
        Clear terminal screen.

        :return None
        """

        system( "clear" )
    
    #[Yutiriti.close( Any *args, Any **kwargs )]: None
    @final
    def close( self, *args:any, **kwargs:any ) -> None:

        """
        Force close the program.

        :params Any *args
        :params Any **kwargs

        :return None
        """

        self.output( *args, **kwargs )
        sys.exit()
    
    #[Yutiriti.colorize( Str format, Str base )]: Str
    @final
    def colorize( self, string:str, base:str=None ) -> str:

        """
        Autormate colorize text of string.

        :params Str string
        :params Str base
            Base color of string
        
        :return Str
        """

        result = ""
        strings = [ x for x in re.split( r"((?:\x1b|\033)\[[0-9\;]+m)", string ) if x != "" ]
        regexps = {
            "number": {
                "pattern": r"(?P<number>\b(?:\d+)\b)",
                "colorize": "\x1b[1;38;5;61m{}{}"
            },
            "define": {
                "handler": lambda match: re.sub( r"(\.|\-){1,}", lambda m: "\x1b[1;38;5;69m{}\x1b[1;38;5;111m".format( m.group() ), match.group( 0 ) ),
                "pattern": r"(?P<define>(?:@|\$)[a-zA-Z0-9_\-\.]+)",
                "colorize": "\x1b[1;38;5;111m{}{}"
            },
            "symbol": {
                "pattern": r"(?P<symbol>\\|\:|\*|-|\+|/|&|%|=|\;|,|\.|\?|\!|\||<|>|\~){1,}",
                "colorize": "\x1b[1;38;5;69m{}{}"
            },
            "bracket": {
                "pattern": r"(?P<bracket>\{|\}|\[|\]|\(|\)){1,}",
                "colorize": "\x1b[1;38;5;214m{}{}"
            },
            "boolean": {
                "pattern": r"(?P<boolean>\b(?:False|True|None)\b)",
                "colorize": "\x1b[1;38;5;199m{}{}"
            },
            "typedef": {
                "pattern": r"(?P<typedef>\b(?:int|float|str|list|tuple|dict|object|set|bool|range|AttributeError|BaseException|BaseExceptionGroup|GeneratorExit|KeyboardInterrupt|BufferError|EOFError|ExceptionGroup|ImportError|ModuleNotFoundError|LookupError|IndexError|KeyError|MemoryError|NameError|UnboundLocalError|OSError|BlockingIOError|ChildProcessError|ConnectionError|BrokenPipeError|ConnectionAbortedError|ConnectionRefusedError|ConnectionResetError|FileExistsError|FileNotFoundError|InterruptedError|IsADirectoryError|NotADirectoryError|PermissionError|ProcessLookupError|TimeoutError|ReferenceError|RuntimeError|NotImplementedError|RecursionError|StopAsyncIteration|StopIteration|SyntaxError|IndentationError|TabError|SystemError|TypeError|ValueError|UnicodeError|UnicodeDecodeError|UnicodeEncodeError|UnicodeTranslateError|Warning|BytesWarning|DeprecationWarning|EncodingWarning|FutureWarning|ImportWarning|PendingDeprecationWarning|ResourceWarning|RuntimeWarning|SyntaxWarning|UnicodeWarning|UserWarning)\b)",
                "colorize": "\x1b[1;38;5;213m{}{}"
            },
            "linked": {
                "handler": lambda match: re.sub( r"(\\|\:|\*|-|\+|/|&|%|=|\;|,|\.|\?|\!|\||<|>|\~){1,}", lambda m: "\x1b[1;38;5;69m{}\x1b[1;38;5;43m".format( m.group() ), match.group( 0 ) ),
                "pattern": r"(?P<linked>\bhttps?://[^\s]+)",
                "colorize": "\x1b[1;38;5;43m\x1b[4m{}{}"
            },
            "version": {
                "handler": lambda match: re.sub( r"([\d\.]+)", lambda m: "\x1b[1;38;5;190m{}\x1b[1;38;5;112m".format( m.group() ), match.group( 0 ) ),
                "pattern": r"(?P<version>\b[vV][\d\.]+\b)",
                "colorize": "\x1b[1;38;5;112m{}{}"
            },
            "yutiriti": {
                "pattern": r"(?P<yutiriti>\b(?:[kK]anash[i|ī])\b)",
                "colorize": "\x1b[1;38;5;111m{}{}"
            },
            "comment": {
                "pattern": r"(?P<comment>\#\S+)",
                "colorize": "\x1b[1;38;5;250m{}{}"
            },
            "string": {
                "handler": lambda match: re.sub( r"(?<!\\)(\\\"|\\\'|\\`|\\r|\\t|\\n|\\s)", lambda m: "\x1b[1;38;5;208m{}\x1b[1;38;5;220m".format( m.group() ), match.group( 0 ) ),
                "pattern": r"(?P<string>(?<!\\)(\".*?(?<!\\)\"|\'.*?(?<!\\)\'|`.*?(?<!\\)`))",
                "colorize": "\x1b[1;38;5;220m{}{}"
            }
        }
        if not isinstance( base, str ):
            base = "\x1b[0m"
        try:
            last = base
            escape = None
            pattern = "(?:{})".format( "|".join( regexp['pattern'] for regexp in regexps.values() ) )
            compile = re.compile( pattern, re.MULTILINE | re.S )
            skipable = []
            for idx, string in enumerate( strings ):
                if idx in skipable:
                    continue
                color = re.match( r"^(?:\x1b|\033)\[([^m]+)m$", string )
                if color != None:
                    index = idx +1
                    escape = color.group( 0 )
                    last = escape
                    try:
                        while( rescape := re.match( r"(?:\x1b|\033)\[([^m]+)m", strings[index] ) ) is not None:
                            skipable.append( index )
                            escape += rescape.group( 0 )
                            last = rescape.group( 0 )
                            index += 1
                    except IndexError:
                        break
                    if index +1 in skipable:
                        index += 1
                    skipable.append( index )
                else:
                    escape = last
                    index = idx
                string = strings[index]
                search = 0
                match = None
                while( match := compile.search( string, search ) ) is not None:
                    if match.groupdict():
                        groups = match.groupdict().keys()
                        for group in groups:
                            if group in regexps and \
                                isinstance( regexps[group], dict ) and \
                                isinstance( match.group( group ), str ):
                                colorize = regexps[group]['colorize']
                                break
                        chars = match.group( 0 )
                        if "rematch" in regexps[group] and isinstance( regexps[group]['rematch'], dict ):
                            pass
                        if "handler" in regexps[group] and callable( regexps[group]['handler'] ):
                            result += escape
                            result += string[search:match.end() - len( chars )]
                            result += colorize.format( regexps[group]['handler']( match ), escape )
                            search = match.end()
                            continue
                        result += escape
                        result += string[search:match.end() - len( chars )]
                        result += colorize.format( chars, escape )
                        search = match.end()
                    pass
                result += escape
                result += string[search:]
                #escape = None
        except Exception as e:
            print( e )
            print( e.__traceback__.tb_lineno )
            exit()
        return result
    
    #[Yutiriti.exit( Any *args, Any **kwargs )]: None
    @final
    def exit( self, *args:any, **kwargs:any ) -> None:

        """
        Exit the program.

        :params Any *args
        :params Any **kwargs

        :return None
        """

        self.close( *args, **kwargs )
    
    #[Yutiriti.emit( BaseException|Error|List error )]: None
    @final
    def emit( self, error:BaseException ) -> None:

        """
        Print thrown exception into terminal screen.

        :params BaseException error

        :return None
        """

        self.clear
        name = type( self ).__name__
        strings = f"{name}\x2e\x65\x72\x72\x6f\x72\x0a"
        if isinstance( error, Error ):
            message = error.message
            code = error.code
            prev = error.prev
            if isinstance( prev, BaseException ):
                prevName = type( prev ).__name__
                prevMessage = str( prev )
                try:
                    prevFile = prev.__traceback__.tb_frame.f_code.co_filename
                    prevLine = prev.__traceback__.tb_lineno
                except AttributeError:
                    prevFile = None
                    prevLine = None
                prev = ""
                if prevFile and prevLine:
                    prev += f"\x20\x20{name}\x2e\x70\x72\x65\x76\x20{prevName}\x0a"
                    prev += f"\x20\x20\x20\x20{prevFile}\x20{prevLine}\x0a"
                prev += f"\x20\x20{name}\x2e\x70\x72\x65\x76\x20{prevName}\x0a"
                prev += f"\x20\x20\x20\x20{prevMessage}\x0a"
            else:
                prev = ""
            try:
                file = error.__traceback__.tb_frame.f_code.co_filename
                line = error.__traceback__.tb_lineno
            except AttributeError:
                file = "Initialize"
                line = "\x70\x61\x73\x73\x65\x64"
            error = type( error ).__name__
            strings += prev
            strings += f"\x20\x20{name}\x2e\x72\x61\x69\x73\x65\x20{error}\x20{code}\x0a"
            strings += f"\x20\x20{name}\x2e\x72\x61\x69\x73\x65\x20{error}\x0a"
            strings += f"\x20\x20\x20\x20{file}\x20{line}\x0a"
            strings += f"\x20\x20\x20\x20{message}\x0a"
        else:
            if isinstance( error, list ):
                try:
                    message = [ str( error[0] ), error[1] ]
                except IndexError:
                    message = str( error[0] )
                try:
                    filename = error[0].__traceback__.tb_frame.f_code.co_filename
                    lineno = error[0].__traceback__.tb_lineno
                except AttributeError:
                    filename = None
                    lineno = None
                error = type( error[0] ).__name__
            else:
                message = str( error )
                try:
                    filename = error.__traceback__.tb_frame.f_code.co_filename
                    lineno = error.__traceback__.tb_lineno
                except AttributeError:
                    filename = None
                    lineno = None
                error = type( error ).__name__
            strings = f"{name}\x2e\x65\x72\x72\x6f\x72\x0a "
            strings += f"\x20\x20{name}\x2e\x72\x61\x69\x73\x65\x20{error}\x0a"
            if filename and lineno:
                strings += f"\x20\x20\x20\x20{filename}\x20{lineno}\x0a"
            if isinstance( message, list ):
                for i in range( len( message ) ):
                    strings += f"\x20\x20\x20\x20{message[i]}\x0a"
            else:
                strings += f"\x20\x20\x20\x20{message}\x0a"
        for subject in findall( r"(\[Errno\s\d+\]\s*)", strings ):
            strings = strings.replace( subject, "" )
        print( "\x0a\x7b\x7d\x0a\x0a\x0a\x7b\x7d".format( self.banner, self.colorize( f"\x1b[0m{strings}" ) ) )
    
    #[Yutiriti.getpass( Str label, Bool ignore )]: Str
    @final
    def getpass( self, label:str, ignore:bool=True ) -> str:

        """
        Get password from input stream of user.

        :params Str label
        :params Bool ignore
            Allow ignore KeyboardInterrupt
        
        :return Int|Str
        """

        if label == None or label == "":
            place = "\x7b\x7d\x2e\x67\x65\x74\x70\x61\x73\x73\x3a\x20".format( type( self ).__name__ )
        else:
            place = "\x7b\x7d\x3a\x20".format( label )
        try:
            value = getpass( self.colorize( place ) )
            if value == "":
                value = self.getpass( label, ignore )
            return value
        except EOFError as e:
            self.close( e, "\x46\x6f\x72\x63\x65\x20\x63\x6c\x6f\x73\x65" )
        except KeyboardInterrupt as e:
            if ignore == False:
                self.close( e, "\x46\x6f\x72\x63\x65\x20\x63\x6c\x6f\x73\x65" )
            print( "\r" )
            return self.getpass( label, ignore )
    
    #[Yutiriti.input( Str label, Any default, Bool number, Bool ignore )]: Int|Str
    @final
    def input( self, label:str, default:any=None, number:bool=False, ignore:bool=True ) -> int|str:

        """
        Get input stream from user.

        :params Str label
        :params Any default
            Default value option
        :params Bool number
            When the value is only number
        :params Bool ignore
            Allow ignore KeyboardInterrupt
        
        :return Int|Str
        """

        if label == None or label == "":
            place = "\x7b\x7d\x2e\x69\x6e\x70\x75\x74\x3a\x20".format( type( self ).__name__ )
        else:
            if not isinstance( label, str ):
                typed = typeof( label )
                if typed == "function" or typed == "method":
                    label = label.__name__
                    label = label.capitalize()
                else:
                    label = typed
            if label != "<<<" and label != ">>>" and not label.endswith( "[Y/n]" ):
                place = "\x7b\x7d\x3a\x20".format( label.strip() )
            else:
                place = "\x7b\x7d\x20".format( label.strip() )
        try:
            if number:
                value = int( float( input( self.colorize( place ) ) ) )
            else:
                value = input( self.colorize( place ) )
                value = value.strip()
            if value == "":
                if default != None:
                    value = default if type( default ).__name__ != "list" else default[0]
                else:
                    value = self.input( label, default, number, ignore )
            if type( default ).__name__ == "list":
                try:
                    default.index( value )
                except ValueError:
                    value = self.input( label, default, number, ignore )
            return value
        except ValueError as e:
            return self.input( label, default, number, ignore )
        except EOFError as e:
            self.close( e, "\x46\x6f\x72\x63\x65\x20\x63\x6c\x6f\x73\x65" )
        except KeyboardInterrupt as e:
            if ignore == False:
                self.close( e, "\x46\x6f\x72\x63\x65\x20\x63\x6c\x6f\x73\x65" )
            print( "\r" )
            return self.input( label, default, number, ignore )
    
    #[Yutiriti.output( Any refer, Dict|List|Str message, Bool line )]: None
    @final
    def output( self, refer:any, message:dict|list|str, line:bool=False ) -> None:

        """
        Print standar output into terminal screen.

        :params Any refer
            Instance object reference
        :params Dict|List|Str message
        :params Bool line

        :return None
        """

        #[Yutiriti.output$.println( Dict|List|Str message, Int indent, Bool line )]: Str
        def println( message:dict|list|str, indent:int=4, line:bool=False ) -> str:

            """
            Output template builder.

            :params Dict|List|Str message
            :params Int indent
            :params Bool line

            :return Str
            """

            space = "\x20" * indent
            stack = ""
            if isinstance( message, dict ):
                for i in message:
                    if isinstance( message[i], dict ):
                        try:
                            stack += println(*[ message[i]['message'], indent +4 if message[i]['line'] else indent, False if message[i]['line'] else True ])
                        except KeyError:
                            stack += println(*[ message[i], indent +4 if line else indent, False if line else True ])
                    elif isinstance( message[i], list ):
                        stack += println(*[ message[i], indent +4 if line else indent, False if line else True ])
                    else:
                        parts = str( message[i] )
                        parts = parts.split( "\n" )
                        for part in parts:
                            if line:
                                stack += "\x7b\x30\x7d\x7b\x31\x7d\x29\x20\x1b[1;38;5;252m\x7b\x32\x7d\x1b[0m\x0a".format( space, i, part )
                            else:
                                stack += "\x7b\x30\x7d\x7b\x31\x7d\x0a ".format( space, part )
            elif isinstance( message, list ):
                u = 0
                l = len( message )
                for i in range( l ):
                    if isinstance( message[i], dict ):
                        try:
                            stack += println(*[ message[i]['message'], indent +4 if message[i]['line'] else indent, False if message[i]['line'] else True ])
                        except KeyError:
                            stack += println(*[ message[i], indent +4 if line else indent, False if line else True ])
                        u += 1
                    elif isinstance( message[i], list ):
                        stack += println(*[ message[i], indent +4 if line else indent, False if line else True ])
                        u += 1
                    else:
                        parts = str( message[i] )
                        parts = parts.split( "\n" )
                        for part in parts:
                            if line:
                                index = i +1 -u
                                length = len( str( l ) )
                                length = length +1 if length == 1 else length
                                format = f"\x7b\x30\x7d\x7b\x31\x3a\x30\x3e{length}\x7d\x29\x20\x1b[1;38;5;252m\x7b\x32\x7d\x1b[0m\x0a"
                                stack += format.format( space, index, part )
                            else:
                                stack += "\x7b\x30\x7d\x7b\x31\x7d\x0a".format( space, part )
            else:
                message = str( message )
                for line in message.split( "\n" ):
                    stack = "\x7b\x30\x7d\x7b\x31\x7d\x0a".format( space, line )
            return stack
        
        self.clear
        base = refer
        try:
            refer = refer.__name__
        except AttributeError:
            named = typeof( refer )
            match named:
                case "str" | "int" | "float" | "complex" | "list" | "tuple" | "range" | "dict" | "set" | "frozenset" | "bool" | "bytes" | "bytearray" | "memoryview" | "NoneType":
                    pass
                case _:
                    refer = named
        named = typeof( self )
        strings = f"{named}\x2e\x6f\x75\x74\x70\x75\x74\x0a"
        if isinstance( refer, BaseException ):
            strings += f"\x20\x20{named}\x2e{refer}\x2e{base.__traceback__.tb__lineno}\x0a"
            strings += f"\x20\x20{named}\x2e{refer}\x2e{__name__}\x0a"
        else:
            strings += f"\x20\x20{named}\x2e{refer}\x0a"
        strings += println( message, 4, line )

        print( "\x0a\x7b\x7d\x0a\x0a\x0a\x7b\x7d".format( self.banner, self.colorize( f"\x1b[0m{strings}".replace( "\t", "\x20" *4 ) ) ) )
    
    #[Yutiriti.previous( Callable back, Str label, Any *args, Any **kwargs )]: Any
    @final
    def previous( self, back:callable, label:str=None, *args:any, **kwargs:any ) -> any:

        """
        Previous action.

        :params Callable back
        :params Str label
        :params Any *args
        :params Any **kwargs

        :return Any
        """

        match typeof( back ):
            case "function" | "method":
                if label == None:
                    try:
                        label = f"Back ({back.__self__.__class__.__name__})"
                    except AttributeError:
                        label = f"Back ({back.__name__})"
                self.input( label, default="" )
                return back( *args, **kwargs )
            case _:
                raise ValueError( f"Argument back must be type Function|Method, {type( back ).__name__} given" )
    
    #[Yutiriti.rmdoc( Dict lists )]: List
    @final
    def rmdoc( self, lists:dict ) -> list:
        stack = []
        for i in lists:
            match typeof( lists[i] ):
                case "dict" | "list" | "set" | "tuple":
                    pass
                case _:
                    stack.append( i )
        return stack
    
    #[Yutiriti.thread( Str strings, Function Object, Any *args, Any **kwargs )]: Any
    @final
    def thread( self, strings:str, target:callable, *args:any, **kwargs:any ) -> any:

        """
        Threading animation.

        :params Str string
            Loading text
        :params Callable target
        :params Any *args
        :params Any **kwargs

        :return Any
        :raises BaseException
            When the error thrown in the thread run is
            not instantce of class EOFError, KeyboardInterrupt
        """

        try:
            self.clear
            print( "\x0a\x7b\x7d\x0a\x0a\x0a".format( self.banner ) )
            task = Thread( target=target, args=args, kwargs=kwargs )
            named = type( self ).__name__
            strings = "\x7b\x30\x7d\x7b\x31\x7d".format( "\x20" *4, strings )
            sys.stdout.write( self.colorize( "\x7b\x31\x7d\x2e\x74\x68\x72\x65\x61\x64\x0a\x7b\x30\x7d\x7b\x31\x7d\x2e\x61\x6c\x69\x76\x65\x0a".format( "\x20" *2, named ) ) )
            for e in strings:
                sys.stdout.write( e )
                sys.stdout.flush()
                if e != "\x20":
                    sleep( 00000.1 )
                    pass
            task.start()
            while task.is_alive():
                for i in "\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x20":
                    print( "\x0d\x7b\x7d\x20\x1b[1;33m\x7b\x7d".format( self.colorize( strings ), i ), end="" )
                    sleep( 00000.1 )
            print( "\x0d\x0a" )
            sleep( 00000.1 )
            self.clear
        except EOFError as e:
            self.close( e, "\x46\x6f\x72\x63\x65\x20\x63\x6c\x6f\x73\x65" )
        except KeyboardInterrupt:
            self.close( e, "\x46\x6f\x72\x63\x65\x20\x63\x6c\x6f\x73\x65" )
        error = task.getExcept()
        if isinstance( error, BaseException ):
            raise error
        else:
            return task.getReturn()
    
    #[Yutiriti.tryAgain( Str label, Callable next, Callable other, Str value, List defaultValue, Any *args, Any **kwargs )]: Any
    @final
    def tryAgain( self, label:str="Try again [Y/n]", next:callable=None, other:callable=None, value:str="Y", defaultValue=[ "Y", "y", "N", "n" ], *args, **kwargs ) -> any:

        """
        Try again input.

        :params Str label
        :params Callable next
        :params Callable other
        :params Str value
        :params List[Str] defaultValue
        :params Any *args
        :params Any **kwargs

        :return Any
        :raises TypeError
            When the parameter value is invalid value type
        """

        if self.input( label, default=defaultValue ).upper() == value:
            if callable( next ):
                return next( *args, **kwargs )
            else:
                raise TypeError( "Invalid \"next\" parameter, value must be type Function|Method, {} passed".format( type( next ).__name__ ) )
        else:
            if callable( other ):
                return other()
        pass

    #[Yutiriti.xdgopen( Str target )]: Int
    @final
    def xdgopen( self, target:str ) -> int:

        """
        Open url or file with xdg-open.

        :params Str target
            File or url target to open
        
        :return Int
        """

        try:
            return system( "xdg-open {}".format( target ) )
        except BaseException:
            pass
    

#[yutiriti.puts( Any *values, Str base, Str end, Str sep )]: None
def puts( *values:any, base:str="\x1b[0m", end:str="\x0a", sep:str="\x20" ) -> None:

    """
    Print output stream into terminal screen with colorize text.

    :params Any *values
    :params Str base
    :params Str end
    :params Str sep

    :return None
    """

    print( *[ Yutiriti.colorize( self=puts, base=base, string=value if isinstance( value, str ) else repr( value ) ) for value in values ], end=end, sep=sep )

