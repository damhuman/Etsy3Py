from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='etsy3py',
    description='ETSY API v3 Client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.0.2',
    license='MIT',
    author="Anton Dasyuk, Ali-Abdulla",
    author_email='anton.dasyuk@gmail.com, alexukr1999@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/damhuman/Etsy3Py',
    keywords=['etsy', 'api', 'client', 'etsy v3 api'],
    install_requires=[
        'requests',
        'requests-oauthlib',
        'mypy',
    ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ]

)
