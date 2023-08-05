# encoding: utf-8
"""
This module defines a convenience layer to access the MAD-X interpreter.

The most interesting class for users is :class:`Madx`.
"""

from __future__ import absolute_import

from functools import partial
import logging
import os
import collections

import numpy as np

from minrpc.util import ChangeDirectory

from . import _rpc
from . import util

try:
    basestring
except NameError:
    basestring = str


__all__ = [
    'Madx',
    'Sequence',
    'BaseElementList',
    'TableProxy',
    'CommandLog',
    'metadata',
]


class Version(object):

    """Version information struct. """

    def __init__(self, release, date):
        """Store version information."""
        self.release = release
        self.date = date
        self.info = tuple(map(int, release.split('.')))

    def __repr__(self):
        """Show nice version string to user."""
        return "MAD-X {} ({})".format(self.release, self.date)


class MadxCommands(object):

    """
    Generic MAD-X command wrapper.

    Raw python interface to issue MAD-X commands. Usage example:

    >>> command = MadxCommands(libmadx.input)
    >>> command('twiss', sequence='LEBT')
    >>> command.title('A meaningful phrase')

    :ivar __dispatch: callable that takes a MAD-X command string.
    """

    def __init__(self, dispatch):
        """Set :ivar:`__dispatch` from :var:`dispatch`."""
        self.__dispatch = dispatch

    def __call__(self, *args, **kwargs):
        """Create and dispatch a MAD-X command string."""
        self.__dispatch(util.mad_command(*args, **kwargs))

    def __getattr__(self, name):
        """Return a dispatcher for a specific command."""
        if name.startswith('_'):
            raise AttributeError("Invalid command name: {!r}! Did you mean {!r}?"
                                 .format(name, name.strip('_') + '_'))
        if name.endswith('_'):
            name = name[:-1]
        return self[name]

    def __getitem__(self, name):
        """Return a dispatcher for a specific command."""
        return partial(self.__call__, name)


def NOP(s):
    """Do nothing."""
    pass


class CommandLog(object):

    """Log MAD-X command history to a text file."""

    @classmethod
    def create(cls, filename, prefix='', suffix='\n'):
        """Create CommandLog from filename (overwrite/create)."""
        return cls(open(filename, 'wt'), prefix=prefix, suffix=suffix)

    def __init__(self, file, prefix='', suffix='\n'):
        """Create CommandLog from file instance."""
        self._file = file
        self._prefix = prefix
        self._suffix = suffix

    def __call__(self, command):
        """Log a single history line and flush to file immediately."""
        self._file.write(self._prefix + command + self._suffix)
        self._file.flush()


