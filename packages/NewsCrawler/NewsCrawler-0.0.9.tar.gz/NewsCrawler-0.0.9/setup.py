from distutils.core import setup

setup(
    name='NewsCrawler',
    version='0.0.9',
    packages=['crawler', 'config'],
    package_data={'': ['config.yaml']},
    scripts=['bin/news_crawler'],
    install_requires=['pyyaml'],
    author='Ash Prince',
    author_email='i7629228@bournemouth.ac.uk',
    description='Creates yaml logs of latest article and twitter data'
)
