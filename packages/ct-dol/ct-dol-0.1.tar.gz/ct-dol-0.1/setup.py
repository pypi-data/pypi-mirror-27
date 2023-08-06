from setuptools import setup

setup(
    name="ct-dol",
    version="0.1",
    description="A tool for pulling down ct unemployment as a dataframe",
    author="Jake Kara",
    author_email="jake@jakekara.com",
    license="GPL-3",
    install_requires=["pandas"],
    packages=["ct_unemployment"]
    
)
    
