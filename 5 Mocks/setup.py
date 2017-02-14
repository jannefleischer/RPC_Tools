# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name="arcpy",
    version="0.1",

    packages=find_packages('.', exclude=['ez_setup']),
    #namespace_packages=['rpctools'],

    package_dir={'': '.'},
    include_package_data=True,
    zip_safe=False,
    data_files=[
        ],
)
