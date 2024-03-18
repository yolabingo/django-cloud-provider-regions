from pathlib import Path

CLOUD_PROVIDERS = [
    "aws",
]

PROJECT_ROOT_DIR = Path(__file__).parent.parent
APP_NAME = "django_cloud_provider_zones"
APP_DIR = PROJECT_ROOT_DIR / "src" / APP_NAME
REGION_DATA_DIR = PROJECT_ROOT_DIR / "region_data"
FIXTURES_DIR = APP_DIR / "fixtures"
