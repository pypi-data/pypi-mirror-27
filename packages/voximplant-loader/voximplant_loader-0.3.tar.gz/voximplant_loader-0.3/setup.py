from setuptools import setup

setup(name='voximplant_loader',
      version='0.3',
      install_requires=[
          'requests',
      ],
      packages=['voximplant_loader'],
      entry_points={
          'console_scripts': ['voximplant-audio=voximplant_loader.audio:main'],
      },
      zip_safe=False)
