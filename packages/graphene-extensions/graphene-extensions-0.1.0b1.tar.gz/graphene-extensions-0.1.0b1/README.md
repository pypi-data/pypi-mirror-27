# graphene-extenstions 

[![Build Status](https://travis-ci.org/karol-gruszczyk/graphene-extenstions.svg?branch=master)](https://travis-ci.org/karol-gruszczyk/graphene-extenstions)
[![Coverage Status](https://coveralls.io/repos/github/karol-gruszczyk/graphene-extenstions/badge.svg?branch=master)](https://coveralls.io/github/karol-gruszczyk/graphene-extenstions?branch=master)

Goal of this library is to make development on graphene a lot simpler and quicker,
  which means less boiler plate and more flexibility.

## Requirements
* Python 3.6+
* graphene 2.0+
* Django 1.10+

## Purpose
Why another library if there is already `graphene-django` available?
* Poor documentation, only a couple of documented features. v1 and v2 documentation is mixed,
  which ends up in user frustration.
  You can copy-paste examples from the documentation and it will result in errors,
  because it hasn't been updated for v2.
* Lack of query optimization, which really should be handled by the framework itself
* Extendability is very poor.
 In most cases you need to copy-paste the source code into your project, to get more custom behaviour.
* But the main reason is, that the project is evolving very slowly and does not seem,
  that there will be any new features in the near future
* `django-rest-framework` dependency. Authors got really lazy and did not bother writing proper `Mutation` classes...
  Seriously, why do I need to install a REST library, when I want to use GraphQL?
* No Server Error handling, which results in Exception message leakage.

This library will try it best to fix all the above, and provide an all-in-one GraphQL framework for django,
 rather than extending it with X plugin libraries

## Features
* Simple schema generation from django models
* Support for model properties and methods
* Query optimization, no more `prefetch_related` and `select_related`(sick!)
* [TODO] `Mutation` generation(with validators, similar to DRF style) from django models
* Schema resolution based on context(for example authenticated user)
* [TODO] `django-filter` support
* [TODO] support for filtering based on the query context(for ex. authenticated user), 
  in order to achieve basic permission-like behaviour
* GraphiQL browser query executor

## Disclaimer
* Support for <Python3.6 may be added in the future, if requested by enough users
* currently only relay schema is supported

## Quick start

### Installation
`pip install graphene-extensions`  # will come soon

#### schema.py
```python
import graphene

from graphene_extensions.types import ModelType
from graphene_extensions.connections import ModelConnectionField
from graphene_extensions.types.decorators import annotate_type, graphene_property

from django.db import models


class Pizza(models.Model):
    name = models.CharField(max_length=128)
    
    @graphene_property(graphene.String)
    def custom_name(self):
        return f'Custom {self.name}'

    @annotate_type(graphene.String)
    def custom_method(self):
        return 'magic'


class PizzaType(ModelType):
    class Meta:
        model = Pizza
        fields = ('name', 'custom_name', 'custom_method')


class Query(graphene.ObjectType):
    pizzas = ModelConnectionField(PizzaType)

schema = graphene.Schema(query=Query)
```

#### urls.py
```python
from django.conf.urls import url

from graphene_extensions.views import GraphQLView

from .schema import schema

urlpatterns = [
    url(r'^graphql', GraphQLView.as_view(schema=schema)),
]
```

## Documentation

### ModelType
```python
from graphene_extensions import ModelType


class UserType(ModelType):
    class Meta:
        model = User  # required, has to be a subclass of django.db.models.Model
        
        # you can specifically pick, which fields should be included
        fields = ('id', 'pk', 'field')  
        # or exclude fields
        exclude_fields = ('password',)
        # or pick all fields
        # it will also include all valid properties, methods and reverse related fields
        fields = '__all__'
        
        # if you don't want to use the default connection, you can specify a custom one by:
        connection = UserConnection
```


### GraphQLView

#### context based schema resolution
Prevent schema leakage by returning different schemas, based on the authenticated user
```python
from django.core.handlers.wsgi import WSGIRequest
from graphene_extensions.views import GraphQLView


def get_schema(request: WSGIRequest):
    if request.user.is_authenticated():
        return authenticated_schema
    return public_schema


urlpatterns = [
    url(r'^graphql', GraphQLView.as_view(schema=get_schema))
]
```
