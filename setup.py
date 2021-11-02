from setuptools import setup

setup(
    name='Mjolk',
    version='0.0.1',
    description='A library for enforcing Flask endpoint parameter validation',
    url='https://github.com/Shopify/mjolk',
    license='MIT',
    author='Shopify Data Acquisition',
    author_email='data-acquisition@shopify.com',
    long_description=__doc__,
    py_modules=[],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['Flask'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
        "Programming Language :: Python :: 3.6",
    ])
