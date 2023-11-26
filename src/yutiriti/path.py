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


import os
import shutil


#[yutiriti.path.Path]
class Path:
    
    #[Path.is( Str dir )]: Bool
    @staticmethod
    def dir( dir:str ) -> bool:
        
        """
        Return if directory name is directory.
        
        :params String dir
            Directory name to be check
        
        :return Bool
            True if directory is directory
            False otherwise
        """
        
        return( os.path.isdir( dir ) )
    
    #[Path.exists( Str dir )]: Bool
    @staticmethod
    def exists( dir:str ) -> bool:
        
        """
        Return if directory is exists.
        
        :params String dir
            Directory name
        
        :return Bool
            True if directory is exists
            False otherwise
        """
        return( os.path.exists( dir ) )
    
    #[Path.mkdir( Str dir )]: None
    @staticmethod
    def mkdir( dir ) -> None:
        
        """
        Make directory
        
        :params String dir
            Directory name
            Its, support slash symbol
        
        :return None
        """
        
        name = "."
        path = dir.split( "/" )
        for dir in path:
            name += "/"
            name += dir
            if not Path.dir( name ):
                os.mkdir( name )
    
    #[Path.pwd()]: Str
    @staticmethod
    def pwd() -> str: return( os.getcwd() )

    #[Path.rmdir( Str dir )]: None
    @staticmethod
    def rmdir( dir:str ) -> None:
        if Path.exists( dir ):
            shutil.rmtree( dir )
    