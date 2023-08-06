"""
Brick Breaker
-------------

Brick Breaker is a simple game based on breaking bricks
and progressing through levels.

You can get it by downloading it directly or by typing:

.. code:: bash

    $ pip install BrickBreakerGame

After it is installed you can start it by simply typing in your terminal:

.. code:: bash

    $ brickbreaker

"""

from setuptools import setup

import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files("BrickBreaker/Assets")


setup(name="BrickBreakerGame",
      version="0.1",
      description="Brick Breaker game",
      long_description=__doc__,
      url="https://github.com/Urosh91/BrickBreaker",
      author="Uros Jevremović",
      author_email="jevremovic.uros91@gmail.com",
      packages=["BrickBreaker", "BrickBreaker.Bricks", "BrickBreaker.Scenes", "BrickBreaker.Shared"],
      install_requires=["pygame"],
      package_data={"": extra_files},
      entry_points={
          "console_scripts": ["brickbreaker=BrickBreaker.brick_breaker:main"],
      },
      )

__author__ = "Uros Jevremović"
