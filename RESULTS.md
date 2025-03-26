# Results collected from our testing
## Hardware ran on
The following is the result of the average response time for each of the above mentioned combination of options.

```
Lenovo T490s laptop                 Air Mac                     AWS EC2
    O/S:    Windows 11 Pro              O/S:    iOS                 O/S:    Linux
    CPU:    Intel i5-8365, 4 cores      CPU:    M2, 8 cores         CPU:    
    Clock:  1.6 GHz - 4.80 GHz          Clock:  2.4 GHz - 3.5 GHz   Clock:  
    RAM:    16 Gib                      RAM:    16 Gib              RAM:    
```
* On our test laptops:
    * Both anti virus scan and network are disabled.
    * The battery charger is plugged in.

## Test setup
The tests are ran with the following combinations of options:
* **Protocol**: `HTTP/1` ,`HTTP/2`
* **Data Size**: `full` <small>(~1Kb)</small> ,`small` <small>(~8Kb)</small> ,`medium` <small>(~32Kb)</small> ,`large` <small>(~135Kb)</small> ,`huge` <small>(~1Mb)</small>
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
| `-c` | `none`|Compression algorithm to use. [`none` ,`br` ,`gzip` ,`zstd`]| 

Depending on which protocol to be used, the server need to be started with different CLI option.

