# ras-common-utils
[![Build Status](https://travis-ci.org/ONSdigital/ras-common-utils.svg?branch=master)](https://travis-ci.org/ONSdigital/ras-common-utils)
[![codecov](https://codecov.io/gh/ONSdigital/ras-common-utils/branch/master/graph/badge.svg)](https://codecov.io/gh/ONSdigital/ras-common-utils)


Provides facilities for access to common facilities, establishing a set of patterns for use within RAS.

The facilities include:
 
- Supply an immutable config object which can easily be used with Flask, and enables separation of environment
specifics from service code (i.e. 12-factor compliant). This relies on a yaml-format config file, a minimal example
of which is below.

- Provide a familiar means of interfacing with common concepts, including Flask config & logging.

As an example of using the new configuration approach and logger:

`Main Python module...`
```Python
import os
import structlog
from ras_common_utils.ras_logger.ras_logger import configure_logger
from ras_common_utils.ras_config.flask_extended import Flask

logger = structlog.get_logger()

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_yaml(os.path.join(app.root_path, 'config/config.yaml'))
    
    configure_logger(app.config)

    from my_ras_service.views import my_view
    app.register_blueprint(my_view, url_prefix='/my_ras_service/v1')

    scheme, host, port = app.config['scheme'], app.config['host'], app.config['port']
    app.run(debug=app.config.get('debug'), port=port)

```

`And in some_other_module.py...`

```Python
from structlog import get_logger

logger = get_logger()

def some_function():
    logger.info('Doing some logging')
```

`config/config.yaml`
```Yaml
service:
    name: my-ras-service
    version: 1.0.0
    scheme: http
    host: 0.0.0.0
    port: 8080
```

## Testing

```sh
$ pip install -e . --upgrade
$ pip install pipenv --upgrade
$ pipenv install --dev
$ pipenv run ./scripts/test.sh
```

## Build / release

Using [zest.releaser](https://pypi.python.org/pypi/zest.releaser).

Please read the zest.releaser documentation to see the available commands and what they do.
In general, run the command `fullrelease` in the project root. To suppress prompts, run `fullrelease --no-input`.
