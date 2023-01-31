import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="extinction_coefficient",
    version="1.3",
    author="Zhang,Ruoyi",
    author_email="zry@mail.bnu.edu.cn",
    description="A package to inquire empirical extinction or reddening coefficients from far-ultraviolet (UV) to the mid-infrared (IR)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vnohhf/extinction_coeffcient",
    packages=setuptools.find_packages(),
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'numpy','pandas'
    ],
    python_requires='>=3',
)
