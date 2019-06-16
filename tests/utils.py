import pytest
from app.libs.models import Ips


class ViewTestMixin(object):
    """
    Automatically load in a session and client, this is common for a lot of
    tests that work with views.
    """

    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, session, client):
        self.session = session
        self.client = client


def db_data():
    new_ip = Ips()
    new_ip.ip_address = "73.131.18.145"
    new_ip.continent_code = "NA"
    new_ip.continent_name = "North America"
    new_ip.country_code = "US"
    new_ip.country_name = "United States"
    new_ip.region_code = "SC"
    new_ip.region_name = "South Carolina"
    new_ip.city = "Charleston"
    new_ip.zip = "29414"
    new_ip.latitude = 32.8215
    new_ip.longitude = -80.0568
    new_ip.rdap_handle = "NET-73-131-0-0-1"
    new_ip.rdap_name = "CHARLESTON-18"
    new_ip.rdap_type = "ASSIGNMENT"
    new_ip.rdap_start_address = "73.131.0.0"
    new_ip.rdap_end_address = "73.131.127.255"
    new_ip.rdap_registrant_handle = "C05596371"
    new_ip.rdap_registrant_description = "Comcast IP Services, L.L.C."
    Ips.create(new_ip)
