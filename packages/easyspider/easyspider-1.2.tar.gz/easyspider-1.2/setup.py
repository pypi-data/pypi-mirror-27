# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Email:  hhczy1003@163.com
# @Date:   2017-08-01 20:37:27
# @Last Modified by:   serena
# @Last Modified time: 2017-12-05 16:22:20

from setuptools import setup

setup(
    name="easyspider",
    version="1.2",
    # author="yiTian.zhang",
    author="hhczy",
    author_email="hhczy1003@163.com",
    packages=["easyspider"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": ["easyspider = easyspider.core.cmdline:execute"]
    }
)
