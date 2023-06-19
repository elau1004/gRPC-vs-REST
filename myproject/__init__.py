# MIT License
#
# Copyright (C) 2023 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#
# Author        Changes On  Comment
# ------        ----------  -------
# E Lau         2020-03-28  Initial creation.
"""
The common initialization for all modules.
The following objects are made available:
    CaseInsensitiveDict - Case Insensitive dictionary.
    config              - The global configuration for all to use.
    get_logger()        - The global method to return a logger for all to use.
    get_db_session()    - The global SQLAlchemy DB session for you to connect to database.
"""

import  datetime
import  inspect
import  logging
import  os
import  sys
from    collections import UserDict
from    pathlib import Path
from    logging import Logger, Handler

import  yaml
from    dotenv  import load_dotenv ,find_dotenv

# Common Global constants.
#
__app__     = "myproject"
__author__  = "Edward Lau<elau1004@netscape.net>"
__version__ = "0.0.1"
__date__    = "Dec 15, 2019"    # Ported from ETLite.


class CaseInsensitiveDict( UserDict ):
    """
    Case insensitive key dictionary.
    """
    def __setitem__( self, key, value ):
        if  isinstance( key, str ):
            key = key.lower()
        super( CaseInsensitiveDict, self ).__setitem__( key, value )

    def __delitem__( self, key ) -> None:
        if  isinstance( key, str ):
            key = key.lower()
        super( CaseInsensitiveDict, self ).__delitem__( key )

    def __getitem__( self, key ):
        if  isinstance( key, str ):
            key = key.lower()
        return super( CaseInsensitiveDict, self ).__getitem__( key )

    def __contains__(self, key):
        if  isinstance( key, str ):
            key = key.lower()
        return key in self.data  # In parent calss.


# Clear out the temporary class objects.
del( UserDict )

# Common initialization section.
#

load_dotenv( find_dotenv() )    # The default does NOT overwrite. 
if 'RUN_ENV' in os.environ:
    RUN_ENV  =  os.environ['RUN_ENV']
else:
    print("\nThe environment variable RUN_ENV is not set.  Defaulting to: 'dev'\n")
    RUN_ENV = 'dev'

# TODO: Finish up the reading of config from the cloud for Non-development environment.
#       Default to local YAML for development.
#       Auto detect installed python modules.
#       Don't let the your IDE warning optics trip you out.
ycfg:dict = {}
# sys.modules are "import modules".  Are trying to detect install packages even though dring development they are all imported.
try:
    from infisical import InfisicalClient
except:
    try:
        from google.cloud import secretmanager
    except:
        try:
            import boto3    # AWS
        except:
            try:
                import oci  # Oracle
            except:
                # TODO: Default to local.
                pass

# TODO: Rework the structure since we have access to infisical.
path2yml = str( sorted( Path( os.getcwd()).glob( '**/*.yaml' )).pop())
with open( path2yml ) as fn:    
    ycfg = yaml.load( fn ,Loader=yaml.FullLoader )
    if  RUN_ENV  not in  ycfg:
        raise KeyError(f"Value '{RUN_ENV}' in variable RUN_ENV is not set in {path2yml} yaml file." )

# NOTE: Setup the global case insensitive key config to be shared.
config = CaseInsensitiveDict({'env': RUN_ENV })
for key in ycfg['global']:
    config[ key ] = ycfg['global'][ key ]
for key in ycfg[ RUN_ENV ]:
    config[ key ] = ycfg[ RUN_ENV ][ key ]

# Clear out the temporary variables and class objects.
del( RUN_ENV )
del( path2yml )
del( fn )
del( key )
del( ycfg )
del( yaml )
del( load_dotenv )
del( find_dotenv )


class MyLogger( logging.Logger ):
    """
    Custom logger to overwrite the makeRecord() method so that I will always have an IP address attribute.
    """
    MYIP:str = None

    def __init__( self, name, level=logging.NOTSET ):
        super().__init__( name ,level )        
        # Set the static class my IP variable.
        if  MyLogger.MYIP is None:
            import socket
            MyLogger.MYIP = ''.join([hex(int(g)).removeprefix('0x').zfill(2).capitalize() for g in socket.gethostbyname( socket.gethostname() ).split('.')])

    # Overwrite this method to default extra variables for formatting log messages.
    def makeRecord( self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None ):
        if  not extra:
            extra={'myip': None}
        if  extra['myip']  is None:
            extra['myip']  =  MyLogger.MYIP

        return super().makeRecord( name, level, fn, lno, msg, args, exc_info, func, extra, sinfo )


# Common routines section.
#
logging.setLoggerClass( MyLogger )

