from typing import Callable
from app.database import db


class BaseModel(db.Model):
    __abstract__ = True

    @staticmethod
    def create(new_entry, commit=True):
        try:
            db.session.add(new_entry)
            if commit:
                db.session.commit()
            return new_entry.id
        except Exception as e:
            print("c", e)
            return False

    @classmethod
    def read(cls, id_) -> Callable[..., "BaseModel"]:
        return BaseModel.query.get(id_)

    def update(self, commit=True):
        try:
            if commit:
                db.session.commit()
            return self.id
        except Exception as e:
            print("u", e)
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return self.id
        except Exception as e:
            print("d", e)
            return False

    @staticmethod
    def commit():
        db.session.commit()
        return True

    @staticmethod
    def object_dump(obj_name, obj_inst):
        def dig_deep(prop_value):
            dd_str = prop_value
            if (
                type(prop_value).__str__ is object.__str__
                and not isinstance(prop_value, str)
                and not isinstance(prop_value, dict)
            ):
                dd_str = BaseModel.object_dump(
                    prop_value.__class__.__name__, prop_value
                )
            return str(dd_str)

        obj_vars = sorted(
            [
                x
                for x in tuple(set(obj_inst.__dict__))
                if not x.startswith("__") and not x.startswith("_sa_instance_state")
            ]
        )
        return "{}({})".format(
            obj_name,
            ", ".join(
                [
                    "{}={}".format(var, dig_deep(getattr(obj_inst, var)))
                    for var in obj_vars
                ]
            ),
        )

    def __repr__(self):
        obj_vars = sorted(
            [
                x
                for x in tuple(set(self.__dict__))
                if not x.startswith("__") and x != "_sa_instance_state"
            ]
        )
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(["{}={}".format(var, getattr(self, var)) for var in obj_vars]),
        )

    def serialize(self):
        fields = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_") and key != "metadata":
                fields[key] = value
        return fields


class Ips(BaseModel):
    __tablename__ = "ips"
    id = db.Column(
        "id", db.Integer, primary_key=True, unique=True, index=True, autoincrement=True
    )
    ip_address = db.Column("ip_address", db.String(255), index=True)
    continent_code = db.Column("continent_code", db.String(255))
    continent_name = db.Column("continent_name", db.String(255))
    country_code = db.Column("country_code", db.String(255))
    country_name = db.Column("country_name", db.String(255))
    region_code = db.Column("region_code", db.String(255))
    region_name = db.Column("region_name", db.String(255))
    city = db.Column("city", db.String(255))
    zip = db.Column("zip", db.String(255))
    latitude = db.Column("latitude", db.Float)
    longitude = db.Column("longitude", db.Float)
    rdap_handle = db.Column("rdap_handle", db.String(255))
    rdap_name = db.Column("rdap_name", db.String(255))
    rdap_type = db.Column("rdap_type", db.String(255))
    rdap_start_address = db.Column("rdap_start_address", db.String(255))
    rdap_end_address = db.Column("rdap_end_address", db.String(255))
    rdap_registrant_handle = db.Column("rdap_registrant_handle", db.String(255))
    rdap_registrant_description = db.Column("rdap_registrant_description", db.Text)

    @classmethod
    def read(cls, id_) -> "Ips":
        return Ips.query.get(id_)
