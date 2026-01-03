"""Build an interaction table from trajectory data.

Initial target: nuScenes (local), but this script should write a dataset-agnostic table:
(scene_id, timestamp, actor_id, x_rel, y_rel, vx_rel, vy_rel, derived features, risk).
"""

from __future__ import annotations

from irm.features import compute_features
from irm.risk import risk_score


def main() -> None:
    print("build_interactions.py: stub")
    print("Next: load nuScenes frames, compute ego-relative kinematics, then features + risk.")

    # Example placeholder:
    feats = compute_features(x_rel_m=10.0, y_rel_m=2.0, vx_rel_mps=-1.0, vy_rel_mps=0.0, horizon_s=5.0)
    r = risk_score(dmin_T_m=feats.dmin_T_m, ttca_s=feats.ttca_s, v_close_mps=feats.v_close_mps)
    print("example risk:", r)


if __name__ == "__main__":
    main()
