from setuptools import setup, find_packages

DESCRIPTION = "Light wrapper for Microsoft's Cognitive Services API to facilitate data gathering for machine learning."
VERSION = '0.0.2'
LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.md').read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    "Programming Language :: Python :: 3",
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

KEYWORDS = ['Microsoft', 'Cognitive Services', 'API', 'Search', 'Image Search', 'Machine Learning', 'Image Scraping']

INSTALL_REQUIRES = [
    'requests',
]

setup(
    name='py-ms-cognitive-ml',
    packages=find_packages(),
    version=VERSION,
    author=u'Oliver Reid',
    author_email='reiol787@student.otago.ac.nz',
    url='https://github.com/beardo01/py-ms-cognitive-ml',
    license='MIT',
    keywords=KEYWORDS,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3'
)