class Madx(object):

    """
    Python interface for a MAD-X process.

    For usage instructions, please refer to:

        https://hibtc.github.io/cpymad/getting-started

    Communicates with a MAD-X interpreter in a background process.

    The state of the MAD-X interpreter is controlled by feeding textual MAD-X
    commands to the interpreter.

    The state of the MAD-X interpreter is accessed by directly reading the
    values from the C variables in-memory and sending the results pickled back
    over the pipe.
    """

    def __init__(self, libmadx=None, command_log=None, error_log=None,
                 **Popen_args):
        """
        Initialize instance variables.

        :param libmadx: :mod:`libmadx` compatible object
        :param command_log: Log all MAD-X commands issued via cpymad.
        :param error_log: logger instance ``logging.Logger``
        :param Popen_args: Additional parameters to ``subprocess.Popen``

        If ``libmadx`` is NOT specified, a new MAD-X interpreter will
        automatically be spawned. This is what you will mostly want to do. In
        this case any additional keyword arguments are forwarded to
        ``subprocess.Popen``. The most prominent use case for this is to
        redirect or suppress the MAD-X standard I/O::

            m = Madx(stdout=False)

            with open('madx_output.log', 'w') as f:
                m = Madx(stdout=f)

            m = Madx(stdout=subprocess.PIPE)
            f = m._process.stdout
        """
        # get logger
        if error_log is None:
            error_log = logging.getLogger(__name__)
        # open history file
        if isinstance(command_log, basestring):
            command_log = CommandLog.create(command_log)
        elif command_log is None:
            command_log = NOP
        # start libmadx subprocess
        if libmadx is None:
            # stdin=None leads to an error on windows when STDIN is broken.
            # Therefore, we need set stdin=os.devnull by passing stdin=False:
            Popen_args.setdefault('stdin', False)
            Popen_args.setdefault('bufsize', 0)
            self._service, self._process = \
                _rpc.LibMadxClient.spawn_subprocess(**Popen_args)
            libmadx = self._service.libmadx
        if not libmadx.is_started():
            libmadx.start()
        # init instance variables:
        self._libmadx = libmadx
        self._command_log = command_log
        self._error_log = error_log

    def __bool__(self):
        """Check if MAD-X is up and running."""
        try:
            return self._libmadx.is_started()
        except (_rpc.RemoteProcessClosed, _rpc.RemoteProcessCrashed):
            return False

    __nonzero__ = __bool__      # alias for python2 compatibility

    @property
    def version(self):
        """Get the MAD-X version."""
        return Version(self._libmadx.get_version_number(),
                       self._libmadx.get_version_date())

    @property
    def command(self):
        """
        Perform a single MAD-X command.

        :param str cmd: command name
        :param kwargs: command parameters
        """
        return MadxCommands(self.input)

    def input(self, text):
        """
        Run any textual MAD-X input.

        :param str text: command text
        """
        # write to history before performing the input, so if MAD-X
        # crashes, it is easier to see, where it happened:
        self._command_log(text)
        try:
            self._libmadx.input(text)
        except _rpc.RemoteProcessCrashed:
            # catch + reraise in order to shorten stack trace (~3-5 levels):
            raise RuntimeError("MAD-X has stopped working!")

    @property
    def globals(self):
        """Get a dict-like interface to global MAD-X variables."""
        return VarListProxy(self._libmadx)

    @property
    def elements(self):
        """Get a dict-like interface to globally visible elements."""
        return GlobalElementList(self._libmadx)

    def set_value(self, name, value):
        """
        Set a variable value ("=" operator in MAD-X).

        Example:

            >>> madx.set_value('R1QS1->K1', '42')
            >>> madx.evaluate('R1QS1->K1')
            42
        """
        self.input(name + ' = ' + str(value) + ';')

    def set_expression(self, name, expr):
        """
        Set a variable expression (":=" operator in MAD-X).

        Example:

            >>> madx.set_expression('FOO', 'BAR')
            >>> madx.set_value('BAR', 42)
            >>> madx.evaluate('FOO')
            42
            >>> madx.set_value('BAR', 43)
            >>> madx.evaluate('FOO')
            43
        """
        self.input(name + ' := ' + str(expr) + ';')

    def help(self, cmd=None):
        """
        Show help about a command or list all MAD-X commands.

        :param str cmd: command name
        """
        # The case 'cmd == None' will be handled by mad_command
        # appropriately.
        self.command.help(cmd)

    def chdir(self, path):
        """
        Change the directory of the MAD-X process (not the current python process).

        :param str path: new path name
        :returns: a context manager that can change the directory back
        :rtype: ChangeDirectory

        It can be used as context manager for temporary directory changes::

            with madx.chdir('/x/y/z'):
                madx.call('file.x')
                madx.call('file.y')

        This method is special in that it is currently the only modification
        of the MAD-X interpreter state that doesn't go through the
        :meth:`Madx.input` method (because there is no MAD-X command to change
        the directory).
        """
        # Note, that the libmadx module includes the functions 'getcwd' and
        # 'chdir' so it can be used as a valid 'os' module for the purposes
        # of ChangeDirectory:
        return ChangeDirectory(path, self._libmadx)

    def call(self, filename, chdir=False):
        """
        CALL a file in the MAD-X interpreter.

        :param str filename: file name with path
        :param bool chdir: temporarily change directory in MAD-X process
        """
        if chdir:
            dirname, basename = os.path.split(filename)
            with self.chdir(dirname):
                self.command.call(file=basename)
        else:
            self.command.call(file=filename)

    def select(self, flag, columns, pattern=[]):
        """
        Run SELECT command.

        :param str flag: one of: twiss, makethin, error, seqedit
        :param list columns: column names
        :param list pattern: selected patterns
        """
        select = self.command.select
        select(flag=flag, clear=True)
        if columns:
            select(flag=flag, column=columns)
        for p in pattern:
            select(flag=flag, pattern=p)

    def twiss(self,
              sequence=None,
              range=None,
              # *,
              # These should be passed as keyword-only parameters:
              twiss_init={},
              columns=None,
              pattern=['full'],
              **kwargs):
        """
        Run SELECT+USE+TWISS.

        :param str sequence: name of sequence
        :param list pattern: pattern to include in table
        :param list columns: columns to include in table, (may be a str)
        :param dict twiss_init: dictionary of twiss initialization variables
        :param bool chrom: Also calculate chromatic functions (slower)
        :param kwargs: further keyword arguments for the MAD-X command

        Note that the kwargs overwrite any arguments in twiss_init.
        """
        self.select('twiss', columns=columns, pattern=pattern)
        sequence = self._use(sequence)
        twiss_init = dict((k, v) for k,v in twiss_init.items()
                          if k not in ['name','closed-orbit'])
        # explicitly specified keyword arguments overwrite values in
        # twiss_init:
        twiss_init.update(kwargs)
        self.command.twiss(sequence=sequence,
                           range=range,
                           **twiss_init)
        return self.get_table('twiss')

    def survey(self,
               sequence=None,
               columns=None,
               pattern=['full'],
               **kwargs):
        """
        Run SELECT+USE+SURVEY.

        :param str sequence: name of sequence
        :param list pattern: pattern to include in table
        :param list columns: Columns to include in table
        :param kwargs: further keyword arguments for the MAD-X command
        """
        self.select('survey', pattern=pattern, columns=columns)
        self._use(sequence)
        self.command.survey(**kwargs)
        return self.get_table('survey')

    def use(self, sequence):
        """
        Run USE to expand a sequence.

        :param str sequence: sequence name
        :returns: name of active sequence
        """
        self.command.use(sequence=sequence)

    def _use(self, sequence):
        """
        USE sequence if it is not active.

        :param str sequence: sequence name, may be None
        :returns: new active sequence name
        :rtype: str
        :raises RuntimeError: if there is no active sequence
        """
        try:
            active_sequence = self.active_sequence
        except RuntimeError:
            if not sequence:
                raise
            active_sequence = None
        else:
            if not sequence:
                sequence = active_sequence.name
        if (sequence != active_sequence
                or not self._libmadx.is_sequence_expanded(sequence)):
            self.use(sequence)
        return sequence

    def sectormap(self, elems, **kwargs):
        """
        Compute the 7D transfer maps (the 7'th column accounting for KICKs)
        for the given elements and return as Nx7x7 array.
        """
        self.command.select(flag='sectormap', clear=True)
        for elem in elems:
            self.command.select(flag='sectormap', range=elem)
        with util.temp_filename() as sectorfile:
            self.twiss(sectormap=True, sectorfile=sectorfile, **kwargs)
        return self.sectortable()

    def sectortable(self, name='sectortable'):
        """Read sectormap + kicks from memory and return as Nx7x7 array."""
        tab = self.get_table(name)
        cnt = len(tab['r11'])
        return np.vstack((
            np.hstack((tab.rmat(slice(None)),
                       tab.kvec(slice(None)).reshape((6,1,-1)))),
            np.hstack((np.zeros((1, 6, cnt)),
                       np.ones((1, 1, cnt)))),
        )).transpose((2,0,1))

    def match(self,
              sequence=None,
              constraints=[],
              vary=[],
              weight=None,
              method=('lmdif', {}),
              knobfile=None,
              twiss_init={},
              **kwargs):
        """
        Perform a simple MATCH operation.

        For more advanced cases, you should issue the commands manually.

        :param str sequence: name of sequence
        :param list constraints: constraints to pose during matching
        :param list vary: knob names to be varied
        :param dict weight: weights for matching parameters
        :param str knobfile: file to write the knob values to
        :param dict twiss_init: initial twiss parameters
        :param dict kwargs: further keyword arguments for the MAD-X command
        :returns: final knob values
        :rtype: dict

        Example:

        >>> from cpymad.madx import Madx
        >>> from cpymad.types import Constraint
        >>> m = Madx()
        >>> m.call('sequence.madx')
        >>> twiss_init = {'betx': 1, 'bety': 2, 'alfx': 3, 'alfy': 4}
        >>> m.match(
        ...     sequence='mysequence',
        ...     constraints=[
        ...         dict(range='marker1',
        ...              betx=Constraint(min=1, max=3),
        ...              bety=2)
        ...     ],
        ...     vary=['qp1->k1',
        ...           'qp2->k1'],
        ...     twiss_init=twiss_init,
        ... )
        >>> tw = m.twiss('mysequence', twiss_init=twiss_init)
        """
        sequence = self._use(sequence)
        twiss_init = dict((k, v) for k,v in twiss_init.items()
                          if k not in ['name','closed-orbit'])
        # explicitly specified keyword arguments overwrite values in
        # twiss_init:
        twiss_init.update(kwargs)

        command = self.command
        # MATCH (=start)
        command.match(sequence=sequence, **twiss_init)
        if weight:
            command.weight(**weight)
        for c in constraints:
            command.constraint(**c)
        for v in vary:
            command.vary(name=v)
        command(method[0], **method[1])
        command.endmatch(knobfile=knobfile)
        return dict((knob, self.evaluate(knob)) for knob in vary)

    def verbose(self, switch=True):
        """Turn verbose output on/off."""
        self.command.option(echo=switch, warn=switch, info=switch)

    def get_table(self, table):
        """
        Get the specified table from MAD-X.

        :param str table: table name
        :returns: a proxy for the table data
        :rtype: TableProxy
        """
        return TableProxy(table, self._libmadx)

    @property
    def active_sequence(self):
        """The active :class:`Sequence` (may be None)."""
        try:
            return Sequence(self._libmadx.get_active_sequence_name(),
                            self, _check=False)
        except RuntimeError:
            return None

    @active_sequence.setter
    def active_sequence(self, sequence):
        if isinstance(sequence, Sequence):
            name = sequence.name
        elif isinstance(sequence, basestring):
            name = sequence
        try:
            active_sequence = self.active_sequence
        except RuntimeError:
            self.use(name)
        else:
            if active_sequence.name != name:
                self.use(name)

    def evaluate(self, cmd):
        """
        Evaluates an expression and returns the result as double.

        :param str cmd: expression to evaluate.
        :returns: numeric value of the expression
        :rtype: float
        """
        # Try to prevent process crashes:
        # NOTE: this limits to a sane subset of accepted MAD-X expressions.
        util.check_expression(cmd)
        return self._libmadx.evaluate(cmd)

    @property
    def sequences(self):
        """A dict like view of all sequences in memory."""
        return SequenceMap(self)

    @property
    def tables(self):
        """A dict like view of all tables in memory."""
        return TableMap(self._libmadx)


