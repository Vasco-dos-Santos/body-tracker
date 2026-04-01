import json
from pathlib import Path

from app.models import Measurements, UserProfile, WeeklyEntry

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "entries.json"
CURRENT_SCHEMA_VERSION = 1


# Internal helpers


def _empty_store() -> dict:
    return {
        "schema_version": CURRENT_SCHEMA_VERSION,
        "profile": None,
        "entries": [],
    }


def _migrate(data: dict, from_version: int) -> dict:
    if from_version < 1:
        for entry in data["entries"]:
            entry.setdefault("notes", None)
            entry.setdefault("amended_from", None)
    return data


# Serialisation helpers


def _profile_to_dict(profile: UserProfile) -> dict:
    return {
        "sex": profile.sex,
        "date_of_birth": profile.date_of_birth,
        "height_cm": profile.height_cm,
        "activity_level": profile.activity_level,
        "created_at": profile.created_at,
    }


def _dict_to_profile(data: dict) -> UserProfile:
    return UserProfile(
        created_at=data["created_at"],
        sex=data["sex"],
        date_of_birth=data["date_of_birth"],
        height_cm=data["height_cm"],
        activity_level=data["activity_level"],
    )


def _entry_to_dict(entry: WeeklyEntry) -> dict:
    return {
        "id": entry.id,
        "recorded_at": entry.recorded_at,
        "weight_kg": entry.weight_kg,
        "measurements": {
            "waist": entry.measurements.waist,
            "hips": entry.measurements.hips,
            "chest": entry.measurements.chest,
            "neck": entry.measurements.neck,
            "left_arm": entry.measurements.left_arm,
            "right_arm": entry.measurements.right_arm,
            "left_thigh": entry.measurements.left_thigh,
            "right_thigh": entry.measurements.right_thigh,
        },
        "notes": entry.notes,
        "amended_from": entry.amended_from,
    }


def _dict_to_entry(data: dict) -> WeeklyEntry:
    m = data.get("measurements", {})
    return WeeklyEntry(
        id=data["id"],
        recorded_at=data["recorded_at"],
        weight_kg=data["weight_kg"],
        measurements=Measurements(
            waist=m.get("waist"),
            hips=m.get("hips"),
            chest=m.get("chest"),
            neck=m.get("neck"),
            left_arm=m.get("left_arm"),
            right_arm=m.get("right_arm"),
            left_thigh=m.get("left_thigh"),
            right_thigh=m.get("right_thigh"),
        ),
        notes=data.get("notes"),
        amended_from=data.get("amended_from"),
    )


# Public API


def init() -> None:
    """Create the data directory and an empty store if none exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        _write_raw(_empty_store())


def _write_raw(data: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _read_raw() -> dict:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    version = data.get("schema_version", 0)
    if version < CURRENT_SCHEMA_VERSION:
        data = _migrate(data, from_version=version)
        _write_raw(data)
    return data


def load_profile() -> UserProfile | None:
    data = _read_raw()
    if data["profile"] is None:
        return None
    return _dict_to_profile(data["profile"])


def save_profile(profile: UserProfile) -> None:
    data = _read_raw()
    data["profile"] = _profile_to_dict(profile)
    _write_raw(data)


def load_entries() -> list[WeeklyEntry]:
    data = _read_raw()
    return [_dict_to_entry(e) for e in data["entries"]]


def save_entry(entry: WeeklyEntry) -> None:
    data = _read_raw()
    data["entries"].append(_entry_to_dict(entry))
    _write_raw(data)


def entry_exists(week_id: str) -> bool:
    """Return True if any entry with this week id already exists."""
    return any(e["id"] == week_id for e in _read_raw()["entries"])
