from setuptools import setup, find_packages

setup(
    name="sythonlab_travel_repo",
    version="1.1.3",
    packages=find_packages(),
    install_requires=[],
    url="https://github.com/sythonlab/SythonLab-Travel-Repo",
    author="José Angel Alvarez Abraira",
    author_email="sythonlab@gmail.com",
    description="Sython Lab Travel Repository",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_data={"sythonlab_travel_repo": ["logo.png"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