def _map_repr(self):
    """String representation of a custom mapping object."""
    return "{}({})".format(self.__class__.__name__, str(dict(self)))


class SequenceMap(collections.Mapping):

    """
    A dict like view of all sequences (:class:`Sequence`) in memory.
    """

    def __init__(self, madx):
        self._madx = madx
        self._libmadx = madx._libmadx

    __repr__ = _map_repr
    __str__ = _map_repr

    def __iter__(self):
        return iter(self._libmadx.get_sequence_names())

    def __getitem__(self, name):
        try:
            return Sequence(name, self._madx)
        except ValueError:
            raise KeyError

    def __contains__(self, name):
        return self._libmadx.sequence_exists(name)

    def __len__(self):
        return self._libmadx.get_sequence_count()


class TableMap(collections.Mapping):

    """
    A dict like view of all tables (:class:`TableProxy`) in memory.
    """

    def __init__(self, libmadx):
        self._libmadx = libmadx

    __repr__ = _map_repr
    __str__ = _map_repr

    def __iter__(self):
        return iter(self._libmadx.get_table_names())

    def __getitem__(self, name):
        try:
            return TableProxy(name, self._libmadx)
        except ValueError:
            raise KeyError

    def __contains__(self, name):
        return self._libmadx.table_exists(name)

    def __len__(self):
        return self._libmadx.get_table_count()


