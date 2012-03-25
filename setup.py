from setuptools import setup, find_packages

setup(
    name='django-mixins',
    version='0.1.8',
    keywords='django, mixins, models, managers, ajax',
    author='Aleksandr Aibulatov',
    author_email='zap.aibulatov@gmail.com',
    url='https://github.com/Zapix/mixins',
    license='BSD',
    package_dir={'mixins': 'mixins'},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Communications",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
    ],
    zip_safe=False
)
