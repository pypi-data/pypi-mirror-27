from setuptools import setup

def readme():
    with open("README.rst") as f:
        return f.read()

setup(name="logslacker",
      version="0.0.1dev1",
      description="Log handler wrapper for the Slack Python API",
      long_description=readme(),
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7",
          "Topic :: System :: Logging"
      ],
      keywords="slack logger handler log loghandler",
      url="http://github.com/inJeans/LogSlacker",
      author="Christopher Jon Watkins",
      author_email="christopher.watkins@me.com",
      license="MIT",
      packages=["logslacker"],
      install_requires=[
          "slackclient",
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite="nose.collector",
      tests_require=["nose"],
      entry_points = {
          "console_scripts": ["logslacker-test=logslacker.command_line:main"],
      })
