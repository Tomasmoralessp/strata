def deepmerge(base: dict, override: dict) -> dict:
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deepmerge(result[key], value)
        else:
            result[key] = value
    return result


class LayeredConfig:
    def __init__(self, layers: list[dict]):
        self.layers = layers

    def build(self) -> dict:
        config = {}

        for layer in self.layers:
            config = deepmerge(config, layer)

        return config
