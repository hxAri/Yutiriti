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


from datetime import datetime, timedelta
from re import match
from urllib.parse import parse_qs as queryparse, urlparse
from typing import final
from requests import Session, Response
from requests.cookies import RequestsCookieJar as Cookies
from requests.structures import CaseInsensitiveDict as Headers

from yutiriti.config import VERSION
from yutiriti.error import ( 
    RequestError, 
    RequestAuthError, 
    RequestDownloadError
)
from yutiriti.object import Object
from yutiriti.readonly import Readonly
from yutiriti.cookie import Cookie
from yutiriti.file import File
from yutiriti.path import Path 
from yutiriti.common import typeof


#[yutiriti.request.Request]
class Request( Readonly ):

    """
    Modified Request object for support usage, this request object can automatically 
    save any request history into json file when the request has successfully sent, 
    then it will automatically download the response content and write into new 
    file if the content type is HTML it will not combine with request history.
    """

    # Default request headers.
    HEADERS = {
        "User-Agent": f"Yutiriti/{VERSION}"
    }

    # Default request timeouts.
    TIMEOUTS = 10
    
    #[Request( Cookies|Dict|Object cookies, Dict|Headers|Object headers, Int timeout, Bool history )]: None
    def __init__( self, cookies:Cookies|dict|Object=None, headers:dict|Headers|Object=None, timeout:int=15, history:bool=True ) -> None:
        
        """
        Construct of method class Request.
        
        :params Cookies|Dict|Object cookies
            Request cookies
        :params Dict|Headers|Object headers
            Header settings for requests
        :params Int timeout
            Default timeout for requests
        :params Bool history
            Allow every successful request to save
        
        :return None
        :raises TypeError
            Raise when the value of parameter is invalid
        """

        # Readonly exceptional.
        self.__except__ = [
            "__previous__",
            "__response__",
            "__timeout__",
            "__history__"
        ]

        # History configurations.
        self.__history__ = []
        self.__historyAllow__ = history is True
        self.__historyFname__ = "requests/response.json"
        self.__historyFormat__ = "requests/{}/response\x20{}.json"
        self.__historyFormatHtml__ = "requests/{}/html/response\x20{}.html"

        # Request configurations.
        self.__session__ = Session()
        self.__cookies__ = self.session.cookies
        self.__headers__ = self.session.headers

        self.__previous__ = None
        self.__response__ = None
        
        # Default request timeout.
        self.__timeout__ = timeout if isinstance( timeout, int ) else Request.TIMEOUTS
        
        if headers is not None:
            if not isinstance( headers, ( dict, Headers, Object ) ):
                raise TypeError( "Invalid \"request\" parameter, value must be type Dict|Headers|Object, {} passed".format( typeof( headers ) ) )
            if isinstance( headers, Headers ):
                headers = dict( headers )
        else:
            headers = {}
        for header in Request.HEADERS.items():
            if header[0] not in headers:
                headers[header[0]] = header[1]
        for header in headers.keys():
            self.headers.update({ header: headers[header] })
        if cookies is not None:
            if not isinstance( cookies, ( Cookies, dict, Object ) ):
                raise TypeError( "Invalid \"request\" parameter, value must be type Cookies|Dict|Object, {} passed".format( typeof( cookies ) ) )
            if isinstance( cookies, Cookies ):
                cookie = dict( cookies )
            for cookie in cookies.keys():
                Cookie.set( self.cookies, cookie, cookies[cookie] )
        
        # If every successful request is allowed to save.
        if self.historyAllow:
            try:
                self.__history__ = File.json( self.historyFname )
            except FileNotFoundError:
                self.clean()
    
    #[Request.__error__( Exception error )]: Exception
    @final
    def __error__( self, error ):
        name = typeof( error )
        names = {
            "InvalidJSONError": "{name}: A JSON error occured",
            "JSONDecodeError": "{name}: Couldn't decode the text into json",
            "HTTPError ": "{name}: An HTTP error occurred",
            "ConnectionError ": "{name}: A Connection error occurred",
            "ProxyError ": "{name}: A proxy error occurred",
            "SSLError ": "{name}: An SSL error occurred",
            "Timeout ": "{name}: The request timed out",
            "ConnectTimeout ": "{name}: The request timed out while trying to connect to the remote server",
            "ReadTimeout ": "{name}: The server did not send any data in the allotted amount of time",
            "URLRequired ": "{name}: A valid URL is required to make a request",
            "TooManyRedirects ": "{name}: Too many redirects",
            "MissingSchema ": "{name}: The URL scheme (e.g. http or https) is missing",
            "InvalidSchema ": "{name}: The URL scheme provided is either invalid or unsupported",
            "InvalidURL ": "{name}: The URL provided was somehow invalid",
            "InvalidHeader ": "{name}: The header value provided was somehow invalid",
            "InvalidProxyURL ": "{name}: The proxy URL provided is invalid",
            "ChunkedEncodingError": "{name}: The server declared chunked encoding but sent an invalid chunk",
            "ContentDecodingError": "{name}: Failed to decode response content",
            "StreamConsumedError": "{name}: The content for this response was already consumed",
            "RetryError": "{name}: Custom retries logic failed",
            "UnrewindableBodyError": "{name}: Requests encountered an error when trying to rewind a body",
            "RequestsWarning": "{name}: Base warning for Requests",
            "FileModeWarning": "{name}: A file was opened in text mode, but Requests determined its binary length",
            "RequestsDependencyWarning": "{name}: An imported dependency doesn't match the expected version range"
        }
        if  name in names:
            string = names[name]
        else:
            string = "{name}: There was an ambiguous exception that occurred while handling your request"
            string += str( error )
        return RequestError( string.format( name=name ), prev=error )
    
    #[Request.__parse__( Str url )]: Dict<Str, Dict|Str>
    def __parse__( self, url:str ) -> dict[str:dict|str]:
        parsed = urlparse( url )
        query = queryparse( parsed.query )
        return {
            "path": parsed.path[1::] if parsed.path != "" else "/",
            "url": parsed.geturl(),
            "query": query
        }
    
    #[Request.__save__()]: Request
    @final
    def __save__( self ):
        
        """
        Save every successful request
        
        :return Request
            Instance of class Request
        """
        
        if  self.historyAllow is not True: return
        if  self.response is not False and \
            self.response is not None:
            try:
                content = self.response.json()
            except Exception:
                try:
                    content = f"[{self.response.headers['Content-Type']}]"
                except Exception:
                    content = None
            parsed = self.__parse__( self.response.url )
            query = parsed['query']
            time = datetime.now()
            file = self.historyFormat.format( parsed['path'], f"{time}" ).replace( "//", "/" )
            timestamp = datetime.timestamp( time )
            self.__history__.append({
                "url": parsed['url'],
                "file": file,
                "time": timestamp
            })
            File.write( self.historyFname, self.history )
            File.write( file, {
                "target": parsed['url'],
                "browser": self.response.request.headers['User-Agent'],
                "unixtime": timestamp,
                "request": {
                    "cookies": dict( self.cookies ),
                    "headers": dict( self.headers ),
                    "method": self.response.request.method,
                    "query": query,
                    "body": self.response.request.body if self.response.request.body is None or isinstance( self.response.request.body, str ) else str( self.response.request.body, encoding="UTF-8" )
                },
                "response": {
                    "status": f"{self.response}",
                    "cookies": dict( self.response.cookies ),
                    "headers": dict( self.response.headers ),
                    "content": content
                }
            })
            if "Content-Type" in self.__response__.headers:
                if match( r"^text/html(?:\;\s*charset\=[A-Z0-9\-]+(\;?\s*)?)?$", self.__response__.headers['Content-Type'] ) is not None:
                    File.write( 
                        self.historyFormatHtml.format( parsed['path'], f"{time}" ).replace( "//", "/" ), 
                        self.response.content.decode( "utf-8" ) 
                    )
        return self
    
    #[Request.clean()]: Bool
    def clean( self ) -> bool:
        Path.rmdir( "requests" )
        self.__history__ = []
        self.__previous__ = None
        self.__response__ = None
        try:
            File.write( self.historyFname, "[]" )
        except Exception:
            return False
        return True
    
    #[Request.cookies]: Cookies => RequestsCookieJar
    @final
    @property
    def cookies( self ) -> Cookies: return self.__cookies__

    #[Request.delete( Str url, **kwargs )]: Response
    @final
    def delete( self, url, **kwargs ) -> Response:
        return self.request( "DELETE", url=url, **kwargs )

    #[Request.download( Str url, Str name, Str fmode, Str encoding, Any **kwargs )]: Bool
    def download( self, url, name, fmode="wb", encoding="utf-8", **kwargs ):
        
        """
        Download content from url.
        
        :params Str url
            The target url of the content
        :params Str name
            Content/ Filename
        :params Str fmode
            File open mode
        :params Str encoding
            File encoding type
        :params Any **kwargs
            Request options
        
        :return Bool<True>
            When the content is successfully saved
        :raises RequestError
            When an error occurs while performing the request
        :raises RequestDownloadError
            When the download is failed
            When the content/ file can't save
        """
        
        try:
            result = self.get( url, **kwargs )
        except RequestError as e:
            raise e
        if result.status_code == 200:
            try:
                return File.write( name, result.content, fmode, encoding )
            except IOError as e:
                raise RequestDownloadError( f"Failed write file \"{name}\"", prev=e )
        raise RequestDownloadError( f"Failed get content from url, status [{result.status_code}]" )
    
    #[Request.get( Str url, **kwargs )]: Response
    @final
    def get( self, url, **kwargs ) -> Response:
        return self.request( method="GET", url=url, **kwargs )
    
    #[Request.head( Str url, **kwargs )]: Response
    @final
    def head( self, url, **kwargs ) -> Response:
        return self.request( method="HEAD", url=url, **kwargs )

    #[Request.headers]: Headers => CaseInsensitiveDict
    @final
    @property
    def headers( self ) -> Headers: return self.__headers__

    #[Request.history]: List
    @final
    @property
    def history( self ) -> list: return self.__history__
    
    #[Request.historyAllow]: Bool
    @final
    @property
    def historyAllow( self ) -> bool: return self.__historyAllow__
    
    #[Request.historyFname]: Str
    @final
    @property
    def historyFname( self ) -> str: return self.__historyFname__
    
    #[Request.historyFormat]: Str
    @final
    @property
    def historyFormat( self ) -> str: return self.__historyFormat__

    #[Request.historyFormatHtml]: Str
    @final
    @property
    def historyFormatHtml( self ) -> str: return self.__historyFormatHtml__

    #[Request.options( Str url, **kwargs )]
    @final
    def options( self, url, **kwargs ):
        return self.request( method="OPTIONS", url=url, **kwargs )
    
    #[Request.patch( Str url, **kwargs )]: Response
    @final
    def patch( self, url, **kwargs ) -> Response:
        return self.request( method="PATCH", url=url, **kwargs )
    
    #[Request.post( Str url, **kwargs )]: Response
    @final
    def post( self, url, **kwargs ) -> Response:
        return self.request( method="POST", url=url, **kwargs )
    
    #[Request.previous]: Response
    @final
    @property
    def previous( self ) -> Response: return self.__previous__
    
    #[Request.previously( Str time )]: List
    def previously( self, time:str ) -> list:
        
        """
        Return previous request responses based on given time.
        
        :params Str time
            Value must be like [0-9](s|m|h|d|w|M|y)
        
        :return List
            List of request responses
        :raises TypeError
            When the given string is invalid syntax
        :raises ValueError
            When the parameter passed is invalid value
        """
        
        current = datetime.now()
        if  not isinstance( time, str ):
            raise ValueError( "Invalid time parameter, value must be type str, {} passed".format( typeof( time ) ) )
        if  valid := match( r"^(?P<diff>[1-9][0-9]*)(?P<unit>s|m|h|d|w|M|y)$", time ):
            diff = int( valid.group( "diff" ) )
            unit = valid.group( "unit" )
            data = []
            match unit:
                case "m":
                    delta = timedelta( minutes=diff )
                case "h":
                    delta = timedelta( hours=diff )
                case "d":
                    delta = timedelta( days=diff )
                case "w":
                    delta = timedelta( weeks=diff )
                case "M":
                    delta = timedelta( days=diff * 30 )
                case "y":
                    delta = timedelta( days=diff * 365 )
            for history in self.history:
                timestamp = datetime.fromtimestamp( history['time'] )
                if  timestamp >= current - delta:
                    data.append( history )
            return data
        raise TypeError( "Invalid time syntax, value must be like \\d+(s|m|h|d|w|M|y)" )
    
    #[Request.put( Str url, **kwargs )]: Response
    @final
    def put( self, url, **kwargs ) -> Response:
        return self.request( method="PUT", url=url, **kwargs )
    
    #[Request.request( Str method, Str url, **kwargs )]: Response
    @final
    def request( self, method, url, **kwargs ) -> Response:
        
        """
        Send request to url target.
        
        :params Str method
            Request method name
        :params Str url
            Request url target
        :params Any **kwargs
            Request options
        
        :return Any
        :raises RequestError
            When an error occurs while performing the request
        :raises RequestAuthError
            When the user login authentication required
        """
        
        self.__previous__ = self.response
        self.__response__ = None
        
        if "timeout" not in kwargs:
            kwargs['timeout'] = self.timeout
        if "cookies" in kwargs:
            for cookie in list( kwargs['cookies'].keys() ):
                kwargs['cookies'][cookie] = str( kwargs['cookies'][cookie] )
        for cookie in self.cookies.items():
            Cookie.set( self.cookies, cookie[0], str( cookie[1] ) )
        if "headers" in kwargs:
            for header in list( kwargs['headers'].keys() ):
                kwargs['headers'][header] = str( kwargs['headers'][header] )
        for header in list( self.headers.keys() ):
            self.headers.update({ 
                header: str( self.headers[header] )
            })
        try:
            self.__response__ = self.session.request( method=method, url=url, **kwargs )
            self.__response__.status = self.__response__.status_code
            self.__save__()
        except BaseException as e:
            raise RequestError(**{
                "message": "There was an error sending the request",
                "prev": self.__error__( e )
            })
        if self.response.status == 401:
            raise RequestAuthError( "Login authentication is required" )
        return self.response
    
    #[Request.response]: Response
    @final
    @property
    def response( self ) -> Response: return self.__response__

    #[Request.session]: Session
    @final
    @property
    def session( self ) -> Session: return self.__session__

    #[Request.response]: Int
    @final
    @property
    def timeout( self ) -> int: return self.__timeout__
    

