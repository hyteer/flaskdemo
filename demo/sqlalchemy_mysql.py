
'''
from sqlalchemy import create_engine, Table,Column,Integer,String,MetaData,ForeignKey

engine = create_engine("mysql+pymysql://tester:111@192.168.198.128:3306/test",echo=True)

metadata = MetaData(engine)

user = Table('user',metadata,
        Column('id',Integer,primary_key=True),
        Column('name',String(20)),
        Column('fullname',String(40))
        )
address_table = Table('address',metadata,
        Column('id',Integer,primary_key=True),
        Column('user_id', None, ForeignKey('user.id')),
        Column('email', String(128), nullable=False)
        )

metadata.create_all()
'''

from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey
engine=create_engine("mysql+pymysql://root:111@192.168.198.128:3306/test",echo=True)
metadata=MetaData(engine)

user=Table('user',metadata,
    Column('id',Integer,primary_key=True),
    Column('name',String(20)),
    Column('fullname',String(40)),
    )
address_table = Table('address', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', None, ForeignKey('user.id')),
    Column('email', String(128), nullable=False)
    )

import pdb; pdb.set_trace()

#metadata.create_all()
