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
class Tester( Readonly ):

	"""
	"""
	
	#[Tester()]: None
	@final
	def __init__( self:Self ) -> None:
		...

	#[Tester.testing( Self@Tester )]: None
	@final
	def testing( self:Self=None ) -> None:

		"""
		"""

		if self is None:
			self = Tester()

		count = 1
		passed = []
		instance = type( self )
		methods = instance.__dict__
		for method in list( methods.keys() ):
			string = Yutiriti.colorize( self, "{}Testing case {}".format( "\x20" * 6, count ) )
			if methods[method] is Tester.testing:
				continue
			elif not callable( methods[method] ):
				continue
			else:
				puts( "{}@{}".format( "\x20" *4, method ) )
				for part in string:
					stdout.write( part )
					stdout.flush()
					if part != "\x20":
						sleep( 00000.1 )
			try:
				thread = Thread( target=lambda: methods[method]( lambda x: puts( "\r\x7b\x7d\x7b\x7d".format( "\x20" *6, "\x0a\x7b\x7d".format( "\x20" *6 ).join( split( r"\x0a", x if isinstance( x, str ) else repr( x ) ) ) ), end="\x0a" + ( "\x20" *5 ) ) ) )
				thread.start()
				while thread.is_alive():
					for u in "\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x5c\x7c\x2f\x2d\x20":
						print( f"\r{string} \x1b[1;33m{u}\x1b[0m", end="" )
						sleep( 00000.1 )
					print( f"\r{string}", end="" )
				thrown = thread.getExcept()
				if thrown is not None:
					print( "\x20\x1b[1;31mFailed", end="" )
					print( Yutiriti.colorize( self, "\x20{} {}".format( typeof( thread.getExcept() ), thread.getExcept() ) ) )
					passed.append( False )
				else:
					print( "\x20\x1b[1;32mSuccess" )
					passed.append( True )
			except EOFError as e:
				puts( f"\r{string}\x20\x1b[1;38;5;149mCanceled" )
			except KeyboardInterrupt as e:
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
	
