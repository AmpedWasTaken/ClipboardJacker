from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clipreplacer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A clipboard text replacement tool using regex patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/clipreplacer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires=">=3.6",
    install_requires=[
        "pyperclip>=1.8.2",
    ],
    entry_points={
        "console_scripts": [
            "clipreplacer=clipreplacer.main:main",
        ],
    },
) 