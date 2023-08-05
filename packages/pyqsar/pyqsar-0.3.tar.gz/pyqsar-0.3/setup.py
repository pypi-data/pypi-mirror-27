from setuptools import setup, find_packages
from os import path

setup_requires = [ ]


install_requires = [
    'numpy>=1.12.0',
    'setuptools>=27.2.0',
    'pandas>=0.20.1',
    'scikit-learn>=0.18.1',
    'matplotlib>=2.0.2',
    'ipywidgets>=6.0.0',
    'ipython>=5.3.0',
    'bokeh>=0.12.5',
    'joblib>=0.11'
    ]


here = path.abspath( path.dirname( __file__ ) )
with open( path.join( here, 'README.rst' ), 'r' ) as f :
    readme = f.read( )

dependency_links = [
]

setup(

        name='pyqsar',

        version='0.3',

        url='https://github.com/crong-k/pyqsar_tutorial',

        license='MIT License',

        description='Feature selection & QSAR modeling package',

        long_description=readme,

        author='Sinyoung Kim',
        author_email='crong24601@gmail.com',

        packages=[ "pyqsar" ],
        include_package_data=True,

        install_requires=install_requires,

        setup_requires=setup_requires,
        dependency_links=dependency_links,

        keywords=['QSAR','feature selection','machine learning'],

        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 2.7',
            'License :: OSI Approved :: MIT License',
        ]

)
