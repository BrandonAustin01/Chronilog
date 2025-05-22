from setuptools import setup, find_packages

setup(
    name="chronilog",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rich>=13.0.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.11",
)
