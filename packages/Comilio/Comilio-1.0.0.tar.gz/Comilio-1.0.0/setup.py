from distutils.core import setup


setup(
    name="Comilio",
    version="1.0.0",
    description="Client library to send SMS using Comilio SMS Gateway API (https://www.comilio.it)",
    author="Comilio",
    author_email="tech@comilio.it",
    license="MIT",
    url="http://github.com/comilio/python-sms-send",
    packages=["comilio"],
    install_requires=["requests"],
    keywords=["comilio", "sms", "api", "gateway"],
    classifiers=[
        "Topic :: Utilities",
        "Topic :: Communications :: Telephony",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
)
