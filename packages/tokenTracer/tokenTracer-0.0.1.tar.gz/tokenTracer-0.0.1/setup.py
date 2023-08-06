
from setuptools import setup, find_packages

setup(name="tokenTracer", 
      version="0.0.1", 
      description="Keycloak token endpoint packet sniffer for HTTP request/response authentication tokens", 
      long_description="Packet sniffer command-line utility that filters for HTTP packets. \
                        The packet sniffer has filters for authentication request/response \
                        pairs to the Keycloak token endpoint that exchange access tokens. \
                        The sniffer may pretty-print or write JSON to either stdout or to an output file. \
                        The utility may either sniff live from a network interface or read from a packet capture file.",
      url="https://github.com/Bio-Core/tokenTracer", 
      author="Dale Dupont", 
      author_email="dale.dupont@uhnresearch.ca", 
      license="MIT", 
      classifiers=["Development Status :: 3 - Alpha", 
                  "Intended Audience :: Developers", 
                  "Intended Audience :: System Administrators",
                  "Topic :: Software Development :: Debuggers",
                  "License :: OSI Approved :: MIT License", 
                  "Programming Language :: Python :: 2", 
                  "Programming Language :: Python :: 2.7",
                  "Natural Language :: English",
                  "Topic :: System :: Networking :: Monitoring",
                  "Topic :: Utilities",
                  "Topic :: System :: Logging"], 
      keywords="utility command-line debugging logging logger monitoring monitor network packet sniffer sniffing HTTP authentication token tokens filter",
      packages=find_packages(exclude=['docs', 'tests']),
      install_requires=["pyshark"],
      python_requires=">=2.7",
      include_package_data=True,
      entry_points={
          "console_scripts": ["tokenTracer = tokenTracer.tracer:main"]
      }) 
