from sqlalchemy.testing.requirements import SuiteRequirements
from sqlalchemy.testing import exclusions


class Requirements(SuiteRequirements):
    @property  # TODO
    def order_by_col_from_union(self):
        return exclusions.closed()

    @property  # WTF
    def broken_cx_oracle6_numerics(self):
        return exclusions.closed()

    @property  # TODO
    def independent_connections(self):
        return exclusions.closed()

    @property
    def autocommit(self):
        return exclusions.open()

    @property  # TODO
    def unicode_data(self):
        return exclusions.closed()

    @property
    def date_coerces_from_datetime(self):
        return exclusions.closed()

    @property
    def datetime_microseconds(self):
        return exclusions.closed()

    @property
    def time_microseconds(self):
        return exclusions.closed()

    @property
    def unbounded_varchar(self):
        return exclusions.closed()

    @property
    def precision_generic_float_type(self):
        return exclusions.closed()

    @property
    def floats_to_four_decimals(self):
        return exclusions.closed()

    @property
    def schema_reflection(self):
        return exclusions.closed()

    @property
    def table_reflection(self):
        return exclusions.closed()

    @property
    def foreign_key_constraint_reflection(self):
        return exclusions.closed()

    @property
    def index_reflection(self):
        return exclusions.closed()

    @property
    def primary_key_constraint_reflection(self):
        return exclusions.closed()

    @property
    def unique_constraint_reflection(self):
        return exclusions.closed()

    @property
    def temp_table_reflection(self):
        return exclusions.closed()

    @property
    def parens_in_union_contained_select_w_limit_offset(self):
        return exclusions.closed()

    @property
    def parens_in_union_contained_select_wo_limit_offset(self):
        return exclusions.closed()

    @property
    def empty_inserts(self):
        return exclusions.closed()

    @property
    def insert_from_select(self):
        return exclusions.closed()

    @property
    def bound_limit_offset(self):
        return exclusions.closed()
