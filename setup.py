from setuptools import setup, find_packages

setup(
    name="sythonlab_travel_repo",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    url="https://github.com/sythonlab/SythonLab-Travel-Repo",
    author="José Angel Alvarez Abraira",
    author_email="sythonlab@gmail.com",
    description="Sython Lab Travel Repository",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
