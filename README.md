# Test Conclusion

## Overview
This section presents the conclusions drawn from the tests conducted on gRPC and REST.

## Environment setup
The following are the commands to setup this project.
```
pip    install -U pip
pip    install pipenv
git    clone   https://github.com/elau1004/gRPC-vs-REST.git
pipenv sync
```

## Test setup
The tests are ran with the following combinations of options:
* **Protocol**: `HTTP/1` ,`HTTP/2`
* **Data Size**: `full` <small>(~1.1Kb)</small> ,`small` <small>(~9.9Kb)</small> ,`medium` <small>(~107Kb)</small> ,`large` <small>(~1.1Mb)</small> ,`huge` <small>(~11Mb)</small>
* **Compression**: `None` ,`gzip` , `br` ,`zstd`

with the following command:
```
python  restful_client.py  -i 1000  -p ppp  -s sss  -c ccc
```

where the command line options are:
|Option|Default|Description|
|------|:-----:|:----------|
| `-i` | 100   |Number of request to make to the server.|
| `-p` | `http`|The protocol to use. [`http` ,`https`]| 
| `-s` | `full`|The size of the data message to respond back by the server. [`full` ,`small` ,`medium` ,`large` ,`huge`]| 
| `-c` | *None*|Compression algorithm to use. [`br` ,`gzip` ,`zstd`]| 

Depending on which protocol to be used, the server need to be started with different CLI option.

When testing with protocol HTTP/**1**, the server need to be started with the following command:
```
hypercorn  restful_server:app
```

When testing with protocol HTTP/**2**, first you need to generate the security key and certificate.  The following command can be used to generate these files:
```
openssl req -x509 -newkey rsa:4096 -sha256 -days 5000 -nodes -keyout key.pem -out cert.pem -subj "/CN=example.com"  -addext "subjectAltName=DNS:example.com,DNS:*.example.com,IP:10.0.0.1"
```

Once both `key.pem` and `cert.pem` are generated, the server need to be started with the following command:
```
hypercorn  --keyfile key.pem  --certfile cert.pem  restful_server:app
```

## Test Results
The following is the result of the average response time for each of the above mentioned combination of options.

### REST with serializing text into JSON
|Protocol|Size  |Compression|Avg Resp|Comment|
|:-------|:-----|:----------|-------:|:------|
| http/1 |full  |           |  0.77 ms|       |
| http/1 |full  | gzip      |  0.77 ms|       |
| http/1 |full  | brotli    |  0.75 ms|       |
| http/1 |full  | zstd      |  0.78 ms|       |
| http/1 |small |           |  0.97 ms|       |
| http/1 |small | gzip      |  1.07 ms|       |
| http/1 |small | brotli    |  0.95 ms|       |
| http/1 |small | zstd      |  0.92 ms|       |
| http/1 |medium|           |  2.92 ms|       |
| http/1 |medium| gzip      |  5.95 ms|       |
| http/1 |medium| brotli    |  2.91 ms|       |
| http/1 |medium| zstd      |  2.41 ms|       |
| http/1 |large |           | 22.91 ms|       |
| http/1 |large | gzip      | 59.99 ms|       |
| http/1 |large | brotli    | 23.09 ms|       |
| http/1 |large | zstd      | 19.55 ms|       |
| http/1 |huge  |           | 45.90 ms|       |
| http/1 |huge  | gzip      |120.94 ms|       |
| http/1 |huge  | brotli    | 46.21 ms|       |
| http/1 |huge  | zstd      | 39.14 ms|       |
|        |      |           |        |       |
| http/2 |full  |           |  0.89 ms|       |
| http/2 |full  | gzip      |  0.88 ms|       |
| http/2 |full  | brotli    |  0.85 ms|       |
| http/2 |full  | zstd      |  0.90 ms|       |
| http/2 |small |           |  1.11 ms|       |
| http/2 |small | gzip      |  1.21 ms|       |
| http/2 |small | brotli    |  1.08 ms|       |
| http/2 |small | zstd      |  1.05 ms|       |
| http/2 |medium|           |  3.11 ms|       |
| http/2 |medium| gzip      |  6.16 ms|       |
| http/2 |medium| brotli    |  3.09 ms|       |
| http/2 |medium| zstd      |  2.59 ms|       |
| http/2 |large |           | 23.67 ms|       |
| http/2 |large | gzip      | 60.29 ms|       |
| http/2 |large | brotli    | 23.66 ms|       |
| http/2 |large | zstd      | 20.01 ms|       |
| http/2 |huge  |           | 46.62 ms|       |
| http/2 |huge  | gzip      |122.21 ms|       |
| http/2 |huge  | brotli    | 47.03 ms|       |
| http/2 |huge  | zstd      | 40.35 ms|       |

#### REST conclusion
* 
* 

### gRPC with serializing protobuf into JSON
|Protocol|Size  |Compression|Avg Resp|Comment|
|:-------|:-----|:----------|-------:|:------|
| http/2 |full  |           |        |       |
| http/2 |full  | deflate   |        |       |
| http/2 |full  | gzip      |        |       |
| http/2 |small |           |        |       |
| http/2 |small | deflate   |        |       |
| http/2 |small | gzip      |        |       |
| http/2 |medium|           |        |       |
| http/2 |medium| deflate   |        |       |
| http/2 |medium| gzip      |        |       |
| http/2 |large |           |        |       |
| http/2 |large | deflate   |        |       |
| http/2 |large | gzip      |        |       |
| http/2 |huge  |           |        |       |
| http/2 |huge  | deflate   |        |       |
| http/2 |huge  | gzip      |        |       |

#### gRPC conclusion
* 
* 

## Conclusion
Summarize the key findings from the test results and provide recommendations based on the performance, resource utilization, and scalability of gRPC and REST.
