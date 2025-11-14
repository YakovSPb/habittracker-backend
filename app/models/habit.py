"""
Модели для привычек, категорий и записей выполнения.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey, ARRAY, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship  # Для связей между таблицами
import uuid
from app.database.database import Base
from datetime import datetime

class HabitCategory(Base):
    #   """
    # Модель категорий привычек.
    # Пользователи могут группировать привычки по категориям (спорт, учеба, здоровье).
    # """
    __tablename__ = "habit_categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    
    # Название категории (например: "Спорт", "Учеба")
    name = Column(String(50), nullable=False)
    
    # Цвет категории в HEX формате для фронтенда
    color = Column(String(7), default="#3B82F6") 
    
    # Связь с пользователем (категория принадлежит пользователю)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Временная метка создания
    created_at = Column(DateTime, default=datetime.time)
    
    # Relationship - связь с моделью User
    # Позволяет обращаться к пользователю через category.user
    user = relationship("User")
    
    # Связь с привычками (одна категория имеет много привычек)
    habits = relationship("Habit", back_populates="category")
    
class Habit(Base):
    """
    Модель привычки.
    Основная сущность - что пользователь хочет отслеживать.
    """
    
    __tablename__ = "habits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Основная информация о привычке
    title = Column(String(100), nullable=False)  # Название привычки
    description = Column(Text)                   # Описание (необязательное)
    
    # Связи с другими таблицами
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))        # Владелец привычки
    category_id = Column(UUID(as_uuid=True), ForeignKey("habit_categories.id"))  # Категория
    
    # Настройки повторения привычки
    frequency_type = Column(String(20), default="daily")  # daily, weekly, monthly
    target_count = Column(Integer, default=1)             # Сколько раз в день/неделю нужно выполнять
    days_of_week = Column(ARRAY(Integer), default=[1,2,3,4,5,6,7])  # Дни недели (1-пн,7-вс)
    
    # Цели для привычки
    target_streak = Column(Integer, default=0)            # Целевой стрик (дней подряд)
    target_completion_rate = Column(Integer, default=100) # Целевой процент выполнения
    
    # Визуальные настройки для фронтенда
    color = Column(String(7), default="#3B82F6")  # Цвет привычки
    icon = Column(String(50), default="📝")       # Иконка эмодзи
    
    # Флаги состояния
    is_active = Column(Boolean, default=True)  # Активна ли привычка
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Автообновление
    
    # Relationships - связи с другими моделями
    user = relationship("User")  # Владелец привычки
    category = relationship("HabitCategory", back_populates="habits")  # Категория
    entries = relationship("HabitEntry", back_populates="habit")       # Записи выполнения
    

class HabitEntry(Base):
    """
    Модель записи выполнения привычки.
    Каждая запись - это факт выполнения привычки в конкретный день.
    """
    
    __tablename__ = "habit_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Связь с привычкой
    habit_id = Column(UUID(as_uuid=True), ForeignKey("habits.id"))
    
    # Дата выполнения (без времени, только день)
    entry_date = Column(DateTime, nullable=False)  # Храним как DateTime для гибкости
    
    # Статус выполнения
    status = Column(String(20), default="completed")  # completed, skipped, partial
    
    # Дополнительные заметки
    notes = Column(Text)  # Пользователь может добавить комментарий
    
    # Временная метка создания записи
    created_at = Column(DateTime, default=datetime.now)
    
    # Связь с привычкой
    habit = relationship("Habit", back_populates="entries")
    
    # Уникальный constraint - нельзя иметь две записи для одной привычки в один день
    __table_args__ = (UniqueConstraint('habit_id', 'entry_date', name='unique_habit_entry'),) 
