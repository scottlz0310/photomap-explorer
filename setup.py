#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PhotoMap Explorer - GPS付き画像の撮影地点を地図表示する軽量ツール
Setup script for distribution packaging
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="photomap-explorer",
    version="2.1.2",
    author="菅原浩恭",
    author_email="hiroyasu@sugaraweb.com",  # 実際のメールアドレスに変更してください
    description="GPS付き画像から撮影地点を地図に自動表示する軽量ツール",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/sugawara-hiroyasu/PhotoMapExplorer",  # GitHubリポジトリURL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-qt>=4.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "photomap-explorer=main:main",
        ],
    },
    package_data={
        "": ["*.md", "*.txt", "*.html", "*.png", "*.ico"],
        "assets": ["*"],
        "docs": ["*"],
    },
    include_package_data=True,
    keywords="gps exif map photo image viewer photography geolocation",
    project_urls={
        "Bug Reports": "https://github.com/sugawara-hiroyasu/PhotoMapExplorer/issues",
        "Documentation": "https://github.com/sugawara-hiroyasu/PhotoMapExplorer/blob/main/README.md",
        "Source": "https://github.com/sugawara-hiroyasu/PhotoMapExplorer",
        "Changelog": "https://github.com/sugawara-hiroyasu/PhotoMapExplorer/blob/main/CHANGELOG.md",
    },
)
