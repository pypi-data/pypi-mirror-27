import sys
from setuptools import setup, find_packages

setup(name='lambda-local-python',
      version="0.0.4",
      description="Run/debug python aws lambda functions locally",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'License :: OSI Approved :: MIT License'
      ],
      keywords="AWS Lambda, vscode, Visual Studio Code, code",
      author="Will Wenhua Yang",
      author_email="will.whyang@gmail.com",
      url="https://github.com/willwhy/lambda-local-python",
      license="MIT",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'lambda-local-python=lambda_local:invoke_function',
            'lambda-local-python-package=lambda_local:package_lambda'
        ]
      })
