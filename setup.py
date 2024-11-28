from setuptools import setup, find_packages

setup(
    name="park-ease",
    version="0.1.0",
    description="Simple parking management app written in Python",
    author="Group 2TM19",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "park-ease = main:main",
        ],
    },
)