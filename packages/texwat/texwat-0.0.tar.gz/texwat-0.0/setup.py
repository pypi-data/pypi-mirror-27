from setuptools import setup

import texwat


setup(
    name='texwat',
    version=texwat.__version__,
    description='Convert Python objects to corresponding Latex source code.',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Documentation',
        'Topic :: Utilities'
    ],
    keywords='Latex tex converter utility',
    url='https://gitlab.com/Dominik1123/Texwat',
    author='Dominik Vilsmeier',
    author_email='dominik.vilsmeier1123@gmail.com',
    license='BSD-3-Clause',
    packages=[
        'texwat',
    ],
    install_requires=[
        'pylatex',
    ],
    python_requires='>=3.5',
    include_package_data=True,
    zip_safe=False
)
