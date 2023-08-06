# nextbus_client [![Build Status](https://travis-ci.org/compybara/nextbus_client.svg?branch=master)](https://travis-ci.org/compybara/nextbus_client)

This module attempts to implement a native Python 3 client for interacting with the Nexbus service's Public XML Feed.

It provides a client class which implements the available commands, and a number of classes to model the data returned 
by the XML feed as Python objects. Each object provides a `to_dict()` method to allow for easy conversion of the XML
data to JSON.

This module was developed following the [specification document](https://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf)
provided by the Nextbus service. 

## Getting Started

To initialize the client module use the `Client` class. By default it will use the base URL specified in the document 
and the recommended request headers (`Accept-Encoding: gzip, deflate`). You can override these in the constructor if 
necessary. 

For example:

    import nextbus_client
    nb = nextbus_client.Client(api_url="http://www.nextbusalternative.com/publicXMLFeed")
    agencies = nb.agency_list()

### Prerequisites

- Python 3 (This module was developed and tested primarily with Python 3.6)
- pip 
- setuptools 

### Installing

You can clone this repo and install the package locally using setuptools:


    git clone https://github.com/compybara/nextbus_client.git
    cd nextbus_client
    python setup.py install 


You can also install directly from this repository using `pip`

    pip install git+git://github.com/compybara/nextbus_client.git


## Testing

This module uses [behave](https://pythonhosted.org/behave/) for testing. Tests are stored in the `/features` directory.

You can run `behave` directly from the command line, or use the `setuptools` script.

### Testing with behave

To run tests using `setuptools`:
    
    python setup.py test
    
A `.behaverc` config file is included with this repository. If you'd like to use `behave` with your own configuration
you can use the `--rcfile` option:

    python setup.py test --rcfile /path/to/mybehaverc


To run the `behave` cli tool directly:
    
    behave features/

### Style tests

The `setup.py` configuration includes a command to run `Pylint` for code linting. 

You can run it with

    python setup.py lint

A custom linter configuration is included in this repo as`.pylintrc`. You can specify a custom configuration using the
`--rcfile` option:

    python setup.py lint --rcfile /path/to/mypylintrc

## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct.

## Versioning

This project follows the [SemVer](http://semver.org/) specification for versioning. 
Available versions are stored as [tags on this repository](https://github.com/compybara/nextbus_client/tags). 

## Authors

* **Adam Duston** - [compybara](https://github.com/compybara)

## License

This project is licensed under the BSD 3 Clause license - see the [LICENSE](./LICENSE) file for details
