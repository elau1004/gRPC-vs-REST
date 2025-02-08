"""
The RESTful server to serve out our test patient data.
"""
import  os
import  time

from    enum       import  Enum
from    typing     import  List

from    fastapi                     import FastAPI, HTTPException
from    fastapi.middleware.gzip     import GZipMiddleware
#rom    fastapi.responses           import RedirectResponse
from    brotli_asgi                 import BrotliMiddleware
from    zstd_asgi                   import ZstdMiddleware

import  model    # Our test patient data model.


# Initialized the API server.
class Size(Enum):
    FULL    = 'full'   # Full packet
    SMALL   = 'small'
    MEDIUM  = 'medium'
    LARGE   = 'large'
    HUGE    = 'huge'

app = FastAPI()
app.add_middleware( BrotliMiddleware )
app.add_middleware( GZipMiddleware   )
app.add_middleware( ZstdMiddleware  )

@app.get("/")
def index() -> str:
    return f'Hello.  {len(model.patients)} patients are ready.  Parameters are: datasize: [full ,small ,medium ,large ,huge]'

@app.get("/patients/{patient_id}")
def get_patient( patient_id: int ) -> model.Patient:
    try:
        patient = model.patients[ patient_id ]
    except Exception as ex:
        # SEE:  https://www.websitepulse.com/kb/4xx_http_status_codes
        raise HTTPException(status_code=400, detail=f"patient with ID={patient_id=} doesn't exist.")

    return  patient

@app.get("/patients/")
def get_patients( runtoken: str = None ,datasize: str = None ) -> List[model.Patient]:
    logfile = 'logs/restful_server.log'

    os.makedirs( os.path.dirname( logfile ) ,exist_ok=True )
    with open( logfile ,'a' ) as file:   # Python has a 8K buffer.
        file.write(f'{time.time_ns():9}\t3 Server Rcv\t{runtoken}\n')
        end: int = 1
        match datasize: # The following sizes are obtained from inspecting the traffic in the browser.
            case Size.FULL.value:   end = 1     # 1.1 kb
            case Size.SMALL.value:  end = 5     # 9.9 kb
            case Size.MEDIUM.value: end = 50    # 107 kb
            case Size.LARGE.value:  end = 500   # 1.1 mb
            case Size.HUGE.value:   end = 5000  # 11  mb
            case _: end = 1

        file.write(f'{time.time_ns():9}\t5 Server Rsp\t{runtoken}\n')
    return  model.patients[0 : end]
