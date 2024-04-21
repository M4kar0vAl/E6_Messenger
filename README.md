## Installation

1. install requirements.txt
   - `pip install -r requirements.txt`
2. channels library use Redis as channel layer
   - Redis version MUST be 5.0.9+
   - OR
   - Use In-Memory channel layer instead of Redis
    ```python 
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }
    ```