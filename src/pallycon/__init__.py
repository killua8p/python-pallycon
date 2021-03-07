import base64
import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict

from Crypto.Cipher import AES
from Crypto.Util import Padding


class PallyConClient:
    """
    The PallyCon client
    """

    # Initial Vector
    iv = b"0123456789abcdef"

    def __init__(
        self,
        site_id: str,
        site_key: str,
        access_key: str,
        drm_type: str,
        user_id: str,
        content_id: str,
        license_rule: Dict,
    ):
        """
        Constructor

        :param site_id:
        :param site_key:
        :param access_key:
        :param drm_type:
        :param user_id:
        :param content_id:
        :param license_rule: See https://pallycon.com/docs/en/multidrm/license/license-token/
        """
        self.site_id = site_id
        self.site_key = site_key
        self.access_key = access_key
        self.drm_type = drm_type
        self.user_id = user_id
        self.content_id = content_id
        self.license_rule = license_rule

    def package_to_dash(self, src_file: str, destination: str) -> str:
        """
        Package the source file to DASH format

        NB. This function only works in Linux (or inside a Linux container)
        """
        src_file = Path(src_file).expanduser().resolve()
        dest_dir = (Path(destination).expanduser() / src_file.stem).resolve()
        packager_bin = (
            Path(__file__).resolve().parent / "bin/PallyConPackager"
        ).resolve()

        subprocess.run(
            [
                str(packager_bin),
                "--site_id",
                self.site_id,
                "--access_key",
                self.access_key,
                "--content_id",
                self.content_id,
                "--dash",
                "-i",
                str(src_file),
                "-o",
                # PallyConPackager doesn't like space in output
                str(dest_dir).replace(" ", "_"),
                "-f",
            ]
        ).check_returncode()

        return str(dest_dir)

    @property
    def encrypted_license_rule(self):
        return self._aes256_encrypt(json.dumps(self.license_rule))

    @property
    def license_token(self) -> Dict:
        """
        The license token that will be used by the HTML5 Player
        """
        return base64.b64encode(json.dumps({
            "drm_type": self.drm_type,
            "site_id": self.site_id,
            "user_id": self.user_id,
            "cid": self.content_id,
            "token": self.encrypted_license_rule,
            "timestamp": self._get_timestamp(),
            "hash": self._get_hash_string(),
        }).encode()).decode()

    def _aes256_encrypt(self, plain_text) -> str:
        """
        Encrypts the input using AES256 (CBC mode and PKCS#7 padding)
        """
        # create cipher config
        cipher = AES.new(self.site_key.encode(), AES.MODE_CBC, self.iv)

        # Remove spaces
        # TODO Confirm if it's needed
        plain_text = plain_text.replace(" ", "")

        # return a dictionary with the encrypted text
        return base64.b64encode(
            cipher.encrypt(
                Padding.pad(plain_text.encode(), AES.block_size, style="pkcs7")
            )
        ).decode()

    @staticmethod
    def _sha256_encrypt(plain_text) -> str:
        """
        input -> sha256 -> base64 -> output
        """
        cipher = hashlib.sha256()
        cipher.update(plain_text.encode())
        return base64.b64encode(cipher.digest()).decode()

    def _get_timestamp(self) -> str:
        """
        Returns the current time as yyyy-mm-ddThh:mm:ssZ""
        """
        return re.sub(r"\.\d+", "Z", datetime.utcnow().isoformat())

    def _get_hash_string(self) -> str:
        """
        Returns a hash string

        The hash message is used to verify the integrity of the entire token
        JSON value and should be generated as follows:

            base64(sha256(
                <site access key> + <drm type> + <site id> + <user id>
                + <cid> + <token> + <timestamp>
            ))

        https://pallycon.com/docs/en/multidrm/license/license-token/#hash-message
        """
        hash_input = (
            self.access_key
            + self.drm_type
            + self.site_id
            + self.user_id
            + self.content_id
            + self.encrypted_license_rule
            + self._get_timestamp()
        )
        return self._sha256_encrypt(hash_input)
