from collections import defaultdict, deque

MAX_GLOBAL_INFLIGHT = 100
MAX_TENANT_INFLIGHT = 10
MAX_TENANT_QUEUE_SIZE = 50

class LoadManager:
    def __init__(self):
        self.global_inflight = 0
        self.tenant_inflight = defaultdict(int)
        self.tenant_queues = defaultdict(lambda: deque())

    def should_queue(self, tenant_id):
        return self.global_inflight >= MAX_GLOBAL_INFLIGHT or self.tenant_inflight[tenant_id] >= MAX_TENANT_INFLIGHT

    def queue_request(self, payload):
        queue = self.tenant_queues[payload.tenant_id]
        if len(queue) >= MAX_TENANT_QUEUE_SIZE:
            return "rejected"
        queue.append(payload)
        return "queued"

    def release(self, tenant_id):
        self.global_inflight = max(0, self.global_inflight - 1)
        self.tenant_inflight[tenant_id] = max(0, self.tenant_inflight[tenant_id] - 1)

    def get_queue_status(self, tenant_id):
        return len(self.tenant_queues[tenant_id])