import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xchain", # Replace with your own username
    version="0.0.1",
    author="kobibarhanin",
    author_email="",
    description="A generic blockchain library",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/kobibarhanin/xchain",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
