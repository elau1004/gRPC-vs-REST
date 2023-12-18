from enum import Enum
from datetime import date, datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, PositiveInt

class TestRecord(BaseModel):
    ID : PositiveInt
    created_on : datetime
    int_value : int

test_records = {
    1: TestRecord(ID=1, created_on=datetime.utcnow() ,int_value=1),
    2: TestRecord(ID=2, created_on=datetime.utcnow() ,int_value=2),
    3: TestRecord(ID=3, created_on=datetime.utcnow() ,int_value=3),
    4: TestRecord(ID=4, created_on=datetime.utcnow() ,int_value=4),
    5: TestRecord(ID=5, created_on=datetime.utcnow() ,int_value=5),
}

app = FastAPI()

@app.get("/")
def test_list() -> dict[str ,dict[int ,TestRecord]]:
    return {"test_records" : test_records}
