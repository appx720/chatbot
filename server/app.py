from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sending = False

class VisitLog(BaseModel):
    url: str
    #title: str
    #time: str

@app.get("/send")
def get_flag():
    return {"send": sending}

@app.post("/trigger_send")
def trigger():
    global sending
    sending = True
    return {"status": "will_send"}

@app.post("/log")
def receive_logs(logs: List[VisitLog]):
    print(f"받은 방문기록 {len(logs)}개")
    for log in logs:
        print(f"- {log.url}")
        #print(f"- {log.time} | {log.title} ({log.url})")
    return {"status": "received", "count": len(logs)}

@app.post("/done")
def clear_flag():
    global sending
    sending = False
    return {"status": "cleared"}
