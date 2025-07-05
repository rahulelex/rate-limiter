# DESIGN.md

## System Architecture
- **API Layer (FastAPI)**: Handles incoming requests.
- **RateLimiter**: Manages per-client rate limit using Sliding Window Log.
- **LoadManager**: Monitors concurrent request limits and queues per tenant.

## Data Structures
- **rate_limiter**: `defaultdict<deque>` storing timestamps.
- **load_manager**: In-memory counters and `defaultdict<deque>` for queues.

## Concurrency Model
- **Thread-safe locks**: `threading.Lock` protects shared structures.

## Error Handling
- Return appropriate `status`: "processed", "queued", or "rejected".

## Scalability
- Move request logs to Redis.
- Replace queues with Kafka.
- Use service mesh for distributed tenant isolation.

## Trade-offs
- Chose simplicity over exact fairness for now.
- Fixed queue size to prevent memory exhaustion.

## Testing Strategy
- Unit tests for rate limit & queuing.
- Concurrency test to simulate high load across tenants.

## AI Usage Discussion
- Sliding Window Log implemented with memory and time efficiency.
- Queue overflow and fairness logic hand-crafted beyond generic AI output.
- Load fairness across tenants and memory cleanup of expired entries considered.
