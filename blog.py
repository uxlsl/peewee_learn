#-*-coding:utf-8-*-

import random
import faker
from faker import Factory
from peewee import *

database = SqliteDatabase('blog.db')


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    username = CharField(max_length=64, null=False, index=True)
    password = CharField(max_length=64, null=False)
    email = CharField(max_length=64, null=False, index=True)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


class UserInfo(BaseModel):
    name = CharField(max_length=64)
    qq = CharField(max_length=11)
    phone = CharField(max_length=11)
    link = CharField(max_length=64)
    user = ForeignKeyField(User, backref="userinfo")


class Category(BaseModel):
    name = CharField(max_length=64, null=False, index=True)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)

    class Meta:
        database = database


class Tag(BaseModel):
    name = CharField(max_length=64)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)


class Article(BaseModel):
    title = CharField(max_length=255, null=False, index=True)
    content = TextField()
    author =  ForeignKeyField(User, backref='articles')
    tags = ManyToManyField(Tag, backref='articles')
    category = ForeignKeyField(Category, backref='articles')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.title)


if __name__ == '__main__':
    database.connect()
    database.create_tables([User, UserInfo,
                            Article,
                            Article.tags.get_through_model(),
                            Category,
                            Tag])

    faker = Factory.create()

    faker_users = [User.create(
        username=faker.name(),
        password=faker.word(),
        email=faker.email(),
    ) for i in range(10)]

    faker_categories = [Category.create(name=faker.word()) for i in range(5)]


    faker_tags= [Tag.create(name=faker.word()) for i in range(20)]


    for i in range(100):
        article = Article(
            title=faker.sentence(),
            content=' '.join(faker.sentences(nb=random.randint(10, 20))),
            author=random.choice(faker_users),
            category=random.choice(faker_categories)
        )

        article.save()

        for tag in random.sample(faker_tags, random.randint(2, 5)):
            article.tags.add(tag)

        article.save()
