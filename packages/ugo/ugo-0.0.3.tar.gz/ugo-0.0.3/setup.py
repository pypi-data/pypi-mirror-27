from setuptools import setup, find_packages

setup(
    name='ugo',
    version='0.0.3',
    keywords=('ugo', 'tustack'),
    description='ugo base project.',
    long_description=open('README.rst').read(),
    py_modules=['ugo'],
    packages=find_packages(),
    scripts=['scripts/shows.py'],
    install_requires=[],
    platforms=["all"],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    license='MIT License',
    author='Showdom',
    author_email='1063951161@qq.com',
    url='https://github.com/showdom/ugo',
)
