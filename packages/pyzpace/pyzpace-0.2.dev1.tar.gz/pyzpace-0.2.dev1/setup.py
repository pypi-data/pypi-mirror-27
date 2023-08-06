from setuptools import setup, find_packages

setup(name='pyzpace',
      version='0.2dev1',
      description='Zach Pace\'s astronomy-related python tools',
      url='http://github.com/zpace/pyzpace',
      author='Zach Pace',
      author_email='zpace@astro.wisc.edu',
      license='MIT',
      zip_safe=False,
      python_requires='>=3',
      install_requires=['numpy', 'scipy', 'matplotlib', 'astropy',
                        'markdown'],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True,
      packages=find_packages(
           exclude=['contrib', 'docs', 'tests*']))
