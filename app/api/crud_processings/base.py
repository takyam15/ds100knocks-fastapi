from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_record(session: Session, Model, primary_key_id):
    primary_key_column = [
        column.name for column in Model.__table__.primary_key.columns
    ][0]
    return session.scalars(
        select(Model).where(getattr(Model, primary_key_column) == primary_key_id)
    ).one()


def get_reference_model(foreign_key_column, Models):
    for Model in Models:
        primary_key_columns = [
            column.name for column in Model.__table__.primary_key.columns
        ]
        if foreign_key_column in primary_key_columns:
            return Model
        
def get_foreign_key_columns(record):
    foreign_key_columns = [
        fk.column.name for fk in record.__table__.foreign_keys
    ]
    return foreign_key_columns
        

def record_to_dict(session: Session, record):
    # master_models = Tuple[Model]
    # transaction_models = Tuple[Model]
    # all_models = master_models + transaction_models
    # schemas = {table_name: Schema}
    foreign_key_columns = get_foreign_key_columns(record)
    record_dict = {}
    for column in record.__table__.columns:
        if column in foreign_key_columns:
            ReferenceModel = get_reference_model(column)
            reference_record_id = record.column
            reference_record = get_record(session, ReferenceModel, reference_record_id)
            reference_table_name = reference_record.__table__.name
            del record.column
            setattr(
                record, reference_table_name, record_to_dict(session, reference_record)
            )
        else:
            record_dict[column] = record.column
    return record_dict


def record_to_schema(session: Session, record, schemas):
    record_dict = record_to_dict(session, record)
    table_name = record.__table__.name
    return schemas[table_name].model_validate(record_dict)


def get_schema_summary(session: Session, record):
    retrieved_schema = record_to_schema(session, record)
    return retrieved_schema.get_summary()
