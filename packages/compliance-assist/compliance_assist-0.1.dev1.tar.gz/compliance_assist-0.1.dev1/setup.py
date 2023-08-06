from setuptools import setup, find_packages

setup(
    name = 'compliance_assist', # Name of PyPI package
    version = '0.1dev1', # First version
    author = 'Matt Lewis',
    author_email = "matt@csiga.org",
    packages = find_packages(exclude=["sensitive"]),
    install_requires = [
        "selenium>=3.8.0"
    ],
    python_requires = ">=3",
    url = "https://github.com/mattl3w1s/sjc-compliance-assist",
    license="MIT",
    description="Webdriver for Compliance Assist scripting, built on Selenium",
    long_description = "Webdriver for Compliance Assist scripting, built on Selenium",
    zip_safe=False,
    include_package_data=True,
)