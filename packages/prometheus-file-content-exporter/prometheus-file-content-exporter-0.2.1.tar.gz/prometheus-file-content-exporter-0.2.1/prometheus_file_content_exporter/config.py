import os
import yaml


class ConfigException(Exception):
    pass


class Config:
    def __init__(self, config_file):
        self.config = self.read(config_file)
        self.validate()

    @property
    def files(self):
        return self.config.get('files', [])

    @staticmethod
    def read(config_file):
        with open(config_file, 'r') as file:
            return yaml.load(file)

    def validate(self):
        """
        Validate the configuration.
        Throws an exception with the error message in case of invalid config, or just pass on success.
        """

        files = []
        # Check for invalid files and remove them from config
        for file in self.config['files']:
            if os.path.isfile(file):
                files.append(file)

        # Ensure there's at least 1 file to read is configured
        if len(files) == 0:
            raise ConfigException('There are no files configured to read.')

        self.config['files'] = files
