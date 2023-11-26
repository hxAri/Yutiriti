# Yutiriti
Yūtiriti is a tool for building Command Line Programs, it is completely built using Python3.

## Warning
Please note that this is strictly intended for use in a Linux environment only. I don't know if this will work well if run on an Operating System such as Windows or MacOS, please report an issue if you encounter any problems.

## Table of Contents
* **Installation**
* **Usage**
  * **Cookie**
  * **Droper**
  * **File**
  * **Object**
  * **Path**
  * **Puts**
  * **Readonly**
  * **Request**
  * **String**
  * **Thread**
  * **Tree**
  * **Typing**
  * **Yutiriti**
* **Request History**
* **License**
* **Donate**

## Installation
First, please clone this repository.
```sh
git clone https://github.com/hxAri/Yutiriti
```
Change current working directory.
```sh
cd Yutiriti
```
Install requirement dependencies.
```sh
pip install -r requirements.txt
```
Install as module into local machine.
```sh
python setup.py install
```

## Usage
Yūtiriti was created with the aim of making it easier to create Command Line programs, I hope you can easily understand it too.
#### yutiriti.cookie.Cookie
#### yutiriti.common.Dropper
Dropper is a function used to retrieve values from a dictionary or list. Note that the **dropper** will retrieve the value even though it also has to go through the list iteration for
```py
from yutiriti.common import droper

# Example key of data want to get.
keys = [
    "users",
    {
        "deep": [
            {
                "more": [
                    "value"
                ]
            }
        ]
    }
]

# Example of Data
data = {
    "users": [
        {
            "id": 12345678,
            "username": "example",
            "fullname": "Example"
        }
    ],
    "deep": {
        "more": {
            "value": "VALUE"
        }
    }
}

# List of data result
print( droper( data, keys ) )
```
You can also keep the nested structure.
```py
print( droper( data, keys, nested=True ) )
```
#### yutiriti.file.File
Simplify the method of reading and also writing file contents.
```py
from yutiriti.file import File

try:

    # Reading file contents.
    result = File.read( "/path/to/file" )

    # Reading file per-lines.
    result = File.line( "/path/to/file" )

    # Reading and decoding json contents.
    result = File.json( "/path/to/file.json" )

    # Write contents into file.
    # Note that the method accepts any data type and will
    # automatically convert it to a string type when writing content.
    result = File.write( "/path/to/file", data, mode="w" )

except BaseException as e:
    print( e )
```
#### yutiriti.object.Object
#### yutiriti.path.Path
#### yutiriti.yutiriti.Puts
Print any type into terminal screen with automatically colorize, It also fully supports parameters such as python's built-in **print** function.
```py
from yutiriti.yutiriti import puts

puts( "Hello World!", end="\n" )
```
#### yutiriti.readonly.Readonly
#### yutiriti.request.Request
#### yutiriti.string.String
#### yutiriti.thread.Thread
Make it easy to catch exceptions and also return values for functions executed via Thread, this is also a derivative of python's built-in Thread, just a few touches away.
```py
from yutiriti.request import Request
from yutiriti.thread import Thread

def ping( utl:str, timeout:int=10 ) -> int:
    request = Request()
    response = request.get( url, timeout=timeout )
    return response.status

try:
    thread = Thread( target=lambda: ping( "https://www.example.com", timeout=10 ) )
    thread = Thread( target=ping, kwargs={
        "url": "https://www.example.com",
        "timeout": 10
    })
    thread.start()
    status = thread.getReturn()
    error = thread.getExcept()
    if isinstance( error, BaseException ):
        raise error 
except RequestError as e:
    # Do something here
```
#### yutiriti.tree.Tree
Build tree structures easily.
```py
from yutiriti import tree

tree({
    ...
})
```
#### yutiriti.typing.Typing
The Typing class works in almost the same way as the Object class from Yutiriti, but Typing will only pass items returned by the **_ _ items _ _** method to its parent class, namely Object from Yutiriti, the aim is to avoid errors when checking response data and so on because Yutiriti treats dictionaries. and also lists as objects, and for example it can be very confusing when it comes to managing response data as Instagram usually provides quite large responses to process and, when the JSON response is passed to a class that extends the Typing class it will only take time and also set the value returned by previous **_ _ items _ _** method, but we can also set incompatible items from outside the class or from inside except the instance, and this is not always intended for things like those previously mentioned

Apart from that, Typing also normalizes strings to int values ​​if the value only contains numbers. To use it you have to create your implementation class.
```py
from yutiriti.object import Object
from yutiriti.typing import Typing

class Example( Typing ):

    @property
    def __items__( self ) -> dict[str:str]|list[str]:
        return [
            # item key list, this is the same as how the dropper works
        ]
    
    @property
    def __nested__( self ) -> bool: return False|True

    @property
    def __mapping__( self ) -> dict|Object: return {
        # This will make the user value a User Object
        "user": User
    }
```
You can also still use Readonly classes.
```py
from yutiriti.object import Object
from yutiriti.readonly import Readonly
from yutiriti.typing import Typing

class Example( Readonly, Typing ):
    ...
```
#### yutiriti.yutiriti.Yutiriti

## Request History
Please note that Yūtiriti stores all successful request results and stores all request logs in the `history` property and also writes them to the `~/requests/response.json` file, you can use each request log for further analysis if you need it and make sure your directory allows it Yūtiriti to write the file.

## Licence
All Yūtiriti source code is licensed under the GNU General Public License v3. Please [see](https://www.gnu.org/licenses) the original document for more details.

## Donate
Give spirit to the developer, no matter how many donations given will still be accepted<br/>
[paypal.me/hxAri](https://paypal.me/hxAri).