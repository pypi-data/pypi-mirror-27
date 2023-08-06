"""
Basic Calculator
-------------

Basic Calculator is a simple calculator app with four basic
operations and a simple GUI.

You can get it by downloading it directly or by typing:

.. code:: bash

    $ pip install BasicCalculator

After it is installed you can start it by simply typing in your terminal:

.. code:: bash

    $ calc

"""

from setuptools import setup


setup(name="BasicCalculator",
      version="0.1",
      description="A simple calculator app",
      long_description=__doc__,
      url="https://github.com/Urosh91/Bitcoin-Value",
      author="Uroš Jevremović",
      author_email="jevremovic.uros91@gmail.com",
      packages=["Calculator"],
      entry_points={
          "console_scripts": ["calc=Calculator.calculator:main"],
      },
      )

__author__ = "Uroš Jevremović"
