from setuptools import setup, find_packages

setup(
    name="pixian_ai",
    version="0.0.1",
    python_requires=">3.6",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Mitchell Bregman",
    author_email="mitch@mitchbregs.com",
    description="Python SDK for pixian.ai",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="pixian.ai remove background",
    url="https://github.com/mitchbregs/pixian-ai",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
