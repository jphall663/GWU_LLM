"""Separate local MCP calculator server. Copyright Patrick Hall, 2026-27. MIT License."""
import math
import os
from mcp.server.fastmcp import FastMCP

# The calculator has no need to inherit the host's API credential.
os.environ.pop('OPENAI_API_KEY', None)
mcp = FastMCP('Lecture 6 calculator')


# Side-effect-free tool definitions.
@mcp.tool()
def revenue_growth(previous: float, current: float) -> dict:
    """Return percentage revenue growth: 100 * (current - previous) / previous.

    Inputs must be finite, nonnegative revenues in the same currency and scale;
    previous must be positive. This performs arithmetic only, with no side effects.
    """
    if not math.isfinite(previous) or not math.isfinite(current) or previous <= 0 or current < 0:
        raise ValueError('Use finite revenues, previous > 0 and current >= 0.')
    return {'previous': previous, 'current': current,
            'growth_percent': 100 * (current - previous) / previous}


@mcp.tool()
def sort_numbers(values: list[float], descending: bool) -> dict:
    """Sort a short list of finite numbers; this has no side effects."""
    if not values or len(values) > 20 or not all(math.isfinite(value) for value in values):
        raise ValueError('Use 1–20 finite numbers.')
    return {'values': values, 'descending': descending,
            'sorted_values': sorted(values, reverse=descending)}


if __name__ == '__main__':
    # stdout carries MCP JSON-RPC. Send any diagnostic logging to stderr.
    mcp.run(transport='stdio')
