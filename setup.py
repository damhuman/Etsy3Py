from setuptools import setup, find_packages


setup(
    name='etsy3py',
    version='0.0.1',
    license='MIT',
    author="Anton Dasyuk, Ali-Abdulla",
    author_email='anton.dasyuk@gmail.com, alexukr1999@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/damhuman/Etsy3Py',
    keywords='etsy',
    install_requires=[
          'requests',
      ],

)
