from setuptools import setup, find_packages

setup(
    name='brainiak-cloud',
    version='0.0.1',
    install_requires=[
        'click',
        'ipython',
        'requests',
        'pathos',
        'tqdm',
        'watchdog',
        'flask',
        'flask_session',
        'binaryornot',
        'cfncluster',
        'matplotlib',
        'pandas',
        'nilearn',
        'numpy',
        'scipy==0.19.1',  # See https://github.com/scipy/scipy/pull/8082
        'pybind11',
        'cython',
        'pika',
        'brainiak',
        'ipywidgets',
        'jupyter_contrib_nbextensions',
        'jupyter'
    ],
    author='Princeton Neuroscience Institute and Intel Corporation',
    author_email='dsuo@princeton.edu',
    url='https://github.com/brainiak/brainiak-cloud',
    description='Brain Imaging Analysis Kit Cloud',
    license='Apache 2',
    keywords='neuroscience, algorithm, fMRI, distributed, scalable',
    packages=find_packages(),
    python_requires='>=3.4',
    entry_points='''
        [console_scripts]
        watch=brainiak.cloud.watcher:watch
        serve=brainiak.cloud.server:serve
    '''
)
