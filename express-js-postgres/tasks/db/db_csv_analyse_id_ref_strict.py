# TODO: this whole logic is too convoluted
# split off into distinct actions
# FIXME: when I have decided on an elegant way to factor out the functions
# Perhaps attach the function definitions to the context?
# e.g. ctx.analyse_table; ctx.analyze_enum

import io
import csv
import os.path
import pandas as pd
import numpy as np


def description(ctx):
    return f"analyse {ctx.ENTITY_ARG} (and dependencies) using constraints and checking data validity"


def exec(ctx):
    ctx.TABLE_DEFINITIONS = {}
    ctx.TABLE_DATAFRAMES = {}

    df = init_df(ctx, ctx.ENTITY_ARG)

    if ctx.ENTITY_SNAKE.endswith("_enum"):
        (enum_dataframe, enum_definition) = analyze_enum(
            ctx, df, df.columns[0], ctx.ENTITY_SNAKE
        )
        ctx.ENTITY_TABLE_NAME = enum_dataframe.name
        ctx.TABLE_DEFINITIONS[ctx.ENTITY_TABLE_NAME] = enum_definition
        ctx.TABLE_DATAFRAMES[ctx.ENTITY_TABLE_NAME] = enum_dataframe
        return

    analyze_table(ctx, df)

    # do this after entity in case ctx.TABLE_DEFINITIONS or
    # ctx.TABLE_DATAFRAMES are replaced
    if ctx.has_opt(ctx.ENTITY_FIELDS_STEM):
        df = init_df(ctx, ctx.ENTITY_FIELDS_CSV_FP)
        (fields_dataframe, fields_definition) = analyze_enum(
            ctx, df, df.columns[0], df.columns[0]
        )
        ctx.ENTITY_FIELDS_TABLE_NAME = fields_dataframe.name
        ctx.TABLE_DEFINITIONS[ctx.ENTITY_FIELDS_TABLE_NAME] = fields_definition
        ctx.TABLE_DATAFRAMES[ctx.ENTITY_FIELDS_TABLE_NAME] = fields_dataframe
        # TODO: check #columns
        # rows, columns = df.shape...


def init_df(ctx, csv_fp):
    ctx.info(f"analysing: {csv_fp}")
    df = pd.read_csv(csv_fp, index_col=False)  # entity dataframe
    df = df.convert_dtypes()
    return df


def analyze_table(ctx, df):
    ref_dataframes = {}
    ref_definitions = {}
    entity_table_definition = []
    entity_table_definition.append(
        [f"{ctx.ENTITY_ID}", "serial primary key", "integer"]
    )

    column_name_check = []
    new_enum_columns = []
    entity_table_constraints = []

    for column, data_type, is_null in zip(df.columns, df.dtypes, df.isnull().any()):
        constraint = "CONSTRAINT ERROR"

        # TODO: fatal until I can find an elegant way of renaming columns with spaces
        stripped_column = column.strip()
        if not stripped_column == column:
            ctx.fatal(f'expected: column "{stripped_column}", found: "{column}"')

        column_name_check.append(column)

        if column.endswith("_enum"):
            # check for a corresponding ref file
            enum_fp = f"{ctx.DATABASE_CSV_SEED_PATH}/{column}.csv"
            if not os.path.isfile(enum_fp):
                ctx.fatal(f"expected: reference/enum file {enum_fp}, found: none")
            enum_df = pd.read_csv(enum_fp, index_col=False)  # ref dataframe
            enum_df = enum_df.convert_dtypes()
            enum_df.name = column

            # check for id
            enum_ref_id = enum_df.name + "_id"
            if not enum_ref_id in df.columns:
                ctx.warn(f'expected: column "{enum_ref_id}", found none')
                new_enum_columns.append(enum_df.name)

            # generates a separate table
            (enum_table_dataframe, enum_table_definition) = analyze_enum(
                ctx, enum_df, column, column
            )

            ref_dataframes[enum_table_dataframe.name] = enum_table_dataframe
            ref_definitions[enum_table_dataframe.name] = enum_table_definition

            constraint = f"integer references {enum_df.name}({enum_ref_id})"

        elif is_null:
            ctx.fatal(f'expected: valid data in column "{column}", found: null')
        elif data_type == "Int64":
            constraint = "integer"
        elif data_type == "Float64":
            constraint = "float"
        elif data_type == "boolean":
            constraint = "boolean"
        else:
            constraint = "varchar"

        entity_table_constraints.append(f"{constraint}")

    # TODO: more efficient check
    for df_ref_name in new_enum_columns:
        loc = df.columns.get_loc(df_ref_name)
        indices = []
        for s_idx, s_enum_name in enumerate(df[df_ref_name]):
            for r_idx, r_enum_name in enumerate(
                ref_dataframes[df_ref_name][df_ref_name]
            ):
                if s_enum_name == r_enum_name:
                    ref_id = r_idx + 1
                    indices.append(ref_id)
        if len(indices) == 0:
            ctx.fatal(f"zero matches in reference lookup for {s_enum_name}")
        rows, _ = df.shape
        if len(indices) != rows:
            ctx.fatal(
                f"unmatched entries in reference lookup for {s_enum_name}, expected: {rows}, found: {len(indices)}"
            )

        enum_id_column_name = f"{df_ref_name}_id"
        df.insert(loc + 1, enum_id_column_name, indices)
        column_name_check.append(enum_id_column_name)

    # remove enum columns
    df.drop(columns=new_enum_columns, inplace=True)

    for idx, column in enumerate(df.columns):
        entity_table_definition.append(
            [f"{column}", f"{entity_table_constraints[idx]}", "string"]
        )

    n = max(set(column_name_check), key=column_name_check.count)
    if column_name_check.count(n) > 1:
        ctx.fatal(f"expected: unique column names, found: duplicates")

    # set definitions/constraints
    ctx.ENTITY_TABLE_NAME = ctx.ENTITY_SNAKE

    ctx.TABLE_DEFINITIONS = ref_definitions  # for constraints generation
    ctx.TABLE_DEFINITIONS[ctx.ENTITY_TABLE_NAME] = entity_table_definition
    # set (future) csv content
    ctx.TABLE_DATAFRAMES = ref_dataframes  # for constraints generation
    ctx.TABLE_DATAFRAMES[ctx.ENTITY_TABLE_NAME] = df


def analyze_enum(ctx, df, column, entity_name):
    if len(df.columns) > 1:
        ctx.fatal(
            f"expected: a single column, found: multiple columns for {entity_name}"
        )

    stripped_column = column.strip()

    if not stripped_column == column:
        ctx.warn(f'expected column name "{stripped_column}", found: "{column}"')
        column = stripped_column
    df.name = column

    if not column == entity_name:
        ctx.fatal(f'expected column name "{entity_name}", found: "{column}"')

    if isinstance(df.dtypes, pd.Series):
        dtype = df.dtypes.iloc[0]
    else:
        dtype = df.dtypes

    if not dtype == "string":
        ctx.fatal(f"expected string, found {dtype}")

    if df.duplicated().any():
        ctx.fatal(f"expected unique data, found: duplicates")

    # all good
    enum_table_definition = [
        [f"{df.name}_id", "serial primary key", "integer"],
        [f"{df.name}", "varchar unique", "string"],
    ]

    ctx.info(f"table definition: {ctx.ENTITY_ARG}->{df.name}")
    ctx.info(f"table dataframe: {ctx.ENTITY_ARG}->{df.name}")

    return (df, enum_table_definition)
