from peewee import SqliteDatabase, Model,CharField,ForeignKeyField,BooleanField

db = SqliteDatabase('sqlite.db')

class Table(Model):
    """БД"""
    class Meta:
        """БД"""
        database = db

class User (Table):
    username = CharField()
    login = CharField(unique=True)
    password = CharField()
    active = BooleanField(default=True)

    

class Teacher (Table):
    user = ForeignKeyField(User, backref='teacher',on_delete="CASCADE", on_update="CASCADE")
    add_teacher = ForeignKeyField("self", on_delete="CASCADE", on_update="CASCADE")

class Student (Table):
    user = ForeignKeyField(User, backref='student',on_delete="CASCADE",on_update="CASCADE")
    add_teacher = ForeignKeyField(Teacher, on_delete="CASCADE", on_update="CASCADE")

class Achievement (Table):
    titel = CharField()
    description = CharField()
    image = CharField()

class GiveAchievement (Table):
    teacher = ForeignKeyField(Teacher, backref='giveachievement',on_delete="CASCADE",on_update="CASCADE")
    student = ForeignKeyField(Student, backref='giveachievement',on_delete="CASCADE",on_update="CASCADE")
    achievement = ForeignKeyField(Achievement, backref='giveachievement',on_delete="CASCADE",on_update="CASCADE")
    date_time = CharField()


if __name__ == "__main__":
    db.connect()
    db.create_tables([User,Teacher,Student,Achievement,GiveAchievement], safe=True)
    db.close()
