from setuptools import setup

setup(name="gkraz",
        version="0.1",
        description="Calculator for the terminal",
        url="http://theovention.de",
        author="Theo Heimel",
        author_email="info@theovention.de",
        license="MIT",
        packages=["gkraz"],
        install_requires=[
            "prompt_toolkit",
            "pygments",
            "numpy",
            "matplotlib",
            "terminaltables"
        ],
        entry_points={
            "console_scripts": [
                "gkraz = gkraz.__main__:main"
            ]
        },
        zip_safe=False)
