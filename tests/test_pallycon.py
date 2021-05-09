from unittest.mock import patch

import pytest

from pallycon import PallyConClient


@pytest.fixture()
def client():
    return PallyConClient(
        site_id="TUTO",
        site_key="lU5D8s3PWoLls3PWFWkClULlFWk5D8oC",
        access_key="LT2FVJDp2Xr018zf4Di6lzvNOv3DKP20",
        drm_type=PallyConClient.DrmType.WIDEVINE.value,
        user_id="test-user",
        content_id="bigbuckbunny",
        license_rule={
            "playback_policy": {"limit": True, "persistent": False, "duration": 3600}
        },
    )


class TestPallyConClient:
    def test_encrypted_license_rule(self, client):
        assert (
            client.encrypted_license_rule
            == "bO9DzyQgtgfbSDWmqGgZXWZdWm7M4oZ4X0hC1hS6QNraiwLI0LwmNY+OfOh1L0KmtuH7NF1blUxep9YLWrNfSy4H/6swQW7pbjZnRqRguDQ="
        )

    def test_license_token(self, client):
        with patch(
            "pallycon.PallyConClient._get_timestamp",
            return_value="2019-07-17T08:57:04Z",
        ):
            # {
            #     "drm_type": "Widevine",
            #     "site_id": "TUTO",
            #     "user_id": "test-user",
            #     "cid": "bigbuckbunny",
            #     "token": "bO9DzyQgtgfbSDWmqGgZXWZdWm7M4oZ4X0hC1hS6QNraiwLI0LwmNY+OfOh1L0KmtuH7NF1blUxep9YLWrNfSy4H/6swQW7pbjZnRqRguDQ=",
            #     "timestamp": "2019-07-17T08:57:04Z",
            #     "hash": "0Zef3WHBbzQAR0oGf5KXn25G1TmvB2Bkvzv+7OqIWvQ=",
            # }
            assert (
                client.license_token
                == "eyJkcm1fdHlwZSI6ICJXaWRldmluZSIsICJzaXRlX2lkIjogIlRVVE8iLCAidXNlcl9pZCI6ICJ0ZXN0LXVzZXIiLCAiY2lkIjogImJpZ2J1Y2tidW5ueSIsICJ0b2tlbiI6ICJiTzlEenlRZ3RnZmJTRFdtcUdnWlhXWmRXbTdNNG9aNFgwaEMxaFM2UU5yYWl3TEkwTHdtTlkrT2ZPaDFMMEttdHVIN05GMWJsVXhlcDlZTFdyTmZTeTRILzZzd1FXN3BialpuUnFSZ3VEUT0iLCAidGltZXN0YW1wIjogIjIwMTktMDctMTdUMDg6NTc6MDRaIiwgImhhc2giOiAiMFplZjNXSEJielFBUjBvR2Y1S1huMjVHMVRtdkIyQmt2enYrN09xSVd2UT0ifQ=="
            )
