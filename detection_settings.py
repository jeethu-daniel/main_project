"""
Detection settings for waste management Django project
"""

from pathlib import Path

# Get the base directory of this file
BASE_DIR = Path(__file__).resolve().parent

# ML Model config
MODEL_DIR = BASE_DIR / 'weights'
DETECTION_MODEL = MODEL_DIR / 'best.pt'

# Webcam index (0 = default/first camera, 1 = second camera, etc.)
# If you see "Camera index out of range", try 0 (only one camera = index 0).
WEBCAM_PATH = 0

# Waste type classifications (each type in exactly ONE list so dashboard matches detection)
# Recyclable: commonly accepted in recycling
RECYCLABLE = ['cardboard_box', 'can', 'paper']
# Non-recyclable: single-use / not accepted in standard recycling
# Include variants your YOLO model outputs (e.g. plastic_bottle, plastic_bottle_cap, plastic_bag)
NON_RECYCLABLE = ['plastic', 'plastic_bottle', 'plastic_bottle_cap', 'plastic_bag', 'stick', 'snack_bag', 'straw', 'cardboard_bowl']
# Hazardous: special handling required
HAZARDOUS = ['battery', 'chemical_spray_can', 'chemical_plastic_bottle', 'chemical_plastic_gallon',
             'light_bulb', 'paint_bucket']

