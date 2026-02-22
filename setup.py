from setuptools import setup, find_packages

setup(
    name="hausverwaltung",
    version="0.1.0",
    description="A property management app built with PySide and Pandas",
    author="Your Name",
    packages=find_packages(),
    package_dir={"": "."},
    install_requires=[
        "PySide6",
        "pandas",
        "SQLAlchemy>=2.0.0",
    ],
    extras_require={
        "build": ["pyinstaller"],
    },
    entry_points={
        "gui_scripts": [
            "hausverwaltung = proment.main:main",
        ],
    },
    python_requires=">=3.11",
)
