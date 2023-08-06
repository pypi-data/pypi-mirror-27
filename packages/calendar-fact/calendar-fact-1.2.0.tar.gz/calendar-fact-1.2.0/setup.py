from setuptools import setup
from calendar_fact import __version__

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()


setup(
    name='calendar-fact',
    version=__version__,
    description='Generate calendar fact from xkcd.com/1930',
    long_description=long_description,
    author='Yehuda Deutsch',
    author_email='yeh@uda.co.il',
    url='https://gitlab.com/uda/calendar-fact',
    license='MIT',
    packages=["calendar_fact"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
    entry_points={
        'console_scripts': [
            'calendar-fact = calendar_fact:run'
        ],
    },
    python_requires='>=3.6',
)
