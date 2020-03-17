import pytest
from requests import ConnectTimeout

from devolo_home_control_api.backend.mprm_rest import MprmDeviceCommunicationError

from .mocks.mock_dnsrecord import MockDNSRecord


@pytest.mark.usefixtures("mprm_instance")
class TestMprm:
    def test_create_connection_remote(self, mock_mprmwebsocket_get_remote_session, mprm_session, mydevolo):
        self.mprm._session = mprm_session
        self.mprm._gateway.external_access = True
        self._mydevolo = mydevolo
        self.mprm.create_connection()

    def test_create_connection_invalid(self):
        with pytest.raises(ConnectionError):
            self.mprm._gateway.external_access = False
            self.mprm.create_connection()

    # TODO: check, why this test takes so long
    def test_detect_gateway_in_lan(self, mock_mprmrest_zeroconf_cache_entries, mock_mprm__try_local_connection):
        assert self.mprm.detect_gateway_in_lan() == self.gateway.get("local_ip")

    @pytest.mark.usefixtures("mock_session_get")
    @pytest.mark.usefixtures("mock_response_json")
    def test_get_local_session_valid(self, mprm_session):
        self.mprm._session = mprm_session
        self.mprm._local_ip = self.gateway.get("local_ip")
        self.mprm.get_local_session()

    @pytest.mark.usefixtures("mock_response_requests_ConnectTimeout")
    def test_get_local_session_ConnectTimeout(self, mprm_session):
        self.mprm._session = mprm_session
        self.mprm._local_ip = self.gateway.get("local_ip")
        with pytest.raises(ConnectTimeout):
            self.mprm.get_local_session()

    @pytest.mark.usefixtures("mock_response_json_JSONDecodeError")
    def test_get_local_session_JSONDecodeError(self, mprm_session):
        self.mprm._session = mprm_session
        self.mprm._local_ip = self.gateway.get("local_ip")
        with pytest.raises(MprmDeviceCommunicationError):
            self.mprm.get_local_session()

    @pytest.mark.usefixtures("mock_response_json_JSONDecodeError")
    def test_get_remote_session_JSONDecodeError(self, mprm_session):
        self.mprm._session = mprm_session
        with pytest.raises(MprmDeviceCommunicationError):
            self.mprm.get_remote_session()

    def test__try_local_connection_success(self, mprm_session, mock_socket_inet_ntoa, mock_response_valid):
        mdns_name = MockDNSRecord()
        mdns_name.address = self.gateway.get("local_ip")
        self.mprm._session = mprm_session
        self.mprm._try_local_connection(mdns_name)
        assert self.mprm._local_ip == self.gateway.get("local_ip")
