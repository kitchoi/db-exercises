CREATE TABLE objects (
    id SERIAL,
    data jsonb
);
CREATE TABLE names (
    id SERIAL,
    name TEXT
);

CREATE INDEX index_objects ON objects USING GIN(data jsonb_ops);


INSERT INTO objects (data) VALUES
    (
        '{"children": [
            {"name": "Sarah"},
            {"name": "Tom"},
            {"name": "Gary"}
        ]}'
    ),
    (
        '{"children": [
            {"name": "Jo"},
            {"name": "Chris"},
            {"name": "Billy"}
        ]}'
    ),
    (
        '{"children": [
            {"name": "Kelly"},
            {"name": "Chris"}
        ]}'
    ),
    (
        '{"children": [
            {"name": "Ben"},
            {"name": "Allen"}
        ]}'
    ),
    (
        '{"children": [
            {"name": "Yan"},
            {"name": "Larry"}
        ]}'
    ),
    (
        '{"children": [
            {"name": "James"},
            {"name": "Peter"},
            {"name": "William"}
        ]}'
    );


INSERT INTO names (name) VALUES
    ('Sarah'),
    ('Tom'),
    ('Gary'),
    ('James'),
    ('Peter'),
    ('William')
;

SELECT * FROM objects;
SELECT * FROM names;

SELECT * FROM objects WHERE (data @> '{"children": [{"name": "Sarah"}]}');

EXPLAIN ANALYZE SELECT * FROM objects WHERE (data @> '{"children": [{"name": "Sarah"}]}');

SELECT * FROM objects WHERE (data @> '{"children": [{"name": "James"}]}') OR (data @> '{"children": [{"name": "Peter"}]}');

EXPLAIN ANALYZE SELECT * FROM objects WHERE (data @> '{"children": [{"name": "James"}]}') OR (data @> '{"children": [{"name": "Peter"}]}');

SELECT * FROM objects, jsonb_array_elements(data->'children') AS child WHERE child->>'name' LIKE '%e%';

EXPLAIN ANALYZE SELECT * FROM objects, jsonb_array_elements(data->'children') AS child WHERE child->>'name' LIKE '%e%';