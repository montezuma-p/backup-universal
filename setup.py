from setuptools import setup, find_packages

setup(
    name="backup-universal",
    version="1.2.0",
    description="Sistema inteligente de backup para Linux",
    author="Montezuma",
    author_email="",
    url="https://github.com/montezuma-p/backup-universal",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "rich>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "pytest-xdist>=3.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "backup=backup.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
