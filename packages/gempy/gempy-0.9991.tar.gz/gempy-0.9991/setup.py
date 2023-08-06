from setuptools import setup

setup(
    name='gempy',
    version='0.9991',
    packages=['gempy'],
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'theano',
        'scikit-image',
        'seaborn'
    ],
    url='https://github.com/cgre-aachen/gempy',
    download_url='https://github.com/cgre-aachen/gempy/archive/0.9991.tar.gz',
    license='MIT',
    author='Miguel de la Varga, Alexander Schaaf',
    author_email='varga@aices.rwth-aachen.de',
    description='An Open-source, Python-based 3-D structural geological modeling software.',
    keywords=['geology', '3-D modeling', 'structural geology', 'uncertainty']
)
