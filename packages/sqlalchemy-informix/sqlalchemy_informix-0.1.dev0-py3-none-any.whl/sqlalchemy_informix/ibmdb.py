from contextlib import contextmanager
from decimal import Decimal, localcontext
import re

import ibm_db_dbi as Database

from sqlalchemy import exc, sql, types
from sqlalchemy.sql import compiler
from sqlalchemy.engine import default

error_re = re.compile(r'SQLCODE=-(\d+)')


@contextmanager
def wrap_ibm_db_errors(statement, params):
    try:
        yield
    except Database.OperationalError as e:
        error = int(error_re.search(e._message).groups()[0])
        errors = [268, 691, 530, 391]
        if error in errors:
            raise exc.IntegrityError(statement, params, e) from e
        raise


class InformixNumeric(types.Numeric):
    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            if self.asdecimal:
                if not isinstance(value, Decimal):
                    with localcontext() as ctx:
                        ctx.prec = 10
                        value = ctx.create_decimal_from_float(value)
            else:
                value = float(value)

            return value

        return process

    def literal_processor(self, dialect):
        def process(value):
            if isinstance(value, float):
                return '%s::float' % str(value)
            return str(value)

        return process


class InformixBoolean(types.Boolean):
    def result_processor(self, dialect, coltype):
        def process(value):
            return bool(value) if value is not None else None

        return process


class InformixTime(types.Time):
    def result_processor(self, dialect, coltype):
        def process(value):
            return value.time() if value is not None else None

        return process


class InformixTypeCompiler(compiler.GenericTypeCompiler):
    def visit_TEXT(self, type_):
        return self.visit_CLOB(type_)

    def visit_INTEGER(self, type_, **kw):
        if kw['type_expression'].primary_key:
            return 'SERIAL'
        else:
            return 'INTEGER'

    def visit_DATETIME(self, type_):
        return 'DATETIME YEAR TO FRACTION'

    def visit_TIME(self, type_):
        return 'DATETIME HOUR TO FRACTION'


class InformixCompiler(compiler.SQLCompiler):
    ansi_bind_rules = True

    def default_from(self):
        return ' FROM sysmaster:"informix".sysdual'

    def visit_true(self, element, **kw):
        return "'t'"

    def visit_false(self, element, **kw):
        return "'f'"

    def get_select_precolumns(self, select, **kw):
        """Called when building a ``SELECT`` statement, position is just
        before column list Informix puts the limit and offset right
        after the ``SELECT``...
        """

        result = ""
        if select._offset_clause is not None:
            result += "SKIP %s " % select._offset
        if select._limit_clause is not None:
            result += "FIRST %d " % select._limit
        if select._distinct:
            result += "DISTINCT "
        return result

    def limit_clause(self, select, **kw):
        """Already taken care of in the `get_select_precolumns` method."""
        return ""


class InformixExecutionContext(default.DefaultExecutionContext):
    def get_lastrowid(self):
        # Massive hack to get the last inserted serial (sqlca.sqlerrd1) or bigserial
        # Apparently both are never set
        cursor = self.create_cursor()
        cursor.execute("SELECT dbinfo('sqlca.sqlerrd1'), dbinfo('bigserial') FROM sysmaster:\"informix\".sysdual")
        result = cursor.fetchone()
        assert(not all(result))
        return result[0] + result[1]


