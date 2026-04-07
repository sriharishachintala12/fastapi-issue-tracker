import time
from fastapi import Request

async def timer_middleware(request:Request,call_next):
    start=time.time()
    response=await call_next(request)
    response.headers["X-Process-Time"]=f"{time.time()-start:.2f} seconds"
    return response

