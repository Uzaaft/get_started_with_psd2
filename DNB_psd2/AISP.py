#!/usr/bin/env python3
import json
from datetime import datetime
from socket import gethostbyname, gethostname
from uuid import uuid4

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class AISP:
    __slots__ = ["endpoint", "s", "consent_payload", "consent"]

    def __init__(self, pem_path: str, key_path: str, PSU_ID: str, webdriver_path: str):
        """Initialize an instance with a connection to the DNB Sandbox API .

        Args:
            pem_path (str): [Path to the *.pem file downloaded from developer.dnb.no]
            key_path (str): [Path to the *.cert file downloaded from developer.dnb.no]
            PSU_ID (str): [Sosial security number or TB-ID to access the data for an entity(human or corporation)]
        """

        self.endpoint = "https://sandboxapi.psd.dnb.no/v1"
        hostname = gethostname()
        local_ip = gethostbyname(hostname)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Request-ID': str(uuid4()).lower(),
            # Change the  PSU-ID to change the person and the cards available.
            # List over the PSU-ID can be found:
            # https://developer.dnb.no/documentation/psd2/prod
            'PSU-IP-Address': local_ip,
            'PSU-ID': PSU_ID,
            'TPP-Redirect-URI': 'https://dnb.no'
        }
        self.s = requests.Session()
        self.s.cert = (pem_path, key_path)
        self.s.headers.update(headers)
        self.post_consents(webdriver_path=webdriver_path)

    @staticmethod
    def authenticate(url: str, webdriver_path) -> None:
        """Authenticate to the server .
        Args:
            url ([string]):[String generated by the DNB api to give consent to the application.]
        """
        chrome_options = Options()
        chrome_options.headless = True
        chrome_options.add_argument("--width=0")
        chrome_options.add_argument("--height=0")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(
            webdriver_path, options=chrome_options)
        driver.get(url)
        try:
            button = driver.find_elements_by_xpath(r'//*[@id="submit"]')[0]
            button.click()
            driver.quit()
        except BaseException:
            print("An error happened. Exiting...")
            driver.quit()

    def post_consents(self, webdriver_path) -> None:
        """Creates the consent ID for the user.
        """

        self.consent_payload = {
            # "validUntil": "{{validUntil}}",
            "validUntil": f"{datetime.date(datetime.now())}",
            "frequencyPerDay": 1,
            "access": {
                "balances": [],
                "accounts": [],
                "transactions": []
            },
            "recurringIndicator": "true",
            "combinedServiceIndicator": "false"}

        r = self.s.request(
            "POST",
            url=f"{self.endpoint}/consents",
            data=json.dumps(
                self.consent_payload))

        self.consent = r.json().get("consentId")
        self.s.headers.update({'Consent-ID': self.consent})

        authentication_url = r.json().get(
            "_links").get("scaRedirect").get("href")
        self.authenticate(url=authentication_url,
                          webdriver_path=webdriver_path)

    def delete_consents(self) -> None:
        """Delete the consent for this user.
        """
        r = self.s.request(
            "DELETE",
            url=f"{self.endpoint}/consents/{self.consent}",
            data=self.consent_payload)
        return r.text

    def get_consent(self):
        """Get the current consent .
        """
        r = self.s.request(
            "GET",
            url=f"{self.endpoint}/consents/{self.consent}",
            data=self.consent_payload)
        return r.text

    def accounts(self) -> list:
        """Get a list of bban accounts .
        Returns:
            list: [List containing all the different bank account numbers]
        """
        payload = {}
        r = self.s.request(
            "GET", url=f"{self.endpoint}/accounts", data=payload)
        # Return a list with the different account numbers
        return [i.get('bban') for i in r.json().get('accounts')]

    def get_account_info(self, bban: int) -> dict:
        """Get account information.
        Args:
            bban (int): [bban/bban nr]
        """
        r = self.s.request(
            "GET", url=f"{self.endpoint}/accounts/{bban}", data={})
        return r.json()

    def get_bank_transactions(
            self,
            bban: int) -> dict:
        """Returns a list of of bban, pending and booked transactions .
        Args:
            bban (int): [The account we want to extract transactions from]
            preprocessed (bool, optional): [Option to let the funciton preprocess the data for the user]. Defaults to False.
        Returns:
            dict: [Either one dict containing the trans info, or a preprocessed dict splitt up for easy of use.]
        """
        r = self.s.request(
            "GET",
            url=f"{self.endpoint}/accounts/{bban}/transactions?bookingStatus=both&dateFrom=2000-01-01",
            data={})
        return r.json()

    def get_card(self) -> list:
        """Get a list of card accounts .
        Returns:
            list: [List containing all the different bank account numbers]
        """
        payload = {}
        r = self.s.request(
            "GET", url=f"{self.endpoint}/card-accounts", data=payload)
        # Return a list with the different account numbers
        return [i.get('resourceId') for i in r.json().get('cardAccounts')]

    def get_card_transactions(self, card_account: int):
        """Get the transactions of a card account .

        Args:
            card_account (int): [description]
        Returns:
            [dict]: [returns a json dictionary with response body]
        """
        r = self.s.request(
            "GET",
            url=f"{self.endpoint}/card-accounts/{bban}/transactions?bookingStatus=both&dateFrom=2019-01-01",
            data={})
        return r.text

    def get_account_balance(self, bban):
        """Get the balance of an account .

        Args:
            bban ([str]): [Account nr.]

        Returns:
            [dict]: [Returns the balance of the spesified account.]
        """
        r = self.s.request(
            "GET",
            url=f"{self.endpoint}/accounts/{bban}/balances",
            data={})
        return r.json()
