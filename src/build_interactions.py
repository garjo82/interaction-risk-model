from __future__ import annotations

from pathlib import Path

import pandas as pd

from irm.features import compute_features
from irm.risk import raw_risk_proxy, risk_score


def build_demo_interactions(horizon_s: float = 5.0, d_unsafe_m: float = 2.0) -> pd.DataFrame:
    """Create a tiny demo interaction table that matches docs/schema.md.

    This is a wiring + schema sanity check before connecting to nuScenes.
    """
    rows = []
    scene_id = "demo_scene"
    ego_id = "ego"

    # (timestamp_s, actor_id, x_rel_m, y_rel_m, vx_rel_mps, vy_rel_mps)
    samples = [
        (0.0, "actor_A", 10.0, 2.0, -1.0, 0.0),
        (0.5, "actor_A", 9.5, 2.0, -1.0, 0.0),
        (1.0, "actor_A", 9.0, 2.0, -1.0, 0.0),
        (0.0, "actor_B", 6.0, -1.0, -0.2, 0.4),
        (0.5, "actor_B", 5.9, -0.8, -0.2, 0.4),
        (1.0, "actor_B", 5.8, -0.6, -0.2, 0.4),
    ]

    # For demo only, dt_s is fixed between samples in a track; real pipeline computes per-row.
    dt_s = 0.5

    for (timestamp_s, actor_id, x_rel_m, y_rel_m, vx_rel_mps, vy_rel_mps) in samples:
        feats = compute_features(
            x_rel_m=x_rel_m,
            y_rel_m=y_rel_m,
            vx_rel_mps=vx_rel_mps,
            vy_rel_mps=vy_rel_mps,
            horizon_s=horizon_s,
        )

        rr = raw_risk_proxy(dmin_T_m=feats.dmin_T_m, ttca_s=feats.ttca_s, v_close_mps=feats.v_close_mps)
        r = risk_score(dmin_T_m=feats.dmin_T_m, ttca_s=feats.ttca_s, v_close_mps=feats.v_close_mps)

        event_dmin = 1 if feats.dmin_T_m < d_unsafe_m else 0

        rows.append(
            {
                "scene_id": scene_id,
                "timestamp_s": float(timestamp_s),
                "ego_id": ego_id,
                "actor_id": actor_id,
                "x_rel_m": float(x_rel_m),
                "y_rel_m": float(y_rel_m),
                "vx_rel_mps": float(vx_rel_mps),
                "vy_rel_mps": float(vy_rel_mps),
                "dt_s": float(dt_s),
                "t_horizon_s": float(horizon_s),
                "d_m": float(feats.d_m),
                "v_close_mps": float(feats.v_close_mps),
                "ttca_s": float(feats.ttca_s),
                "dmin_T_m": float(feats.dmin_T_m),
                "risk_raw": float(rr),
                "risk": float(r),
                "risk_version": "v0.1",
                "d_unsafe_m": float(d_unsafe_m),
                "event_dmin": int(event_dmin),
            }
        )

    df = pd.DataFrame(rows)

    # Column order (nice for humans; not required for machines)
    col_order = [
        "scene_id",
        "timestamp_s",
        "ego_id",
        "actor_id",
        "x_rel_m",
        "y_rel_m",
        "vx_rel_mps",
        "vy_rel_mps",
        "dt_s",
        "t_horizon_s",
        "d_m",
        "v_close_mps",
        "ttca_s",
        "dmin_T_m",
        "risk_raw",
        "risk",
        "risk_version",
        "d_unsafe_m",
        "event_dmin",
    ]
    return df[col_order]


def main() -> None:
    out_path = Path("outputs") / "demo_interactions.parquet"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = build_demo_interactions(horizon_s=5.0, d_unsafe_m=2.0)
    df.to_parquet(out_path, index=False)

    print(f"Wrote {len(df)} rows to {out_path}")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
