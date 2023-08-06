from setuptools import setup, find_packages

PACKAGE = "pyseri"
NAME = "pyseri"
DESCRIPTION = "a Python class serializer to make python class to dict, you can easy use it to convert a python class to json"
AUTHOR = "Taylor"
AUTHOR_EMAIL = "tank357@icloud.com"
URL = "https://github.com/TaylorHere/pyseri"
VERSION = "0.1.0"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description="""

    """,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="GPL",
    url=URL,
    packages=['pyseri'],
    package_data={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    ],
    zip_safe=False,
    install_requires=[],
    entry_points={
        # 'console_scripts': [
        #     'sample=sample:main',
        # ],
    },
)
