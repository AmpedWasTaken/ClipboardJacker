from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clipboardjacker",
    version="0.1.3",
    author="AmpedWastaken",
    author_email="ampedwastaken@gmail.com",
    description="A powerful Python tool for clipboard text replacement and monitoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ampedwastaken/ClipboardJacker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyperclip>=1.8.2",
    ],
    entry_points={
        "console_scripts": [
            "clipboardjacker=clipboardjacker.main:run_clipboard_jacker",
        ],
    },
) 