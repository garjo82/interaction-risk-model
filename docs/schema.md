# Interaction Table Schema

This schema defines the core “data API” for the project: one row per **(scene, time, actor)**,
expressed in the **ego frame**, plus derived proximity features and a continuous risk score.

The schema is designed to be dataset-agnostic. nuScenes is the initial source, but the
table structure should transfer to other domains (e.g., UAS / drone deconfliction).

---

## 1) Keys and identifiers

These columns uniquely identify each interaction row.

| Column | Type | Description |
|---|---|---|
| `scene_id` | string | Scenario identifier (dataset-specific) |
| `timestamp_s` | float | Timestamp in seconds (monotonic within scene) |
| `ego_id` | string | Ego identifier (may be constant per scene) |
| `actor_id` | string | Other actor identifier |

**Notes**
- `timestamp_s` is the canonical time representation for this project.
- `dt_s` should be computed from adjacent timestamps and/or the differencing method used for velocity.

---

## 2) Ego-relative state (required)

These columns describe the actor state relative to the ego agent at the given timestamp.

| Column | Type | Description |
|---|---|---|
| `x_rel_m` | float | Actor position in ego frame (forward +) |
| `y_rel_m` | float | Actor position in ego frame (left +) |
| `vx_rel_mps` | float | Actor velocity in ego frame (forward +) |
| `vy_rel_mps` | float | Actor velocity in ego frame (left +) |
| `dt_s` | float | Time delta used to estimate velocity |

**Conventions**
- The ego frame is ego-centric and right-handed: `x` forward, `y` left.
- Velocities must be computed with a consistent differencing method (forward/central) and `dt_s`.

---

## 3) Derived interaction features (Option D)

These are computed from ego-relative state and a chosen horizon `T`.

| Column | Type | Description |
|---|---|---|
| `t_horizon_s` | float | Horizon used for TTCA / dmin calculations |
| `d_m` | float | Current separation distance `sqrt(x^2 + y^2)` |
| `v_close_mps` | float | Closing speed along line-of-sight (positive = approaching) |
| `ttca_s` | float | Time-to-closest-approach, clamped to `[0, T]` |
| `dmin_T_m` | float | Predicted minimum separation within horizon `T` |

---

## 4) Risk outputs

The risk model produces a continuous score intended for downstream decision logic.

| Column | Type | Description |
|---|---|---|
| `risk_raw` | float | Unbounded proxy score before squashing/calibration |
| `risk` | float | Final risk score in `[0, 1]` |
| `risk_version` | string | Version tag for comparability (e.g., `v0.1`) |

---

## 5) Event proxy (for evaluation and calibration)

Because perfect ground truth is often unavailable, evaluation uses a simple proximity-based
event proxy derived from predicted minimum separation.

| Column | Type | Description |
|---|---|---|
| `d_unsafe_m` | float | Unsafe separation threshold used for proxy event |
| `event_dmin` | int | 1 if `dmin_T_m < d_unsafe_m`, else 0 |

This proxy supports:
- event rate by risk decile
- calibration diagnostics
- ranking checks (“top-k risk windows capture higher event frequency”)

---

## 6) Optional metadata (add later if useful)

These columns improve slicing and interpretation but are not required for the core model.

| Column | Type | Description |
|---|---|---|
| `actor_type` | string | Actor class (vehicle, pedestrian, cyclist, etc.) |
| `ego_speed_mps` | float | Ego speed magnitude |
| `range_bucket` | string | e.g., `0-10m`, `10-20m` |
| `source_dataset` | string | e.g., `nuscenes` |
