from core.config.models import DatasetConfig


class DatasetRegistry:
    def __init__(self, datasets: dict[str, DatasetConfig], storage: dict[str, str]):
        self._datasets = datasets
        self._storage = storage

    def __str__(self):
        return str(self._datasets)

    def get(self, name: str) -> DatasetConfig:
        if name not in self._datasets:
            raise ValueError("Dataset is not defined in the configuration.")
        return self._datasets[name]

    def uri(self, name: str) -> str:
        dataset_layer = self.get(name).layer

        if dataset_layer not in self._storage:
            raise ValueError("Dataset layer not defined in the storage configuration.")

        base = self._storage[dataset_layer]
        version = self.get(name).version
        path = f"{base}/{name}/{version}"
        return path

    def partitions(self, name: str) -> list[str]:
        dataset = self.get(name)
        return dataset.partition_by or []

    def datasets_in_layer(self, layer: str) -> list[str]:
        return [
            name
            for name, dataset_config in self._datasets.items()
            if dataset_config.layer == layer
        ]
