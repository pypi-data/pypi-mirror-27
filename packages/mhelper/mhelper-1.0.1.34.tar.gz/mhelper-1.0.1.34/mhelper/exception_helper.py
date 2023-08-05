import subprocess
import traceback
from typing import Iterable, Union

import itertools


def add_details( exception: Exception, **kwargs ) -> None:
    args = list( exception.args )
    
    message = create_details_message( **kwargs )
    
    if len( args ) > 0 and isinstance( args[0], str ):
        args[0] += message
    else:
        args.append( message )
    
    exception.args = tuple( args )


def create_details_message( **kwargs ):
    from mhelper import string_helper
    
    result = [""]
    
    lk = 1
    lt = 1
    
    for k, v in kwargs.items():
        lk = max( len( str( k ) ), lk )
        lt = max( len( string_helper.type_name( v ) ), lt )
    
    for k, v in kwargs.items():
        result.append( "--> {0} ({1}) = «{2}»".format( str( k ).ljust( lk ), string_helper.type_name( v ).ljust( lt ), v ) )
    
    return "\n".join( result )


def assert_type( name, value, type ):
    if not isinstance( value, type ):
        from mhelper.string_helper import type_name
        raise TypeError( "`{0}` should be of type `{1}`, but it is a `{2}` with value `{3}`.".format( name, type.__name__, type_name( value ), value ) )


def exception_to_string( ex: BaseException ):
    result = []
    
    while ex:
        result.append( str( ex ) )
        ex = ex.__cause__
    
    return "\n---CAUSED BY---\n".join( result )


class NotSupportedError( Exception ):
    """
    Since `NotImplementedError` looks like an abstract-base-class error to the IDE you can use `NotSupportedError` if desired.
    """
    pass


class ImplementationError( Exception ):
    pass


class LogicError( Exception ):
    pass


class NotFoundError( Exception ):
    pass


class SwitchError( Exception ):
    def __init__( self, name, value, *, instance = False, details = None ):
        if details is not None:
            details = " Further details: {}".format( details )
        
        if instance:
            super().__init__( "The switch on the type of «{}» does not recognise the value «{}» of type «{}».{}".format( name, value, type( value ), details ) )
        else:
            super().__init__( "The switch on «{}» does not recognise the value «{}» of type «{}».{}".format( name, value, type( value ), details ) )


class SubprocessError( Exception ):
    pass


def run_subprocess( command ):
    status = subprocess.call( command, shell = True )
    
    if status:
        raise SubprocessError( "The command «{}» exited with error code {}. If available, checking the console output may provide more details.".format( command, status ) )


TType = Union[type, Iterable[type]]


def format_types( type_: TType ) -> str:
    if isinstance( type_, type ):
        return str( type_ )
    else:
        from mhelper import string_helper
        return string_helper.join_ex( type_, delimiter = ", ", last_delimiter = " or ", formatter = "«{}»" )


def assert_instance( name: str, value: object, type_: TType ):
    if isinstance( type_, type ):
        type_ = (type_,)
    
    if not any( isinstance( value, x ) for x in type_ ):
        raise TypeError( instance_message( name, value, type_ ) )


def assert_instance_or_none( name: str, value: object, type_: type ):
    if isinstance( type_, type ):
        type_ = (type_,)
    
    type_ = list( itertools.chain( type_, (type( None ),) ) )
    
    assert_type( name, value, type_ )


def instance_message( name: str, value: object, type_: TType ):
    return "The value of «{}», which is «{}», should be of type {}, but it's not, it's a «{}».".format( name, value, format_types( type_ ), type( value ) )


def full_traceback():
    return "**** Handler Traceback ****\n" + current_stack_text() + "\n**** Error traceback ****\n" + traceback.format_exc()


def current_stack_text():
    return "\n".join( x.strip() for x in traceback.format_stack() )


def type_error( name, value, type_: TType ):
    raise TypeError( instance_message( name, value, type_ ) )
