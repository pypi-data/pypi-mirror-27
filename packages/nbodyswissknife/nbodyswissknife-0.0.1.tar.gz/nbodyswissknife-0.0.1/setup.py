from distutils.core import setup, Extension
import numpy


def requirements():
    """
    Read the content of requirements.txt and return them as a list
    :return: list
    """
    return map(str.strip, open('requirements.txt').readlines())


module1 = Extension(
    "nbodyswissknife.potential_cpu",
    include_dirs=[numpy.get_include()],
    libraries=['pthread', 'gomp'],
    extra_compile_args=[
        '-fno-strict-aliasing',
        '-fopenmp',
        '-std=gnu11'
    ],
    sources=['nbodyswissknife/backends/cpu/potential.c']
)

setup(
    name='nbodyswissknife',
    version='0.0.1',
    description='Package with various handy tools for nbody calculations',
    author='Mher Kazandjian',
    author_email='mherkazandjian@gmail.com',
    url='https://github.com/mherkazandjian/nbodyswissknife',
    download_url='https://github.com/mherkazandjian/nbodyswissknife/archive/master.zip',
    keywords=['physics', 'nbody', 'numerics', 'simulation', 'astrophysics'],
    requires=requirements(),
    packages=['nbodyswissknife'],
    ext_modules=[module1]
)

