from setuptools import setup, find_packages

setup(
    name="audio_generation_service",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.0",
        "uvicorn==0.27.0",
        "requests==3.9.1",
        "pydantic==2.5.3",
        "python-multipart==0.0.6",
    ],
)