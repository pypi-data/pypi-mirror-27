# -*- coding: utf-8 -*-

import sys
from setuptools import setup

if sys.version_info.major < 3:
    raise RuntimeError('Installing requires Python 3 or newer')

setup(
  name='prometheus-file-content-exporter',
  packages=['prometheus_file_content_exporter'],
  version='0.2.1',
  description='Prometheus file content exporter',
  author='Marcin Brański',
  author_email='marcin.branski@spreaker.com',
  url='https://github.com/spreaker/prometheus-file-content-exporter',
  keywords=['prometheus', 'exporter'],
  classifiers=[],
  python_requires=' >= 3',
  install_requires=['prometheus_client==0.0.21', 'python-json-logger==0.1.5', 'PyYAML==3.12'],
  entry_points={
    'console_scripts': [
      'prometheus-file-content-exporter = prometheus_file_content_exporter.main:main',
    ],
  },

)
