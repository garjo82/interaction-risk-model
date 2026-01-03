"""Risk scoring for interaction-risk-model.

Option D: a continuous proximity-based risk proxy mapped into [0, 1].
Calibration can be added later (e.g., Platt scaling / isotonic) once you define an event proxy.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class RiskParams:
    # Weights for the raw proxy score
    w_inv_dmin: float = 1.0
    w_inv_ttca: float = 0.5
    w_vclose: float = 0.2

    # Numerical stability
    eps: float = 1e-6


def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))


def raw_risk_proxy(
    dmin_T_m: float,
    ttca_s: float,
    v_close_mps: float,
    params: RiskParams = RiskParams(),
) -> float:
    """Compute an unbounded risk proxy score.

    Higher score => higher interaction risk.
    """
    inv_dmin = 1.0 / (dmin_T_m + params.eps)
    inv_ttca = 1.0 / (ttca_s + params.eps)

    return (
        params.w_inv_dmin * inv_dmin
        + params.w_inv_ttca * inv_ttca
        + params.w_vclose * max(0.0, v_close_mps)
    )


def risk_score(
    dmin_T_m: float,
    ttca_s: float,
    v_close_mps: float,
    params: RiskParams = RiskParams(),
) -> float:
    """Bounded risk score in [0, 1]."""
    s = raw_risk_proxy(dmin_T_m=dmin_T_m, ttca_s=ttca_s, v_close_mps=v_close_mps, params=params)
    return sigmoid(s)