class Sequence(object):

    """
    MAD-X sequence representation.
    """

    def __init__(self, name, madx, _check=True):
        """Store sequence name."""
        self._name = name
        self._madx = madx
        self._libmadx = madx._libmadx
        if _check and not self._libmadx.sequence_exists(name):
            raise ValueError("Invalid sequence: {!r}".format(name))

    def __str__(self):
        """String representation."""
        return "<{}: {}>".format(self.__class__.__name__, self._name)

    def __eq__(self, other):
        """Comparison by sequence name."""
        if isinstance(other, Sequence):
            other = other.name
        return self.name == other

    # in py3 __ne__ delegates to __eq__, but we still need this for py2:
    def __ne__(self, other):
        """Comparison by sequence name."""
        return not (self == other)

    __repr__ = __str__

    @property
    def name(self):
        """Get the name of the sequence."""
        return self._name

    @property
    def beam(self):
        """Get the beam dictionary associated to the sequence."""
        return self._libmadx.get_sequence_beam(self._name)

    @beam.setter
    def beam(self, beam):
        self._madx.command.beam(sequence=self._name, **beam)

    @property
    def twiss_table(self):
        """Get the TWISS results from the last calculation."""
        return TableProxy(self.twiss_table_name, self._libmadx)

    @property
    def twiss_table_name(self):
        """Get the name of the table with the TWISS results."""
        return self._libmadx.get_sequence_twiss_table_name(self._name)

    @property
    def elements(self):
        """Get list of elements."""
        return ElementList(self._libmadx, self._name)

    @property
    def expanded_elements(self):
        """List of elements including implicit drifts."""
        return ExpandedElementList(self._libmadx, self._name)

    def element_names(self):
        return self._libmadx.get_element_names(self._name)

    def element_positions(self):
        return self._libmadx.get_element_positions(self._name)

    def expanded_element_names(self):
        return self._libmadx.get_expanded_element_names(self._name)

    def expanded_element_positions(self):
        return self._libmadx.get_expanded_element_positions(self._name)

    def _parse_range(self, range):
        """
        Return a tuple (start, stop) for the given range.
        """
        if range is None:
            beg, end = ('#s', '#e')
        elif isinstance(range, basestring):
            beg, end = range.split('/')
        else:
            beg, end = range
        return beg, end

    @property
    def is_expanded(self):
        """Check if sequence is already expanded."""
        return self._libmadx.is_sequence_expanded(self._name)

    @property
    def has_beam(self):
        """Check if the sequence has an associated beam."""
        try:
            self.beam
            return True
        except RuntimeError:
            return False

    def expand(self):
        """Expand sequence (needed for expanded_elements)."""
        if self.is_expanded:
            return
        if not self.has_beam:
            self.beam = {}
        self.use()

    def use(self):
        """Set this sequence as active."""
        self._madx.use(self._name)


