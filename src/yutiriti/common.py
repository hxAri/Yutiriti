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


from datetime import datetime
from re import match


#[yutiriti.utility.common.classmethods( Object obj, Bool wrapper )]: Dict<Str, Callable>
def classmethods( obj:object, wrapper:bool=False ) -> dict[str:callable]:

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
	

#[yutiriti.utility.common.droper( Dict|List|Object items, List<Dict|List|Object|Dict> search, Bool nested )]: Dict
def droper( items:dict|list, search:list, nested:bool=False ) -> dict:
	
	"""
	Drops item based keys given.
	
	:params Dict|List|Object items
	:params List<Dict|List|Object|Str> search
	:params Bool nested
	
	Object, 
	:return Dict
		Droped items
	
	:raises TypeError
		When the value type if parameter is invalid
	"""
	
	if isinstance( search, ( dict, str ) ):
		search = [search]
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


#[yutiriti.itility.common.typedef( Mixed instance, Mixed of, Bool opt )]: Bool
def typedef( instance, of=None, opt:bool=None ) -> bool:
	
	"""
	Returns if instance is instance of instead.
	
	:params Mixed instance
	:params Mixed of
	:params Bool opt
		Negative check
	
	:return Bool
	"""
	
	if  isinstance( opt, bool ):
		return typedef( instance, of ) == opt
	else:
		try:
			of = of.__name__
		except AttributeError:
			if  not isinstance( of, str ):
				of = type( of ).__name__
		instance = type( instance ).__name__
		if  instance == of:
			return True
		return False
	

#[yutiriti.utility.common.typeof( Mixed instance )]: Str
def typeof( instance ) -> str:
	
	"""
	Return object instance name.
	
	:params Mixed instance
	
	:return Str
		Instance name
	"""
	
	return type( instance ).__name__
	
