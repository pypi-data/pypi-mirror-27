from setuptools import setup

version = "0.0.1"

requirements = [
    "graphics.py"
]

with open("README.rst") as file:
    readme = file.read()

setup(
    name="graphics.py-extra",
    version=version,
    description="Extra objects for the graphics.py package",
    long_description=readme,
    author="yurihs",
    url='https://github.com/yurihs/graphics_extra/',
    packages=["graphics_extra"],
    packagedir={"graphics_extra": "graphics_extra"},
    include_package_data=True,
    python_requires=">=3",
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
