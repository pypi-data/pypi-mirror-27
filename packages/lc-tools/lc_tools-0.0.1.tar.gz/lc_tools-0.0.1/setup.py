# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='lc_tools',
    version='0.0.1',
    keywords=("lc_tools", "sinianluoye"),
    description=(
        'the tool create by sinianluoye'
    ),
    long_description=open('README.rst').read(),
    author='sinianluoye',
    author_email='372900338@qq.com',
    maintainer='sinianluoye',
    maintainer_email='372900338@qq.com',
    license='GPL',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/sinianluoye/lc_tools',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[]
)