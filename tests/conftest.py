import json
import sys

import pytest

from devolo_home_control_api.backend.mprm_rest import MprmRest
from devolo_home_control_api.backend.mprm_websocket import MprmWebsocket
from devolo_home_control_api.homecontrol import HomeControl

from .mocks.mock_gateway import Gateway
from .mocks.mock_homecontrol import mock__inspect_devices


try:
    with open("test_data.json") as file:
        test_data = json.load(file)
except FileNotFoundError:
    print("Please run tests from within the tests directory.")
    sys.exit(127)


pytest_plugins = ['tests.fixtures.mydevolo', 'tests.fixtures.requests', 'tests.mocks.mock_mydevolo']


@pytest.fixture()
def fill_device_data(request):
    consumption_property = request.cls.homecontrol.devices.get(test_data.get('devices').get("mains").get("uid")) \
        .consumption_property
    consumption_property.get(f"devolo.Meter:{test_data.get('devices').get('mains').get('uid')}").current = 0.58
    consumption_property.get(f"devolo.Meter:{test_data.get('devices').get('mains').get('uid')}").total = 125.68

    binary_switch_property = \
        request.cls.homecontrol.devices.get(test_data.get('devices').get("mains").get("uid")).binary_switch_property
    binary_switch_property.get(f"devolo.BinarySwitch:{test_data.get('devices').get('mains').get('uid')}").state = False

    voltage_property = request.cls.homecontrol.devices.get(test_data.get('devices').get("mains").get("uid")).voltage_property
    voltage_property.get(f"devolo.VoltageMultiLevelSensor:{test_data.get('devices').get('mains').get('uid')}").current = 236


@pytest.fixture()
def mock_get_local_session(mocker):
    mocker.patch("devolo_home_control_api.backend.mprm_rest.MprmRest.get_local_session", return_value=True)


@pytest.fixture()
def mock_get_remote_session(mocker):
    mocker.patch("devolo_home_control_api.backend.mprm_rest.MprmRest.get_remote_session", return_value=True)


@pytest.fixture()
def mock_gateway(mocker):
    mocker.patch("devolo_home_control_api.devices.gateway.Gateway.__init__", Gateway.__init__)


@pytest.fixture()
def mock_inspect_devices_metering_plug(mocker, mock_mydevolo__call):
    mocker.patch("devolo_home_control_api.homecontrol.HomeControl._inspect_devices", mock__inspect_devices)


@pytest.fixture()
def mock_mprmrest__detect_gateway_in_lan(mocker, request):
    if request.node.name not in ["test_detect_gateway_in_lan_valid"]:
        mocker.patch("devolo_home_control_api.backend.mprm_rest.MprmRest.detect_gateway_in_lan", return_value=None)


@pytest.fixture()
def mock_mprmrest__extract_data_from_element_uid(mocker, request):
    properties = {}
    properties['test_fetch_binary_switch_state_valid_on'] = {"properties": {"state": 1}}
    properties['test_fetch_binary_switch_state_valid_off'] = {"properties": {"state": 0}}
    properties['test_fetch_consumption_valid'] = {
        "properties": {"currentValue": test_data.get("devices").get("mains").get("current_consumption"),
                       "totalValue": test_data.get("devices").get("mains").get("total_consumption")}}
    properties['test_fetch_led_setting_valid'] = {
        "properties": {"led": test_data.get("devices").get("mains").get("led_setting")}}
    properties['test_fetch_param_changed_valid'] = {
        "properties": {"paramChanged": test_data.get("devices").get("mains").get("param_changed")}}
    properties['test_fetch_general_device_settings_valid'] = {
        "properties": {"eventsEnabled": test_data.get("devices").get("mains").get("events_enabled"),
                       "name": test_data.get("devices").get("mains").get("name"),
                       "icon": test_data.get("devices").get("mains").get("icon"),
                       "zoneID": test_data.get("devices").get("mains").get("zone_id")}}
    properties['test_fetch_protection_setting_valid'] = {
        "properties": {"localSwitch": test_data.get("devices").get("mains").get("local_switch"),
                       "remoteSwitch": test_data.get("devices").get("mains").get("remote_switch")}}
    properties['test_fetch_voltage_valid'] = {
        "properties": {"value": test_data.get("devices").get("mains").get("voltage")}}
    properties['test_update_consumption_valid'] = {
        "properties": {"currentValue": test_data.get("devices").get("mains").get("current_consumption"),
                       "totalValue": test_data.get("devices").get("mains").get("total_consumption")}}

    mocker.patch("devolo_home_control_api.backend.mprm_rest.MprmRest.extract_data_from_element_uid",
                 return_value=properties.get(request.node.name))