When testing with protocol HTTP/**1**, the server need to be started with the following command:
```
hypercorn  restful_server:app
```

When testing with protocol HTTP/**2**, first you need to generate the security key and certificate.  Most major web browser only support HTTP/**2** over encrypted connection, making encryption essentially mandatory.  The following command can be used to generate these files:
```
openssl req -x509 -newkey rsa:4096 -sha256 -days 5000 -nodes -keyout key.pem -out cert.pem \
            -subj "/CN=example.com" -addext "subjectAltName=DNS:example.com,DNS:*.example.com,IP:10.0.0.1"
```

Once both `key.pem` and `cert.pem` are generated, the server need to be started with the following command:
```batch
::  Windows
SET COMPRESSION_LEVEL=5
hypercorn  --keyfile key.pem  --certfile cert.pem  restful_server:app
```

You could run the server app in either 2 different terminals to listen on different ports for different protocol or run them in the background and manage them yourself.
```bash
#   Bash
export  COMPRESSION_LEVEL=5
hypercorn  restful_server:app --bind 0.0.0.0:8000 &
hypercorn  restful_server:app --bind 0.0.0.0:8443 --keyfile key.pem --certfile cert.pem &
```

### Terminal script used to run the test:
You should test both `HTTP/1` and `HTTP/2` as close to each other to yield results that are closer together in time.
```batch
:: Windows with 2 instances of the restful server.
for %s in ( full small medium large huge ) do (
    for %c in ( none br gzip zstd ) do (
        for %u in ( http://127.0.0.1:8000  https://127.0.0.1:8443 ) do (
            for %i in ( 1 2 3 ) do (
                @del   logs\*.log
                python restful_client.py -i 1000 -s %s -c %c -u %u  ))))
```
```bash
#  Bash with 2 instances of the restful server.
for s in full small medium large huge; do {
    for c in  none  br gzip zstd; do {
        for u in  'http://127.0.0.1:8000'  'https://127.0.0.1:8443'; do {
            for i  in 1 2 3; do {
                rm      logs/*.log
                echo    restful_client.py -i 1000 -s $s -c $c -u $u
                python  restful_client.py -i 1000 -s $s -c $c -u $u
            };  done
        };  done
    };  done
};  done
```

* For each combination, we run it three times and pick the middle number.
* The compression level is manually changed in the `restful_server.py` script.


### RESTful JSON data serialized into Python dictionary
|Caption      | Description|
|:------------|:-----------|
| Lvl         | Compression level. [1-9]|
| Size        | Size of the requested JSON data. `full` <small>(~1Kb)</small> ,`small` <small>(~8Kb)</small> ,`medium` <small>(~32Kb)</small> ,`large` <small>(~135Kb)</small> ,`huge` <small>(~1Mb)</small>|
| Compression | The type of compression used.  `none` ,`br` , `gzip` ,`zstd`|
| Msg Size    | The uncompress message size.|
| Trf Size    | The transferred message size.|
| Ratio       | The compression ration.|
| Win H1      | Tested on Windows 11 using `HTTP/1.1` measured in ms.|
| Win H2      | Tested on Windows 11 using `HTTP/2` measured in ms.|
| Win H3      | Tested on Windows 11 using `HTTP/3` measured in ms.|
| AWS H1      | Tested in the cloud using `HTTP/1.1` measured in ms.|
| AWS H2      | Tested in the cloud using `HTTP/2` measured in ms.|
| AWS H3      | Tested in the cloud using `HTTP/3` measured in ms.|

|Lvl|Size  |Compression|Msg Size|Tfr Size|Ratio|  Win H1|  Win H2|  GCP H1| GCP H2|
|:-:|:-----|:----------|-------:|-------:|----:|-------:|-------:|-------:|------:|
|   |full  |           |     972|     972|    0|    8.36|    8.37|   20.78|  22.33|
| 3 |full  | br        |     972|     505| 1.92|    2.79|    2.96|   20.56|  20.86|
| 3 |full  | gzip      |     972|     527| 1.84|    2.86|    3.21|   19.76|  21.65|
| 3 |full  | zstd      |     972|     518| 1.88|    3.15|    3.50|   19.73|  21.29|
|   |small |           |    7649|    7649|    0|    8.07|    9.56|   25.12|  23.51|
| 3 |small | br        |    7649|    2322| 3.29|    3.17|    4.91|   20.00|  22.10|
| 3 |small | gzip      |    7649|    2464| 3.10|    3.12|    4.86|   20.43|  21.85|
| 3 |small | zstd      |    7649|    2342| 3.27|    3.39|    5.21|   20.97|  21.77|
|   |medium|           |   33918|   33918|    0|   10.29|   12.30|   25.79|  25.54|
| 3 |medium| br        |   33918|    8583| 3.95|    4.20|    6.76|   24.28|  25.66|
| 3 |medium| gzip      |   33918|    9267| 3.66|    4.53|    6.95|   23.87|  24.56|
| 3 |medium| zstd      |   33918|    8610| 3.94|    4.44|    6.78|   24.19|  24.75|
|   |large |           |  138492|  138492|    0|   19.13|   24.63|   30.90|  34.54|
| 3 |large | br        |  138492|   31791| 4.36|   12.31|   14.90|   31.01|  32.31|
| 3 |large | gzip      |  138492|   34864| 3.97|   15.06|   16.34|   30.98|  31.28|
| 3 |large | zstd      |  138492|   31593| 4.38|   10.92|    8.99|   30.25|  31.11| 
|   |huge  |           | 1129275| 1129275|    0|  100.54|  133.13|  155.06| 153.43|
| 3 |huge  | br        | 1129275|  247084| 4.57|   74.59|   56.51|  101.34| 104.89|
| 3 |huge  | gzip      | 1129275|  274970| 4.11|   83.40|   63.99|  106.95| 108.67|
| 3 |huge  | zstd      | 1129275|  238049| 4.74|   67.17|   51.25|   96.02|  98.12|
|   |      |           |        |        |     |        |        |
|   |full  |           |     972|     972|    0|    8.36|    8.37|   20.78|  22.33|
| 4 |full  | br        |     972|     495| 1.96|    2.72|    3.24|
| 4 |full  | gzip      |     972|     523| 1.86|    2.90|    3.41|
| 4 |full  | zstd      |     972|     518| 1.88|    3.32|    5.16|
|   |small |           |    7649|    7649|    0|    8.07|    9.56|   25.12|  23.51|
| 4 |small | br        |    7649|    2273| 3.37|    3.26|    5.04|
| 4 |small | gzip      |    7649|    2425| 3.15|    3.30|    4.62|
| 4 |small | zstd      |    7649|    2339| 3.27|    3.49|    5.60|
|   |medium|           |   33918|   33918|    0|   10.29|   12.30|   25.79|  25.54|
| 4 |medium| br        |   33918|    8384| 4.05|    4.73|    6.92|
| 4 |medium| gzip      |   33918|    9070| 3.74|    4.68|    7.08|
| 4 |medium| zstd      |   33918|    8609| 3.94|    4.75|    7.07|
|   |large |           |  138492|  138492|    0|   19.13|   24.63|   30.90|  34.54|
| 4 |large | br        |  138492|   30572| 4.53|   13.94|   15.03|
| 4 |large | gzip      |  138492|   33760| 4.10|   15.70|   16.73|
| 4 |large | zstd      |  138492|   31559| 4.39|   12.15|   13.95|
|   |huge  |           | 1129275| 1129275|    0|  100.54|  133.13|  155.06| 153.43|
| 4 |huge  | br        | 1129275|  226082| 4.99|   85.28|   58.76|
| 4 |huge  | gzip      | 1129275|  266054| 4.24|   88.38|  102.53|
| 4 |huge  | zstd      | 1129275|  237121| 4.76|   68.80|   67.45|
|   |      |           |        |        |     |        |        |
|   |full  |           |     972|     972|    0|    8.36|    8.37|   20.78|  22.33|
| 5 |full  | br        |     972|     471| 2.06|    3.25|    4.11|
| 5 |full  | gzip      |     972|     516| 1.88|    3.23|    4.65|
| 5 |full  | zstd      |     972|     515| 1.89|    3.84|    5.58|
|   |small |           |    7649|    7649|    0|    8.07|    9.56|   25.12|  23.51|
| 5 |small | br        |    7649|    2123| 3.60|    4.15|    5.77|
| 5 |small | gzip      |    7649|    2318| 3.30|    3.71|    5.01|
| 5 |small | zstd      |    7649|    2301| 3.32|    4.64|    6.42|
|   |medium|           |   33918|   33918|    0|   10.29|   12.30|   25.79|  25.54|
| 5 |medium| br        |   33918|    7857| 4.32|    6.54|    8.12|
| 5 |medium| gzip      |   33918|    8535| 3.97|    5.80|    7.17|
| 5 |medium| zstd      |   33918|    8455| 4.01|    5.68|    8.00|
|   |large |           |  138492|  138492|    0|   19.13|   24.63|   30.90|  34.54|
| 5 |large | br        |  138492|   28781| 4.81|   17.21|   18.78|
| 5 |large | gzip      |  138492|   31680| 4.37|   15.49|   17.38|
| 5 |large | zstd      |  138492|   30755| 4.50|   15.32|   17.26|
|   |huge  |           | 1129275| 1129275|    0|  100.54|  133.13|  155.06| 153.43|
| 5 |huge  | br        | 1129275|  210248| 5.37|  113.61|  125.45|
| 5 |huge  | gzip      | 1129275|  250215| 4.51|  105.42|  102.52|
| 5 |huge  | zstd      | 1129275|  228880| 4.93|   80.48|   97.53|
|   |      |           |        |        |     |        |        |
|   |full  |           |     972|     972|    0|    8.36|    8.37|   20.78|  22.33|
| 7 |full  | br        |     972|     466| 2.09|    3.02|    5.75|
| 7 |full  | gzip      |     972|     516| 1.88|    3.27|    4.63|
| 7 |full  | zstd      |     972|     513| 1.89|    5.04|    6.75|
|   |small |           |    7649|    7649|    0|    8.07|    9.56|   25.12|  23.51|
| 7 |small | br        |    7649|    2109| 3.63|    7.40|    9.79|
| 7 |small | gzip      |    7649|    2267| 3.37|    3.89|    5.20|
| 7 |small | zstd      |    7649|    2233| 3.43|    5.48|    7.71|
|   |medium|           |   33918|   33918|    0|   10.29|   12.30|   25.79|  25.54|
| 7 |medium| br        |   33918|    7740| 4.38|   12.68|   12.13|
| 7 |medium| gzip      |   33918|    8262| 4.11|    5.96|    8.19|
| 7 |medium| zstd      |   33918|    8057| 4.21|    7.27|    9.54|
|   |large |           |  138492|  138492|    0|   19.13|   24.63|   30.90|  34.54|
| 7 |large | br        |  138492|   28317| 4.89|   25.60|   20.82|
| 7 |large | gzip      |  138492|   30572| 4.53|   19.24|   15.25|
| 7 |large | zstd      |  138492|   29025| 4.77|   17.67|   14.65|
|   |huge  |           | 1129275| 1129275|    0|  100.54|  133.13|  155.06| 153.43|
| 7 |huge  | br        | 1129275|  205453| 5.50|  138.31|  145.84|
| 7 |huge  | gzip      | 1129275|  241460| 4.68|  114.66|  122.18|
| 7 |huge  | zstd      | 1129275|  215582| 5.24|   87.85|   98.56|
|   |      |           |        |        |     |        |        |
|   |full  |           |     972|     972|    0|    8.36|    8.37|   20.78|  22.33|
| 9 |full  | br        |     972|     467| 2.08|    4.00|    4.36|
| 9 |full  | gzip      |     972|     516| 1.88|    2.84|    3.45|
| 9 |full  | zstd      |     972|     513| 1.89|    5.77|    5.69|
|   |small |           |    7649|    7649|    0|    8.07|    9.56|   25.12|  23.51|
| 9 |small | br        |    7649|    2109| 3.63|    9.45|    7.01|
| 9 |small | gzip      |    7649|    2257| 3.39|    3.33|    3.84|
| 9 |small | zstd      |    7649|    2194| 3.49|    6.21|    6.07|
|   |medium|           |   33918|   33918|    0|   10.29|   12.30|   25.79|  25.54|
| 9 |medium| br        |   33918|    7707| 4.40|   20.73|   13.36|
| 9 |medium| gzip      |   33918|    8162| 4.16|    6.59|    6.26|
| 9 |medium| zstd      |   33918|    7913| 4.29|    8.66|    7.23|
|   |large |           |  138492|  138492|    0|   19.13|   24.63|   30.90|  34.54|
| 9 |large | br        |  138492|   28122| 4.92|   39.56|   24.68|
| 9 |large | gzip      |  138492|   30115| 4.60|   25.93|   16.55|
| 9 |large | zstd      |  138492|   28366| 4.88|   17.94|   11.91|
|   |huge  |           | 1129275| 1129275|    0|  100.54|  133.13|  155.06| 153.43|
| 9 |huge  | br        | 1129275|  202881| 5.57|  186.05|  205.22|
| 9 |huge  | gzip      | 1129275|  237292| 4.76|  187.45|  156.16|
| 9 |huge  | zstd      | 1129275|  211132| 5.35|   99.78|   65.14|

* We notice a marginal improvement but **not** significant improvement running `zstd` using 2 threads.  We suspect that it is due to the GIL and will not provide significant improvement until free threaded Python is released in later versions, for this test is CPU bound rather than I/O bound.

## References:
* [Enhancing FastAPI performance with HTTP and QUIC(HTTP3)](https://medium.com/@vamsikrishnabhuvanam/enhancing-fastapi-performance-with-http-2-and-quic-http-3-for-efficient-machine-learning-189cd054846e)
