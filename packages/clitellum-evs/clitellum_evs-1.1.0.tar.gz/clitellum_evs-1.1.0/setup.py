from setuptools import setup

setup(
    name='clitellum_evs',
    version='1.1.0',
    packages=['clitellum_evs'],
    package_dir={'clitellum_evs': 'src'},
    url='',
    license='APACHE',
    author='Sergio.Bermudez',
    author_email='sbermudezlozano@gmail.com',
    description='Event Sourcing Library',
    extras_require={
    },
    requires=['pymongo']
)
