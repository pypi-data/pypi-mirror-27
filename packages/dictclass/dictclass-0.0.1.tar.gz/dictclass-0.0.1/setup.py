from setuptools import setup

setup(
    name='dictclass',
    author='Daniel Hilst Selli',
    author_email='danielhilst@gmail.com',
    version='0.0.1',
    license='Apache 2.0',
    description='Write inheritable dicts using class syntax.',
    url='https://github.com/dhilst/py-dictclass',
    download_url='https://github.com/dhilst/py-dictclass/archive/master.zip',
    py_modules=['dictclass'],
    test_suite='dictclass.test',
    keywords='development',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
