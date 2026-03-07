# Map app types to mandatory permissions
MANDATORY_PERMISSIONS = {
    "social": ["camera", "microphone", "contacts","location"],
    "game": ["microphone", "storage"],
    "maps": ["location"],
    "shopping": ["location", "storage"],
    "other": [],  # optional
}

# Friendly explanations for each permission type
PERMISSION_EXPLANATIONS = {
    "camera": "Allows you to take photos/videos within the app",
    "microphone": "Allows you to record audio messages or calls",
    "contacts": "Lets you connect with friends already using the app",
    "location": "Tracks your location to provide accurate directions",
    "storage": "Accesses your device storage to save files or offline data",
    "usage_data": "Collects usage data to improve recommendations and features"
}

def get_mandatory_permissions(app_type: str):
    """Return list of mandatory permissions for the given app type"""
    return MANDATORY_PERMISSIONS.get(app_type.lower(), [])