"""Separate local MCP calculator server. Copyright Patrick Hall, 2026-27. MIT License."""
import math
import os
from mcp.server.fastmcp import FastMCP

# The calculator has no need to inherit the host's API credential.
os.environ.pop('OPENAI_API_KEY', None)
mcp = FastMCP('Lecture 6 calculator')


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


if __name__ == '__main__':
    # stdout carries MCP JSON-RPC. Send any diagnostic logging to stderr.
    mcp.run(transport='stdio')
