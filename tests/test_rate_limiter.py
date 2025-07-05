import time
from rate_limiter import RateLimiter

def test_rate_limit_allows_under_limit():
    rl = RateLimiter()
    allowed, remaining, _ = rl.check_and_consume("t1", "u1", "api", 5, 60)
    assert allowed
    assert remaining == 4

def test_rate_limit_blocks_over_limit():
    rl = RateLimiter()
    for _ in range(5):
        rl.check_and_consume("t1", "u1", "api", 5, 60)
    allowed, remaining, _ = rl.check_and_consume("t1", "u1", "api", 5, 60)
    assert not allowed
    assert remaining == 0
