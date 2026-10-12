"""Fitness program logic adapted from the supplied ACEest desktop examples."""
import math

PROGRAMS = {
    'FL': {'name': 'Fat Loss', 'calorie_factor': 22},
    'MG': {'name': 'Muscle Gain', 'calorie_factor': 35},
    'BG': {'name': 'Beginner', 'calorie_factor': 26},
}


def calorie_target(weight, program):
    if program not in PROGRAMS:
        raise ValueError('Program must be FL, MG or BG')
    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        raise ValueError('Weight must be a number')
    if not math.isfinite(weight) or weight <= 0 or weight > 500:
        raise ValueError('Weight must be greater than 0 and at most 500 kg')
    return int(weight * PROGRAMS[program]['calorie_factor'])
