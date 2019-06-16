from app.libs.ip_utils import (
    get_datatable_result,
    get_ips,
    get_ip,
    create_ip,
    update_ip,
    get_rdap_info,
    get_geoip_info,
    parse_file_for_ips,
)
import responses
from werkzeug.datastructures import ImmutableMultiDict
from app.libs.models import Ips
import configparser
import os
import json
from tests.utils import ViewTestMixin


class TestIPViews(ViewTestMixin):
    def test_get_datatable_result(self):
        params = ImmutableMultiDict(
            [
                ("draw", "1"),
                ("columns[0][data]", "0"),
                ("columns[0][name]", ""),
                ("columns[0][searchable]", "true"),
                ("columns[0][orderable]", "true"),
                ("columns[0][search][value]", ""),
                ("columns[0][search][regex]", "false"),
                ("columns[1][data]", "1"),
                ("columns[1][name]", ""),
                ("columns[1][searchable]", "true"),
                ("columns[1][orderable]", "true"),
                ("columns[1][search][value]", ""),
                ("columns[1][search][regex]", "false"),
                ("columns[2][data]", "2"),
                ("columns[2][name]", ""),
                ("columns[2][searchable]", "true"),
                ("columns[2][orderable]", "true"),
                ("columns[2][search][value]", ""),
                ("columns[2][search][regex]", "false"),
                ("columns[3][data]", "3"),
                ("columns[3][name]", ""),
                ("columns[3][searchable]", "true"),
                ("columns[3][orderable]", "true"),
                ("columns[3][search][value]", ""),
                ("columns[3][search][regex]", "false"),
                ("columns[4][data]", "4"),
                ("columns[4][name]", ""),
                ("columns[4][searchable]", "true"),
                ("columns[4][orderable]", "true"),
                ("columns[4][search][value]", ""),
                ("columns[4][search][regex]", "false"),
                ("columns[5][data]", "5"),
                ("columns[5][name]", ""),
                ("columns[5][searchable]", "true"),
                ("columns[5][orderable]", "true"),
                ("columns[5][search][value]", ""),
                ("columns[5][search][regex]", "false"),
                ("columns[6][data]", ""),
                ("columns[6][name]", ""),
                ("columns[6][searchable]", "true"),
                ("columns[6][orderable]", "false"),
                ("columns[6][search][value]", ""),
                ("columns[6][search][regex]", "false"),
                ("columns[7][data]", ""),
                ("columns[7][name]", ""),
                ("columns[7][searchable]", "true"),
                ("columns[7][orderable]", "false"),
                ("columns[7][search][value]", ""),
                ("columns[7][search][regex]", "false"),
                ("columns[8][data]", ""),
                ("columns[8][name]", ""),
                ("columns[8][searchable]", "true"),
                ("columns[8][orderable]", "false"),
                ("columns[8][search][value]", ""),
                ("columns[8][search][regex]", "false"),
                ("columns[9][data]", ""),
                ("columns[9][name]", ""),
                ("columns[9][searchable]", "true"),
                ("columns[9][orderable]", "false"),
                ("columns[9][search][value]", ""),
                ("columns[9][search][regex]", "false"),
                ("order[0][column]", "0"),
                ("order[0][dir]", "desc"),
                ("start", "0"),
                ("length", "10"),
                ("search[value]", ""),
                ("search[regex]", "false"),
                ("_", "1523458499553"),
            ]
        ).to_dict()
        result = get_datatable_result(params)
        assert result["recordsTotal"] == "1"
        assert result["recordsFiltered"] == "1"

    def test_get_ips(self):
        result = get_ips()
        assert len(result) == 1

    def test_get_ip(self):
        result = get_ip(1)
        assert result.ip_address == "73.131.18.145"

    def test_create_ip(self):
        result = create_ip("73.131.18.15")
        assert result == 2
        ip_data = Ips.read(2)
        assert ip_data.ip_address == "73.131.18.15"

    def test_update_ip(self):
        data_dict = {"ip_address": "127.0.0.1"}
        result = update_ip(1, data_dict)
        assert result == 1
        ip_data = Ips.read(1)
        assert ip_data.ip_address == "127.0.0.1"

    def test_parse_file_for_ips(self):
        ip_list = parse_file_for_ips("list_of_ips.txt")
        assert len(ip_list) == 10

    @responses.activate
    def test_get_rdap_info(self):
        with open("rdap_response.json", "r") as rdap_response:
            responses.add(
                responses.GET,
                "https://rdap.arin.net/registry/ip/73.131.18.145",
                json=json.loads(rdap_response.read()),
                status=200,
            )
            get_rdap_info("73.131.18.145")
            assert len(responses.calls) == 1
            assert (
                responses.calls[0].request.url
                == "https://rdap.arin.net/registry/ip/73.131.18.145"
            )

    @responses.activate
    def test_get_geoip_info(self):
        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "testconfig.ini"
        )
        config = configparser.ConfigParser()
        config.read(config_path)
        access_key = config["IPSTACK"]["IPSTACK_KEY"]
        with open("geoip_response.json", "r") as geoip_response:
            responses.add(
                responses.GET,
                f"http://api.ipstack.com/73.131.18.145?access_key={access_key}",
                json=json.loads(geoip_response.read()),
                status=200,
            )
        get_geoip_info("73.131.18.145", access_key)
        assert len(responses.calls) == 1
        assert (
            responses.calls[0].request.url
            == f"http://api.ipstack.com/73.131.18.145?access_key={access_key}"
        )

    def test_ggi(self):
        get_geoip_info("73.131.18.145", "ef50a43d25981da6cdb73ebcff14bfa4")
