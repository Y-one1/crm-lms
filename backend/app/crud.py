from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime, timedelta
from sqlalchemy import func
from collections import defaultdict
import os

#==============================
# children
#==============================

def create_child(db: Session, child: schemas.ChildrenCreate):
    """Создание нового ребенка"""
    db_child = models.Children(**child.model_dump())
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child

def get_child(db: Session, child_id: int):
    """Получение данных об одном ребенке"""
    return db.query(models.Children).filter(models.Children.child_id == child_id).first()

def get_all_children(db: Session):
    """Получение списка детей"""
    return db.query(models.Children).all()

def update_child(db: Session, child_id: int, child_data: schemas.ChildrenCreate):
    """Обновление данных ребёнка"""
    db_child = db.query(models.Children).filter(models.Children.child_id == child_id).first()
    if db_child:
        for key, value in child_data.model_dump().items():
            setattr(db_child, key, value)
        db.commit()
        db.refresh(db_child)
    return db_child

def delete_child(db: Session, child_id: int):
    """Удаление ребенка"""
    db_child = db.query(models.Children).filter(models.Children.child_id == child_id).first()
    if db_child:
        db.delete(db_child)
        db.commit()
    return db_child

def get_child_notes(db: Session, child_id: int, start_date=None, end_date=None):
    """Получить заметки из уроков ребёнка (только непустые)"""
    query = db.query(models.Lessons).filter(
        models.Lessons.child_id == child_id,
        (
            (models.Lessons.notes_for_yourself != None) & (models.Lessons.notes_for_yourself != '')
        ) | (
            (models.Lessons.notes_for_parents != None) & (models.Lessons.notes_for_parents != '')
        )
    )
    if start_date and end_date:
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(
            models.Lessons.lesson_datetime >= start_datetime,
            models.Lessons.lesson_datetime <= end_datetime,
        )
    return query.order_by(models.Lessons.lesson_datetime.desc()).all()

#==============================
# parents
#==============================

def create_parent(db: Session, parent: schemas.ParentsCreate):
    """Создание нового родителя"""
    db_parent = models.Parents(**parent.model_dump())
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent

def get_parent(db: Session, parent_id: int):
    """Получение данных об одном родителе"""
    return db.query(models.Parents).filter(models.Parents.parent_id == parent_id).first()

def get_all_parents(db: Session):
    """Получение списка родителей (опционально последовательность)"""
    return db.query(models.Parents).all()

def update_parent(db: Session, parent_id: int, parent_data: schemas.ParentsCreate):
    """Обновление данных родителя"""
    db_parent = db.query(models.Parents).filter(models.Parents.parent_id == parent_id).first()
    if db_parent:
        for key, value in parent_data.model_dump().items():
            setattr(db_parent, key, value)
        db.commit()
        db.refresh(db_parent)
    return db_parent

def delete_parent(db: Session, parent_id: int):
    """Удаление родителя"""
    db_parent = db.query(models.Parents).filter(models.Parents.parent_id == parent_id).first()
    if db_parent:
        db.delete(db_parent)
        db.commit()
    return db_parent

def get_parent_notes(db: Session, parent_id: int, start_date=None, end_date=None):
    """Заметки для родителя — из уроков всех его детей"""
    children = get_children_by_parent(db, parent_id)
    child_ids = [c.child_id for c in children]
    if not child_ids:
        return []
    query = db.query(models.Lessons).filter(
        models.Lessons.child_id.in_(child_ids),
        models.Lessons.notes_for_parents != None,
        models.Lessons.notes_for_parents != '',
    )
    if start_date and end_date:
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(
            models.Lessons.lesson_datetime >= start_datetime,
            models.Lessons.lesson_datetime <= end_datetime,
        )
    return query.order_by(models.Lessons.lesson_datetime.desc()).all()

def get_payments_by_parent(db: Session, parent_id: int):
    """Получить платежи родителя"""
    return db.query(models.Payments).filter(
        models.Payments.parent_id == parent_id
    ).order_by(models.Payments.payment_date.desc()).all()

#==============================
# parent_child
#==============================

