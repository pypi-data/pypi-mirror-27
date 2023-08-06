from setuptools import setup
 
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
 

setup(
    name = "flatpakdev",
    packages = ["flatpakdev"],
    entry_points = {
        "console_scripts": ['flatpakdev = flatpakdev.flatpakdev:main']
        },
    version = 0.1,
    description = "Python command line tool that wrapps Flatpak-Builder",
    long_description = long_descr,
    author = "Kevin Lopez Andrade",
    author_email = "kevin@kevlopez.com",
    url = "https://github.com/kevinlopezandrade/FlatpakDev"
)
