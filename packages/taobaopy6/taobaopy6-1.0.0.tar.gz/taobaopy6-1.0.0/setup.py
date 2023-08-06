from setuptools import setup

__author__ = 'Sempr'

setup(
    name='taobaopy6',
    version='1.0.0',
    url='https://github.com/sempr/taobaopy6',
    license='BSD',
    author='Fred Wang',
    author_email='taobao-pysdk@1e20.com',
    description='A Very Easy Learned Python SDK For TaoBao.com API Support python2 and python3',
    long_description=__doc__,
    packages=['taobaopy6'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['requests==2.18.4', 'future==0.16.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