def create_parent_child(db: Session, parent_child: schemas.ParentСhildCreate):
    """Создать новую связь родителя с ребёнком"""
    db_parent_child = models.ParentChild(**parent_child.model_dump())
    db.add(db_parent_child)
    db.commit()
    db.refresh(db_parent_child)
    return db_parent_child

def delete_parent_child(db: Session, parent_id: int, child_id: int):
    """Удалить связь родителя с ребёнком"""
    db_parent_child = db.query(models.ParentChild).filter(
        models.ParentChild.parent_id == parent_id,
        models.ParentChild.child_id == child_id
    ).first()
    if db_parent_child:
        db.delete(db_parent_child)
        db.commit()
    return db_parent_child

def update_parent_child(db: Session, parent_id: int, child_id: int, data: schemas.UpdateParentChildRequest):
    """Обновить связь родителя с ребёнком"""
    db_parent_child = db.query(models.ParentChild).filter(
        models.ParentChild.parent_id == parent_id,
        models.ParentChild.child_id == child_id
    ).first()
    if db_parent_child:
        db_parent_child.is_main = data.is_main
        db.commit()
        db.refresh(db_parent_child)
    return db_parent_child

def get_parents_by_child(db: Session, child_id: int):
    """Получить всех родителей одного ребёнка"""
    return db.query(models.Parents).join(
        models.ParentChild,
        models.Parents.parent_id == models.ParentChild.parent_id
    ).filter(models.ParentChild.child_id == child_id).all()

def get_children_by_parent(db: Session, parent_id: int):
    """Получить всех детей одного родителя"""
    return db.query(models.Children).join(
        models.ParentChild,
        models.Children.child_id == models.ParentChild.child_id
    ).filter(models.ParentChild.parent_id == parent_id).all()

def get_parent_children_with_relations(db: Session, parent_id: int):
    """Получить всех детей одного родителя со статусом связи (is_main)"""
    rows = db.query(models.Children, models.ParentChild).join(
        models.ParentChild,
        models.Children.child_id == models.ParentChild.child_id
    ).filter(models.ParentChild.parent_id == parent_id).all()

    return [
        {**{c: getattr(child, c) for c in child.__table__.columns.keys()},
         'is_main': pc.is_main}
        for child, pc in rows
    ]

#==============================
# tariff
#==============================

def create_tariff(db: Session, tariff: schemas.TariffCreate):
    """Создание нового тарифа"""
    db_tariff = models.Tariff(**tariff.model_dump())
    db.add(db_tariff)
    db.commit()
    db.refresh(db_tariff)
    return db_tariff

def get_tariff(db: Session, tariff_id: int):
    """Получение данных об одном тарифе"""
    return db.query(models.Tariff).filter(models.Tariff.tariff_id == tariff_id).first()

def get_all_tariffs(db: Session):
    """Получение списка тарифов не из архива"""
    return db.query(models.Tariff).filter(models.Tariff.is_archived == False).all()

def get_archived_tariffs(db: Session):
    """Получение списка тарифов из архива"""
    return db.query(models.Tariff).filter(models.Tariff.is_archived == True).all()

def update_tariff(db: Session, tariff_id: int, tariff_data: schemas.TariffCreate):
    """Обновление данных тарифа"""
    db_tariff = db.query(models.Tariff).filter(models.Tariff.tariff_id == tariff_id).first()
    if db_tariff:
        for key, value in tariff_data.model_dump().items():
            setattr(db_tariff, key, value)
        db.commit()
        db.refresh(db_tariff)
    return db_tariff

def delete_tariff(db: Session, tariff_id: int):
    """Удаление тарифа"""
    db_tariff = db.query(models.Tariff).filter(models.Tariff.tariff_id == tariff_id).first()
    if db_tariff:
        db_tariff.is_archived = True
        db.commit()
        db.refresh(db_tariff)
    return db_tariff

#==============================
# child_tariff_periods
#==============================