#[yutiriti.request.RequestRequired]
class RequestRequired:

    """
    This class is only for handle when the class has required Request instance to run any functionality in the class
    """
    
    #[RequestRequired( Request request )]: None
    def __init__( self, request ) -> None:
        
        """
        Construct method of class RequestRequired.
        
        :params Object app
            Application context
        :return None
        :raises TypeError
            When the class is inherit from Object
        :raises ValueError
            When invalid argument passed
        """
        
        if  isinstance( self, Object ):
            raise TypeError( "Class \"{}\" may not inherit an Object if it has inherited a previous RequestRequired".format( type( self ).__name__ ) )
        if  isinstance( request, Request ):
            self.__request__ = request
            RequestRequired.__setup__( self, request )
        else:
            raise ValueError( "Parameter request must be type Request, {} passed".format( type( request ).__name__ ) )
    
    #[RequestRequired.__setattr__( Str name, Any value )]: None
    @final
    def __setattr__( self, name, value ) -> None:
        if  name == "__request__":
            if  isinstance( value, Request ):
                self.__dict__[name] = value
                RequestRequired.__setup__( self, value )
                return
        if  isinstance( self, Readonly ):
            Readonly.__setattr__( self, name, value )
        else:
            self.__dict__[name] = value
    
    #[RequestRequired.__setup__( Request request )]: None
    @final
    def __setup__( self, request ) -> None:
        try:
            self.__cookies__ = request.cookies
            self.__headers__ = request.headers
            self.__session__ = request.session
        except AttributeError:
            pass
    
    #[RequestRequired.cookies]: Cookies => RequestsCookieJar
    @final
    @property
    def cookies( self ) -> Cookies: return self.__cookies__

    #[RequestRequired.headers]: Headers => CaseInsensitiveDict
    @final
    @property
    def headers( self ) -> Headers: return self.__headers__

    #[RequestRequired.request]: Request
    @final
    @property
    def request( self ) -> Request: return self.__request__

    #[RequestRequired.session]: Session
    @final
    @property
    def session( self ) -> Session: return self.__session__
    