from setuptools import setup

deps = []
deps.append("psutils")

setup(
    name='net-tester',
    version='0.0.1',
    author='Jomaker',
    author_email='hrunker@gmail.com',
    url='http://sparkera.net',
    description=u'简单网速测试工具',
    packages=['net-tester'],
    install_requires=deps
)