activipy_pgsql
==============

An activipy environment to use PostgreSQL as the data store for ActivityStream
objects.

----

The `activipy module <http://activipy.readthedocs.io/en/latest/>`_ enables the
use of `ActivityStreams <https://www.w3.org/TR/activitystreams-core/>`_ in
your applications and includes the support of different "environments" to
extend functionality.

This package provides a "pgsql" environment that maps storage methods to
PostgreSQL queries using psycopg2. Object data is stored using the jsonb
data type to simplify the schema and provide maximum performance.

Example Code
------------

Open a database::

    >>> from activipy import core, vocab
    >>> from activipy.pgsql import pgsql
    >>> db = pgsql.JsonPgSQL.open(
    ... host="<db_server>", dbname="<db_name>",
    ... user="<db_user>", password="<db_user_pass>")
    >>> env = pgsql.PgSQLNormalizedEnv

Create a new record and save to database::

    >>> post_this = core.ASObj({
    ...     "@type": "Create",
    ...     "@id": "http://tsyesika.co.uk/act/foo-id-here/",
    ...     "actor": {
    ...         "@type": "Person",
    ...         "@id": "https://tsyesika.co.uk/",
    ...         "displayName": "Jessica Tallon"},
    ...     "to": ["acct:cwebber@identi.ca",
    ...            "acct:justaguy@rhiaro.co.uk",
    ...            "acct:ladyaeva@hedgehog.example"],
    ...     "object": {
    ...         "@type": "Note",
    ...         "@id": "https://tsyesika.co.uk/chat/sup-yo/",
    ...         "content": "Up for some root beer floats?"}},
    ... pgsql.PgSQLNormalizedEnv)
    >>> post_this.m.save(db)
    {'@type': 'Create',
     '@id': 'http://tsyesika.co.uk/act/foo-id-here/',
     'actor': 'https://tsyesika.co.uk/',
     'to': ['acct:cwebber@identi.ca',
            'acct:justaguy@rhiaro.co.uk',
            'acct:ladyaeva@hedgehog.example'],
     'object': 'https://tsyesika.co.uk/chat/sup-yo/'}

Note how in this example the record has been normalized. In this environment
the actor and object are created in separate records and made into references
in the parent record.  To retrieve the original denormalized form::

    >>> normalized_post = pgsql.pgsql_fetch(
    ... "http://tsyesika.co.uk/act/foo-id-here/", db, env)
    >>> normalized_post.m.denormalize(db)
    <ASObj Create "http://tsyesika.co.uk/act/foo-id-here/">
    >>> normalized_post.m.denormalize(db).json()
    {'to': ['acct:cwebber@identi.ca',
            'acct:justaguy@rhiaro.co.uk',
            'acct:ladyaeva@hedgehog.example'],
     '@id': 'http://tsyesika.co.uk/act/foo-id-here/',
     '@type': 'Create',
     'actor': {'@id': 'https://tsyesika.co.uk/',
               '@type': 'Person',
               'displayName': 'Jessica Tallon'},
     'object': {'@id':
                'https://tsyesika.co.uk/chat/sup-yo/',
                '@type': 'Note',
                'content': 'Up for some root beer floats?}}