def assign_tariff_to_child(db: Session, child_id: int, tariff_id: int, start_date):
    """Подключить тариф к ученику"""
    tariff = get_tariff(db, tariff_id)
    if not tariff:
        raise ValueError("Тариф не найден")

    # Деактивируем текущий активный тариф если есть
    active = db.query(models.ChildTariffPeriods).filter(
        models.ChildTariffPeriods.child_id == child_id,
        models.ChildTariffPeriods.active == True
    ).first()
    if active:
        active.active = False
        db.commit()

    # Считаем debt с учётом баланса ученика
    child = db.query(models.Children).filter(models.Children.child_id == child_id).first()
    debt = float(tariff.price) - float(child.balance)
    if debt < 0:
        # Баланс покрывает тариф полностью — списываем с баланса
        child.balance = abs(debt)
        debt = 0
    else:
        child.balance = 0

    # Считаем consecutive_count
    last_period = db.query(models.ChildTariffPeriods).filter(
        models.ChildTariffPeriods.child_id == child_id
    ).order_by(models.ChildTariffPeriods.start_date.desc()).first()
    
    consecutive = 1
    if last_period and last_period.tariff_id == tariff_id:
        consecutive = (last_period.consecutive_count or 1) + 1

    new_period = models.ChildTariffPeriods(
        child_id=child_id,
        tariff_id=tariff_id,
        start_date=start_date,
        lessons_rest=tariff.num_of_lessons,
        debt=debt,
        active=True,
        consecutive_count=consecutive,
    )
    db.add(new_period)
    db.commit()
    db.refresh(new_period)
    return new_period

def get_active_tariff_by_child(db: Session, child_id: int):
    """Получить активный тариф ребёнка"""
    tariff_period = db.query(models.ChildTariffPeriods).filter(
        models.ChildTariffPeriods.child_id == child_id,
        models.ChildTariffPeriods.active == True
    ).first()
    if tariff_period:
        tariff = get_tariff(db, tariff_period.tariff_id)
        return {
            'tariff_period': tariff_period,
            'tariff': tariff
        }
    return None

def get_all_child_tariff_periods(db: Session, child_id: int):
    """Получить все тарифные периоды ребёнка (историю)"""
    return db.query(models.ChildTariffPeriods).filter(
        models.ChildTariffPeriods.child_id == child_id
    ).order_by(models.ChildTariffPeriods.start_date.desc()).all()

def decrement_lessons_rest(db: Session, tariff_period_id: int):
    """Уменьшить счётчик оставшихся уроков на 1"""
    db_tariff_period = db.query(models.ChildTariffPeriods).filter(
        models.ChildTariffPeriods.tariff_period_id == tariff_period_id
    ).first()
    if db_tariff_period:
        if db_tariff_period.lessons_rest > 0:
            db_tariff_period.lessons_rest -= 1
            db.commit()
            db.refresh(db_tariff_period)
        elif db_tariff_period.lessons_rest == 0:
            raise ValueError("Занятия в тарифе закончились!")
        else:
            raise ValueError("Кол-во занятий стало отрицательным!")
    return db_tariff_period

def update_tariff_period_fields(db: Session, tariff_period_id: int, lessons_rest: int = None, debt: float = None):
    """Обновить данные текущего тарифа"""
    period = db.query(models.ChildTariffPeriods).filter(
        models.ChildTariffPeriods.tariff_period_id == tariff_period_id
    ).first()
    if not period:
        return None
    if lessons_rest is not None:
        period.lessons_rest = lessons_rest
    if debt is not None:
        period.debt = debt
    db.commit()
    db.refresh(period)
    return period

def close_tariff_period(db: Session, tariff_period_id: int):
    """Закрыть тарифный период"""
    db_tariff_period = db.query(models.ChildTariffPeriods).filter(
        models.ChildTariffPeriods.tariff_period_id == tariff_period_id
    ).first()
    if db_tariff_period:
        db_tariff_period.active = False
        db.commit()
        db.refresh(db_tariff_period)
    return db_tariff_period

def get_children_with_tariff_count(db: Session, tariff_id: int):
    """Получить кол-во активных учеников с конкретным тарифом"""
    return db.query(models.ChildTariffPeriods).filter(
        models.ChildTariffPeriods.tariff_id == tariff_id,
        models.ChildTariffPeriods.active == True
    ).count()

