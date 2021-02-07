from unittest.mock import patch

import pytest

from pallycon.pallycon import PallyConClient


@pytest.fixture()
def client():
    return PallyConClient(
        site_id="TUTO",
        site_key="lU5D8s3PWoLls3PWFWkClULlFWk5D8oC",
        access_key="LT2FVJDp2Xr018zf4Di6lzvNOv3DKP20",
        drm_type="Widevine",
        user_id="test-user",
        content_id="bigbuckbunny",
    )


class TestPallyConClient:
    def test_license_rule(self, client):
        assert client.license_rule == {
            "playback_policy": {"limit": True, "persistent": False, "duration": 3600}
        }

    def test_encrypted_license_rule(self, client):
        assert (
            client.encrypted_license_rule
            == "bO9DzyQgtgfbSDWmqGgZXWZdWm7M4oZ4X0hC1hS6QNraiwLI0LwmNY+OfOh1L0KmtuH7NF1blUxep9YLWrNfSy4H/6swQW7pbjZnRqRguDQ="
        )

    def test_license_token(self, client):
        with patch(
            "pallycon.pallycon.PallyConClient._get_timestamp",
            return_value="2019-07-17T08:57:04Z",
        ):
            assert client.license_token == {
                "drm_type": "Widevine",
                "site_id": "TUTO",
                "user_id": "test-user",
                "cid": "bigbuckbunny",
                "token": "bO9DzyQgtgfbSDWmqGgZXWZdWm7M4oZ4X0hC1hS6QNraiwLI0LwmNY+OfOh1L0KmtuH7NF1blUxep9YLWrNfSy4H/6swQW7pbjZnRqRguDQ=",
                "timestamp": "2019-07-17T08:57:04Z",
                "hash": "0Zef3WHBbzQAR0oGf5KXn25G1TmvB2Bkvzv+7OqIWvQ=",
            }
