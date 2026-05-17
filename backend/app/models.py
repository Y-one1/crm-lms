from app.database import Base
from sqlalchemy import Enum
from sqlalchemy import Column, Integer, String, Date, SmallInteger, \
                       Text, Boolean, ForeignKey, text, Numeric, DateTime

# Определяем типы (PostgreSQL подхватит их из схемы)
payment_method_enum = Enum(
    'cash', 'card', 'bank_transfer', 'sbp', 'online_payment', 'qr_code',
    name='payment_method',
    create_type=False
)
lesson_status_enum = Enum(
    'planned', 'completed', 'cancelled',
    name='lesson_status',
    schema='crm',
    create_type=False
)

#==============================
# children
#==============================

class Children(Base):
    __tablename__ = 'children'
    __table_args__ = {'schema': 'crm'}

    child_id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    patronymic = Column(String(50))
    phone_number = Column(String(20), nullable=False)
    school_class = Column('class', SmallInteger, nullable=False)
    day_of_addition = Column(Date, server_default=text('CURRENT_DATE'))
    day_of_last_lesson = Column(Date)
    notes = Column(Text)
    balance = Column(Numeric(10, 2), nullable=False, server_default=text('0'))

#==============================
# parents
#==============================

class Parents(Base):
    __tablename__ = 'parents'
    __table_args__ = {'schema': 'crm'}

    parent_id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    patronymic = Column(String(50))
    phone_number = Column(String(20), nullable=False)
    email = Column(Text, nullable=False, unique=True)
    relationship = Column(String(50), nullable=False)
    notes = Column(Text)

#==============================
# parent_child
#==============================

class ParentChild(Base):
    __tablename__ = 'parent_child'
    __table_args__ = {'schema': 'crm'}

    parent_id = Column(Integer, ForeignKey('crm.parents.parent_id', ondelete='CASCADE'), primary_key=True)
    child_id = Column(Integer, ForeignKey('crm.children.child_id', ondelete='CASCADE'), primary_key=True)
    is_main = Column(Boolean, default=False)

#==============================
# tariff
#==============================

class Tariff(Base):
    __tablename__ = 'tariff'
    __table_args__ = {'schema': 'crm'}

    tariff_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    num_of_lessons = Column(SmallInteger, nullable=False)
    tariff_type = Column(String(50), nullable=False)
    is_archived = Column(Boolean, nullable=False, default=False)

#==============================
# child_tariff_periods
#==============================

class ChildTariffPeriods(Base):
    __tablename__ = 'child_tariff_periods'
    __table_args__ = {'schema': 'crm'}

    tariff_period_id  = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('crm.children.child_id', ondelete='CASCADE'), nullable=False)
    tariff_id = Column(Integer, ForeignKey('crm.tariff.tariff_id', ondelete='RESTRICT'), nullable=False)
    start_date = Column(Date, nullable=False)
    lessons_rest = Column(SmallInteger, nullable=False)
    debt = Column(Numeric(10, 2), nullable=False)
    active = Column(Boolean, default=True)
    consecutive_count = Column(Integer, default=1)

#==============================
# lessons
#==============================

class Lessons(Base):
    __tablename__ = 'lessons'
    __table_args__ = {'schema': 'crm'}

    lesson_id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('crm.children.child_id', ondelete='CASCADE'), nullable=False)
    lesson_datetime = Column(DateTime, nullable=False)
    theme = Column(String(50), nullable=False)
    status = Column(lesson_status_enum, default='planned')
    homework_done = Column(Boolean, default=False)
    grade = Column(SmallInteger, nullable=True)  # теперь nullable, т.к. плана урока ещё не оценена
    notes_for_yourself = Column(Text)
    notes_for_parents = Column(Text)

#==============================
# payments
#==============================

class Payments(Base):
    __tablename__ = 'payments'
    __table_args__ = {'schema': 'crm'}

    payment_id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('crm.children.child_id', ondelete='SET NULL'))
    parent_id = Column(Integer, ForeignKey('crm.parents.parent_id', ondelete='SET NULL'))
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date, server_default=text('CURRENT_DATE'))
    method = Column(payment_method_enum, nullable=False)

#==============================
# lesson_attachments
#==============================

class LessonAttachments(Base):
    __tablename__ = 'lesson_attachments'
    __table_args__ = {'schema': 'crm'}

    attachment_id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('crm.lessons.lesson_id', ondelete='CASCADE'), nullable=False)
    file_path = Column(Text, nullable=False)
    file_name = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

#==============================
# payment_details
#==============================

class PaymentDetails(Base):
    __tablename__ = 'payment_details'
    __table_args__ = {'schema': 'crm'}

    payment_details_id = Column(Integer, primary_key=True)
    details_text = Column(Text, nullable=False)
    created_at = Column(Date, server_default=text('CURRENT_DATE'))
    tutor_name = Column(String(100))
    tutor_phone = Column(String(20))
    tutor_subject = Column(String(50))
    tutor_bio = Column(Text)