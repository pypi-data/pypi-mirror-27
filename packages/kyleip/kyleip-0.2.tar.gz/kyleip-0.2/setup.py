from setuptools import setup, find_packages


install_requires = [
    'setuptools',

    ]

setup(name='kyleip',
      version='0.2',
      description='The kyleip project',
      packages=find_packages(),
      url='https://github.com/kyle38459/kyleip',
      download_url='https://github.com/kyle38459/kyleip/archive/0.1.tar.gz',
      keywords=['testing', 'logging', 'ip'],
      install_requires=install_requires
      )