class BaseElementList(object):

    """
    Immutable list of beam line elements.

    Each element is a dictionary containing its properties.
    """

    def __contains__(self, element):
        """
        Check if sequence contains element with specified name.

        Can be invoked with either the element dict or the element name.
        """
        try:
            self.index(element)
            return True
        except ValueError:
            return False

    def __getitem__(self, index):
        """Return element with specified index."""
        if isinstance(index, (dict, basestring)):
            # allow element names to be passed for convenience:
            index = self.index(index)
        # _get_element accepts indices in the range [0, len-1]. The following
        # extends the accepted range to [-len, len+1], just like for lists:
        _len = len(self)
        if index < -_len or index >= _len:
            raise IndexError("Index out of bounds: {}, length is: {}"
                             .format(index, _len))
        if index < 0:
            index += _len
        data = self._get_element(index)
        data['index'] = index
        return data

    def __len__(self):
        """Get number of elements."""
        return self._get_element_count()

    def index(self, element):
        """
        Find index of element with specified name.

        Can be invoked with either the element dict or the element name.

        :raises ValueError: if the element is not found
        """
        if isinstance(element, dict):
            name = element['name']
        else:
            name = element
        if len(self) == 0:
            raise ValueError('Empty element list.')
        if name == '#s':
            return 0
        elif name == '#e':
            return len(self) - 1
        index = self._get_element_index(name)
        if index == -1:
            raise ValueError("Element not in list: {!r}".format(name))
        return index


