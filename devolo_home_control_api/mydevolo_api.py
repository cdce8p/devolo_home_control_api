import logging

import requests


class Mydevolo:
    """
    The Mydevolo object handles calls to the my devolo API v1. It does not cover all API calls, just those requested up to now.
    All calls are done in a user context, so you need to provide credentials of that user.
    :param user: devolo ID
    :param password: password
    :param url: URL of the stage (typically use default value)
    """

    def __init__(self, user: str, password: str, url: str = "https://www.mydevolo.com"):
        self._logger = logging.getLogger(self.__class__.__name__)

        self._user = user
        self._password = password

        self.url = url
        self.uuid = self._get_uuid()

    def get_gateway_serials(self) -> list:
        """
        Get gateway serial numbers.
        :return: Gateway serial numbers
        """
        gateways = []
        try:
            self._logger.debug(f"Getting list of gateways")
            r = requests.get(self.url + "/v1/users/" + self.uuid + "/hc/gateways/status",
                             auth=(self._user, self._password), timeout=60).json()['items']
            for gateway in r:
                gateways.append(gateway['gatewayId'])
                self._logger.debug(f"Adding {gateway['gatewayId']} to list of gateways.")
        except KeyError:
            self._logger.error("Could not get gateway list. Wrong Username or Password?")
            raise
        except requests.exceptions.ConnectionError:
            self._logger.error("Could not get gateway list. Wrong URL used?")
            raise
        if len(gateways) == 0:
            self._logger.error("Could not get gateway list. No Gateway attached to account?")
            raise IndexError("No gateways")
        return gateways

    def get_local_passkey(self, serial: str) -> str:
        """
        Get the local passkey of the given gateway for local authentication.
        :param serial: gateway serial number
        :return: passkey for local authentication
        """
        local_passkey = None
        try:
            self._logger.debug("Getting local passkey")
            local_passkey = requests.get(self.url + "/v1/users/" + self.uuid + "/hc/gateways/" + serial,
                                         auth=(self._user, self._password), timeout=60).json()['localPasskey']
        except KeyError:
            self._logger.error("Could not get local passkey. Wrong Username or Password?")
            raise
        except requests.exceptions.ConnectionError:
            self._logger.error("Could not get local passkey. Wrong URL used?")
            raise
        return local_passkey


    def _get_uuid(self) -> str:
        """
        Get the UUID of the current user.
        :return: UUID of current user
        """
        try:
            self._logger.debug("Getting UUID")
            uuid = requests.get(self.url + "/v1/users/uuid",
                                auth=(self._user, self._password), timeout=60).json()['uuid']
        except KeyError:
            self._logger.error("Could not get UUID. Wrong Username or Password?")
            raise
        except requests.exceptions.ConnectionError:
            self._logger.error("Could not get UUID. Wrong URL used?")
            raise
        return uuid
