# python-pallycon

The Python SDK for [Pallycon](https://pallycon.com/)

## Installation

```shell script
$ pip install python-pallycon
```

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
    license_rule={
        "playback_policy": {"limit": True, "persistent": False, "duration": 3600}
    },
)

# Get the license token
license_token = client.license_token
```
