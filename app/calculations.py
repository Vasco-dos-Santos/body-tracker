from datetime import date, timedelta

from app.models import UserProfile

# Age


def calculate_age(profile: UserProfile) -> int:
    """Return the user's current age in whole years."""
    today = date.today()
    dob = date.fromisoformat(profile.date_of_birth)
    years = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        years -= 1
    return years


# BMI


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """BMI rounded to one decimal place."""
    height_m = height_cm / 100
    return round(weight_kg / (height_m**2), 1)


def bmi_category(bmi: float) -> str:
    """WHO classification label for a given BMI."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal weight"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"


# Formula: Mifflin-St Jeor
# Reference: https://reference.medscape.com/calculator/846/mifflin-st-jeor-equation


def calculate_bmr(profile: UserProfile, weight_kg: float) -> float:
    """Return Basal Metabolic Rate in kcal/day."""
    age = calculate_age(profile)
    bmr = (10 * weight_kg) + (6.25 * profile.height_cm) - (5 * age)
    if profile.sex == "male":
        return round(bmr + 5, 1)
    else:
        return round(bmr - 161, 1)


ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "lightly_active": 1.375,
    "moderately_active": 1.55,
    "very_active": 1.725,
    "extra_active": 1.9,
}


def calculate_tdee(profile: UserProfile, weight_kg: float) -> float:
    """Return Total Daily Energy Expenditure in kcal/day."""
    bmr = calculate_bmr(profile, weight_kg)
    multiplier = ACTIVITY_MULTIPLIERS[profile.activity_level]
    return round(bmr * multiplier, 1)


# Week ID


def week_id(d: date | None = None) -> str:
    """Return the ISO date string of the Sunday that opens the current week."""
    if d is None:
        d = date.today()
    days_since_sunday = (d.weekday() + 1) % 7
    sunday = d - timedelta(days=days_since_sunday)
    return sunday.isoformat()
