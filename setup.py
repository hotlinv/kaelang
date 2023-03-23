import setuptools #导入setuptools打包工具
import os
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="kaelang", 
    version="0.0.1",    #包版本号，便于维护版本
    author="Linux_23",    
    author_email="linux_23@163.com",    
    description="kæ语言，一门用python实现的中文编程语言。",
    long_description=long_description,    #包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://gitee.com/linux_23/kaelang",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',    #对python的最低版本要求
    entry_points={
        'console_scripts': ['kae=kae.lang:doo', 'kaecli=kae.lang:karuncli']
    },
    include_package_data=True,
    data_files=[
        ('', ['urlmap.yml']),
        ("dict", ["dict/"+f for f in os.listdir("dict")]),
        ("kalib", ["kalib/"+f for f in os.listdir("kalib")]),
        # ("kalib", ["kalib/"+f for f in os.listdir("kalib")]),
        # ('/usr/lib/systemd/system/', ['bin/*.service']),
    ],
)