def get_logger(
        name:str=None,
        log_pathname:str=None,
        err_pathname:str=None,
        msg_format:str=None,
        asc_format:str=None,
        log_level:str=None,
    ) -> Logger:
    """
    Return a global standardized logger for you to log your messages.
    
    Args:
        name        - Name for this logger.  Default to the name of the calling module.
        log_pathname- Full path name to the log file.
        err_pathname- Full path name to the err file.
        msg_format  - The logger message format.  Default to "%(asctime)s.%(msecs)03d (%(process)d.%(thread)05d)[%(levelname)s %(name)s] %(message)s".
        asc_format  - The timestamp format to be used during logging.  Default is "%Y%m%d %H%M%S"
        log_level   - Set the logger level.  Default to INFO.
    Return:
        Logger
    """
    if  not name:
        # Get the name of the caller and NOT this module.
        name = inspect.getmodulename( inspect.stack()[1][1] )

    logger = logging.getLogger( name )
    if logger.hasHandlers():
        # Was previously setup and cached by the Python logger.
        return logger

    # Continue to intialize the new logger.
    if  not log_level:
        if 'LOG_LEVEL' in os.environ:
            log_level  =  os.environ['LOG_LEVEL']
        else:
            if 'log_level' in config['logger']:
                log_level  =  config['logger']['log_level']
            else:
                log_level  = logging.INFO
    if  not log_pathname:
        if 'log_pathname' in config['logger']:
            log_pathname = config['logger']['log_pathname']
            if  log_pathname:
                log_pathname = datetime.datetime.utcnow().strftime( log_pathname )
    if  not err_pathname:
        if 'err_pathname' in config['logger']:
            err_pathname = config['logger']['err_pathname']
            if  err_pathname:
                err_pathname = datetime.datetime.utcnow().strftime( err_pathname )
    if  not asc_format:
        if 'asc_format' in config['logger']:
            asc_format  =  config['logger']['asc_format']
        else:
            asc_format  =  "%Y%m%d%a %H%M%S.%f"
    if  not msg_format:
        if 'msg_format' in config['logger']:
            msg_format  =  config['logger']['msg_format']
        else:
            msg_format  = "%(asctime)s.%(msecs)03d (%(myip)s.%(process)d.%(thread)05d)[%(levelname)s %(module)s] %(message)s"

    logger.setLevel( log_level )
    log_formatter = logging.Formatter( msg_format ,datefmt=asc_format ,defaults={} )

    if 'TERM' in os.environ or ('SESSIONNAME' in os.environ and os.environ['SESSIONNAME'] == 'Console'):
        # NOTE: We are NOT running in the background therefore spool to console.
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter( log_formatter )
        logger.addHandler( stream_handler )

    if  'CLOUD_CONFIG_URL' in os.environ and os.environ['CLOUD_CONFIG_URL']:
        # TODO: Finish up the cloud logger handler.
        #       "Auto" detect install python modules.
        cloud_handle:Handler = logging.NullHandler()
        # TODO: Check out https://www.papertrail.com/
        try:
            from google.cloud import logging as cloud_logging
        except:
            try:
                import boto3
            except:
                try:
                    import oci
                except:
                    pass

        logger.addHandler( cloud_handle )
    else:
        # TODO: Implement log rotation.
        # SEE:  https://www.blog.pythonlibrary.org/2014/02/11/python-how-to-create-rotating-logs/

        if  log_pathname:
            Path( os.path.dirname( log_pathname )).mkdir( parents=True ,exist_ok=True )
            file_log_handler=logging.FileHandler( log_pathname ,mode='a' )
            file_log_handler.setFormatter( log_formatter )
            logger.addHandler( file_log_handler )

        if  err_pathname:
            Path( os.path.dirname( err_pathname )).mkdir( parents=True ,exist_ok=True )
            file_err_handler=logging.FileHandler( err_pathname ,mode='a' )
            file_err_handler.setFormatter( log_formatter )
            file_err_handler.setLevel( logging.ERROR )
            logger.addHandler( file_err_handler )

    # NOTE: Keep the level name length fixed so that the log line before the message is consistent.
    logging._levelToName = {
        logging.CRITICAL: 'CRIT',   # 50
        logging.ERROR: 'ERR ',      # 40
        logging.WARNING: 'WARN',    # 30
        logging.INFO: 'INFO',       # 20
        logging.DEBUG: 'DBUG',      # 10
        logging.NOTSET: 'NOTSET',   # 00
    }
    return logger


def get_db_session(name:str = None) -> object:
    """
    Return a SQLAlchemy session.  All information need to instantiate a session is the root config dict.

    Args:
        None
    Return:
        Session
    """
    # TODO: Finish this up.
    return None
