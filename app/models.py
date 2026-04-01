from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Measurements:
    waist: Optional[float] = None
    hips: Optional[float] = None
    chest: Optional[float] = None
    neck: Optional[float] = None
    left_arm: Optional[float] = None
    right_arm: Optional[float] = None
    left_thigh: Optional[float] = None
    right_thigh: Optional[float] = None


@dataclass
class UserProfile:
    sex: str
    date_of_birth: str
    height_cm: float
    activity_level: str
    created_at: str


@dataclass
class WeeklyEntry:
    id: str
    recorded_at: str
    weight_kg: float
    measurements: Measurements = field(default_factory=Measurements)
    notes: Optional[str] = None
    amended_from: Optional[str] = None
