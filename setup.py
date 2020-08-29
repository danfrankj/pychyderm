from setuptools import find_packages, setup

setup(
    # Package metadata
    name="pychyderm",
    versioning="post",
    version="0.0.0",
    author="danfrankj",
    author_email="NA",
    description=("pychyderm"),
    long_description="this is pychyderm",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    # Package details
    packages=find_packages(),
    include_package_data=True,
    # Dependencies
    setup_requires=["setupmeta"],
    install_requires=["networkx"],
)
