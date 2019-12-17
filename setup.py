import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aioparser",
    version="0.0.1",
    author="powersemmi aka Chebotarev Victor",
    author_email="powersemmi@gmail.com",
    description="A small async parser lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://192.168.192.193:10080/t",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)