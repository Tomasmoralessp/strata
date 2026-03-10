# ESTO ES PARA PRACTICAR

from core.config import layered_config
from core.config.loader import YamlLoader
from core.config.layered_config import LayeredConfig
from core.config.models import (
    ConfigModel,
    DatasetConfig,
    PipelineConfig,
    MetricConfig,
    PortfolioConfig,
)

from infrastructure.storage.dataset_registry import DatasetRegistry
from pathlib import Path

from pprint import pprint

ROOT_FILE_PATH = Path(__file__).parent
BASE_YAML_CONFIG_FILE_PATH = ROOT_FILE_PATH / "config" / "base.yaml"
DATASET_YAML_CONFIG_FILE_PATH = ROOT_FILE_PATH / "config" / "datasets.yaml"

# 1. Read the base yaml
base_config = YamlLoader.read(BASE_YAML_CONFIG_FILE_PATH)

# 2. Construct the file path for the environment selected
selected_env = base_config["environment"]

SELECTED_ENV_YAML_CONFIG_FILE_PATH = (
    ROOT_FILE_PATH / "config" / "environments" / f"{selected_env}.yaml"
)

# 3. Read the selected emv yaml configuration
selected_env_config = YamlLoader.read(SELECTED_ENV_YAML_CONFIG_FILE_PATH)

# 4. Read the datasets yaml configuration
datasets_config = YamlLoader.read(DATASET_YAML_CONFIG_FILE_PATH)

# 5. Include all the layers in a list
layers = [base_config, selected_env_config, datasets_config]

# 5. Combine the base_yaml_config, selected_env_yaml_config, and the dataset_yaml_config
merged_config = LayeredConfig(layers).build()

# 6. Create the ConfigModel
config = ConfigModel(environment=selected_env, 
                     pipeline=PipelineConfig(engine="",
                                    write_mode=""),
                     datasets=
                     metrics=
                     portfolios=
                     )


    # environment: str
    #
    # pipeline: PipelineConfig
    #
    # datasets: Dict[str, DatasetConfig]
    #
    # metrics: List[MetricConfig]
    #
    # portfolios: Dict[str, PortfolioConfig]

dataset_registry = DatasetRegistry(merged_config["datasets"])

print(dataset_registry.get("bronze_prices"))


# 6. Construct the ConfigModel object
