import logging
import os
import signal
import time

import sys
from prometheus_client import start_http_server, REGISTRY
from prometheus_client.core import GaugeMetricFamily
from pythonjsonlogger import jsonlogger

# configuration
from .config import Config

EXPORTER_PORT = int(os.environ.get('EXPORTER_PORT', 9100))
EXPORTER_CONFIG = os.environ.get('EXPORTER_CONFIG', '')
PREFIX = 'file_content'
# logging
log = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '(asctime) (levelname) (message) (funcName)',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logHandler.setFormatter(formatter)
log.setLevel(logging.INFO)
log.addHandler(logHandler)


class FileContentMetricsCollector:
    def __init__(self, files):
        self.files = files

    def collect(self):
        metrics = {}
        metrics.update(self._create_metrics())

        for name, data in metrics.items():
            gauge_name = f'{PREFIX}{name}'
            gauge = GaugeMetricFamily(gauge_name.replace('/', '_'), '', labels=data.get('labels', []))
            value = data['metrics']['value']
            labels = data['labels'] if 'labels' in data else {}

            gauge.add_metric(value=value, labels=labels.values())
            yield gauge

    @staticmethod
    def _check_file(file):
        with open(file, 'r') as f:
            content = f.readline()
        return content

    def _create_metrics(self):
        data = dict()
        for file in self.files:
            try:
                value = float(self._check_file(file))
            except ValueError:
                log.error(f"Couldn't get int from file {file}!")
                continue

            data[file] = dict()
            data[file]['labels'] = {
                'file': file
            }
            data[file]['metrics'] = {
                'value': value,
            }

        return data


class SignalHandler:
    def __init__(self):
        self.shutdown = False

        # Register signal handler
        signal.signal(signal.SIGINT, self._on_signal_received)
        signal.signal(signal.SIGTERM, self._on_signal_received)

    def is_shutting_down(self):
        return self.shutdown

    def _on_signal_received(self, _signal, _frame):
        log.info('Prometheus File Content Exporter is shutting down')
        self.shutdown = True


def main():
    log.info(f'Prometheus File Content Exporter http server started', extra=dict(port=EXPORTER_PORT))

    if not EXPORTER_CONFIG:
        log.fatal('This exporter needs config file provided. Please read README.md for details.')
        sys.exit(1)

    config = Config(EXPORTER_CONFIG)

    start_http_server(EXPORTER_PORT)
    file_content_collector = FileContentMetricsCollector(config.files)
    REGISTRY.register(file_content_collector)

    # Register signal handler
    signal_handler = SignalHandler()

    while not signal_handler.is_shutting_down():
        time.sleep(1)

    log.info(f'Prometheus File Content Exporter shutdown')


if __name__ == '__main__':
    main()
