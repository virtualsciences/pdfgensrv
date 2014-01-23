from setuptools import setup, find_packages

version = '0.1.4'

setup(name='pdfgensrv',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[],
      keywords='',
      author='Jan Murre',
      author_email='jan.murre@pareto.nl',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'otto',
          'wsgiutils',
      ],
      entry_points={
        'paste.app_factory': [
            'main=pdfgensrv.server:app_factory',
            ]},
      )