#==============================
# lessons
#==============================

def get_overlapping_lesson(db: Session, child_id: int, lesson_datetime, exclude_lesson_id: int = None):
    """Проверяет, есть ли у ребёнка занятие, пересекающееся с указанным временем.
    Считаем, что занятие длится 60 минут."""
    lesson_end = lesson_datetime + timedelta(hours=1)
    lesson_start_max = lesson_datetime - timedelta(hours=1)

    query = db.query(models.Lessons).filter(
        models.Lessons.child_id == child_id,
        models.Lessons.status != 'cancelled',
        models.Lessons.lesson_datetime < lesson_end,
        models.Lessons.lesson_datetime > lesson_start_max
    )
    if exclude_lesson_id:
        query = query.filter(models.Lessons.lesson_id != exclude_lesson_id)

    return query.first()

def create_lesson(db: Session, lesson: schemas.LessonsCreate):
    """Создание нового урока"""
    db_lesson = models.Lessons(**lesson.model_dump())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def get_lesson(db: Session, lesson_id: int):
    """Получение данных об одном уроке"""
    return db.query(models.Lessons).filter(models.Lessons.lesson_id == lesson_id).first()

def get_all_lessons(db: Session, skip: int = 0, limit: int = 100, start_date=None, end_date=None):
    """Получение списка уроков (опционально последовательность, с фильтром по датам)"""
    query = db.query(models.Lessons)
    # Если указаны даты — фильтруем
    if start_date and end_date:
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(
            models.Lessons.lesson_datetime >= start_datetime,
            models.Lessons.lesson_datetime <= end_datetime
        )
    
    return query.order_by(models.Lessons.lesson_datetime.desc()).offset(skip).limit(limit).all()

def update_lesson(db: Session, lesson_id: int, lesson_data: dict):
    """Обновление данных урока"""
    db_lesson = db.query(models.Lessons).filter(models.Lessons.lesson_id == lesson_id).first()
    if db_lesson:
        for key, value in lesson_data.items():
            setattr(db_lesson, key, value)
        db.commit()
        db.refresh(db_lesson)
    return db_lesson

def delete_lesson(db: Session, lesson_id: int):
    """Удаление урока"""
    db_lesson = db.query(models.Lessons).filter(models.Lessons.lesson_id == lesson_id).first()
    if db_lesson:
        db.delete(db_lesson)
        db.commit()
    return db_lesson

def get_lessons_by_child_and_date_range(db: Session, child_id: int, start_date, end_date):
    """Получить уроки ребёнка в диапазоне дат"""
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())

    return db.query(models.Lessons).filter(
        models.Lessons.child_id == child_id,
        models.Lessons.lesson_datetime >= start_datetime,
        models.Lessons.lesson_datetime <= end_datetime
    ).order_by(models.Lessons.lesson_datetime).all()

def clear_lesson_notes(db: Session, lesson_id: int, field: str):
    """Очистить заметку в уроке (notes_for_yourself или notes_for_parents)"""
    if field not in ('notes_for_yourself', 'notes_for_parents'):
        raise ValueError("Недопустимое поле")
    lesson = db.query(models.Lessons).filter(models.Lessons.lesson_id == lesson_id).first()
    if lesson:
        setattr(lesson, field, None)
        db.commit()
        db.refresh(lesson)
    return lesson

#==============================
# payments
#==============================

def create_payment(db: Session, payment: schemas.PaymentsCreate):
    """Создание нового платежа"""
    db_payment = models.Payments(**payment.model_dump())
    db.add(db_payment)

    # Гасим debt текущего тарифа, остаток идёт в balance
    child = db.query(models.Children).filter(models.Children.child_id == payment.child_id).first()
    active_period = db.query(models.ChildTariffPeriods).filter(
        models.ChildTariffPeriods.child_id == payment.child_id,
        models.ChildTariffPeriods.active == True
    ).first()

    amount = float(payment.amount)

    if active_period:
        debt = float(active_period.debt)
        if amount >= debt:
            active_period.debt = 0
            child.balance = float(child.balance) + (amount - debt)
        else:
            active_period.debt = debt - amount

    else:
        # Нет активного тарифа — всё на баланс
        child.balance = float(child.balance) + amount

    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: int):
    """Получение данных об одном платеже"""
    return db.query(models.Payments).filter(models.Payments.payment_id == payment_id).first()

