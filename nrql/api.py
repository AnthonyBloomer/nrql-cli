import os

import colorful
import requests


class NRQL:
    INSIGHTS_URL = "https://insights-api.newrelic.com/v1/accounts/%s/query"
    INSIGHTS_EU_REGION_URL = "https://insights-api.eu.newrelic.com/v1/accounts/%s/query"

    """
    NRQL API.
    """

    def __init__(self, api_key=None, account_id=None):
        """
        :param api_key: The Insights query API key.
        :param account_id: The New Relic account id.
        """
        self.api_key = api_key
        self.account_id = account_id
        self._url = self.INSIGHTS_URL
        self._eu_url = self.INSIGHTS_EU_REGION_URL
        self._region = "US"
        self._verbose = False
        self._environment = None

    @property
    def api_key(self):
        """
        The Insights query API key.
        :return: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """
        Set the Insights query API key.
        :param api_key: atr
        :return: str
        """
        self._api_key = api_key

    @property
    def account_id(self):
        """
        Set the New Relic account id.
        :return: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """
        The New Relic account id.
        :param account_id:
        :return: str
        """
        self._account_id = account_id

    @property
    def region(self):
        """
        The account region.
        :return: str
        """
        return self._region

    @region.setter
    def region(self, region: str):
        """
        Set the account region (EU or US). By default the region is set to US.
        :param region: str
        :return: str
        """
        self._region = region

    @property
    def verbose(self):
        """
        If True output the entire JSON response.
        :return: bool
        """
        return self._verbose

    @verbose.setter
    def verbose(self, verbose):
        """
        Set to True output the entire JSON response.
        :param verbose:
        :return:
        """
        self._verbose = verbose

    @property
    def environment(self):
        """
        # The development environment.
        :return: str
        """
        return self._environment

    @environment.setter
    def environment(self, environment):
        """
        # Set the environment.
        :param environment:
        :return:
        """
        self._environment = environment

    @staticmethod
    def _print_messages(response):
        if "metadata" in response and "messages" in response["metadata"]:
            for message in response["metadata"]["messages"]:
                print(colorful.bold(message))

    def _multiple_account_handler(self):
        if self.environment is None:
            nr_api_key = os.environ.get("NR_API_KEY")
            nr_account_id = os.environ.get("NR_ACCOUNT_ID")
        else:
            nr_api_key = os.environ.get("NR_API_KEY_%s" % self.environment.upper())
            nr_account_id = os.environ.get(
                "NR_ACCOUNT_ID_%s" % self.environment.upper()
            )
        return nr_api_key, nr_account_id

    def _make_request(self, query_stmt):
        payload = {"nrql": query_stmt}
        req = requests.get(
            self._url % self.account_id,
            headers={"X-Query-Key": self.api_key},
            params=payload,
        )
        if self.verbose:
            print(colorful.bold("Request URL: %s" % req.url))
            print(colorful.bold("Status Code: %s" % req.status_code))
        response = req.json()
        self._print_messages(response)
        if not self.verbose:
            response.pop("metadata", None)
            response.pop("performanceStats", None)

        return response

    def query(self, stmt):
        """
        Parse the query.
        :param stmt: str
        :return: str
        """
        nr_api_key, nr_account_id = self._multiple_account_handler()
        if not self.api_key or not self.account_id:
            if nr_api_key and nr_account_id:
                self._api_key = nr_api_key
                self._account_id = nr_account_id
            else:
                raise Exception("An api key and account id is required.")

        if not self.region == "US":
            self._url = self._eu_url

        resp = self._make_request(stmt)
        return resp
