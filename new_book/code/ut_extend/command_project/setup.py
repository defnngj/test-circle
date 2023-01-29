from setuptools import setup

setup(
    name='kb',
    description="kb - 简单性能测试工具",
    version='0.1.0',
    py_modules=['run'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'kb = run:main',
        ],
    },
)
