from setuptools import setup, PEP420PackageFinder


setup(
    name='tangled.site',
    version='1.0a5',
    description='Simple site/blog/cms',
    long_description=open('README.rst').read(),
    url='https://tangledframework.org/',
    download_url='https://github.com/TangledWeb/tangled.site/tags',
    author='Wyatt Baldwin',
    author_email='self@wyattbaldwin.com',
    packages=PEP420PackageFinder.find(include=['tangled*']),
    include_package_data=True,
    install_requires=[
        'tangled.mako>=1.0a5',
        'tangled.sqlalchemy>=0.1a5',
        'tangled.web>=1.0a12',
        'bcrypt>=3.1.4',
        'Markdown>=2.6.10',
        'SQLAlchemy>=1.1.15',
    ],
    entry_points="""
    [tangled.scripts]
    site = tangled.site.command

    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
