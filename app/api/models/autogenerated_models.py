from typing import List, Optional

from sqlalchemy import Column, Date, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, Table
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = (
        PrimaryKeyConstraint('category_small_cd', name='category_pk'),
    )

    category_small_cd = mapped_column(String)
    category_major_cd = mapped_column(String)
    category_major_name = mapped_column(String)
    category_medium_cd = mapped_column(String)
    category_medium_name = mapped_column(String)
    category_small_name = mapped_column(String)

    product: Mapped[List['Product']] = relationship('Product', uselist=True, back_populates='category')


t_geocode = Table(
    'geocode', metadata,
    Column('postal_cd', String),
    Column('prefecture', String),
    Column('city', String),
    Column('town', String),
    Column('street', String),
    Column('address', String),
    Column('full_address', String),
    Column('longitude', Numeric),
    Column('latitude', Numeric)
)


class Store(Base):
    __tablename__ = 'store'
    __table_args__ = (
        PrimaryKeyConstraint('store_cd', name='store_pk'),
    )

    store_cd = mapped_column(String)
    store_name = mapped_column(String)
    prefecture_cd = mapped_column(String)
    prefecture = mapped_column(String)
    address = mapped_column(String)
    address_kana = mapped_column(String)
    tel_no = mapped_column(String)
    longitude = mapped_column(Numeric)
    latitude = mapped_column(Numeric)
    floor_area = mapped_column(Numeric)

    customer: Mapped[List['Customer']] = relationship('Customer', uselist=True, back_populates='store')
    receipt: Mapped[List['Receipt']] = relationship('Receipt', uselist=True, back_populates='store')


class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = (
        ForeignKeyConstraint(['application_store_cd'], ['store.store_cd'], name='customer_store_fk'),
        PrimaryKeyConstraint('customer_id', name='customer_pk')
    )

    customer_id = mapped_column(String)
    customer_name = mapped_column(String)
    gender_cd = mapped_column(String)
    gender = mapped_column(String)
    birth_day = mapped_column(Date)
    age = mapped_column(Integer)
    postal_cd = mapped_column(String)
    address = mapped_column(String)
    application_store_cd = mapped_column(String)
    application_date = mapped_column(String)
    status_cd = mapped_column(String)

    store: Mapped[Optional['Store']] = relationship('Store', back_populates='customer')


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = (
        ForeignKeyConstraint(['category_small_cd'], ['category.category_small_cd'], name='product_category_fk'),
        PrimaryKeyConstraint('product_cd', name='product_pk')
    )

    product_cd = mapped_column(String)
    category_major_cd = mapped_column(String)
    category_medium_cd = mapped_column(String)
    category_small_cd = mapped_column(String)
    unit_price = mapped_column(Integer)
    unit_cost = mapped_column(Integer)

    category: Mapped[Optional['Category']] = relationship('Category', back_populates='product')
    receipt: Mapped[List['Receipt']] = relationship('Receipt', uselist=True, back_populates='product')


class Receipt(Base):
    __tablename__ = 'receipt'
    __table_args__ = (
        ForeignKeyConstraint(['product_cd'], ['product.product_cd'], name='receipt_product_fk'),
        ForeignKeyConstraint(['store_cd'], ['store.store_cd'], name='receipt_store_fk'),
        PrimaryKeyConstraint('sales_ymd', 'store_cd', 'receipt_no', 'receipt_sub_no', name='receipt_pk')
    )

    sales_ymd = mapped_column(Integer, nullable=False)
    store_cd = mapped_column(String, nullable=False)
    receipt_no = mapped_column(SmallInteger, nullable=False)
    receipt_sub_no = mapped_column(SmallInteger, nullable=False)
    sales_epoch = mapped_column(Integer)
    customer_id = mapped_column(String)
    product_cd = mapped_column(String)
    quantity = mapped_column(Integer)
    amount = mapped_column(Integer)

    product: Mapped[Optional['Product']] = relationship('Product', back_populates='receipt')
    store: Mapped['Store'] = relationship('Store', back_populates='receipt')
