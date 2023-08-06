from distutils.core import setup

setup(
    name='pip_test_swagger',
    version='0.1.1',
    packages=['drf_swagger'],
    url='https://github.com/koyouhun/drf_swagger',
    license='BSD',
    author='YouHyeon Ko',
    author_email='koyouhun@gmail.com',
    description='Django REST Framework + Swagger',
    keywords=['django', 'swagger', 'api', 'documentation'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7'
      ],
    install_requires=[
        'Django<=1.11',
        'PyYAML',
        'six',
        'uritemplate',
        'djangorestframework>=3.6.0'
    ]
)
