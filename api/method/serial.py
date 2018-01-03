from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute
import json
import datetime
from method.logger import default_logger as log
from functools import lru_cache


__all__ = ["to_json", "to_dict_with_label", "merge_from_dict"]


# javascript using JSON.stringify() to deserialize JSON data.
def alchemy_encoder(revisit_self=False, fields_to_expand=[]):
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x != 'classes']:
                    data = obj.__getattribute__(field)
                    try:
                        json.dumps(data)  # this will fail on non-encodable values, like other classes
                        fields[field] = data
                    except TypeError:  # 添加了对datetime的处理
                        if isinstance(data, datetime.datetime):
                            fields[field] = data.isoformat()
                        elif isinstance(data, datetime.date):
                            fields[field] = data.isoformat()
                        elif isinstance(data, datetime.timedelta):
                            fields[field] = (datetime.datetime.min + data).time().isoformat()
                        else:
                            fields[field] = None
                # a json-encodable dict
                return fields
            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


def to_json(obj, indent=0):
    """
    将整个对象转换为 json
    :param obj:
    :param indent:
    :return:
    """
    ret = json.dumps(obj, cls=alchemy_encoder(), ensure_ascii=False, indent=indent)
    return ret


# private
@lru_cache()
def find_field(model_type, label):
    """
        从 model 类型中，查找被 doc 描述的字段
        将所有符合条件的字段名称 以集合方式返回
    """
    field_set = set()
    for k in model_type.__dict__.keys():
        v = model_type.__dict__[k]
        if isinstance(v, InstrumentedAttribute):
            if label is None:
                field_set.add(k)
            else:
                if isinstance(v.__doc__, str) and v.__doc__ == label:
                    field_set.add(k)
                    continue
                if isinstance(v.__doc__, tuple) and label in v.__doc__:
                    field_set.add(k)
    return field_set


# private
def to_dict(model_obj, field_set):
    """
        将 model 对象中指定的字段的值，映射至一个 dict
    """
    values = dict()
    for f in field_set:
        values[f] = model_obj.__dict__[f]
    return values


def to_dict_with_label(model_obj, label):
    field_set = find_field(type(model_obj), label)
    return to_dict(model_obj, field_set)


def merge_from_dict(model_obj, dict_obj):
    assert isinstance(dict_obj, dict)
    editable_fileds = find_field(type(model_obj), 'edit')
    for k, v in dict_obj.items():
        if k in editable_fileds:
            model_obj.__dict__[k] = v
