import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mystical",
    version="1.0.0",
    author="Magnus Martínez",
    author_email="shainnymarcruz345@gmail.com",
    description="Paquete para el procesamiento de tablas, permite la selección de celdas en cualquier dirección.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/magnusmartinez/pytable.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", ),
    python_requires=">=3.6",
    install_requires=[
        "tabulate>=0.8.9"
    ]
)
