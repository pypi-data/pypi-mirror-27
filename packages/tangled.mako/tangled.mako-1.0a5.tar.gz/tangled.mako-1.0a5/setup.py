from setuptools import setup


setup(
    name='tangled.mako',
    version='1.0a5',
    description='Tangled Mako integration',
    long_description=open('README.rst').read(),
    url='http://tangledframework.org/',
    download_url='https://github.com/TangledWeb/tangled.mako/tags',
    author='Wyatt Baldwin',
    author_email='self@wyattbaldwin.com',
    include_package_data=True,
    packages=[
        'tangled',
        'tangled.mako',
        'tangled.mako.tests',
    ],
    install_requires=[
        'tangled.web>=1.0a12',
        'Mako>=1.0',
    ],
    extras_require={
        'dev': [
            'tangled[dev]>=1.0a11',
            'tangled.web[dev]>=1.0a12',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
