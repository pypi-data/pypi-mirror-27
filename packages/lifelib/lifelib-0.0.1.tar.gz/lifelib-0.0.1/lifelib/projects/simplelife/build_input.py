"""A script called from :mod:`build.py <simplelife.build>`
to create "Input" space and its subspaces from input data.

This module contains a function :py:func:`build_input`,
which creates "Input" space and its subspaces by reading
input data into them from an Excel file.

By default, :py:func:`build_input` reads data from *input.xlsm* in the
same folder as this module, and the structure of ``Input`` space is illustrated
by the diagram below.


.. figure:: /images/input_drawio.png
   :width: 50%

Below are descriptions of Input spaces and its subspaces.

Input
    The parent module of all other input spaces.

    Some tables in *input.xlsm* are imported as cells directly under this space.



PolicyData
    The sample policy data read from *PolicyData* tab in *input.xlsm*.
    Records and fields of *PolicyData* represents policies and policy
    attributes respectively.
    Each record of *PolicyData* is accessible as a dynamic space under
    ``PolicyData`` space indexed by *Policy* column in the input table.
    Each field of a record is accessible as a scalar cells in the dynamic
    space corresponding to the record.

    For example::

        >>> model.Input.PolicyData[3].PolicyTerm()

    gives the value of the policy term of the policy record 3.

MortalityTables
    The sample mortality tables read from *Mortality* tab.
    For Each mortality table, a dynamic space is created indexed
    by *TableID*, and `MortalityTable` cells indexed
    by ``Sex`` and ``Age`` is created in that space.

    The script below will return the mortality rate of Male, Age 41
    from the mortality table 3::

        >>> model.Input.MortalityTables[3].MortalityTable('M', 41)


ProductSpec
    The sample product spec table read from *ProductSpec* tab.
    ``ProductSpec`` dynamic subspaces holds parameters to specify products
    as cells. The dynamic subspaces are indexed by ``Product``,
    ``PolType`` and ``Gen``, and
    each of the subspace has scalar cells defined by the columns
    of *ProductSpec* tab other than the index columns.

    Empty cells in the index columns are imported as ``None``.
    ``Cells.match`` method treats ``None`` as the wildcard when
    finding the closest matching indexes for the given arguments.


Assumptions
    The sample assumption table read from *Assumptions* tab.

    The ``Assumptions`` space has dynamic subspaces indexed by ``Product``,
    ``PolType`` and ``Gen``, each of which has scalar cells defined by the
    columns of *Assumptions* tab other than the index columns.

    Empty cells in the index columns are imported as ``None``.
    ``Cells.match`` method treats ``None`` as the wildcard when
    finding the closest matching indexes for the given arguments.

AssumptionTables
    The sample assumption table read from *AssumptionTables* tab.
    The tab holds assumptions by policy duration, such as mortality factors
    and lapse assumptions.

    Each assumption in the table is imported as a cells in the
    ``AssumptionTables`` space.

Scenarios
    The sample scenario table read from *Scenarios* tab.
    TODO


"""
import os.path as path

default_input = path.join(path.abspath(path.dirname(__file__)), 'input.xlsm')


def build_input(model, input_file=default_input):
    """Create "Input" space and its sub spaces by reading data from an Excel
    file into it.

    This function creates a space named "Input" under ``model``,
    reads tables from ``input_file`` into cells and subspaces
    under the "Input" space.

    By default, this function assumes reading data from *input.xlsm*
    located in the same folder as this module.

    Args:
        model: Model object in which 'Input' space is created.
        input_file(str): Path to the Excel input file.
    """
    import time
    debug_dur = True
    timestamp = time.time()

    def print_duration(msg):
        global timestamp
        print(msg, time.time() - timestamp)
        timestamp = time.time()

    inp = model.new_space(name='Input')
    inp.can_have_none = True

    timestamp = time.time()

    policydata = inp.new_space_from_excel(
        book=input_file,
        range_='B7:O307',
        sheet='PolicyData',
        name='PolicyData',
        names_row=0,
        param_cols=[0],
        space_param_order=[0],
        cells_param_order=[])

    print_duration('policydata: ') if debug_dur else None

    mortbl = inp.new_space_from_excel(
        book=input_file,
        range_='E4:Q137',
        sheet='Mortality',
        name='MortalityTables',
        names_row=0,
        param_cols=[0],
        names_col=0,
        param_rows=[1, 2],
        space_param_order=[1],
        cells_param_order=[2, 0])

    print_duration('mortbl: ') if debug_dur else None

    prodspec = inp.new_space(name='ProductSpec')
    prodspec.new_cells_from_excel(
        book=input_file,
        range_='B7:V22',
        sheet='ProductSpec',
        names_row=0,
        param_cols=[0, 1, 2],
        param_order=[0, 1, 2])

    print_duration('prodspec: ') if debug_dur else None

    inp.new_cells_from_excel(
        book=input_file,
        range_='G6:H9',
        sheet='OtherParams',
        names_row=0,
        param_cols=[0],
        param_order=[0])

    print_duration('OtherParams1: ') if debug_dur else None

    inp.new_cells_from_excel(
        book=input_file,
        range_='V6:W9',
        sheet='OtherParams',
        names_row=0,
        param_cols=[0],
        param_order=[0])

    print_duration('OtherParams2: ') if debug_dur else None

    asmp = inp.new_space(name='Assumptions')
    asmp.new_cells_from_excel(
        book=input_file,
        range_='B7:T17',
        sheet='Assumptions',
        names_row=0,
        param_cols=[0, 1, 2],
        param_order=[0, 1, 2])

    print_duration('Assumptions: ') if debug_dur else None

    asmptbls = inp.new_space(name='AssumptionTables')
    asmptbls.new_cells_from_excel(
        book=input_file,
        range_='B7:J27',
        sheet='AssumptionTables',
        names_row=0,
        param_cols=[0],
        param_order=[0])

    print_duration('AssumptionTables: ') if debug_dur else None

    scenarios = inp.new_space_from_excel(
        book=input_file,
        range_='A3:C1513',
        sheet='Scenarios',
        name='Scenarios',
        names_row=0,
        param_cols=[0, 1],
        space_param_order=[0],
        cells_param_order=[1])

    if debug_dur: print_duration('Scenarios: ')

    return inp