import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timesheet-utils",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="to fill",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests~=2.23.0",
        "werkzeug==0.16.1",
        "flask~=1.1.2",
        "flask_restplus",
        "sqlalchemy~=1.3.17",
        "py_eureka_client~=0.7.4"
    ]
)
