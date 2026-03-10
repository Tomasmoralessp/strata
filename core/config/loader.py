import yaml


class YamlLoader:
    @staticmethod
    def read(file_path):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return data
