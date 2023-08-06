from setuptools import setup

with open("README.rst") as file:
    long_description = file.read()

setup(
    name = "alpaca_isp",
    version = "0.2.0",
    author = "Clayton G. Hobbs",
    author_email = "clay@lakeserv.net",
    description = "In-system programming tool for LPC microcontrollers",
    license = "Apache",
    keywords = "lpc microcontroller mcu flash isp",
    url = "https://git.clayhobbs.com/clay/alpaca_isp",
    packages = ['alpaca_isp'],
    long_description = long_description,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Embedded Systems"
    ],
    install_requires=["pyserial>=3.4", "IntelHex>=2.1"],
    entry_points = {
        "console_scripts": [
            "alpaca_isp=alpaca_isp:main"
        ]
    }
)
