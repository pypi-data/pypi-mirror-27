from setuptools import setup, find_packages

setup(name='wcxf',
      version='0.2.5',
      author='David M. Straub, Jason Aebischer',
      author_email='david.straub@tum.de, jason.aebischer@tum.de',
      license='MIT',
      packages=find_packages(),
      package_data={
        'wcxf': ['data/*.yml',
                 'bases/*']
      },
      install_requires=['pyyaml', 'ckmutil>=0.3'],
      tests_require=['nose', 'smeftrunner'],
      entry_points={
        'console_scripts': [
            'wcxf = wcxf.cli:wcxf_cli',
            'wcxf2eos = wcxf.cli:eos',
        ]
      },
    )
