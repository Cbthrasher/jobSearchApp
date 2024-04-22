from setuptools import setup, find_packages

setup(
    name='job_search_app',
    version='1.0.0',
    author='Chris Thrasher',
    description='Automated job search application',
    packages=find_packages(),
    install_requires=[
        'tk',
        'selenium',
    ],
    entry_points={
        'console_scripts': [
            'job_search_app=job_search_app.main:main',
        ],
    },
)
