# peewee教程-python另类orm
## 一、实验介绍
### 1.1 实验内容

创建一个博客应用所需要的数据表，并介绍了使用 SQLAlchemy 进行简单了 CURD 操作及使用 Faker 生成测试数据

### 1.2 实验知识点 
+ 学会用 peewee 连接数据库(MySQL, SQLite, PostgreSQL), 创建数据表；
+ 掌握表数据之间一对一，一对多及多对多的关系并能转化为对应 peewee 描述；
+ 掌握使用 peewee 进行 CURD 操作；
+ 学会使用 Faker 生成测试数据

### 1.3 实验环境

ubuntu 14.04

### 1.4 适合人群

python 初学者

### 1.5 代码获取

```

git clone git@github.com:uxlsl/peewee_learn.git


```


## 二、实验原理

### ORM 与 peewee 简介

ORM 全称 Object Relational Mapping, 翻译过来叫对象关系映射。简单的说，ORM 将数据库中的表与面向对象语言中的类建立了一种对应关系。这样，我们要操作数据库，数据库中的表或者表中的一条记录就可以直接通过操作类或者类实例来完成

peewee 是一个简单，小的ORM, 它只有很少概念, 容易学习与使用.
+ 少的表达式
+ 支持2.7+ 3.2+
+ 支持sqlite,mysql, postgresql
+ 支持一些扩展, postgres hstore/json/array,sqlite 全文检索

## 三、开发准备

安装peewee, 由于使用最新的peewee，pypi目前不是最新版本,
所以安装最新版的peewee, 使用pip git+ 安装


```

 pip install git+https://github.com/coleifer/peewee.git


```

## 四、实验步骤

### 连接数据库

目前先使用 sqlite 数据库，实验


``` python

from peewee import *

database = SqliteDatabase('blog.db')
database.connect()


```

### 描述表结构
与django orm sqlalchemy差不多


``` python


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    username = CharField(max_length=64, null=False, index=True)
    password = CharField(max_length=64, null=False)
    email = CharField(max_length=64, null=False, index=True)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)

```

### 建表

使用database的create_tables方法

``` python

database.connect()
database.create_tables([User])

```

### 一对一，一对多的定义

对于一个普通的博客应用来说，用户和文章显然是一个一对多的关系，一篇文章属于一个用户，一个用户可以写很多篇文章，那么他们之间的关系可以这样定义：

``` python

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


class Article(BaseModel):
    title = CharField(max_length=255, null=False, index=True)
    content = TextField()
    author =  ForeignKeyField(User, backref='articles')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.title)

```


对于一个普通的博客应用来说，用户和文章显然是一个一对多的关系，一篇文章属于一个用户，一个用户可以写很多篇文章，那么他们之间的关系可以这样定义：


``` python


    author =  ForeignKeyField(User, backref='articles')

```

### 多对多关系
一篇文章通常有好几个标签, 标签与博客之间就是一个多对多的关系
可以直接使用peewee， ManyToManyField


``` python

    tags = ManyToManyField(Tag, backref='articles')


```

### 建表

``` python

    database.connect()
    database.create_tables([User, UserInfo,
                            Article,
                            Article.tags.get_through_model(),
                            Category,
                            Tag])
```

### 简单操作
#### 插入一些测试数据

``` python

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

```

#### create

```

In [15]: bar = User.create(username='bar', password='123456', email='bar@qq.com')

In [16]: list(User.filter(username='bar'))
Out[16]: [User('bar')]

```

#### update

```

In [19]: bar =User.get(username='bar')

In [20]: bar
Out[20]: User('bar')

In [21]: bar.email
Out[21]: 'bar@qq.com'

In [22]: bar.email = 'bar123@qq.com'

In [23]: bar.save()
Out[23]: 1

In [24]: bar =User.get(username='bar')

In [25]: bar.email
Out[25]: 'bar123@qq.com'

```

#### retrieve
可以使用model多种方法

+ User.get(username='XXX') 拿一个
+ User.select().where(User.username = 'XXX') 返回迗代子
+ User.filter(username='XXX') 返回迗代子


```

In [41]: User.get(username='bar')
Out[41]: User('bar')

In [42]: list(User.select().where(User.username=='bar'))
Out[42]: [User('bar')]

In [43]: list(User.filter(username='bar'))
Out[43]: [User('bar')]

```

#### delete

```

In [24]: bar = User.create(username='bar', password='123456', email='bar@qq.com')

In [25]: bar
Out[25]: User('bar')

In [26]: list(User.select())
Out[26]: [User('bar')]

In [27]: bar.delete_instance()
Out[27]: 1

In [28]: list(User.select())
Out[28]: []

```

可以看到已经查不到了!


## 五、全部源代码

``` python

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

```

## 六、实验总结
学习peewee的连接数据库和一些基本的使用!

## 七、课后习题

+ 学习peewee更高级的查询,插入的方法
+ 学习peewee扩展模块playhouse的使用

## 八、参考链接


+ [SQLAlchemy 基础教程](https://www.shiyanlou.com/courses/724/labs/2382/document)

+ [peewee 3.0.6 documentation](http://docs.peewee-orm.com/en/latest/)
