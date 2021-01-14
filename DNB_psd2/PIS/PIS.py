import requests


class PIS():
    __slots__ = "s", "headers", "endpoint"
    """
    docstring
    """

    def __init__(self, pem_path: str, key_path: str) -> None:
        self.s = requests.Session()
        self.endpoint = "https://sandboxapi.psd.dnb.no/v1/payments"
        self.headers = {
            'PSU-ID': 'TB76688',
            'PSU-IP-Address': '123.123.123.123',
            'TPP-Redirect-Preferred': 'true',
            'TPP-Redirect-URI': 'http://tpp-service.net ',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Request-ID': 'c3bc3320-6ccd-49de-a24d-660f5e99b4e6',
            'TPP-Explicit-Authorisation-Preferred': 'true'
        }
        self.s.cert = (pem_path, key_path)

    def approval(self):
        response = self.s.request(
            "GET", f"{self.endpoint}/approval", headers=self.headers, data={})
        return response.text

    def get_norwegian_cross_border_credit_transfer():
        response = self.s.request("POST")
        return None


if __name__ == "__main__":
    instance = PIS(pem_path="./certificate/certificate.pem",
                   key_path="./certificate/private.key")
    instance.approval()
