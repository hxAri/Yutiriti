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


from threading import Thread as Threading


#[yutiriti.utility.thread.Thread]
class Thread( Threading ):
	
	#[Thread()]: None
	def __init__( self, group=None, target=None, name=None, args=(), kwargs={} ) -> None:
		Threading.__init__( self, group=group, target=target, name=name, args=args, kwargs=kwargs )
		self._return = None
		self._except = None
	
	#[Thread.run()]: None
	def run( self ) -> None:
		if self._target is not None:
			try:
				self._return = self._target( *self._args, **self._kwargs )
			except BaseException as e:
				self._except = e
	
	#[Thread.getExcept()]: BaseException
	def getExcept( self ) -> BaseException:
		
		"""
		Return raised exception.
		
		:return BaseException
			Raised Exception on thread
		"""
		
		return( self._except )
	
	#[Thread.getReturn()]: Any
	def getReturn( self ) -> any:
		
		"""
		Return value from task.
		
		:return Any
		"""
		
		return( self._return )
	