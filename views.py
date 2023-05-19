from postgres_model import *
from exceptions import NonUniqKey
from dataclasses import make_dataclass


def data_to_dict(cls):
    """Декоратор, который добаляет к Peewee model метод для выгрузки данных в словарь"""

    @classmethod
    def wrapper(cls, lst_pk: list[str] = None, unique: bool = True):
        """
        Преобразовываем таблицу в словарь
        :param lst_pk: Список атрибутов, которые будут ключами словаря
        :param unique: True - по одному ключу одна запись / False - по одному ключу может быть несколько записей
        Если unique = False - В значениях будут храниться списки
        """
        data_dict = dict()

        # если нет заданного
        if not lst_pk:
            lst_pk = [cls._meta.primary_key.name]

        # атрибуты таблицы
        attrs = (
            get_field_names(cls) + getattr(cls, "add_fields", [])
        )

        # у модели может быть собственный запрос на выгрузку
        if not (query := cls.query() if hasattr(cls, 'query') else None):
            query = cls.super.select()

        # на основе атрибутов таблицы строим датакласс
        metaclass = make_dataclass(cls.__name__, attrs)

        # выгружаем данные в словарь
        for value in query.tuples():
            data = metaclass(*value)
            pk_values = tuple(getattr(data, pk) for pk in lst_pk) if len(lst_pk) != 1 else getattr(data, lst_pk[0])
            if not unique:
                data_dict.setdefault(pk_values, []).append(data)
            else:
                if pk_values in data_dict:
                    raise NonUniqKey(f"ERROR: {cls.__name__} добавление неуникального ключа {pk_values}")
                data_dict[pk_values] = data

        return data_dict

    # добавляем метод к классу
    setattr(cls, 'data_to_dict', wrapper)
    return cls


def get_field_names(cls) -> list:
    """Список имен атрибутов peewee model"""
    return [item.name for item in cls._meta.sorted_fields]


@data_to_dict
class TprChapterView(TprChapters):
    @staticmethod
    def select_query():
        return (
            TprChapters
            .select(TprChapters, Disciplines.dis_id, TeachProgTypes.tpt_id)
            .join(TpDeliveries)
            .join(TeachPrograms)
            .join(Disciplines)
            .switch(TeachPrograms)
            .join(TeachProgTypes)
        )

    query = select_query
    add_fields = ["dis_id", "tpt_id"]


@data_to_dict
class StuGroupView(StuGroups):

    @staticmethod
    def select_query():
        return (
            StuGroups
            .select(StuGroups, GroupWorks.wt_wot)
            .join(GroupWorks)
        )

    query = select_query
    add_fields = ["wot_id"]


@data_to_dict
class DgrPeriodView(DgrPeriods):
    super = DgrPeriods


@data_to_dict
class TctimeView(TcTimes):

    @staticmethod
    def select_query():
        return (
            TcTimes
            .select(TcTimes, TimeRules)
            .join(TimeRules, on=(TcTimes.wt_wot == TimeRules.wt_wot_id))
        )

    query = select_query
    add_fields = get_field_names(TimeRules)


if __name__ == "__main__":
    for key, item in TctimeView.data_to_dict(["tch_tch"]).items():
        print(f"{key}, value: {item}")