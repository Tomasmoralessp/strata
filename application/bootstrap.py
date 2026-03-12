from loguru import logger
from pyspark.sql import SparkSession

from config.paths import (
    BASE_CONFIG_PATH,
    ENVIRONMENT_DIR,
    DATASETS_CONFIG_PATH,
    METRICS_CONFIG_PATH,
    PORTFOLIOS_CONFIG_PATH,
)
from core.config.loader import YamlLoader
from core.config.layered_config import LayeredConfig

from core.config.models import (
    ComputeConfig,
    SparkConfig,
    ConfigModel,
    DatasetConfig,
    MetricConfig,
    IngestionConfig,
    PipelineConfig,
    PortfolioConfig,
    UniverseConfig,
)
from pipeline.pipeline import Pipeline
from pipeline.stages.ingestion_stage import IngestionStage

from infrastructure.datasets.dataset_registry import DatasetRegistry
from infrastructure.storage.storage import DataStorage
from application.application_context import ApplicationContext


class ApplicationBootstrap:
    def _load_config_to_dict(self) -> dict:
        logger.info("[BOOTSTRAP] Loading configuration...")
        # 1. Read the base yaml
        base_config = YamlLoader.read(BASE_CONFIG_PATH)

        logger.debug("[BOOTSTRAP] Base config: {}", BASE_CONFIG_PATH)
        selected_env_str = base_config["environment"]

        logger.info("[BOOTSTRAP] Environment selected: {}", selected_env_str)

        # Construct the SELECTED_ENV_CONFIG_PATH
        SELECTED_ENV_CONFIG_PATH = ENVIRONMENT_DIR / f"{selected_env_str}.yaml"

        logger.debug("[BOOTSTRAP] Environment config: {}", SELECTED_ENV_CONFIG_PATH)

        # 2. Read the file path for the selected environment
        selected_env_config = YamlLoader.read(SELECTED_ENV_CONFIG_PATH)

        logger.debug("[BOOTSTRAP] Datasets config: {}", DATASETS_CONFIG_PATH)

        # 3. Read the datasets yaml
        datasets_config = YamlLoader.read(DATASETS_CONFIG_PATH)

        # 4. Read the metrics yaml configuration
        metrics_config = YamlLoader.read(METRICS_CONFIG_PATH)

        # 5. Read the portfolios yaml configuration
        portfolios_config = YamlLoader.read(PORTFOLIOS_CONFIG_PATH)

        # 6. Create an array with all the layers
        layers = [
            base_config,
            selected_env_config,
            datasets_config,
            metrics_config,
            portfolios_config,
        ]

        # 7. Combine all the dictionaries in a merged dictionary

        config_dict = LayeredConfig(layers).build()

        logger.info("[BOOTSTRAP] Compute engine: {}", config_dict["compute"]["engine"])
        logger.info("[BOOTSTRAP] Datasets loaded: {}", len(config_dict["datasets"]))
        logger.info("[BOOTSTRAP] Metrics loaded: {}", len(config_dict["metrics"]))
        logger.info("[BOOTSTRAP] Storage layers: {}", config_dict["storage"])

        return config_dict

    def _build_config(self) -> ConfigModel:
        config_dict = self._load_config_to_dict()

        # 1. Create compute config
        engine = config_dict["compute"]["engine"]

        spark_data = config_dict["compute"].get("spark")
        if spark_data:
            spark_config = SparkConfig(
                master=spark_data["master"],
                **(
                    {"app_name": spark_data["app_name"]}
                    if "app_name" in spark_data
                    else {}
                ),
            )

            compute_config = ComputeConfig(engine=engine, spark=spark_config)
        else:
            compute_config = ComputeConfig(engine=engine)

        # 2. Create pipeline config
        pipeline_config = PipelineConfig(
            write_mode=config_dict["pipeline"]["write_mode"],
            ingestion=IngestionConfig(
                start_date=config_dict["pipeline"]["ingestion"]["start_date"]
            ),
        )

        # 3. Create dataset configs
        dataset_configs = {}

        for dataset_name, dataset_data in config_dict["datasets"].items():
            dataset_config = DatasetConfig(
                description=dataset_data.get("description"),
                layer=dataset_data["layer"],
                path=dataset_data["path"],
                version=dataset_data["version"],
                format=dataset_data["format"],
                partition_by=dataset_data.get("partition_by"),
            )

            dataset_configs[dataset_name] = dataset_config

        # 4. Create metric configs
        metric_configs = []

        for metric_data in config_dict["metrics"]:
            metric_config = MetricConfig(
                name=metric_data["name"],
                window=metric_data.get("window"),
                benchmark=metric_data.get("benchmark"),
            )

            metric_configs.append(metric_config)

        # 5. Create portfolio configs
        portfolio_data = config_dict.get("portfolio")

        portfolio_configs = {}

        if portfolio_data:
            for portfolio_name, portfolio_item in portfolio_data.items():
                portfolio_config = PortfolioConfig(
                    name=portfolio_name,
                    description=portfolio_item.get("description"),
                    weights=portfolio_item["weights"],
                )

                portfolio_configs[portfolio_name] = portfolio_config

        # 6. Create universe config
        universe_config = UniverseConfig(etfs=config_dict["universe"]["etfs"])

        # 7. Create final config object
        config = ConfigModel(
            environment=config_dict["environment"],
            compute=compute_config,
            pipeline=pipeline_config,
            storage=config_dict["storage"],
            datasets=dataset_configs,
            metrics=metric_configs,
            portfolios=portfolio_configs,
            universe=universe_config,
        )

        return config

    def _build_dataset_registry(self, config: ConfigModel) -> DatasetRegistry:
        logger.info("[BOOTSTRAP] Initializing dataset registry")

        dataset_registry = DatasetRegistry(config.datasets, config.storage)
        logger.debug("[BOOTSTRAP] Datasets registered: {}", len(config.datasets))
        return dataset_registry

    def _build_spark(self, config: ConfigModel) -> SparkSession:
        logger.info("[BOOTSTRAP] Starting spark bootstrap")
        if config.compute.engine == "spark":
            builder = SparkSession.builder
            spark_config = config.compute.spark
            if spark_config:
                app_name = spark_config.app_name
                master = spark_config.master

                if app_name:
                    logger.debug("[BOOTSTRAP] Spark app name: {}", app_name)
                    builder = builder.appName(app_name)

                if master:
                    logger.debug("[BOOTSTRAP] Spark master: {}", master)
                    builder = builder.master(master)

                if config.environment == "prod":
                    builder = builder.config(
                        "spark.hadoop.fs.s3a.aws.credentials.provider",
                        "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
                    )
                    builder = builder.config(
                        "spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4"
                    )

            spark = builder.getOrCreate()
            return spark
        else:
            raise ValueError("Compute engine is not spark")

    def _build_storage(
        self, spark: SparkSession, dataset_registry: DatasetRegistry
    ) -> DataStorage:
        logger.info("[BOOTSTRAP] Initializing storage layer")
        data_storage = DataStorage(spark, dataset_registry)
        return data_storage

    def build_context(self) -> ApplicationContext:
        logger.info("[BOOTSTRAP] Starting application bootstrap")
        config = self._build_config()
        spark = self._build_spark(config)
        dataset_registry = self._build_dataset_registry(config)
        storage = self._build_storage(spark, dataset_registry)

        logger.info("[BOOTSTRAP] Bootstrap completed successfully")

        application_context = ApplicationContext(
            config=config,
            spark=spark,
            dataset_registry=dataset_registry,
            storage=storage,
        )

        return application_context

    def build_pipeline(self, context: ApplicationContext):
        pipeline = Pipeline(context)

        pipeline_config = context.config.pipeline

        if pipeline_config.ingestion:
            pipeline.add_stage(IngestionStage())

        return pipeline
