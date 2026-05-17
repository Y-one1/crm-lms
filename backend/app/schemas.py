from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, Field
from typing import Optional, Literal
from datetime import date, datetime
import re

#==============================
# service_classes
#==============================

class PhoneValidatorMixin(BaseModel):
    phone_number: str

    @field_validator('phone_number')
    @classmethod
    def normalize_phone(cls, v):
        v = re.sub(r'[^\+\d]', '', v)
        if v.startswith('8'):
            v = '+7' + v[1:]
        elif v.startswith('7'):
            v = '+' + v
        elif not v.startswith('+7'):
            v = '+7' + v
        if len(v) != 12:
            raise ValueError('Неверный формат номера телефона, должно быть +7XXXXXXXXXX')
        return v

#==============================
# children
#==============================

# 1. Схема для создания (без ID и дат, которые создает БД)
# То, что прилетает от пользователя при создании
class ChildrenCreate(PhoneValidatorMixin):
    last_name: str
    first_name: str
    patronymic: Optional[str] = None
    school_class: int = Field(ge=1, le=11)
    notes: Optional[str] = None

# 2. Схема для ответа (включает всё, что есть в БД)
# То, что мы отдаем пользователю
class ChildrenRead(ChildrenCreate):
    child_id: int
    day_of_addition: date
    day_of_last_lesson: Optional[date] = None
    balance: float

    # Это магия, которая позволяет Pydantic читать данные из моделей SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

#==============================
# parents
#==============================

class ParentsCreate(PhoneValidatorMixin):
    last_name: str
    first_name: str
    patronymic: Optional[str] = None
    phone_number: str
    email: EmailStr
    relationship: str
    notes: Optional[str] = None

class ParentsRead(ParentsCreate):
    parent_id: int

    model_config = ConfigDict(from_attributes=True)

#==============================
# parent_child
#==============================

# Здесь нет авто-генерируемого ID, поэтому Read практически повторяет Create
class ParentСhildCreate(BaseModel):
    parent_id: int
    child_id: int
    is_main: bool = False

class ParentСhildRead(ParentСhildCreate):
    # Тут нет id, так как ключи составные
    model_config = ConfigDict(from_attributes=True)

#==============================
# tariff
#==============================

class TariffCreate(BaseModel):
    name: str
    price: int = Field(gt=0)
    num_of_lessons: int = Field(gt=0)
    tariff_type: str

class TariffRead(TariffCreate):
    tariff_id: int
    is_archived: bool = False

    model_config = ConfigDict(from_attributes=True)

#==============================
# child_tariff_periods
#==============================

class ChildTariffPeriodsCreate(BaseModel):
    child_id: int
    tariff_id: int
    start_date: date
    lessons_rest: int
    debt: float = Field(ge=0)
    active: bool = True

class ChildTariffPeriodsRead(ChildTariffPeriodsCreate):
    tariff_period_id: int
    consecutive_count: int = 1

    model_config = ConfigDict(from_attributes=True)

#==============================
# lessons
#==============================

class LessonsCreate(BaseModel):
    child_id: int
    lesson_datetime: datetime
    theme: str
    status: Literal['planned', 'completed', 'cancelled'] = 'planned'
    homework_done: bool = False
    grade: Optional[int] = Field(default=None, ge=2, le=5)
    notes_for_yourself: Optional[str] = None
    notes_for_parents: Optional[str] = None

class LessonsRead(LessonsCreate):
    lesson_id: int

    model_config = ConfigDict(from_attributes=True)

#==============================
# payments
#==============================

class PaymentsCreate(BaseModel):
    child_id: int
    parent_id: int
    amount: float = Field(gt=0)
    method: Literal['cash', 'card', 'bank_transfer', 'sbp', 'online_payment', 'qr_code']

class PaymentsRead(PaymentsCreate):
    payment_id: int
    payment_date: date

    model_config = ConfigDict(from_attributes=True)

#==============================
# lesson_attachments
#==============================

class LessonAttachmentsCreate(BaseModel):
    lesson_id: int
    file_path: str
    file_name: str

class LessonAttachmentsRead(LessonAttachmentsCreate):
    attachment_id: int
    uploaded_at: datetime
    file_size: int

    model_config = ConfigDict(from_attributes=True)

#==============================
# payment_details
#==============================

class PaymentDetailsCreate(BaseModel):
    details_text: str
    tutor_name: Optional[str] = None
    tutor_phone: Optional[str] = None
    tutor_subject: Optional[str] = None
    tutor_bio: Optional[str] = None

class PaymentDetailsRead(PaymentDetailsCreate):
    payment_details_id: int
    created_at: date

    model_config = ConfigDict(from_attributes=True)

#==============================
# service_classes
#==============================

# При назначении тарифа ученику фронт присылает только это
class AssignTariffRequest(BaseModel):
    tariff_id: int
    start_date: date

# При обновлении тарифа ученика фронт присылает только это
class UpdateTariffPeriodRequest(BaseModel):
    lessons_rest: Optional[int] = None
    debt: Optional[float] = None

# При очистке заметки фронт говорит, какую именно
class ClearNoteRequest(BaseModel):
    field: Literal['notes_for_yourself', 'notes_for_parents']

# Для смены флага "основной контакт" между родителем и учеником
class UpdateParentChildRequest(BaseModel):
    is_main: bool