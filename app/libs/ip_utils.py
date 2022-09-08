import re
import pathlib
from app.libs.models import Ips
import requests
from concurrent.futures import ThreadPoolExecutor
from datatables import DataTables, ColumnDT
import os
import configparser


def get_datatable_result(params):
    """
    Streaming IP query DataTable data.
    :param params:
    :type params:
    :return:
    :rtype:
    """
    columns = [
        ColumnDT(Ips.ip_address),
        ColumnDT(Ips.country_code),
        ColumnDT(Ips.region_code),
        ColumnDT(Ips.city),
        ColumnDT(Ips.zip),
        ColumnDT(Ips.latitude),
        ColumnDT(Ips.longitude),
        ColumnDT(Ips.rdap_registrant_handle),
        ColumnDT(Ips.rdap_registrant_description),
        ColumnDT(Ips.rdap_type),
    ]
    ip_query = Ips.query.with_entities(
        Ips.ip_address,
        Ips.country_code,
        Ips.region_code,
        Ips.city,
        Ips.zip,
        Ips.latitude,
        Ips.longitude,
        Ips.rdap_registrant_handle,
        Ips.rdap_registrant_description,
        Ips.rdap_type,
    )
    row_table = DataTables(params, ip_query, columns)
    output_result = row_table.output_result()
    return output_result


def get_ips(filters=None):
    """
    Get all ips.
    :param filters:
    :type filters:
    :return:
    :rtype:
    """
    query = Ips.query
    if filters:
        for attr, value in filters.items():
            query = query.filter(getattr(Ips, attr) == value)
    return query.all()


def get_ip(ip_id):
    """
    Get ip.
    :param ip_id:
    :type ip_id:
    :return:
    :rtype:
    """
    return Ips.read(ip_id)


def create_ip(ip_address, commit=True):
    """
    Create new ip.
    :param ip_address:
    :type ip_address:
    :param commit:
    :return:
    :rtype:
    """
    new_ip = Ips()
    new_ip.ip_address = ip_address
    return Ips.create(new_ip, commit)


def update_ip(ip_id, data_dict, commit=True):
    """
    Update a ip.
    :param ip_id:
    :type ip_id:
    :param data_dict:
    :type data_dict:
    :param commit:
    :return:
    :rtype:
    """
    ip_data = Ips.read(ip_id)
    for k in data_dict:
        try:
            setattr(ip_data, k, data_dict.get(k))
        except AttributeError:
            pass
    return ip_data.update(commit)


def get_geoip_info(ip_address, access_key):
    """
    Lookup geo IP info and update the db info.
    :param ip_address:
    :param access_key:
    """
    url = f"http://api.ipstack.com/{ip_address}?access_key={access_key}"
    response = requests.get(url)

    if response.status_code == 200:
        ip_info = response.json()
        db_ip = Ips.query.filter(Ips.ip_address == ip_info.get("ip")).one()
        update_ip(db_ip.id, ip_info)
    else:
        print(response.status_code, ip_address)


def get_rdap_info(ip_address):
    """
    Lookup RDAP info and update the db info.
    :param ip_address:
    """
    url = f"https://rdap.arin.net/registry/ip/{ip_address}"
    response = requests.get(url)
    if response.status_code == 200:
        ip_info = response.json()
        data_dict = {
            "rdap_handle": ip_info.get("handle"),
            "rdap_name": ip_info.get("name"),
            "rdap_type": ip_info.get("type"),
            "rdap_registrant_handle": None,
            "rdap_registrant_description": None,
            "rdap_start_address": ip_info.get("startAddress"),
            "rdap_end_address": ip_info.get("endAddress"),
        }
        entity = ip_info.get("entities")
        # I could do a lot more checks here, but if something ends up being out of place filling it with None
        # is the default for now.
        try:
            if entity:
                data_dict["rdap_registrant_handle"] = entity[0].get("handle")
                data_dict["rdap_registrant_description"] = entity[0].get("vcardArray")[
                    1
                ][1][3]
        except TypeError as e:
            print(e, ip_address)
        db_ip = Ips.query.filter(Ips.ip_address == ip_address).one()
        update_ip(db_ip.id, data_dict)
    else:
        print(response.status_code, ip_address)


def ingest_ip_data(ip):
    """
    Gather and ingest all the IP data.
    :param ip:
    """
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../config.ini"
    )
    config = configparser.ConfigParser()
    config.read(config_path)

    create_ip(ip)
    get_rdap_info(ip)
    get_geoip_info(ip, config["IPSTACK"]["IPSTACK_KEY"])


def insert_data():
    """
    Setup a new DB.
    """
    file_path = pathlib.Path("list_of_ips.txt")
    ip_list = parse_file_for_ips(file_path)
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(ingest_ip_data, ip_list)


def parse_file_for_ips(file_path):
    """
    Parse a file for all v4 IPs.
    :param file_path:
    :return:
    """
    with open(file_path, "r") as ip_file:
        pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
        ip_file_data = ip_file.read()
        ip_list = re.findall(pattern, ip_file_data)
    return ip_list
