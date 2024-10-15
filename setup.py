from setuptools import setup, find_packages

setup(
    name="frame",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "colorama",
        "openai",
        "tenacity",
        "textual",
        "pydantic",
    ],
    extras_require={
        "dev": ["pytest", "pytest-asyncio", "black", "isort"],
    },
    entry_points={
        "console_scripts": [
            "frame=frame.__main__:main",
        ],
    },
)
