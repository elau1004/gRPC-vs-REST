"""
The RESTful client to request data from the server.
"""
import argparse
import os
import time

import httpx    # Support HTTP/2
import orjson

parser = argparse.ArgumentParser(description='Request JSON data from the RESTful server.')

parser.add_argument('-c',dest='comp'    ,type=str ,default='none' ,choices=['none' ,'br' ,'gzip' ,'zstd']
                        ,help="compression to be used by server.  Default is 'none'.")
parser.add_argument('-i',dest='iter'    ,type=int ,default= 100
                        ,help="request iterations to make to the server.  Default is 100.")
parser.add_argument('-H',dest='host'    ,type=str ,default='127.0.0.1:8000'
                        ,help="host server to request from.  Default is '127.0.0.1:8000'.")
parser.add_argument('-l',dest='logf'    ,type=str ,default='logs/restful_client.log'
                        ,help="filename to log into.  Default is 'logs/restful_client.log'.")
parser.add_argument('-s',dest='size'    ,type=str ,default='full' ,choices=['full' ,'small' ,'medium' ,'large' ,'huge']
                        ,help="size of the data.  Default is 'full'.")
parser.add_argument('-p',dest='proto'   ,type=str ,default='http' ,choices=['http' ,'https']
                        ,help="protocol to use.  Default is 'http/1'.")
parser.add_argument('-u',dest='url'     ,type=str
                        ,help="base url to use.")
args = parser.parse_args()

# HTTP/1 testing.
# Server:
#   hypercorn restful_server:app --reload
#
# Client:
#   python restful_client.py -s medium         # No     compression
#   python restful_client.py -s medium -c br   # Brotli compression
#   python restful_client.py -s medium -c gzip # Gzip   compression
#   python restful_client.py -s medium -c zstd # Zstd   compression
#
# Browser:
#   http://127.0.0.1:8000/patients/?datasize=medium
#
# HTTP/2 testing.
# Server:
#   hypercorn restful_server:app --reload --keyfile key.pem --certfile cert.pem 
#
# Client:
#   python restful_client.py -p https -s medium         # No     compression
#   python restful_client.py -p https -s medium -c br   # Brotli compression
#   python restful_client.py -p https -s medium -c gzip # Gzip   compression
#   python restful_client.py -p https -s medium -c zstd # Zstd   compression
#
# Browser:
#   https://127.0.0.1:8000/patients/?datasize=medium

# Methods

ONE_NANO_SEC = 1_000_000_000

def run_id() -> int:
    return  time.time_ns()

def run_token() -> str:
    # 1 sec == 1,000 ms == 1,000,000 us == 1,000,000,000 ns
    _id = run_id()
    return f"[{time.strftime('%M:%S', time.gmtime( _id // ONE_NANO_SEC ))}.{_id % ONE_NANO_SEC:0<9}]"


# Main section
ttl_bytes:    int = 0
ttl_chars:    int = 0
ttl_nano_sec: int = 0
min_nano_sec: int = ONE_NANO_SEC
max_nano_sec: int = 0
headers = {}  if args.comp == 'none' else {'Accept-Encoding': args.comp }

os.makedirs( os.path.dirname( args.logf ) ,exist_ok=True )
with open( args.logf ,'a') as file: # Python has a 8K buffer.
#   file.write( f'{time.time_ns():9}\t0 Client Bgn\t{args}\n')
    print(      f'{time.time_ns():9}\t0 Client Bgn\t{args}')

    base_url = args.url if args.url else f'{args.proto}://{args.host}'
    with  httpx.Client( base_url=base_url ,headers=headers ,http2=True ,verify=False) as client:
        for i in  range( args.iter ):
            runtoken = run_token()
#           file.write( f'{time.time_ns():9}\t1 Client Req\t{runtoken}\n')
            bgn_nano_sec = time.perf_counter_ns()

            # Request the data from the server.
#           r = client.get( '/patients/3' )
            r = client.get(f'/patients/?runtoken={runtoken}&datasize={args.size}')

            # Calculate the time taken to receive the data.
            elp_nano_sec = time.perf_counter_ns() - bgn_nano_sec
            elp_msec     = elp_nano_sec   / 1_000_000.0 # Convert nano into milli second.
            file.write( f'{time.time_ns():19}\t7 Client Rcv\t{runtoken}\tRcv {r.num_bytes_downloaded:>8} bytes in {elp_msec:7.3f} ms over  {r.http_version}\n')

            # Accumulate the statistics.
            ttl_bytes   += r.num_bytes_downloaded
            ttl_chars   += len(r.text)
            ttl_nano_sec+= elp_nano_sec
            if  min_nano_sec > elp_nano_sec:
                min_nano_sec = elp_nano_sec
            if  max_nano_sec < elp_nano_sec:
                max_nano_sec = elp_nano_sec

            # Serialize the JSON data.
            bgn_nano_sec = time.perf_counter_ns()
            _ = orjson.loads( r.text )
            elp_nano_sec = time.perf_counter_ns() - bgn_nano_sec
            elp_msc1     = elp_msec if elp_msec > 0 else 0.0001
            elp_msec     = elp_nano_sec   / 1_000_000.0 # Convert nano into millisecond.
#           file.write( f'{time.time_ns():19}\t8 Client Rcv\t{runtoken}\tJsn {len(r.text):>8} bytes in {elp_msec:7.3f} ms ({(len(r.text)/r.num_bytes_downloaded):3.2f} S  {(elp_msec/elp_msc1):3.2f} J)\n')

#   file.write( f'{time.time_ns():9}\t9 Client End\tMin: {min_nano_sec/1_000_000.0:>5.2f}ms  Avg: {ttl_nano_sec/1_000_000.0/args.iter:>5.2f}ms  Max: {max_nano_sec/1_000_000.0:>6.2f}ms  Size: {ttl_chars/(i+1)}b  Trnf: {ttl_bytes/(i+1)}b\n')
    print(      f'{time.time_ns():9}\t9 Client End\tMin: {min_nano_sec/1_000_000.0:>5.2f}ms  Avg: {ttl_nano_sec/1_000_000.0/args.iter:>5.2f}ms  Max: {max_nano_sec/1_000_000.0:>6.2f}ms  Size: {ttl_chars/(i+1)}b  Trnf: {ttl_bytes/(i+1)}b\n')
