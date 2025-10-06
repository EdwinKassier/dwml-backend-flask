"""Backwards-compatible rate limiting middleware."""

from flask import request, jsonify, current_app
from functools import wraps
import time
from collections import defaultdict, deque


class RateLimitMiddleware:
    """Simple in-memory rate limiter that doesn't break existing functionality."""

    def __init__(self):
        self.requests = defaultdict(deque)
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = time.time()

    def is_rate_limited(self, identifier, limit=60, window=60):
        """Check if request should be rate limited."""
        now = time.time()

        # Cleanup old entries periodically
        if now - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_entries(now)
            self.last_cleanup = now

        # Get requests for this identifier
        requests = self.requests[identifier]

        # Remove requests older than the window
        while requests and requests[0] <= now - window:
            requests.popleft()

        # Check if we're over the limit
        if len(requests) >= limit:
            return True

        # Add current request
        requests.append(now)
        return False

    def _cleanup_old_entries(self, now):
        """Clean up old entries to prevent memory leaks."""
        cutoff = now - 3600  # 1 hour
        for identifier in list(self.requests.keys()):
            requests = self.requests[identifier]
            while requests and requests[0] <= cutoff:
                requests.popleft()

            # Remove empty entries
            if not requests:
                del self.requests[identifier]

    def get_client_identifier(self):
        """Get unique identifier for rate limiting."""
        # Use IP address as primary identifier
        return request.remote_addr or "unknown"


# Global rate limiter instance
rate_limiter = RateLimitMiddleware()


def rate_limit(limit=60, window=60):
    """Rate limiting decorator that preserves existing behavior."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Only apply rate limiting if enabled
            if not current_app.config.get("RATE_LIMIT_ENABLED", False):
                return f(*args, **kwargs)

            identifier = rate_limiter.get_client_identifier()

            if rate_limiter.is_rate_limited(identifier, limit, window):
                # Return rate limit error in same format as other errors
                return (
                    jsonify(
                        {"message": "Rate limit exceeded. Please try again later."}
                    ),
                    429,
                    {"ContentType": "application/json"},
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator
