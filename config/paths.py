from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
ENVIRONMENT_DIR = CONFIG_DIR / "environments"
BASE_CONFIG_PATH = CONFIG_DIR / "base.yaml"
DATASETS_CONFIG_PATH = CONFIG_DIR / "datasets.yaml"
METRICS_CONFIG_PATH = CONFIG_DIR / "metrics.yaml"
PORTFOLIOS_CONFIG_PATH = CONFIG_DIR / "portfolio.yaml"