def get_all_payments(db: Session, skip: int = 0, limit: int = 100, start_date=None, end_date=None):
    """Получение списка платежей (опционально последовательность, с фильтром по датам)"""
    query = db.query(models.Payments)

    if start_date:
        start_datetime = datetime.combine(start_date, datetime.min.time())
        query = query.filter(models.Payments.payment_date >= start_datetime)

    if end_date:
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(models.Payments.payment_date <= end_datetime)

    return query.order_by(models.Payments.payment_date.desc()).offset(skip).limit(limit).all()

def update_payment(db: Session, payment_id: int, payment_data: dict):
    """Обновление данных платежа"""
    db_payment = db.query(models.Payments).filter(models.Payments.payment_id == payment_id).first()
    if db_payment:
        for key, value in payment_data.items():
            setattr(db_payment, key, value)
        db.commit()
        db.refresh(db_payment)
    return db_payment

def delete_payment(db: Session, payment_id: int):
    """Удаление платежа"""
    db_payment = db.query(models.Payments).filter(models.Payments.payment_id == payment_id).first()
    if db_payment:
        db.delete(db_payment)
        db.commit()
    return db_payment

def get_child_payments(db: Session, child_id: int, start_date, end_date):
    """Получить оплаты ребёнка за период"""
    return db.query(models.Payments).filter(
        models.Payments.child_id == child_id,
        models.Payments.payment_date >= start_date,
        models.Payments.payment_date <= end_date
    ).order_by(models.Payments.payment_date.desc()).all()

def get_debtors(db: Session):
    """Получить список должников с суммой долга"""
    rows = db.query(models.Children, models.ChildTariffPeriods).join(
        models.ChildTariffPeriods,
        models.Children.child_id == models.ChildTariffPeriods.child_id
    ).filter(
        models.ChildTariffPeriods.debt > 0,
        models.ChildTariffPeriods.active == True
    ).all()

    result = []
    for child, period in rows:
        result.append({
            'child_id':     child.child_id,
            'last_name':    child.last_name,
            'first_name':   child.first_name,
            'patronymic':   child.patronymic,
            'phone_number': child.phone_number,
            'school_class': child.school_class,
            'balance':      float(child.balance),
            'debt':         float(period.debt),
        })
    return result

def get_payments_summary(db: Session, start_date=None, end_date=None):
    """Сводная финансовая статистика за период"""
    query = db.query(models.Payments)
    if start_date and end_date:
        query = query.filter(
            models.Payments.payment_date >= start_date,
            models.Payments.payment_date <= end_date,
        )
    payments = query.all()

    total_income = sum(float(p.amount) for p in payments)
    avg_payment  = (total_income / len(payments)) if payments else 0

    # Суммарный долг по всем активным тарифным периодам
    total_debt = db.query(func.sum(models.ChildTariffPeriods.debt)).filter(
        models.ChildTariffPeriods.active == True,
        models.ChildTariffPeriods.debt > 0,
    ).scalar() or 0

    # Суммарный баланс предоплат (balance > 0)
    total_prepaid = db.query(func.sum(models.Children.balance)).filter(
        models.Children.balance > 0,
    ).scalar() or 0

    # Группировка по месяцам для графика
    by_month = defaultdict(float)
    for p in payments:
        key = p.payment_date.strftime('%Y-%m')
        by_month[key] += float(p.amount)

    payments_by_period = [
        {'period': k, 'amount': round(v, 2)}
        for k, v in sorted(by_month.items())
    ]

    return {
        'total_income':    round(total_income, 2),
        'total_debt':      round(float(total_debt), 2),
        'total_prepaid':   round(float(total_prepaid), 2),
        'avg_payment':     round(avg_payment, 2),
        'payments_by_period': payments_by_period,
    }