class InformixDDLCompiler(compiler.DDLCompiler):
    def _constraint_name(self, constraint):
        if 'TEMP' in constraint.table._prefixes:
            return ""  # No constraint names allowed for temp tables
        if constraint.name is not None:
            formatted_name = self.preparer.format_constraint(constraint)
            if formatted_name is not None:
                return " CONSTRAINT %s " % formatted_name
        else:
            return ""

    def visit_foreign_key_constraint(self, constraint):
        preparer = self.preparer
        text = ""
        remote_table = list(constraint.elements)[0].column.table
        text += "FOREIGN KEY(%s) REFERENCES %s (%s)" % (
            ', '.join(preparer.quote(f.parent.name)
                      for f in constraint.elements),
            self.define_constraint_remote_table(
                constraint, remote_table, preparer),
            ', '.join(preparer.quote(f.column.name)
                      for f in constraint.elements)
        )
        text += self.define_constraint_match(constraint)
        text += self.define_constraint_cascades(constraint)
        text += self._constraint_name(constraint)
        return text

    def visit_primary_key_constraint(self, constraint):
        if len(constraint) == 0:
            return ''
        text = ""
        text += "PRIMARY KEY "
        text += "(%s)" % ', '.join(self.preparer.quote(c.name)
                                   for c in (constraint.columns_autoinc_first
                                   if constraint._implicit_generated
                                   else constraint.columns))
        text += self._constraint_name(constraint)
        return text

    def visit_unique_constraint(self, constraint):
        if len(constraint) == 0:
            return ''
        text = ""
        text += "UNIQUE (%s)" % (
                ', '.join(self.preparer.quote(c.name)
                          for c in constraint))
        text += self._constraint_name(constraint)
        return text

    def visit_create_table(self, create):
        table = create.element

        if table._prefixes == ['TEMPORARY']:
            table._prefixes[:] = ['TEMP']

        return super().visit_create_table(create)


class InformixDialect(default.DefaultDialect):
    name = 'informix'
    driver = 'ibmdb'

    execution_ctx_cls = InformixExecutionContext

    statement_compiler = InformixCompiler
    type_compiler = InformixTypeCompiler
    ddl_compiler = InformixDDLCompiler

    supports_native_boolean = True
    supports_native_decimal = True

    colspecs = {
        types.Time: InformixTime,
        types.Boolean: InformixBoolean,
        types.Numeric: InformixNumeric
    }

    @classmethod
    def dbapi(cls):
        return Database

    def create_connect_args(self, url):
        opts = url.translate_connect_args()
        {'database': 'mhilf', 'host': 'apo.bap.lan',
            'username': 'informix', 'password': 'informix', 'port': 9092}
        connectors = []
        available_options = {
            'username': 'UID',
            'password': 'PWD',
            'host': 'HOSTNAME',
            'port': 'PORT',
            'database': 'DATABASE'
        }
        for sa_opt, ifx_opt in available_options.items():
            if sa_opt in opts:
                connectors.append('%s=%s' % (ifx_opt, opts[sa_opt]))
        connectors.append('PROTOCOL=TCPIP')
        return [[';'.join(connectors)], {}]

    def has_table(self, connection, tablename, schema=None):
        schema = schema or self.default_schema_name
        result = connection.scalar(
            sql.text('SELECT count(*) FROM "informix".systables WHERE tabname=:name AND owner=:schema'),
            name=tablename, schema=schema
        )
        return bool(result)

    def _get_default_schema_name(self, connection):
        return connection.scalar('SELECT CURRENT_USER FROM sysmaster:"informix".sysdual')

    def set_isolation_level(self, connection, level):
        if level == 'AUTOCOMMIT':
            connection.set_autocommit(True)

    def do_executemany(self, cursor, statement, parameters, context=None):
        # At least inserts with execute_many seem to fail
        # SQLRowCount failed: [IBM][CLI Driver] CLI0125E  Function sequence error. SQLSTATE=HY010 SQLCODE=-99999
        # Also executemany needs homogenous types :/
        with wrap_ibm_db_errors(statement, parameters):
            for param in parameters:
                cursor.execute(statement, param)

    def do_execute(self, cursor, statement, parameters, context=None):
        with wrap_ibm_db_errors(statement, parameters):
            return cursor.execute(statement, parameters)

    def do_execute_no_params(self, cursor, statement, context=None):
        with wrap_ibm_db_errors(statement, []):
            return cursor.execute(statement)
