from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import crud, models, schemas
from .database import Base, engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from datetime import date

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

#==============================
# Самостоятельные коллекции
#==============================

# ===== children =====
@app.post("/children/", response_model=schemas.ChildrenRead)
def create_child(child: schemas.ChildrenCreate, db: Session = Depends(get_db)):
    """Создать ученика"""
    return crud.create_child(db=db, child=child)

@app.get("/children/", response_model=list[schemas.ChildrenRead])
def read_children(db: Session = Depends(get_db)):
    """Получить данные о списке учеников"""
    return crud.get_all_children(db=db)

@app.get("/children/{child_id}", response_model=schemas.ChildrenRead)
def read_child(child_id: int, db: Session = Depends(get_db)):
    """Получить данные об одном ученике"""
    db_child = crud.get_child(db=db, child_id=child_id)
    if db_child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ребенок с id {child_id} не найден")
    return db_child

@app.patch("/children/{child_id}", response_model=schemas.ChildrenRead)
def update_child(child_id: int, child_data: schemas.ChildrenCreate, db: Session = Depends(get_db)):
    """Обновить данные ученика"""
    if not crud.get_child(db=db, child_id=child_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ребенок с id {child_id} не найден")
    return crud.update_child(db=db, child_id=child_id, child_data=child_data)

@app.delete("/children/{child_id}", response_model=schemas.ChildrenRead)
def delete_child(child_id: int, db: Session = Depends(get_db)):
    """Удалить ученика"""
    if not crud.get_child(db=db, child_id=child_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ребенок с id {child_id} не найден")
    return crud.delete_child(db=db, child_id=child_id)

# ===== parents =====
@app.post("/parents/", response_model=schemas.ParentsRead)
def create_parent(parent: schemas.ParentsCreate, db: Session = Depends(get_db)):
    """Создать родителя"""
    return crud.create_parent(db=db, parent=parent)

@app.get("/parents/", response_model=list[schemas.ParentsRead])
def read_parents(db: Session = Depends(get_db)):
    """Получить данные о всех родителях"""
    return crud.get_all_parents(db=db)

@app.get("/parents/{parent_id}", response_model=schemas.ParentsRead)
def read_parent(parent_id: int, db: Session = Depends(get_db)):
    """Получить данные одного родителя"""
    db_parent = crud.get_parent(db=db, parent_id=parent_id)
    if db_parent is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Родитель с id {parent_id} не найден")
    return db_parent

@app.patch("/parents/{parent_id}", response_model=schemas.ParentsRead)
def update_parent(parent_id: int, parent_data: schemas.ParentsCreate, db: Session = Depends(get_db)):
    """Обновить данные родителя"""
    if not crud.get_parent(db=db, parent_id=parent_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Родитель с id {parent_id} не найден")
    return crud.update_parent(db=db, parent_id=parent_id, parent_data=parent_data)

@app.delete("/parents/{parent_id}", response_model=schemas.ParentsRead)
def delete_parent(parent_id: int, db: Session = Depends(get_db)):
    """Удалить родителя"""
    if not crud.get_parent(db=db, parent_id=parent_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Родитель с id {parent_id} не найден")
    return crud.delete_parent(db=db, parent_id=parent_id)

# ===== lessons =====
@app.post("/lessons/", response_model=schemas.LessonsRead)
def create_lesson(lesson: schemas.LessonsCreate, db: Session = Depends(get_db)):
    """Создать занятие (только если нет другого занятия в это время)"""
    overlap = crud.get_overlapping_lesson(db, lesson.child_id, lesson.lesson_datetime)
    if overlap:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"У ученика уже есть занятие в это время (id={overlap.lesson_id})")
    return crud.create_lesson(db=db, lesson=lesson)

@app.get("/lessons/", response_model=list[schemas.LessonsRead])
def read_lessons(skip: int = 0, limit: int = 100, start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    """Получить данные о списке занятий"""
    return crud.get_all_lessons(db=db, skip=skip, limit=limit, start_date=start_date, end_date=end_date)

@app.get("/lessons/{lesson_id}", response_model=schemas.LessonsRead)
def read_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Получить данные об одном занятии"""
    db_lesson = crud.get_lesson(db=db, lesson_id=lesson_id)
    if db_lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Занятие с id {lesson_id} не найдено")
    return db_lesson

@app.patch("/lessons/{lesson_id}/report", response_model=schemas.LessonsRead)
def update_lesson(lesson_id: int, lesson_update: schemas.LessonsCreate, db: Session = Depends(get_db)):
    """
    Обновить данные занятия (тема, оценка, заметки, статус, время).
    При смене статуса на 'completed' автоматически списывается одно занятие с активного тарифа.
    Если активного тарифа нет — завершить занятие нельзя.
    При изменении времени проверяется пересечение с другими занятиями ученика.
    """
    db_lesson = crud.get_lesson(db, lesson_id)
    if not db_lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Занятие с id {lesson_id} не найдено")
    old_status = db_lesson.status
    update_data = lesson_update.model_dump(exclude_unset=True)
    if 'lesson_datetime' in update_data:
        overlap = crud.get_overlapping_lesson(db, db_lesson.child_id, update_data['lesson_datetime'], exclude_lesson_id=lesson_id)
        if overlap:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"У ученика уже есть занятие в это время (id={overlap.lesson_id})")
    updated_lesson = crud.update_lesson(db, lesson_id, update_data)
    if old_status != 'completed' and updated_lesson.status == 'completed':
        active_period = crud.get_active_tariff_by_child(db, updated_lesson.child_id)
        if active_period:
            try:
                crud.decrement_lessons_rest(db, active_period['tariff_period'].tariff_period_id)
            except ValueError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Невозможно завершить занятие: у ученика нет активного тарифа")
    return updated_lesson

@app.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Удалить занятие"""
    if not crud.get_lesson(db, lesson_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Занятие с id {lesson_id} не найдено")
    crud.delete_lesson(db, lesson_id)
    return {"message": "Занятие удалено"}

@app.patch("/lessons/{lesson_id}/clear-note/", response_model=schemas.LessonsRead)
def clear_lesson_note(lesson_id: int, data: schemas.ClearNoteRequest, db: Session = Depends(get_db)):
    """
    Очистить заметку в занятии.
    Поле field: 'notes_for_yourself' или 'notes_for_parents'.
    """
    try:
        result = crud.clear_lesson_notes(db, lesson_id, data.field)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not result:
        raise HTTPException(status_code=404, detail="Занятие не найдено")
    return result

# ===== tariff =====
@app.post("/tariff/", response_model=schemas.TariffRead)
def create_tariff(tariff: schemas.TariffCreate, db: Session = Depends(get_db)):
    """Создать тариф"""
    return crud.create_tariff(db=db, tariff=tariff)

@app.get("/tariff/", response_model=list[schemas.TariffRead])
def read_tariffs(db: Session = Depends(get_db)):
    """Получить данные обо всех тарифах"""
    return crud.get_all_tariffs(db=db)

@app.get("/tariff/archived/", response_model=list[schemas.TariffRead])
def read_archived_tariffs(db: Session = Depends(get_db)):
    """Получить данные об архиве тарифов"""
    return crud.get_archived_tariffs(db=db)

@app.get("/tariff/{tariff_id}", response_model=schemas.TariffRead)
def read_tariff(tariff_id: int, db: Session = Depends(get_db)):
    """Получить данные об одном тарифе"""
    db_tariff = crud.get_tariff(db=db, tariff_id=tariff_id)
    if db_tariff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Тарифа с id {tariff_id} не найдено")
    return db_tariff

@app.patch("/tariff/{tariff_id}", response_model=schemas.TariffRead)
def update_tariff(tariff_id: int, tariff_data: schemas.TariffCreate, db: Session = Depends(get_db)):
    """Обновить данные о тарифе"""
    if not crud.get_tariff(db=db, tariff_id=tariff_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Тариф с id {tariff_id} не найден")
    return crud.update_tariff(db=db, tariff_id=tariff_id, tariff_data=tariff_data)

@app.delete("/tariff/{tariff_id}")
def delete_tariff(tariff_id: int, db: Session = Depends(get_db)):
    """Удалить тариф"""
    if not crud.get_tariff(db=db, tariff_id=tariff_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Тариф с id {tariff_id} не найден")
    try:
        return crud.delete_tariff(db=db, tariff_id=tariff_id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Нельзя удалить тариф: он используется в тарифных периодах учеников"
        )

# ===== payments =====
@app.post("/payments/", response_model=schemas.PaymentsRead)
def create_payment(payment: schemas.PaymentsCreate, db: Session = Depends(get_db)):
    """Добавить оплату"""
    return crud.create_payment(db=db, payment=payment)

@app.get("/payments/", response_model=list[schemas.PaymentsRead])
def read_payments(skip: int = 0, limit: int = 100, start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    """Получить данные о списке оплат"""
    return crud.get_all_payments(db=db, skip=skip, limit=limit, start_date=start_date, end_date=end_date)

@app.delete("/payments/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    """Удалить оплату"""
    if not crud.get_payment(db, payment_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Платёж не найден")
    return crud.delete_payment(db, payment_id)

# ===== tariff-periods =====
@app.patch("/tariff-periods/{tariff_period_id}/", response_model=schemas.ChildTariffPeriodsRead)
def update_tariff_period(tariff_period_id: int, data: schemas.UpdateTariffPeriodRequest, db: Session = Depends(get_db)):
    """Обновить данные о текущем тарифном периоде ученика"""
    result = crud.update_tariff_period_fields(db, tariff_period_id, data.lessons_rest, data.debt)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тарифный период не найден")
    return result

@app.post("/tariff-periods/{tariff_period_id}/close/")
def close_tariff_period(tariff_period_id: int, db: Session = Depends(get_db)):
    """Закрыть текущий тарифный период"""
    result = crud.close_tariff_period(db, tariff_period_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тарифный период не найден")
    return {"message": "Тариф закрыт"}

# ===== parent-child =====
@app.post("/parent-child/", response_model=schemas.ParentСhildRead)
def create_parent_child_link(parent_child: schemas.ParentСhildCreate, db: Session = Depends(get_db)):
    """Создать связь между родителем и учеником"""
    if not crud.get_parent(db, parent_child.parent_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Родитель с id {parent_child.parent_id} не найден")
    if not crud.get_child(db, parent_child.child_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ребенок с id {parent_child.child_id} не найден")
    return crud.create_parent_child(db=db, parent_child=parent_child)

@app.patch("/parent-child/{parent_id}/{child_id}")
def update_parent_child_link(parent_id: int, child_id: int, data: schemas.UpdateParentChildRequest, db: Session = Depends(get_db)):
    """Обновить поле 'главный контакт'"""
    db_parent_child = crud.update_parent_child(db, parent_id, child_id, data)
    if not db_parent_child:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Связь родитель ({parent_id}) - ребенок ({child_id}) не найдена")
    return db_parent_child

@app.delete("/parent-child/{parent_id}/{child_id}")
def delete_parent_child_link(parent_id: int, child_id: int, db: Session = Depends(get_db)):
    """Удалить связь между родителем и учеником"""
    db_parent_child = crud.delete_parent_child(db, parent_id, child_id)
    if not db_parent_child:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Связь родитель ({parent_id}) - ребенок ({child_id}) не найдена")
    return {"message": "Связь удалена успешно"}

# ===== payment_details =====
@app.post("/payment-details/", response_model=schemas.PaymentDetailsRead)
def create_payment_details(payment_details: schemas.PaymentDetailsCreate, db: Session = Depends(get_db)):
    """Создать информацию об оплате"""
    return crud.create_payment_details(db=db, payment_details=payment_details)

@app.get("/payment-details/latest/", response_model=schemas.PaymentDetailsRead)
def get_latest_payment_details(db: Session = Depends(get_db)):
    """Получать актуальную информацию об оплате"""
    result = crud.get_current_payment_details(db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Реквизиты не найдены")
    return result

@app.patch("/payment-details/{payment_details_id}", response_model=schemas.PaymentDetailsRead)
def update_payment_details(payment_details_id: int, data: schemas.PaymentDetailsCreate, db: Session = Depends(get_db)):
    """Обновить существующие реквизиты."""
    db_details = crud.get_payment_details(db, payment_details_id)
    if not db_details:
        raise HTTPException(status_code=404, detail="Реквизиты не найдены")
    return crud.update_payment_details(db, payment_details_id, data)

@app.get("/payment-details/{payment_details_id}", response_model=schemas.PaymentDetailsRead)
def read_payment_details(payment_details_id: int, db: Session = Depends(get_db)):
    """Получить конкретную информацию об оплате"""
    db_payment_details = crud.get_payment_details(db=db, payment_details_id=payment_details_id)
    if db_payment_details is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Реквизиты с id {payment_details_id} не найдены")
    return db_payment_details

# ===== lesson_attachments =====
@app.post("/lesson-attachments/", response_model=schemas.LessonAttachmentsRead)
def create_lesson_attachment(lesson_attachment: schemas.LessonAttachmentsCreate, db: Session = Depends(get_db)):
    """Создать материал к занятию"""
    return crud.create_lesson_attachment(db=db, lesson_attachment=lesson_attachment)

@app.get("/lesson-attachments/{attachment_id}", response_model=schemas.LessonAttachmentsRead)
def read_lesson_attachment(attachment_id: int, db: Session = Depends(get_db)):
    """Получить материал к занятию"""
    db_attachment = crud.get_lesson_attachment(db=db, attachment_id=attachment_id)
    if db_attachment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Материал с id {attachment_id} не найден")
    return db_attachment

#==============================
# Вложенные ресурсы
#==============================

# ===== children → ... =====
@app.get("/children/{child_id}/parents/", response_model=list[schemas.ParentsRead])
def read_child_parents(child_id: int, db: Session = Depends(get_db)):
    """Получить данные о родителях ученика"""
    if not crud.get_child(db, child_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ребенок с id {child_id} не найден")
    return crud.get_parents_by_child(db=db, child_id=child_id)

@app.get("/children/{child_id}/lessons/", response_model=list[schemas.LessonsRead])
def read_child_lessons(child_id: int, start_date: date, end_date: date, db: Session = Depends(get_db)):
    """Получить данные о занятиях ученика"""
    if not crud.get_child(db, child_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ребенок с id {child_id} не найден")
    return crud.get_lessons_by_child_and_date_range(db, child_id, start_date, end_date)

@app.get("/children/{child_id}/notes/", response_model=list[schemas.LessonsRead])
def read_child_notes(child_id: int, start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    """Получить данные о заметках об ученике"""
    if not crud.get_child(db, child_id):
        raise HTTPException(status_code=404, detail=f"Ребенок {child_id} не найден")
    return crud.get_child_notes(db, child_id, start_date, end_date)

@app.get("/children/{child_id}/payments/", response_model=list[schemas.PaymentsRead])
def read_child_payments(child_id: int, start_date: date, end_date: date, db: Session = Depends(get_db)):
    """Получить данные об оплатах ученика"""
    if not crud.get_child(db, child_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ребенок с id {child_id} не найден")
    return crud.get_child_payments(db, child_id, start_date, end_date)

@app.get("/children/{child_id}/tariff-periods/", response_model=list[schemas.ChildTariffPeriodsRead])
def get_child_tariff_periods(child_id: int, db: Session = Depends(get_db)):
    """Получить историю тарифных периодов ученика"""
    if not crud.get_child(db, child_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ребенок с id {child_id} не найден")
    return crud.get_all_child_tariff_periods(db, child_id)

@app.get("/children/{child_id}/active-tariff/")
def read_student_status(child_id: int, db: Session = Depends(get_db)):
    """Получить данные тарифа ученика"""
    active_data = crud.get_active_tariff_by_child(db, child_id)
    if not active_data:
        return None
    period = active_data['tariff_period']
    tariff = active_data['tariff']
    return {
        "tariff_name": tariff.name,
        "lessons_rest": period.lessons_rest,
        "total_lessons_in_package": tariff.num_of_lessons,
        "current_debt": period.debt,
        "is_active": period.active
    }

@app.post("/children/{child_id}/assign-tariff/", response_model=schemas.ChildTariffPeriodsRead)
def assign_tariff(child_id: int, data: schemas.AssignTariffRequest, db: Session = Depends(get_db)):
    """Подключение тарифа ученику"""
    if not crud.get_child(db, child_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ребенок с id {child_id} не найден")
    try:
        return crud.assign_tariff_to_child(db, child_id, data.tariff_id, data.start_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ===== parents → ... =====
@app.get("/parents/{parent_id}/children/", response_model=list[schemas.ChildrenRead])
def read_parent_children(parent_id: int, db: Session = Depends(get_db)):
    """Получить данные о детях родителя"""
    if not crud.get_parent(db, parent_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Родитель с id {parent_id} не найден")
    return crud.get_children_by_parent(db=db, parent_id=parent_id)

@app.get("/parents/{parent_id}/children-relations/")
def read_parent_children_relations(parent_id: int, db: Session = Depends(get_db)):
    """Получить всех детей одного родителя со статусом связи is_main"""
    if not crud.get_parent(db, parent_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Родитель с id {parent_id} не найден")
    return crud.get_parent_children_with_relations(db=db, parent_id=parent_id)

@app.get("/parents/{parent_id}/notes/", response_model=list[schemas.LessonsRead])
def read_parent_notes(parent_id: int, start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    """Получить заметки родителю"""
    if not crud.get_parent(db, parent_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Родитель с id {parent_id} не найден")
    return crud.get_parent_notes(db, parent_id, start_date, end_date)

@app.get("/parents/{parent_id}/payments/", response_model=list[schemas.PaymentsRead])
def read_parent_payments(parent_id: int, db: Session = Depends(get_db)):
    """Получить данные об оплатах родителя"""
    if not crud.get_parent(db, parent_id):
        raise HTTPException(status_code=404, detail="Родитель не найден")
    return crud.get_payments_by_parent(db, parent_id)

# ===== tariff → ... =====
@app.get("/tariff/{tariff_id}/active-children-count/")
def get_children_with_tariff_count(tariff_id: int, db: Session = Depends(get_db)):
    """Получить количество учеников с активным конкретным тарифом"""
    if not crud.get_tariff(db, tariff_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Тариф с id {tariff_id} не найден")
    return crud.get_children_with_tariff_count(db=db, tariff_id=tariff_id)

# ===== lessons → ... =====
@app.get("/lessons/{lesson_id}/attachments/", response_model=list[schemas.LessonAttachmentsRead])
def read_lesson_attachments(lesson_id: int, db: Session = Depends(get_db)):
    """Получить материалы к занятию"""
    if not crud.get_lesson(db, lesson_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Занятие с id {lesson_id} не найдено")
    return crud.get_attachments_by_lesson(db, lesson_id)

#==============================
# Статистика
#==============================

@app.get("/debtors/")
def read_debtors(db: Session = Depends(get_db)):
    """Получить данные о должниках"""
    return crud.get_debtors(db=db)

@app.get("/stats/payments-summary/")
def get_payments_summary(start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    """Получить статистику оплат"""
    return crud.get_payments_summary(db, start_date, end_date)