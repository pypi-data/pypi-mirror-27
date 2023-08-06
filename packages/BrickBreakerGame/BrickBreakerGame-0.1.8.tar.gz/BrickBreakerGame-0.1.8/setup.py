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


setup(name="BrickBreakerGame",
      version="0.1.8",
      description="Brick Breaker game",
      long_description=__doc__,
      url="https://github.com/Urosh91/BrickBreaker",
      author="Uros Jevremović",
      author_email="jevremovic.uros91@gmail.com",
      packages=["BrickBreaker", "BrickBreaker.Bricks", "BrickBreaker.Scenes", "BrickBreaker.Shared"],
      install_requires=["pygame"],
      include_package_data=True,
      entry_points={
          "console_scripts": ["brickbreaker=BrickBreaker.brick_breaker:main"],
      },
      )

__author__ = "Uros Jevremović"
