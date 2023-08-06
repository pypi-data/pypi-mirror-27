"""This file is part of the activipy_pgsql package

Copyright (c) 2017 Mark Shane Hayden <mhayden@coalesco.ca>
Copyright (c) 2017 Coalesco Digital Systems Inc. <info@coalesco.ca>
Copyright (c) 2015 Christopher Allan Webber <cwebber@dustycloud.org>

See the COPYRIGHT.txt file in the root directory of the package source for
full copyright notice

Distribution granted under the terms of EITHER GPLv3+ OR Apache v2

See LICENSE_*.txt files in the root directory for full license terms.
"""

import json

import psycopg2

from activipy import core, vocab


class JsonPgSQL(object):
    """
    interface to PostgreSQL database table using jsonb field as data store
    """
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.cur.execute(
            """
            SELECT exists(
                SELECT 1 FROM information_schema.tables WHERE table_name=%s
            );
            """, ('as_objects',))
        if not self.cur.fetchone()[0]:
            self.cur.execute(
                """
                CREATE TABLE as_objects(
                    sn bigserial PRIMARY KEY,
                    create_time timestamp DEFAULT now(),
                    update_time timestamp DEFAULT now(),
                    as_object jsonb
                );
                CREATE UNIQUE INDEX as_objects_idx_id ON as_objects
                    USING BTREE((as_object->>'@id'));
                CREATE INDEX as_objects_idx_type ON as_objects
                    USING BTREE((as_object->>'@type'));
                CREATE INDEX as_objects_idx_create_time ON as_objects(create_time);
                CREATE INDEX as_objects_idx_update_time ON as_objects(update_time);
                """)
            self.conn.commit()

    def __getitem__(self, key):
        self.cur.execute(
            """
            SELECT as_object FROM as_objects
            WHERE as_object->>'@id'=%s;
            """, (key,))
        return self.cur.fetchone()[0]

    def __setitem__(self, key, value):
        value['@id'] = key
        self.cur.execute(
            """
            INSERT INTO as_objects (as_object) VALUES (%s)
            ON CONFLICT ((as_object->>'@id'))
            DO UPDATE SET update_time = now(), as_object = EXCLUDED.as_object;
            """, (json.dumps(value),))
        self.conn.commit()

    def __delitem__(self, key):
        self.cur.execute(
            """
            DELETE FROM as_objects
            WHERE as_object->>'@id'=%s;
            """, (key,))
        self.conn.commit()

    def __contains__(self, key):
        self.cur.execute(
            """
            SELECT exists(
                SELECT 1 FROM as_objects
                WHERE as_object->>'@id'=%s
            );
            """, (key,))
        return self.cur.fetchone()[0]

    @classmethod
    def open(cls, dsn=None,
        connection_factory=None, cursor_factory=None, async=False,
        **kwargs):
        return cls(psycopg2.connect(
            dsn=dsn, connection_factory=connection_factory,
            cursor_factory=cursor_factory, async=async,
            **kwargs))

    def close(self):
        self.cur.close()
        self.conn.close()

    def get(self, key, default=None):
        self.cur.execute(
            """
            SELECT exists(
                SELECT 1 FROM as_objects
                WHERE as_object->>'@id'=%s
            );
            """, (key,))
        if self.cur.fetchone()[0]:
            return self[key]
        else:
            return default

    def fetch_asobj(self, env):
        return core.ASObj(self[id], env)

# Each of these returns the full object stored in the database

def pgsql_fetch(id, pgsqldb, env):
    return core.ASObj(pgsqldb[id], env)

def pgsql_save(asobj, pgsqldb):
    assert asobj.id is not None
    new_val = asobj.json()
    pgsqldb[asobj.id] = new_val
    return new_val

def pgsql_delete(asobj, pgsqldb):
    assert asobj.id is not None
    del pgsqldb[asobj.id]


pgsql_save_method = core.MethodId(
    "save", "Save object to the PostgreSQL store.",
    core.handle_one)
pgsql_delete_method = core.MethodId(
    "delete", "Delete object from the PostgreSQL store.",
    core.handle_one)

PgSQLEnv = core.Environment(
    vocabs=[vocab.CoreVocab],
    methods={
        (pgsql_save_method, vocab.Object): pgsql_save,
        (pgsql_delete_method, vocab.Object): pgsql_delete},
    shortids=core.shortids_from_vocab(vocab.CoreVocab),
    c_accessors=core.shortids_from_vocab(vocab.CoreVocab))


def pgsql_activity_normalized_save(asobj, pgsqldb):
    assert asobj.id is not None
    as_json = asobj.json()

    def maybe_normalize(key):
        val = as_json.get(key)
        # Skip if not a dictionary with a "@type"
        if not isinstance(val, dict) or not "@type" in val:
            return

        val_asobj = core.ASObj(val, asobj.env)
        # yup, time to normalize
        if asobj.env.is_astype(val_asobj, vocab.Object, inherit=True):
            # If there's no id, then okay, don't normalize
            if val_asobj.id is None:
                return

            # save referenced object to the database
            # (save == create or update if already exists)
            asobj.env.asobj_run_method(val_asobj, pgsql_save_method, pgsqldb)

            # and set the key to be the .id
            as_json[key] = val_asobj.id

    maybe_normalize("actor")
    maybe_normalize("object")
    maybe_normalize("target")
    # save the main object back with normalized data
    pgsqldb[asobj.id] = as_json
    return as_json


pgsql_denormalize_method = core.MethodId(
    "denormalize", "Expand out an activitystreams object recursively",
    # @@: Should this be a handle_fold?
    core.handle_one)


def pgsql_denormalize_object(asobj, pgsqldb):
    # TODO: For now, on any standard object, just return that as-is
    return asobj


def pgsql_denormalize_activity(asobj, pgsqldb):
    as_json = asobj.json()

    def maybe_denormalize(key):
        val = as_json.get(key)
        # If there's no specific val, or it's not a string,
        # or not in database then just leave it!
        if val is None or not isinstance(val, str) or val not in pgsqldb:
            return

        # Otherwise, looks like that value *is* in the database... hey!
        # Let's pull it out and set it as the key.
        as_json[key] = pgsqldb[val]
	
    maybe_denormalize("actor")
    maybe_denormalize("object")
    maybe_denormalize("target")
    return core.ASObj(as_json, asobj.env)


PgSQLNormalizedEnv = core.Environment(
    vocabs=[vocab.CoreVocab],
    methods={
        (pgsql_save_method, vocab.Object): pgsql_save,
        (pgsql_save_method, vocab.Activity): pgsql_activity_normalized_save,
        (pgsql_delete_method, vocab.Object): pgsql_delete,
        (pgsql_denormalize_method, vocab.Object): pgsql_denormalize_object,
        (pgsql_denormalize_method, vocab.Activity): pgsql_denormalize_activity},
    shortids=core.shortids_from_vocab(vocab.CoreVocab),
    c_accessors=core.shortids_from_vocab(vocab.CoreVocab))


def pgsql_fetch_denormalized(id, pgsqldb, env):
    """
    Fetch a fully denormalized ASObj from the database.
    """
    return env.asobj_run_method(
        pgsql_fetch(id, pgsqldb, env),
        pgsql_denormalize_method, pgsqldb)
