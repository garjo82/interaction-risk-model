"""Feature computation for interaction-risk-model.

This module should be dataset-agnostic: given ego-relative position/velocity,
compute interaction geometry features like distance, closing speed, TTCA, and dmin.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class InteractionFeatures:
    d_m: float
    v_close_mps: float
    ttca_s: float
    dmin_T_m: float


def compute_features(
    x_rel_m: float,
    y_rel_m: float,
    vx_rel_mps: float,
    vy_rel_mps: float,
    horizon_s: float = 5.0,
    eps: float = 1e-6,
) -> InteractionFeatures:
    """Compute proximity-based interaction features in the ego frame.

    Args:
        x_rel_m, y_rel_m: actor position in ego frame (forward, left)
        vx_rel_mps, vy_rel_mps: actor velocity in ego frame (forward, left)
        horizon_s: prediction horizon for dmin/ttca
        eps: numerical stability constant

    Returns:
        InteractionFeatures with d, closing speed, TTCA, and predicted dmin within horizon.
    """
    # Current separation
    d_m = math.hypot(x_rel_m, y_rel_m)

    # Closing speed along line of sight (positive means approaching)
    v_close_mps = -((x_rel_m * vx_rel_mps) + (y_rel_m * vy_rel_mps)) / (d_m + eps)

    # Time-to-closest-approach (clamped to [0, horizon_s])
    v2 = (vx_rel_mps * vx_rel_mps) + (vy_rel_mps * vy_rel_mps)
    t_star = 0.0 if v2 < eps else -((x_rel_m * vx_rel_mps) + (y_rel_m * vy_rel_mps)) / (v2 + eps)
    ttca_s = max(0.0, min(horizon_s, t_star))

    # Predicted minimum distance within horizon
    x_min = x_rel_m + vx_rel_mps * ttca_s
    y_min = y_rel_m + vy_rel_mps * ttca_s
    dmin_T_m = math.hypot(x_min, y_min)

    return InteractionFeatures(d_m=d_m, v_close_mps=v_close_mps, ttca_s=ttca_s, dmin_T_m=dmin_T_m)
