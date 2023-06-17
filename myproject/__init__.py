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
    cfg           - The global configuraiton for all to use.
    RUN_ENV       - The global variable to indicate the runtime environment.  e.g. 'dev' ,'cicd' ,'test' ,stg' ,'qa' ,'prod'.
    get_logger()  - The global method to return a logger for all to use.
"""

import  datetime
import  inspect
import  logging
import  os
import  sys
from    pathlib import Path
from    logging import Logger

import  yaml
from    dotenv  import load_dotenv ,find_dotenv

# Common Global constants.
#
__app__     = "myexample"
__author__  = "Edward Lau<elau1004@netscape.net>"
__version__ = "0.0.1"
__date__    = "Dec 15, 2019"    # Ported from ETLite.

# Common initialization section.
#

load_dotenv( find_dotenv() )    # The default does NOT overwrite. 
if 'RUN_ENV' in os.environ:
    RUN_ENV  =  os.environ['RUN_ENV']
else:
    raise KeyError( "The environment variable RUN_ENV is not set.  Try: 'dev' ,'cicd' ,'test' ,stg' ,'qa' ,'prod'." )

# TODO: Finish up the reading of config from the cloud for Non-development environment.
#       Default to local YAML for development.
#       Auto detect installed python modules.
cloud_handle = None
try:
    from infisical import InfisicalClient
except:
    try:
        import hvac     # HashiCorp Vault
    except:
        try:
            from google.cloud import secretmanager
        except:
            try:
                import boto3    # AWS
            except:
                try:
                    from azure.keyvault.secrets import SecretClient
                except:
                    try:
                        import oci  # Oracle
                    except:
                        # TODO: Default to local.
                        pass

path2yml = str( sorted( Path( os.getcwd()).glob( '**/*.yaml' )).pop())
with open( path2yml ) as fn:    
    ycfg = yaml.load( fn ,Loader=yaml.FullLoader )
    if  RUN_ENV  not in  ycfg:
        raise KeyError(f"Value '{RUN_ENV}' in variable RUN_ENV is not set in {path2yml} yaml file." )

# NOTE: Setup the global config to be shared.
config = {'env': RUN_ENV }
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
    Custom logger to overwrite the makeRecord() method so that I wil lalways have an IP address attribute.
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
logging.setLoggerClass(MyLogger)

def get_logger(
        name:str=None,
        log_pathname:str=None,
        err_pathname:str=None,
        log_dir:str=None,
        log_group:str=None,
        msg_format:str=None,
        dtm_format:str=None,
        log_level:str=None
    ) -> Logger:
    """
    Return a global standardized logger for you to log your messages.
    
    Args:
        name        - Name for this logger.  Default to the name of the calling module.
        log_pathname- Full path name to the log file.  Will default timestamp into the name.
        err_pathname- Full path name to the err file.  Will default timestamp into the name.
        log_dir     - The root directory for collecting the logs.  Default to 'logs' in your home direcory.
        log_group   - The grouping sub-directory to further organize logs under.  Default is "."
        msg_format  - The logger message format.  Default to "%(asctime)s.%(msecs)03d (%(process)d.%(thread)05d)[%(levelname)s %(name)s] %(message)s".
        dtm_format  - The timestamp format to be used during logging.  Default is "%Y%m%d %H%M%S.%f"
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

    if  not log_level:
        if 'LOG_LEVEL' in os.environ:
            log_level  =  os.environ['LOG_LEVEL']
        else:
            if 'log_level' in config['logger']:
                log_level  =  config['logger']['log_level']
            else:
                log_level  = logging.INFO
    if  not log_dir:
        if 'log_dir' in config['logger']:
            log_dir  =  config['logger']['log_dir']
        else:
            if  sys.platform.find('win') == 0:
                home = os.environ['HOMEPATH']
            else:
                home = os.environ['HOME']
            log_dir  = os.path.join( home ,'logs' ) 
    if  not log_group:
        if 'log_group' in config['logger']:
            log_group  =  config['logger']['log_group']
        else:
            log_group = '.'
    if  not dtm_format:
        if 'dtm_format' in config['logger']:
            dtm_format  =  config['logger']['dtm_format']
        else:
            dtm_format  =  "%Y%m%d%a %H%M%S.%f"
    if  not msg_format:
        if 'msg_format' in config['logger']:
            msg_format  =  config['logger']['msg_format']
        else:
            msg_format  = "%(asctime)s.%(msecs)03d (%(myip)s.%(process)d.%(thread)05d)[%(levelname)s %(module)s] %(message)s"

    logger.setLevel( log_level )
    log_fragment = datetime.datetime.utcnow().strftime( config['logger']['log_fragment'] )
    log_formatter = logging.Formatter( msg_format ,datefmt=dtm_format ,defaults={} )

    if 'TERM' in os.environ or ('SESSIONNAME' in os.environ and os.environ['SESSIONNAME'] == 'Console'):
        # NOTE: We are NOT running in the background therefore spool to console.
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter( log_formatter )
        logger.addHandler( stream_handler )

    if  'CLOUD_CONFIG_URL' in os.environ and os.environ['CLOUD_CONFIG_URL']:
        # TODO: Finish up the cloud logger handler.
        #       "Auto" detect install python modules.
        cloud_handle = logging.NullHandler()
        try:
            from google.cloud import logging as cloud_logging
        except:
            try:
                import boto3
            except:
                try:
                    from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
                except:
                    try:
                        import oci
                    except:
                        pass

        logger.addHandler( cloud_handle )
    else:
        # TODO: Implement log rotation.
        # SEE:  https://www.blog.pythonlibrary.org/2014/02/11/python-how-to-create-rotating-logs/

        # Set up the file handler.
        if  log_pathname:
            log_pathname = os.path.join( log_dir ,log_group ,name +'_' +log_fragment +'.log' ) 
        else:
            # TODO: Check config.  If configured build the log_pathanme.
            pass

        if  log_pathname:
            Path( os.path.dirname( log_pathname )).mkdir( parents=True ,exist_ok=True )

            file_info_handler=logging.FileHandler( log_pathname ,mode='a' )
            file_info_handler.setFormatter( log_formatter )
            logger.addHandler( file_info_handler )

        # Set up the err handler.
        if  err_pathname:
            err_pathname = os.path.join( log_dir ,log_group ,name +'_' +log_fragment +'.err' ) 
        else:
            # TODO: Check config.  If configured build the log_pathanme.
            pass

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


def get_db_session() -> object:
    """
    Return a SQLAlchemy session.  All information need to instantiate a session is the root config dict.

    Args:
        None
    Return:
        Session
    """
    # TODO: Finish this up.
    return None
