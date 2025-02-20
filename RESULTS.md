# Results collected from our testing
## Hardware ran on
The following is the result of the average response time for each of the above mentioned combination of options.

```
Lenovo T490s laptop                 Air Mac                     AWS EC2
    O/S:    Windows 11 Pro              O/S:                        O/S:    Linux
    CPU:    Intel i5-8365, 4 cores      CPU:    M4                  CPU:    
    Clock:  1.6 GHz - 4.80 GHz          Clock:                      Clock:  
    RAM:    16 Gib                      RAM:                        RAM:    
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

When testing with protocol HTTP/**2**, first you need to generate the security key and certificate.  The following command can be used to generate these files:
```
openssl req -x509 -newkey rsa:4096 -sha256 -days 5000 -nodes -keyout key.pem -out cert.pem -subj "/CN=example.com"  -addext "subjectAltName=DNS:example.com,DNS:*.example.com,IP:10.0.0.1"
```

Once both `key.pem` and `cert.pem` are generated, the server need to be started with the following command:
```
hypercorn  --keyfile key.pem  --certfile cert.pem  restful_server:app
```

### Command use to return the test:
```batch
:: Windows
for %s in ( full small medium large huge ) do ( 
    for %c in ( none br gzip zstd ) do ( 
        for %p in ( http https ) do (
            for %i in ( 1 2 3 ) do ( 
                python restful_client.py -i 1000 -s %s -c %c -p %p  & del logs\*.log
            )
        )
    )
)
```

```bash
#  Bash
for s in full small medium large huge; do {
    for c in  none  br gzip zstd; do {
        for p in http https; do {
            for i  in 1 2 3; do {
                echo    restful_client.py -i 1000 -s $s -c $c -p $p
                python  restful_client.py -i 1000 -s $s -c $c -p $p  && rm logs/*.log
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
| Win H1      | Tested on Windows 11 using `HTTP/1.1` measured in ms.|
| Win H2      | Tested on Windows 11 using `HTTP/2` measured in ms.|
| AWS H1      | Tested in the cloud using `HTTP/1.1` measured in ms.|
| AWS H2      | Tested in the cloud using `HTTP/2` measured in ms.|

|Lvl|Size  |Compression|  Win H1|  Win H2| Mac H1| Mac H2|
|:-:|:-----|:----------|-------:|-------:|------:|------:|
| 3 |full  |           |    2.52|    3.58|
| 3 |full  | br        |    2.86|    4.46|
| 3 |full  | gzip      |    3.79|    3.96|
| 3 |full  | zstd      |    3.92|    9.45|
| 3 |small |           |    4.35|   10.48|
| 3 |small | br        |    4.48|   12.14|
| 3 |small | gzip      |    4.77|    5.14|
| 3 |small | zstd      |    4.90|    8.89|
| 3 |medium|           |    6.46|   21.27|
| 3 |medium| br        |    6.02|   21.90|
| 3 |medium| gzip      |    5.94|    8.31|
| 3 |medium| zstd      |    5.60|   10.81|
| 3 |large |           |   12.94|   37.42|
| 3 |large | br        |   12.49|   37.62|
| 3 |large | gzip      |   13.61|   28.60|
| 3 |large | zstd      |   11.88|   18.51|
| 3 |huge  |           |   90.88|  167.29|
| 3 |huge  | br        |   96.64|  189.43|
| 3 |huge  | gzip      |  112.36|  200.62|
| 3 |huge  | zstd      |   88.76|  109.49|
| 4 |full  |           |    2.53|        |
| 4 |full  | br        |    2.44|        |
| 4 |full  | gzip      |    2.44|        |
| 4 |full  | zstd      |    3.10|        |
| 4 |small |           |    3.27|        |
| 4 |small | br        |    3.12|        |
| 4 |small | gzip      |    2.96|        |
| 4 |small | zstd      |    3.51|        |
| 4 |medium|           |    5.77|        |
| 4 |medium| br        |    6.17|        |
| 4 |medium| gzip      |    6.12|        |
| 4 |medium| zstd      |    4.75|        |
| 4 |large |           |    9.20|        |
| 4 |large | br        |    9.24|        |
| 4 |large | gzip      |   10.18|        |
| 4 |large | zstd      |   12.37|        |
| 4 |huge  |           |   66.58|        |
| 4 |huge  | br        |   64.69|        |
| 4 |huge  | gzip      |   81.88|        |
| 4 |huge  | zstd      |   70.48|        |
| 5 |full  |           |    3.07|        |
| 5 |full  | br        |    3.51|        |
| 5 |full  | gzip      |    2.62|        |
| 5 |full  | zstd      |    4.66|        |
| 5 |small |           |    3.80|        |
| 5 |small | br        |    4.71|        |
| 5 |small | gzip      |    3.11|        |
| 5 |small | zstd      |    4.79|        |
| 5 |medium|           |    6.95|        |
| 5 |medium| br        |    5.31|        |
| 5 |medium| gzip      |    5.61|        |
| 5 |medium| zstd      |    5.28|        |
| 5 |large |           |   14.02|        |
| 5 |large | br        |   12.21|        |
| 5 |large | gzip      |   12.82|        |
| 5 |large | zstd      |   11.31|        |
| 5 |huge  |           |   96.00|        |
| 5 |huge  | br        |   83.86|        |
| 5 |huge  | gzip      |   75.55|        |
| 5 |huge  | zstd      |   69.01|        |
| 9 |full  |           |    2.47|        |
| 9 |full  | br        |    2.37|        |
| 9 |full  | gzip      |    3.46|        |
| 9 |full  | zstd      |    4.11|        |
| 9 |small |           |    4.06|        |
| 9 |small | br        |    3.98|        |
| 9 |small | gzip      |    4.13|        |
| 9 |small | zstd      |    4.58|        |
| 9 |medium|           |    5.87|        |
| 9 |medium| br        |    5.85|        |
| 9 |medium| gzip      |    6.11|        |
| 9 |medium| zstd      |    6.05|        |
| 9 |large |           |   12.62|        |
| 9 |large | br        |    8.89|        |
| 9 |large | gzip      |   14.16|        |
| 9 |large | zstd      |   12.64|        |
| 9 |huge  |           |   89.55|        |
| 9 |huge  | br        |   90.85|        |
| 9 |huge  | gzip      |  103.96|        |
| 9 |huge  | zstd      |   81.03|        |

* We notice a marginal improvement but **not** significant improvement running `zstd` using 2 threads.  We suspect that it is due to the GIL and will not provide significant improvement until free threaded Python is released in later versions, for this test is CPU bound rather than I/O bound.


