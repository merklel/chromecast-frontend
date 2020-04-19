import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chromecast_volumecontrol", # Replace with your own username
    version="0.0.5",
    author="Lukas Merkle",
    author_email="lukas.merkle@live.de",
    description="Control Chromecast Volume",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/merklel/chromecast-frontend",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={'': ['ico/*.png']},
    python_requires='>=3.6',
    scripts=['cc_volumecontrol'],
    install_requires=[
        "pychromecast",
            ]
)
