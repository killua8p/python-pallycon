# python-pallycon

The Python SDK of [Pallycon](https://pallycon.com/)

## Installation

TODO

## Usage

```python
from pallycon import PallyConClient

# Initialise the client
client = PallyConClient(
    site_id="TUTO",
    site_key="lU5D8s3PWoLls3PWFWkClULlFWk5D8oC",
    access_key="LT2FVJDp2Xr018zf4Di6lzvNOv3DKP20",
    drm_type="Widevine",
    user_id="test-user",
    content_id="bigbuckbunny",
)

# Get the license token
license_token = client.license_token
```
