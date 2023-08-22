from setuptools import setup, find_packages

"""
打包指令: python3 setup.py sdist
twine upload dist/*
"""

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pycqBot",
    version="0.5.1",
    description="go-cqhttp python 框架，可以用于快速塔建 bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="AGPL-3.0 License",
    url="https://github.com/FengLiuFeseliud/pycqBot",
    author="FengLiuFeseliud",
    author_email="17351198406@qq.com",
    packages=find_packages(),
    package_data={
        '': ['*.py'],
    },
    include_package_data=True,
    platforms="any",
    install_requires=[
        "requests",
        "websockets",
        "aiohttp",
        "aiofiles",
        "lxml",
        "pyyaml"
    ],
    python_requires='>=3.9'
)
