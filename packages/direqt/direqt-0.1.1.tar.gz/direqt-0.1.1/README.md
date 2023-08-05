# Direqt Software Development Kit for Python

Direqt is an advertising platform for chatbots.

The Direqt Software Development Kit (SDK) for Python contains library code and examples designed to enable developers to
integrate ads into chatbot agents written in Python. This SDK current supports only RCS agents using Google's RBM APIs.

    $ pip install direqt    # install library locally (or into a virtualenv)
    
Before using the SDK, you need an API key from <https://www.direqt.io>. You will also need to have configured one or
more ad units for your agent's network in order to dynamically fetch ads.

### Quick Peek:

```python
from direqt import DireqtClient
API_KEY = "<API_KEY>" # from management console

direqt = DireqtClient(API_KEY)    # create SDK instance

def deliver_ad(msisdn, ad_unit): 
    """Fetch an ad for the specified ad_unit, and deliver it to the user."""
    rbm_message = direqt.fetch(ad_unit=ad_unit)
    resp, content = http.request(
        "/v1/phones/{0}/agentMessages?messageId={1}".format(msisdn, uuid.uuid4()),
        "POST",
        rbm_message,
        {'Content-Type': 'application/json'})
```

## Documentation

See <http://direqt-sdk-python.readthedocs.org/en/latest/> for documentation on using Direqt with Python.

Copyright (c) 2017 Direqt Inc. All Rights Reserved.

