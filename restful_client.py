"""
The RESTful client to request data from the server.
"""
import argparse
import time

import httpx    # Support HTTP/2

parser = argparse.ArgumentParser(description='Request JSON data from the RESTful server.')

parser.add_argument('-c',dest='comp'  ,type=str ,default='none' ,choices=['none' ,'brotli' ,'deflate' ,'gzip' ,'zstd']
                        ,help="compression to be used by server.  Default is 'none'.")
parser.add_argument('-i',dest='iter'  ,type=int ,default= 10
                        ,help="request iterations to make to the server.  Default is 100.")
parser.add_argument('-H',dest='host'  ,type=str ,default='127.0.0.1:8000'
                        ,help="host server to request from.  Default is '127.0.0.1:8000'.")
parser.add_argument('-l',dest='logf'  ,type=str ,default='logs/restful_client.log'
                        ,help="filename to log into.  Default is 'logs/restful_client.log'.")
parser.add_argument('-s',dest='size'  ,type=str ,default='full' ,choices=['full' ,'small' ,'medium' ,'large' ,'huge']
                        ,help="size of the data.  Default is 'full'.")
args = parser.parse_args()

# Methods

ONE_NANO_SEC = 1_000_000_000

def run_id() -> int:
    return  time.time_ns()

def run_token() -> str:
    # 1 sec == 1,000 ms == 1,000,000 us == 1,000,000,000 ns
    _id = run_id()
    return f"[{time.strftime('%M:%S', time.gmtime( _id // ONE_NANO_SEC ))}.{_id % ONE_NANO_SEC:0<9}]"


# Main section
ttl_nano_sec: int = 0
min_nano_sec: int = ONE_NANO_SEC
max_nano_sec: int = 0
headers = {}  if args.comp != 'none' else {'Accept-Encoding': args.comp }

with open( args.logf ,'a') as file: # Python has a 8K buffer.
    file.write(f'{time.time_ns():9}\t0 Client Bgn\t{args}\n')

    with  httpx.Client( base_url=f'http://{args.host}', headers=headers ,http2=True ) as client:
        for i in  range( args.iter ):
            runtoken = run_token()
            bgn_nano_sec = time.time_ns()
            file.write(f'{time.time_ns():9}\t1 Client Req\t{runtoken}\n')

#           r = client.get( '/patients/3' )
            r = client.get(f'/patients/?runtoken={runtoken}&datasize={args.size}')

            elp_nano_sec = time.time_ns() - bgn_nano_sec
            elp_msec     = elp_nano_sec   / 1_000_000.0 # Convert nano into milli second.
            file.write(f'{time.time_ns():19}\t7 Client Rcv\t{runtoken}\t{r.num_bytes_downloaded:>8} bytes in {elp_msec:7.2f}ms over {r.http_version}\n')

            ttl_nano_sec+= elp_nano_sec
            if  min_nano_sec > elp_nano_sec:
                min_nano_sec = elp_nano_sec
            if  max_nano_sec < elp_nano_sec:
                max_nano_sec = elp_nano_sec

    file.write(f'{time.time_ns():9}\t9 Client End\tMin: {min_nano_sec/1_000_000.0:>5.2f}ms  Avg: {ttl_nano_sec/1_000_000.0/args.iter:>5.2f}ms  Max: {max_nano_sec/1_000_000.0:>5.2f}ms\n')
