#!/usr/bin/env python

from setuptools import setup

setup(
    name="pyocr",
    # Don't forget to update
    # - src/pyocr/pyocr.py:VERSION
    # - setup.py:version
    # - setup.py:download_url
    # - ChangeLog
    # - push
    # - tag
    # - python3 ./setup.py sdist upload
    version="0.5",
    description=("A Python wrapper for OCR engines (Tesseract, Cuneiform,"
                 " etc)"),
    keywords="tesseract cuneiform ocr",
    url="https://github.com/openpaperwork/pyocr",
    download_url="https://github.com/openpaperwork/pyocr/archive/0.5.zip",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later"
        " (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Multimedia :: Graphics :: Capture :: Scanners",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    license="GPLv3+",
    author="Jerome Flesch",
    author_email="jflesch@openpaper.work",
    packages=[
        'pyocr',
        'pyocr.libtesseract',
    ],
    package_dir={
        'pyocr': 'src/pyocr',
        'pyocr.libtesseract': 'src/pyocr/libtesseract',
    },
    data_files=[],
    scripts=[],
    zip_safe=True,
    install_requires=[
        "Pillow",
        "six",
    ],
)