#==============================
# lesson_attachments
#==============================

def create_lesson_attachment(db: Session, lesson_attachment: schemas.LessonAttachmentsCreate):
    """Создание нового материала к занятию"""
    # Определяем размер файла автоматически
    attachment_data = lesson_attachment.model_dump()
    file_path = attachment_data.get('file_path')
    
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
    else:
        file_size = 0
    
    attachment_data['file_size'] = file_size
    
    db_lesson_attachment = models.LessonAttachments(**attachment_data)
    db.add(db_lesson_attachment)
    db.commit()
    db.refresh(db_lesson_attachment)
    return db_lesson_attachment

def get_lesson_attachment(db: Session, attachment_id: int):
    """Получение данных об одном материале к занятию"""
    return db.query(models.LessonAttachments).filter(
            models.LessonAttachments.attachment_id == attachment_id).first()

def get_all_lesson_attachments(db: Session, skip: int = 0, limit: int = 100):
    """Получение списка материалов к занятиям (опционально последовательность)"""
    return db.query(models.LessonAttachments).offset(skip).limit(limit).all()

def update_lesson_attachment(db: Session, attachment_id: int, lesson_attachment_data: dict):
    """Обновление данных материала к занятию"""
    db_lesson_attachment = db.query(models.LessonAttachments).filter(
            models.LessonAttachments.attachment_id == attachment_id).first()
    if db_lesson_attachment:
        for key, value in lesson_attachment_data.items():
            setattr(db_lesson_attachment, key, value)
        db.commit()
        db.refresh(db_lesson_attachment)
    return db_lesson_attachment

def delete_lesson_attachment(db: Session, attachment_id: int):
    """Удаление материала к занятию"""
    db_lesson_attachment = db.query(models.LessonAttachments).filter(
            models.LessonAttachments.attachment_id == attachment_id).first()
    if db_lesson_attachment:
        db.delete(db_lesson_attachment)
        db.commit()
    return db_lesson_attachment

def get_attachments_by_lesson(db: Session, lesson_id: int):
    """Получить все вложения (ДЗ, материалы) к конкретному уроку"""
    return db.query(models.LessonAttachments).filter(
        models.LessonAttachments.lesson_id == lesson_id
    ).all()

#==============================
# payment_details
#==============================

def create_payment_details(db: Session, payment_details: schemas.PaymentDetailsCreate):
    """Создание новой информации об оплате"""
    db_payment_details = models.PaymentDetails(**payment_details.model_dump())
    db.add(db_payment_details)
    db.commit()
    db.refresh(db_payment_details)
    return db_payment_details

def get_payment_details(db: Session, payment_details_id: int):
    """Получение данных об одной записи информации об оплате"""
    return db.query(models.PaymentDetails).filter(
            models.PaymentDetails.payment_details_id == payment_details_id).first()

def get_all_payment_details(db: Session):
    """Получение списка записей информации об оплате"""
    return db.query(models.PaymentDetails).all()

def update_payment_details(db: Session, payment_details_id: int, payment_data: dict):
    """Обновление данных записи информации об оплате"""
    db_payment_details = db.query(models.PaymentDetails).filter(
            models.PaymentDetails.payment_details_id == payment_details_id).first()
    if db_payment_details:
        for key, value in payment_data.model_dump().items():
            setattr(db_payment_details, key, value)
        db.commit()
        db.refresh(db_payment_details)
    return db_payment_details

def delete_payment_details(db: Session, payment_details_id: int):
    """Удаление записи информации об оплате"""
    db_payment_details = db.query(models.PaymentDetails).filter(
            models.PaymentDetails.payment_details_id == payment_details_id).first()
    if db_payment_details:
        db.delete(db_payment_details)
        db.commit()
    return db_payment_details

def get_current_payment_details(db: Session):
    """Получить текущие реквизиты для оплаты (последняя запись)"""
    return db.query(models.PaymentDetails).order_by(
        models.PaymentDetails.created_at.desc()
    ).first()