from flask import url_for
from werkzeug.datastructures import ImmutableMultiDict
from tests.utils import ViewTestMixin


class TestIPViews(ViewTestMixin):
    def test_index(self):
        response = self.client.get(url_for("core.index"))
        assert response.status_code == 200

    def test_ip_query_datatable(self):
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
        )
        response = self.client.get(
            url_for("core.ip_query_datatable_datastream"), data=params
        )
        assert response.status_code == 200
