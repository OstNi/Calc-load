from postgres_model import *
from views import (
    StuGroupView, TprChapterView, DgrPeriodView,
    TctimeView
)
from exceptions import *


def get_ty_periods_list(ty_id: int) -> list | None:
    """
    Список всех TyPeriod, которые входят в указанный год
    :param ty_id: id учебного года
    """
    if query := TyPeriods.select(TyPeriods.typ_id).where(TyPeriods.ty_ty == ty_id):
        return [item.typ_id for item in query]

    return None


def get_tpr_chapter(dis_id: int | None, tpt_id: int | None) -> tuple:
    """
    Создание словаря TprChapter с удобным для перебора ключом
    :param dis_id: id входного параметра disciplines
    :param tpt_id: id входного параметра teach_prog_types
    """
    pk_fields = ["tch_id"]
    if dis_id:
        pk_fields.append("dis_id")
    if tpt_id:
        pk_fields.append("tpt_id")
    return TprChapterView.data_to_dict() if len(pk_fields) == 1 else TprChapterView.data_to_dict(pk_fields), \
        get_key_to_chapters(dis_id, tpt_id)


def get_key_to_chapters(dis_id: int | None, tpt_id: int | None) -> tuple:
    """Ключ для итерации по TprChapters"""
    key = []
    if dis_id:
        key.append(dis_id)
    if tpt_id:
        key.append(tpt_id)
    return tuple(key)


def start_load(
        *,
        teach_years: int,
        dis_id: int = None,
        tpt_id: int = None,
        division_id: int = None
):
    dgr_periods = DgrPeriodView.data_to_dict(["typ_typ"], unique=False)
    tpr_chapters, key_chapter = get_tpr_chapter(dis_id=dis_id, tpt_id=tpt_id)
    tc_time = TctimeView.data_to_dict(["tch_tch"])

    for typ_id in get_ty_periods_list(teach_years):
        for dgr_period in dgr_periods[typ_id]:
            key = dgr_period.tch_tch if len(key_chapter) == 0 else ((dgr_period.tch_tch, ) + key_chapter)
            if not (tpr_chapter := tpr_chapters.get(key)):
                continue

            if not (curr_tc_time := tc_time.get(tpr_chapter.tch_id)):
                print(f"ERROR: для {tpr_chapter.tch_id} не существует TC_TIME")
                continue

            print('SUCCESS')
            tw_value = curr_tc_time.val * curr_tc_time.value

            new_tw_block = TwBlocks.create(
                val=tw_value,
                dgp_dgp=dgr_period.dgp_id,
                conv_value=tw_value*1.5,
                wt_wot=curr_tc_time.wt_wot
            )


if __name__ == "__main__":
    start_load(teach_years=2022)