class ElementList(BaseElementList, collections.Sequence):

    def __init__(self, libmadx, sequence_name):
        """
        Initialize instance.
        """
        self._libmadx = libmadx
        self._sequence_name = sequence_name

    def at(self, pos):
        """Find the element at specified S position."""
        return self._get_element_at(pos)

    def _get_element(self, element_index):
        return self._libmadx.get_element(self._sequence_name, element_index)

    def _get_element_count(self):
        return self._libmadx.get_element_count(self._sequence_name)

    def _get_element_index(self, element_name):
        return self._libmadx.get_element_index(self._sequence_name, element_name)

    def _get_element_at(self, pos):
        return self._libmadx.get_element_index_by_position(self._sequence_name, pos)


class ExpandedElementList(ElementList):

    def _get_element(self, element_index):
        return self._libmadx.get_expanded_element(self._sequence_name, element_index)

    def _get_element_count(self):
        return self._libmadx.get_expanded_element_count(self._sequence_name)

    def _get_element_index(self, element_name):
        return self._libmadx.get_expanded_element_index(self._sequence_name, element_name)

    def _get_element_at(self, pos):
        return self._libmadx.get_expanded_element_index_by_position(self._sequence_name, pos)


class GlobalElementList(BaseElementList, collections.Mapping):

    """
    Provides dict-like access to MAD-X global elements.
    """

    def __init__(self, libmadx):
        self._libmadx = libmadx
        self._get_element = libmadx.get_global_element
        self._get_element_count = libmadx.get_global_element_count
        self._get_element_index = libmadx.get_global_element_index

    def __iter__(self):
        for i in range(len(self)):
            yield self._libmadx.get_global_element_name(i)


