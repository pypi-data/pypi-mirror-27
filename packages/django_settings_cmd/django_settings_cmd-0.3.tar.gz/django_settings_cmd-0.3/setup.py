# coding: utf-8
from setuptools import setup

setup(
  name = 'django_settings_cmd',
  packages = ['django_settings_cmd'], 
  version = '0.3',
  description = 'A commmand line tool to manage the django settings file',
  author = 'Ruben Nørgaard',
  author_email = 'email@rubennoergaard.dk',
  url = 'https://github.com/RubenNorgaard/django-settings-cmd', 
  download_url = 'https://github.com/RubenNorgaard/django-settings-cmd/archive/0.3.tar.gz', 
  keywords = ['django', 'settings', 'commandline'],
  classifiers = [],
  entry_points = {
      'console_scripts':
          ['django-settings-enable-app = django_settings_cmd.command_line:enable_app',
          'django-settings-disable-app = django_settings_cmd.command_line:disable_app'], 
  }
)