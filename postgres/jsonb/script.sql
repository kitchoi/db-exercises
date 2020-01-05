CREATE TABLE objects (
  id SERIAL,
  data jsonb
);
CREATE INDEX ix_age ON objects USING BTREE (cast (data->>'age' as int));
CREATE INDEX ix_objects_data_ops ON objects USING GIN(data jsonb_ops);
/*CREATE INDEX ix_location ON objects ((data->>'location'));*/

/* CREATE INDEX ix_name ON objects ((data->>'name')); */
INSERT INTO objects (data) VALUES ('{"name": "Paul", "age": 30}');
INSERT INTO objects (data) VALUES ('{"name": "Mary", "age": 12}');
INSERT INTO objects (data) VALUES ('{"name": "Charlie", "age": 18}');
INSERT INTO objects (data) VALUES ('{"name": "James", "age": 23}');
INSERT INTO objects (data) VALUES ('{"name": "Jenny", "age": 40}');
INSERT INTO objects (data) VALUES ('{"name": "Unknown"}');
INSERT INTO objects (data) VALUES ('{"location": "GB"}');
INSERT INTO objects (data) VALUES ('{"location": "US"}');

SELECT * FROM objects WHERE (data->>'age')::int IN (30, 40);
EXPLAIN ANALYZE SELECT * FROM objects WHERE (data->>'age')::int IN (30, 40);

SELECT * FROM objects WHERE data->>'name' = 'James';
EXPLAIN ANALYZE SELECT * FROM objects WHERE data->>'name' = 'James';

SELECT * FROM objects WHERE data@>'{"name": "James"}';
EXPLAIN ANALYZE SELECT * FROM objects WHERE data@>'{"name": "James"}';

SELECT * FROM objects WHERE data->>'location' IN ('GB', 'FR');
EXPLAIN ANALYZE SELECT * FROM objects WHERE data->>'location' IN ('GB', 'FR');