class TableProxy(collections.Mapping):

    """
    Proxy object for lazy-loading table column data.
    """

    def __init__(self, name, libmadx, _check=True):
        """Just store the table name for now."""
        self._name = name
        self._libmadx = libmadx
        self._cache = {}
        if _check and not libmadx.table_exists(name):
            raise ValueError("Invalid table: {!r}".format(name))

    def __getitem__(self, column):
        """Get the column data."""
        try:
            return self._cache[column]
        except KeyError:
            return self.reload(column)

    def _query(self, column):
        """Retrieve the column data."""
        try:
            return self._libmadx.get_table_column(self._name, column.lower())
        except ValueError:
            raise KeyError(column)

    def __iter__(self):
        """Iterate over all column names."""
        return iter(self._libmadx.get_table_column_names(self._name) or
                    self._libmadx.get_table_column_names_all(self._name))

    def __len__(self):
        """Return number of columns."""
        return (self._libmadx.get_table_column_count(self._name) or
                self._libmadx.get_table_column_count_all(self._name))

    @property
    def summary(self):
        """Get the table summary."""
        return self._libmadx.get_table_summary(self._name)

    @property
    def range(self):
        """Get the element names (first, last) of the valid range."""
        row_count = self._libmadx.get_table_row_count(self._name)
        range = (0, row_count-1)
        return tuple(self._libmadx.get_table_row_names(self._name, range))

    def reload(self, column):
        """Reload (recache) one column from MAD-X."""
        self._cache[column] = data = self._query(column)
        return data

    def cache(self, columns=None):
        """Make sure given columns are cached locally."""
        if columns is None:
            columns = self
        for column in columns:
            _tmp = self[column]

    def copy(self, columns=None):
        """
        Return a frozen table with the desired columns.

        :param list columns: column names or ``None`` for all columns.
        :returns: column data
        :rtype: dict
        :raises ValueError: if the table name is invalid
        """
        if columns is None:
            columns = self
        return {column: self[column] for column in columns}

    def getvec(self, name, idx, dim):
        return np.array([
            self['{}{}'.format(name, i+1)][idx]
            for i in range(dim)])

    def getmat(self, name, idx, dim):
        return np.array([
            [self['{}{}{}'.format(name, i+1, j+1)][idx]
             for j in range(dim)]
            for i in range(dim)])

    def kvec(self, idx, dim=6):
        """Kicks."""
        return self.getvec('k', idx, dim)

    def rmat(self, idx, dim=6):
        """Sectormap."""
        return self.getmat('r', idx, dim)

    def sigmat(self, idx, dim=6):
        """Beam matrix."""
        return self.getmat('sig', idx, dim)

class VarListProxy(collections.MutableMapping):

    """
    Provides dict-like access to MAD-X global variables.
    """

    def __init__(self, libmadx):
        self._libmadx = libmadx

    __repr__ = _map_repr
    __str__ = _map_repr

    def __getitem__(self, name):
        return self._libmadx.get_var(name)

    def __setitem__(self, name, value):
        self._libmadx.set_var(name, value)

    def __delitem__(self, name):
        raise NotImplementedError("Currently, can't erase a MAD-X global.")

    def __iter__(self):
        """Iterate names of all non-constant globals."""
        for name in self._libmadx.get_globals():
            # var_type=0 is for (predefined) constants like PI:
            if self._libmadx.get_var_type(name) > 0:
                yield name

    def __len__(self):
        return self._libmadx.num_globals()


class Metadata(object):

    """MAD-X metadata (license info, etc)."""

    __title__ = u'MAD-X'

    @property
    def __version__(self):
        return self._get_libmadx().get_version_number()

    __summary__ = (
        u'MAD is a project with a long history, aiming to be at the '
        u'forefront of computational physics in the field of particle '
        u'accelerator design and simulation. The MAD scripting language '
        u'is de facto the standard to describe particle accelerators, '
        u'simulate beam dynamics and optimize beam optics.'
    )

    __support__ = u'mad@cern.ch'

    __uri__ = u'http://madx.web.cern.ch/madx/'

    __credits__ = (
        u'MAD-X is developed at CERN and has many contributors. '
        u'For more information see:\n'
        u'\n'
        u'http://madx.web.cern.ch/madx/www/contributors.html'
    )

    def get_copyright_notice(self):
        from pkg_resources import resource_string
        return resource_string('cpymad', 'COPYING/madx.rst').decode('utf-8')

    _libmadx = None

    def _get_libmadx(self):
        if not self._libmadx:
            svc, proc = _rpc.LibMadxClient.spawn_subprocess()
            self._libmadx = svc.libmadx
        return self._libmadx


metadata = Metadata()
