from setuptools import setup

setup(
    name="gpxconverter",
    version="0.3",

    description="gpx to csv converter",

    license="MIT",
    url="https://github.com/linusyoung/GPXConverter",
    download_url="""https://github.com/linusyoung/
    GPXConverter/archive/0.3.tar.gz""",

    author="Linus Yang",
    author_email="linusyoungrice@gmail.com",

    classifiers=[
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    packages=["gpxconverter"],

    entry_points={
        "console_scripts": [
            "gpxconverter = gpxconverter.__main__:main",
        ],
    },
)
