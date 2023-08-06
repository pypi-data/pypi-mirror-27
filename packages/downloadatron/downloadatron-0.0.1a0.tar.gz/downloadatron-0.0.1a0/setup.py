from setuptools import setup, find_packages

install_requires=[
        'requests'
]

setup(name='downloadatron',
        version='0.0.1alpha',
        description='toolkit for downloading files from the internet',
        url='https://github.com/rutherford/downloadatron',
        author='Matt Rutherford',
        author_email='rutherford@clientsideweb.net',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
        ],
        packages=find_packages(),
        zip_safe=False)
