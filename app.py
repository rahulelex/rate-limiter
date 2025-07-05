from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rate_limiter import RateLimiter
from load_manager import LoadManager

app = FastAPI()
rate_limiter = RateLimiter()
load_manager = LoadManager()

class RequestPayload(BaseModel):
    tenant_id: str
    client_id: str
    action_type: str
    max_requests: int
    window_duration_seconds: int

@app.post("/check_and_consume")
def check_and_consume(payload: RequestPayload):
    if load_manager.should_queue(payload.tenant_id):
        status = load_manager.queue_request(payload)
        return {"allowed": False, "remaining_requests": 0, "status": status}
    try:
        allowed, remaining, reset_time = rate_limiter.check_and_consume(
            payload.tenant_id,
            payload.client_id,
            payload.action_type,
            payload.max_requests,
            payload.window_duration_seconds
        )
        return {
            "allowed": allowed,
            "remaining_requests": remaining,
            "reset_time_seconds": reset_time,
            "status": "processed" if allowed else "rejected"
        }
    finally:
        load_manager.release(payload.tenant_id)

@app.get("/status/{tenant_id}/{client_id}/{action_type}")
def status(tenant_id: str, client_id: str, action_type: str):
    state = rate_limiter.get_status(tenant_id, client_id, action_type)
    queue_size = load_manager.get_queue_status(tenant_id)
    return {
        "current_request_count": len(state),
        "timestamps": state,
        "queued_requests": queue_size
    }
