from setuptools import setup
import pip.req

try:
    requirements = pip.req.parse_requirements('requirements.txt')
except:
    requirements = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

setup(
    name="gidown",
    version='0.1.0',
    author='BonsAI d.o.o',
    author_email='opensource@bonsai.hr',
    description='Wrapper library for Google Image Search',
    license='Apache 2.0',
    keywords="google image search download wrapper",
    url='https://github.com/bonsaihr/gidown',
    packages=['gidown'],
    zip_safe=True,
    install_requires=[
        'beautifulsoup4',
        'requests'
      ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
    ],
)
