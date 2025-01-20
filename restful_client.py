"""
The RESTful client to request data from the server.
"""
import argparse
import requests
import time

#import httpx

parser = argparse.ArgumentParser(description='Request JSON data from the RESTful server.')  

parser.add_argument('-C',dest='comp'  ,type=str ,default='none' ,choices=['none' ,'brotli' ,'deflate' ,'gzip' ,'zstd'] 
                        ,help="compression to be used by server.  Default is 'none'.")  
parser.add_argument('-I',dest='iter'  ,type=int ,default= 100
                        ,help="request iterations to make to the server.  Default is 100.")
parser.add_argument('-H',dest='host'  ,type=str ,default='127.0.0.1:8000'
                        ,help="host server to request from.  Default is '127.0.0.1:8000'.")  
parser.add_argument('-L',dest='logf'  ,type=str ,default='client.log'
                        ,help="filename to log into.  Default is 'client.log'.")  
parser.add_argument('-S',dest='size'  ,type=str ,default='full' ,choices=['full' ,'small' ,'medium' ,'large' ,'huge']
                        ,help="size of the data.  Default is 'full'.")
args = parser.parse_args()  


# Methods

ONE_NANO_SEC = 1_000_000_000

def run_id() -> int:
    return  time.time_ns()
 
def run_token() -> str:
    run_id = run_id()
    return f"{time.strftime('%H.%M:%S') ,time.gmtime( run_id // ONE_NANO_SEC )}.{run_id % ONE_NANO_SEC:0<9}"


# Main section


with open('result.txt', 'w') as file:
    ttl_nano_sec: int = 0
    headers = {}  if  args.comp != 'none' else {'Accept-Encoding': args.comp }

    file.write(f'{time.time_ns():9}\t{run_id}\tClient Bgn\t{args}')

    for i in  range( iter ):
        runtoken = run_token()
        file.write(f'{run_id():9}\t{run_id}\tClient Req')

        bgn_nano_sec = time.time_ns()
        response = requests.get( f'{args.host}/patient?runtoken={runtoken}&datasize={args.size}' ,headers=headers )

#       file.write(f'{time.time_ns():9}\t{run_id}\tServer Rcv')
#       file.write(f'{time.time_ns():9}\t{run_id}\tServer Rsp')

        elp_nano_sec = time.time_ns() - bgn_nano_sec
        ttl_nano_sec+= elp_nano_sec
        file.write(f'{run_id():9}\t{run_id}\tClient Rcv\t{response.content:>7} bytes\t{elp_nano_sec} ns')

    file.write(f'{run_id():9}\t{run_id}\tClient End\tAvg elapsed: {ttl_nano_sec/iter} ns ,Ttl elapsed: {ttl_nano_sec} ns')
