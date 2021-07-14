import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TableType",
    version="0.0.1",
    author="Magnus Martínez",
    author_email="shainnymarcruz345@gmail.com",
    description="Módulo Python para el procesamiento de tablas, permite la selección de celdas en cualquier dirección.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/magnusmartinez/pytable.git",
    project_urls={
       "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GENERAL PUBLIC",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", ),
    python_requires=">=3.6",
)