from datetime import datetime
from json import dumps

import requests

from DNB_psd2 import AISP


class PIS:
    __slots__ = "s", "headers", "endpoint"
    """
    docstring
    """

    def __init__(self, pem_path: str, key_path: str, webdriver_path: str) -> None:
        self.s = requests.Session()
        self.endpoint = "https://sandboxapi.psd.dnb.no/v1/payments"
        headers = {
            "PSU-ID": "TB76688",
            "PSU-IP-Address": "123.123.123.123",
            "TPP-Redirect-Preferred": "true",
            "TPP-Redirect-URI": "https://dnb.no",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Request-ID": "c3bc3320-6ccd-49de-a24d-660f5e99b4e6",
            "TPP-Explicit-Authorisation-Preferred": "true",
        }
        self.s.cert = (pem_path, key_path)
        self.s.headers.update(headers)
        self.AISP = AISP(
            pem_path=pem_path, key_path=key_path, webdriver_path=webdriver_path
        )

    def approval(self):
        response = self.s.request("GET", f"{self.endpoint}/approval", data={})
        return response.text

    def get_domestic_credit_transfers_consent(self):
        payload = {
            "debtorAccount": {"bban": "12035864022"},
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
        response = response.json()
        print(response.get("_links"))
        return None


if __name__ == "__main__":
    instance = PIS(
        pem_path="./certificate/certificate.pem", key_path="./certificate/private.key"
    )
    instance.approval()
    print(instance.get_domestic_credit_transfers_consent())
