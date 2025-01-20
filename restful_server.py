"""
The RESTful server to serve out our test patient data.
"""

from    enum       import  Enum
from    typing     import  List

from    fastapi            import FastAPI, HTTPException
from    fastapi.responses  import RedirectResponse

import  model    # Our test patient data model.


# Initialized the API server.
class Size(Enum):
    FULL    = 'full'   # Full packet
    SMALL   = 'small'
    MEDIUM  = 'medium'
    LARGE   = 'large'
    HUGE    = 'huge'

app = FastAPI()

@app.get("/")
def index() -> str:
    return 'Hello.  Server is running.  Parameters are: datasize: [full ,small ,medium ,large ,huge]'

@app.get("/patient/")
def get_patients( runtoken: str = None ,compression: str = None ,datasize: str = None ) -> List[model.Patient]:
    end: int = 1
    match datasize: # The following sizes are obtained from inspecting the traffic in the browser.
        case Size.FULL.value:   end = 1     # 1.1 kb
        case Size.SMALL.value:  end = 5     # 9.9 kb
        case Size.MEDIUM.value: end = 50    # 107 kb
        case Size.LARGE.value:  end = 500   # 1.1 mb
        case Size.HUGE.value:   end = 5000  # 11  mb
        case _: end = 1

    return  model.patients[0 : end]

@app.get("/patient/{patient_id}")
def get_patient( patient_id: int ) -> model.Patient:
    try:
        patient = model.patients[ patient_id ]
    except Exception as ex:
        # SEE:  https://www.websitepulse.com/kb/4xx_http_status_codes
        raise HTTPException(status_code=400, detail=f"patient with ID={patient_id=} doesn't exist.")
    return  patient
