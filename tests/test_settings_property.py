import pytest

@pytest.mark.usefixtures("home_control_instance")
@pytest.mark.usefixtures("mock_mprmrest__extract_data_from_element_uid")
@pytest.mark.usefixtures("mock_mydevolo__call")
class TestSettingsProperty:
    def test_get_general_device_settings_valid(self):
        name, icon, zone_id, events_enabled = \
            self.homecontrol.devices.get(self.devices.get("mains").get("uid")).settings_property.get("general_device_settings").get_general_device_settings()
        assert name == self.devices.get('mains').get('name')
        assert icon == self.devices.get('mains').get('icon')
        assert zone_id == self.devices.get('mains').get('zone_id')
        assert events_enabled

    def test_get_led_setting_valid(self):
        assert self.homecontrol.devices.get(self.devices.get("mains").get("uid")).settings_property.get("led").get_led_setting()

    def test_get_param_changed_valid(self):
        assert not self.homecontrol.devices.get(self.devices.get("mains").get("uid")).settings_property.get("param_changed").get_param_changed_setting()

    def test_get_protection_setting_valid(self):
        local_switch = self.homecontrol.devices.get(self.devices.get("mains").get("uid"))\
            .settings_property.get("protection_setting").get_protection_setting(protection_setting="local")
        remote_switch = self.homecontrol.devices.get(self.devices.get("mains").get("uid"))\
            .settings_property.get("protection_setting").get_protection_setting(protection_setting="remote")
        assert local_switch
        assert not remote_switch