# python-df-parser

Parser for (dataforge)[http://npm.mipt.ru/dataforge/] envelope format

## Installation 
Latest version on PyPi can be installed by command:

       pip3 install dfparser
       
To install latest version use:
   
       pip3 install https://github.com/kapot65/python-df-parser/archive/master.zip
       
## Build
To update protobuf formats use:

        cd configs && protoc rsb_event.proto  --python_out ../ && cd ..

(Protobuf 3.2.0+)[https://github.com/google/protobuf/releases] should be installed