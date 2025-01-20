from peewee import SqliteDatabase, Model,CharField,ForeignKeyField

db = SqliteDatabase('sqlite.db')

class Table(Model):
    """БД"""
    class Meta:
        """БД"""
        database = db

class User (Table):
    login = CharField()
    password = CharField()
    full_name = CharField()

class Teacher (Table):
    user = ForeignKeyField(User, backref='teacher',on_delete="CASCADE", on_update="CASCADE")
    add_teacher = ForeignKeyField("self", on_delete="CASCADE", on_update="CASCADE")

class Student (Table):
    user = ForeignKeyField(User, backref='student',on_delete="CASCADE",on_update="CASCADE")
    add_teacher = ForeignKeyField(Teacher, on_delete="CASCADE", on_update="CASCADE")

class Acc (Table):
    titel = CharField()
    description = CharField()
    image = CharField()

class GiveAcc (Table):
    teacher = ForeignKeyField(Teacher, backref='giveacc',on_delete="CASCADE",on_update="CASCADE")
    student = ForeignKeyField(Student, backref='giveacc',on_delete="CASCADE",on_update="CASCADE")
    acc = ForeignKeyField(Acc, backref='giveacc',on_delete="CASCADE",on_update="CASCADE")
    date_time = CharField()


if __name__ == "__main__":
    db.connect()
    db.create_tables([User,Teacher,Student,Acc,GiveAcc], safe=True)
    db.close()
