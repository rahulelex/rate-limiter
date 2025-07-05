import time
from collections import defaultdict, deque
from threading import Lock

class RateLimiter:
    def __init__(self):
        self.lock = Lock()
        self.request_logs = defaultdict(lambda: deque())

    def check_and_consume(self, tenant_id, client_id, action_type, max_requests, window_duration):
        key = (tenant_id, client_id, action_type)
        now = time.time()
        with self.lock:
            logs = self.request_logs[key]
            while logs and logs[0] <= now - window_duration:
                logs.popleft()
            if len(logs) < max_requests:
                logs.append(now)
                return True, max_requests - len(logs), int(now + window_duration)
            else:
                return False, 0, int(logs[0] + window_duration)

    def get_status(self, tenant_id, client_id, action_type):
        key = (tenant_id, client_id, action_type)
        with self.lock:
            return list(self.request_logs[key])