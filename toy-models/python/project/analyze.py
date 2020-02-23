import contextlib

import sqlalchemy as sa
from sqlalchemy import event


@contextlib.contextmanager
def explain_analyze(engine, analyze=True):

    second_engine = engine.execution_options(is_spy=True)
    results = []

    @event.listens_for(engine, "after_execute")
    def _explain_analyze(conn, clause, *args, **kwargs):
        if not conn.get_execution_options().get("is_spy", False):
            text = "EXPLAIN "
            if analyze:
                text += "ANALYZE "
            query_text = str(
                clause.compile(compile_kwargs={"literal_binds": True}))
            text += query_text
            result = [query_text]
            text = sa.sql.expression.text(text)
            result.extend(second_engine.execute(text).fetchall())
            results.append(result)

    try:
        yield results
    finally:
        event.remove(engine, "after_execute", _explain_analyze)
        second_engine.dispose()
