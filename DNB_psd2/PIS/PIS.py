import urllib.parse
from datetime import datetime
from json import dumps
from socket import gethostbyname, gethostname
from urllib.parse import urlparse
from uuid import uuid4

import requests

from DNB_psd2 import AISP


class PIS:
    __slots__ = "s", "headers", "endpoint"
    """
    docstring
    """

    def __init__(self, pem_path: str, key_path: str) -> None:
        hostname = gethostname()
        local_ip = gethostbyname(hostname)
        self.s = requests.Session()
        self.endpoint = "https://sandboxapi.psd.dnb.no/v1/payments"
        headers = {
            "PSU-ID": "TB76688",
            "PSU-IP-Address": local_ip,
            "TPP-Redirect-Preferred": "true",
            "TPP-Redirect-URI": "https://dnb.no",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Request-ID": str(uuid4()).lower(),
            # "TPP-Explicit-Authorisation-Preferred": "true",
            "PSU-User-Agent": "Chrome",
        }
        self.s.cert = (pem_path, key_path)
        self.s.headers.update(headers)

    def approval(self):
        response = self.s.request("GET", f"{self.endpoint}/approval", data={})
        return response.text

    def get_domestic_credit_transfers_consent(self, account: int):
        payload = {
            "debtorAccount": {"bban": f"{account}"},
            "creditorAccount": {"bban": "12094355778"},
            "creditorName": "Foo Bar",
            "instructedAmount": {"amount": 13.37, "currency": "NOK"},
            "remittanceInformationUnstructured": "Test of payment to another Norwegian account.",
            "requestedExecutionDate": f"{datetime.date((datetime.now()))}",
        }
        response = self.s.request(
            "POST",
            f"{self.endpoint}/norwegian-domestic-credit-transfers",
            data=dumps(payload),
        )
        url = response.json().get("_links").get("scaRedirect").get("href")
        self.authenticate(url)
        return response.text

    @staticmethod
    def authenticate(url):
        payload = urllib.parse.quote(url)
        payload = payload.replace("/", "%2F")
        payload = f"auth_status=Ok&url={payload}"
        parsed_url = urlparse(url)
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": f"{parsed_url.scheme}://{parsed_url.netloc}",
            "Referer": url,
            "Content-Length": "901",
            "Host": f"{parsed_url.netloc}",
            "Accept-Language": "en-gb",
            "User-Agent": "Chrome",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest",
        }
        requests.request(
            "POST",
            f"{parsed_url.scheme}://{parsed_url.netloc}/Prod/bankid/auth",
            headers=headers,
            data=payload,
        )

    def get_domestic_credit_transfers(self):
        return None


if __name__ == "__main__":
    pem_path = "./certificate/certificate.pem"
    key_path = "./certificate/private.key"
    webdriver_path = "./webdriver/chromedriver"
    AISP_instance = AISP(
        pem_path=pem_path,
        key_path=key_path,
        PSU_ID="TB76688",
    )
    accounts = AISP_instance.accounts()
    instance = PIS(pem_path=pem_path, key_path=key_path)
    a = instance.approval()
    instance.get_domestic_credit_transfers_consent(account=accounts[0])
