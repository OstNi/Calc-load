from postgres_model import *

from tqdm import tqdm


__all__ = ["Data"]

class PostgresData:
    bar = tqdm(desc=f"[*] Выгрузка таблиц", total=15)
    stu_group: dict = get_dict(StuGroups)
    bar.update(1)
    division: dict = get_dict(Divisions)
    bar.update(1)
    exam_type: dict = get_dict(ExamType)
    bar.update(1)
    disciplines: dict = get_dict(Disciplines)
    bar.update(1)
    teach_prog_type: dict = get_dict(TeachProgTypes)
    bar.update(1)
    teach_program: dict = get_dict(TeachPrograms)
    bar.update(1)
    tp_deliveries: dict = get_dict(TpDeliveries)
    bar.update(1)
    tpr_chapters: dict = get_dict(TprChapters)
    bar.update(1)
    teach_years: dict = get_dict(TeachYears)
    bar.update(1)
    ty_periods: dict = get_dict(TyPeriods)
    bar.update(1)
    version: dict = get_dict(Versions)
    bar.update(1)
    dgr_period: dict = get_dict(DgrPeriods)
    bar.update(1)
    group_faculty: dict = get_dict(GroupFaculties)
    bar.update(1)
    group_work: dict = get_dict(GroupWorks)
    bar.update(1)
    work_type: dict = get_dict(WorkTypes)
    bar.update(1)
    bar.set_description("Table loading completed")
    bar.close()


Data = PostgresData()






