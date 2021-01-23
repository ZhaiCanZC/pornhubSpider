import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pornhubSpider",
    version="1.1.0",
    author="ZoinkCN",
    author_email="zoinkcn@outlook.com",
    description="A simple spider of Pornhub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZoinkCN/pornhubSpider",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "requests",
        "Js2Py",
        "beautifulsoup4",
        "lxml"
        ]
)