@pytest.fixture()
def mock_mprmrest__post(mocker, request):
    properties = {}
    properties["test_get_name_and_element_uids"] = {"result": {"items": [{"properties":
                                                                          {"itemName": "test_name",
                                                                           "zone": "test_zone",
                                                                           "batteryLevel": "test_battery",
                                                                           "icon": "test_icon",
                                                                           "elementUIDs": "test_element_uids",
                                                                           "settingUIDs": "test_setting_uids",
                                                                           "deviceModelUID": "test_device_model_uid",
                                                                           "status": "test_status"}}]}}
    properties["test_extract_data_from_element_uid"] = {"result": {"items": [{"properties": {"itemName": "test_name"}}]}}
    properties["test_get_all_devices"] = {"result": {"items": [{"properties": {"deviceUIDs": "deviceUIDs"}}]}}

    mocker.patch("devolo_home_control_api.backend.mprm_rest.MprmRest.post", return_value=properties.get(request.node.name))


@pytest.fixture(autouse=True)
def mock_mprmwebsocket_websocket_connection(mocker, request):
    def mock_websocket_connection():
        pass

    mocker.patch("devolo_home_control_api.backend.mprm_websocket.MprmWebsocket.websocket_connection",
                 side_effect=mock_websocket_connection)


@pytest.fixture()
def mock_homecontrol_is_online(mocker):
    mocker.patch("devolo_home_control_api.homecontrol.HomeControl.is_online", return_value=False)


@pytest.fixture()
def mock_mprmrest__post_set(mocker, request):
    status = {}
    status['test_set_binary_switch_valid'] = {"result": {"status": 1}}
    status['test_set_binary_switch_error'] = {"result": {"status": 2}}

    mocker.patch("devolo_home_control_api.backend.mprm_rest.MprmRest.post", return_value=status.get(request.node.name))


@pytest.fixture()
def mock_publisher_dispatch(mocker):
    mocker.patch("devolo_home_control_api.publisher.publisher.Publisher.dispatch", return_value=None)


@pytest.fixture()
def mprm_instance(request, mocker, mydevolo, mock_gateway,
                  mock_inspect_devices_metering_plug, mock_mprmrest__detect_gateway_in_lan):
    if "TestMprmRest" in request.node.nodeid:
        request.cls.mprm = MprmRest(gateway_id=test_data.get("gateway").get("id"), url="https://homecontrol.mydevolo.com")
    elif "TestMprmWebsocket" in request.node.nodeid:
        request.cls.mprm = MprmWebsocket(gateway_id=test_data.get("gateway").get("id"), url="https://homecontrol.mydevolo.com")
    else:
        def _websocket_connection_mock():
            pass

        mocker.patch("devolo_home_control_api.backend.mprm_websocket.MprmWebsocket.websocket_connection",
                     side_effect=_websocket_connection_mock)
        request.cls.mprm = MprmWebsocket(gateway_id=test_data.get("gateway").get("id"), url="https://homecontrol.mydevolo.com")
    yield
    request.cls.mprm.del_instance()


@pytest.fixture()
def home_control_instance(request, mydevolo, mock_gateway,
                          mock_inspect_devices_metering_plug, mock_mprmrest__detect_gateway_in_lan):
    request.cls.homecontrol = HomeControl(test_data.get("gateway").get("id"))
    request.cls.homecontrol.devices['hdm:ZWave:F6BF9812/4'].binary_switch_property['devolo.BinarySwitch:hdm:ZWave:F6BF9812/4'] \
        .is_online = request.cls.homecontrol.is_online
    yield
    MprmWebsocket.del_instance()


@pytest.fixture(autouse=True)
def test_data_fixture(request):
    request.cls.user = test_data.get("user")
    request.cls.gateway = test_data.get("gateway")
    request.cls.devices = test_data.get("devices")


@pytest.fixture(autouse=True)
def mock_mprm_create_connection(mocker):
    mocker.patch("devolo_home_control_api.backend.mprm_websocket.MprmWebsocket.create_connection", return_value=None)


@pytest.fixture()
def mock_properties(mocker):
    mocker.patch("devolo_home_control_api.properties.consumption_property.ConsumptionProperty.fetch_consumption",
                 return_value=None)
    mocker.patch("devolo_home_control_api.properties.binary_switch_property.BinarySwitchProperty.fetch_binary_switch_state",
                 return_value=None)
    mocker.patch("devolo_home_control_api.properties.voltage_property.VoltageProperty.fetch_voltage",
                 return_value=None)
    mocker.patch("devolo_home_control_api.properties.settings_property.SettingsProperty.fetch_general_device_settings",
                 return_value=None)
    mocker.patch("devolo_home_control_api.properties.settings_property.SettingsProperty.fetch_param_changed_setting",
                 return_value=None)
    mocker.patch("devolo_home_control_api.properties.settings_property.SettingsProperty.fetch_protection_setting",
                 return_value=None)
    mocker.patch("devolo_home_control_api.properties.settings_property.SettingsProperty.fetch_led_setting",
                 return_value=None)


@pytest.fixture()
def mock_get_local_session_json_decode_error(mocker):
    def inner():
        raise json.JSONDecodeError(msg="message", doc="doc", pos=1)

    mocker.patch("devolo_home_control_api.backend.mprm_rest.MprmRest.get_local_session", side_effect=inner)


@pytest.fixture()
def mock_websocket_connection(mocker):
    mocker.patch("devolo_home_control_api.backend.mprm_websocket.MprmWebsocket.websocket_connection", return_value=None)
