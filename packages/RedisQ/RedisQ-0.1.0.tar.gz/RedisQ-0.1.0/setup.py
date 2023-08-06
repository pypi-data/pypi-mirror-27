from setuptools import setup, find_packages

PACKAGE = "RedisQ"
NAME = "RedisQ"
DESCRIPTION = "A task queue based on Redis RPOPLPUSH"
AUTHOR = "Taylor"
AUTHOR_EMAIL = "li.yanhong@tsimage.cn"
URL = "https://github.com/Tsimage/RedisQ"
VERSION = "0.1.0"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description="""
        From RedisQ import Qlist, Qjob
    """,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="GPL",
    url=URL,
    packages=['RedisQ'],
    package_data={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    ],
    zip_safe=False,
    install_requires=['redis', 'pickleshare'],
    entry_points={
       
    },
)
