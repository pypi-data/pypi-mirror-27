import decimal
import numpy as np
from typing import (Union, Dict, List, Optional, Tuple,
                    NoReturn, Any, Set, Sequence)
import bottleneck as bn
from .utils import check_duplicate_list

DataConstructor = Union[Dict[str, Union[np.ndarray, List]], np.ndarray]
BlockConstructor = Dict[str, List[np.ndarray]]
Block = Dict[str, Optional[np.ndarray]]

# can change to array of strings?
ColumnType = Optional[Union[List[str], np.ndarray]]

ColumnSelection = Union[int, str, slice, List[Union[str, int]]]
RowSelection = Union[int, slice, List[int]]

max_cols: int = 10
max_rows: int = 10

_NUMERIC_KINDS: Set[str] = set('buif')


class DataFrame:
    def __init__(self, data: DataConstructor,
                 columns: ColumnType=None) -> None:

        self._columns: np.ndarray
        self._data: Block = {'b': None, 'i': None, 'f': None, 'U': None}

        self._dtype_column: Dict[str, List] = {'b': [], 'i': [],
                                               'f': [], 'U': []}
        self._column_dtype: Dict[str, str] = {}

        if isinstance(data, dict):
            self._initialize_columns_from_dict(columns, list(data.keys()))
            self._initialize_data_from_dict(data)

        elif isinstance(data, np.ndarray):
            data = self._validate_data_from_array(data)
            self._initialize_columns_from_array(columns, data.shape[1])
            self._initialize_data_from_array(data)

        else:
            raise TypeError('data parameter must be either a dict '
                            'of arrays or an array')
        self._map_columns_to_types()

    @property
    def columns(self) -> List[str]:
        return self._columns.tolist()

    # Only gets called after construction, when renaming columns
    @columns.setter
    def columns(self, new_columns: ColumnType) -> None:
        self._check_column_validity(new_columns)
        new_columns = np.asarray(new_columns)
        len_new, len_old = len(new_columns), len(self._columns)
        if len_new != len_old:
            raise ValueError(f'''There are {len_old} columns in the DataFrame.
                              You provided {len_new}''')
        self._map_types_to_columns(new_columns)
        self._map_columns_to_types()
        self._columns = new_columns

    def _initialize_columns_from_dict(self, columns: ColumnType,
                                      dict_keys: List[Any]) -> None:
        if columns is None:
            columns = np.array(dict_keys)
        self._check_column_validity(columns)
        if set(columns) != set(dict_keys):
            raise ValueError("Column names don't match dictionary keys")
        else:
            self._columns = np.asarray(columns)

    def _initialize_columns_from_array(self, columns: ColumnType,
                                       num_cols: int) -> None:
        if columns is None:
            self._columns = np.array(['a' + str(i) for i in range(num_cols)])
        else:
            self._check_column_validity(columns)
            if len(columns) != num_cols:
                raise ValueError(f'Number of column names {len(columns)}'
                                 'does not match number columns '
                                 f'of data {num_cols}')
            self._columns = np.asarray(columns)

    @staticmethod
    def _check_column_validity(cols: ColumnType) -> None:
        if not isinstance(cols, (list, np.ndarray)):
            raise TypeError('Columns must be a list or an array')
        if isinstance(cols, np.ndarray):
            if cols.ndim != 1:
                raise ValueError('Array of column must be 1 dimension')
        for i, col in enumerate(cols):
            if not isinstance(col, str):
                raise TypeError('Column names must be a string')
            if col in cols[i + 1:]:
                raise ValueError(f'Column name {col} is duplicated. '
                                 'Column names must '
                                 'be unique')
        return None

    def _initialize_data_from_dict(self, data: DataConstructor) -> None:
        data_dict: BlockConstructor = {'b': [], 'i': [], 'f': [], 'U': []}
        for i, (k, values) in enumerate(data.items()):
            if not isinstance(values, (list, np.ndarray)):
                raise TypeError('Values of dictionary must be an '
                                'array or a list')
            if isinstance(values, list):
                values = np.array(values)
            data_dict = self._add_1darray(values, data_dict, k)

            if i == 0:
                first_len = len(values)
            if len(values) != first_len:
                raise ValueError('All columns must be the same length')

        # concatenate all columns of same type into a single array
        for k, v in data_dict.items():
            if v:
                self._data[k] = np.column_stack(v)

    def _validate_data_from_array(self, data: np.ndarray) -> np.ndarray:
        if data.dtype.kind not in 'bifU':
            raise TypeError('Array must be of type boolean, integer, '
                            'float or unicode')
        elif data.ndim not in [1, 2]:
            raise ValueError('Array must be either one or two dimensions')
        else:
            if data.ndim == 1:
                data = data[:, np.newaxis]
        return data

    def _initialize_data_from_array(self, data: np.ndarray) -> None:
        kind = data.dtype.kind
        self._data = {dt: data if dt == kind else None for dt in 'bifU'}
        self._dtype_column[kind].extend(list(self._columns))

    def _add_1darray(self, values: np.ndarray,
                     data_dict: BlockConstructor,
                     col_name: str) -> BlockConstructor:
        if values.ndim != 1:
            raise TypeError('Each array of data must be one dimension')
        kind = values.dtype.kind
        data_dict[kind].append(values)
        self._dtype_column[kind].append(col_name)
        return data_dict

    def _map_types_to_columns(self, new_columns: ColumnType) -> None:
        temp_col_attrs: Dict[str, List] = {}
        old_new_map = dict(zip(self._columns, new_columns))
        for kind, old_cols in self._dtype_column.items():
            new_cols = [old_new_map[old_col] for old_col in old_cols]
            temp_col_attrs[kind] = new_cols
        self._dtype_column = temp_col_attrs

    def _map_columns_to_types(self) -> None:
        self._column_dtype: Dict[str, str] = {}
        for kind, cols in self._dtype_column.items():
            for col in cols:
                self._column_dtype[col] = kind

    @property
    def values(self) -> np.ndarray:
        arrays: List[np.ndarray] = []
        this_column_order: List[str] = []
        cur_kinds: List[str] = []
        for kind in 'bifU':
            if self._data[kind] is not None:
                cur_kinds.append(kind)
                if kind == 'U' and len(cur_kinds) > 1:
                    arrays.append(self._data[kind].astype('O'))
                else:
                    arrays.append(self._data[kind])
                this_column_order.extend(self._dtype_column[kind])

        new_data = np.concatenate(arrays, axis=1)
        correct_order = [this_column_order.index(col) for col in self.columns]
        return new_data[:, correct_order]

    @values.setter
    def values(self, data: Any) -> NoReturn:
        raise AttributeError("Can't set attribute")

    def _get_col_array(self, col_name: str) -> np.ndarray:
        kind: str = self._column_dtype[col_name]
        idx: int = self._dtype_column[kind].index(col_name)
        return self._data[kind][:, idx]

    def _get_num_decimals(self, num):
        return abs(decimal.Decimal(str(num)).as_tuple().exponent)

    def _build_repr(self) -> Tuple:
        columns: List[str] = self.columns
        num_rows: int = len(self)
        if len(columns) > max_cols:
            col_num: int = max_cols // 2
            columns = columns[:col_num] + ['...'] + columns[-col_num:]

        if num_rows > max_rows:
            first: List[int] = list(range(max_rows // 2))
            last: List[int] = list(range(num_rows - max_rows // 2, num_rows))
            idx: List[int] = first + last
        else:
            idx = list(range(num_rows))

        data_list: List[List[str]] = [[''] + [str(i) for i in idx]]
        long_len: List[int] = [len(data_list[0][-1])]
        decimal_len: List[int] = [0]
        for column in columns:
            if column != '...':
                data = [column] + self._get_col_array(column)[idx].tolist()
            else:
                data = ['...'] * (len(idx) + 1)

            if self._column_dtype[column] == 'U':
                long_len.append(max([len(x) for x in data]))
                decimal_len.append(0)
            elif self._column_dtype[column] in ['f', 'i']:
                max_decimal = max([self._get_num_decimals(x)
                                   for x in data[1:]])
                lengths = [len(column)] + [len(f'{x: >10.6g}')
                                           for x in data[1:]]
                long_len.append(max(lengths))
                decimal_len.append(min(max_decimal, 6))
            elif self._column_dtype[column] == 'b':
                long_len.append(max(len(column), 5))
                decimal_len.append(0)

            data_list.append(data)

        return data_list, long_len, decimal_len, idx

    def __repr__(self) -> str:
        data_list, long_len, decimal_len, idx = self._build_repr()
        string: str = ''
        for i in range(len(idx) + 1):
            for d, fl, dl in zip(data_list, long_len, decimal_len):
                if str(d[i]) == 'nan':
                    d[i] = 'NaN'
                if isinstance(d[i], bool):
                    d[i] = str(d[i])
                if isinstance(d[i], str):
                    string += f'{d[i]: >{str(fl)}}  '
                else:
                    string += f'{d[i]: >10.{dl}f}  '
            string += '\n'
            if i == max_rows // 2 and len(self) > max_rows:
                for j, fl in enumerate(long_len):
                    string += f'{"...": >{str(fl)}}'
                string += '\n'
        return string

    def _repr_html_(self) -> str:
        data_list, long_len, decimal_len, idx = self._build_repr()
        string: str = '<table>'
        for i in range(len(idx) + 1):
            if i == 0:
                string += '<thead>'
            elif i == 1:
                string += '<tbody>'
            string += '<tr>'
            for j, (d, fl, dl) in enumerate(zip(data_list, long_len,
                                                decimal_len)):
                if str(d[i]) == 'nan':
                    d[i] = 'NaN'
                ts = '<th>' if j * i == 0 else '<td>'
                te = '</th>' if j * i == 0 else '</td>'
                if isinstance(d[i], bool):
                    d[i] = str(d[i])
                if isinstance(d[i], str):
                    string += f'{ts}{d[i]: >{str(fl)}}{te}'
                else:
                    string += f'{ts}{d[i]: >{str(fl)}.{dl}f}{te}'
            if i == max_rows // 2 and len(self) > max_rows:
                string += '<tr>'
                for j, fl in enumerate(long_len):
                    ts = '<th>' if j == 0 else '<td>'
                    te = '</th>' if j == 0 else '</td>'
                    string += f'{ts}{"...": >{str(fl)}}{te}'
                string += '</tr>'
            string += '</tr>'
            if i == 0:
                string += '</thead>'
        return string + '</tbody></table>'

    def __len__(self) -> int:
        for kind in 'ifUb':
            a: Optional[np.ndarray] = self._data[kind]
            if a is not None:
                return len(a)
        return 0

    @property
    def shape(self) -> Tuple[int, int]:
        return len(self), len(self._columns)

    @property
    def size(self) -> int:
        return len(self) * len(self._columns)

    def _is_numeric(self):
        return all([v.dtype.kind in _NUMERIC_KINDS
                    for k, v in self._data.items()])

    def select_dtypes(self, include=None, exclude=None):
        dkind = _NUMERIC_KINDS if include == 'number' else ['O']
        new_data = {k: v for k, v in self.data.items()
                    if v.dtype.kind in dkind}
        return DataFrame(new_data)

    def _find_col_location(self, col: str) -> int:
        iloc = np.where(self._columns == col)[0]
        if len(iloc) == 0:
            raise ValueError(f'{col} is not in the columns')
        return iloc[0]

    def _get_col_name_from_int(self, iloc: int) -> str:
        try:
            return self._columns[iloc]
        except IndexError:
            raise IndexError(f'Index {iloc} is out of bounds for '
                             'the columns')

    def _convert_col_selection(self, cs: ColumnSelection) -> List[str]:
        if isinstance(cs, str):
            if cs not in self.columns:
                raise ValueError(f'{cs} is not a column')
            cs = [cs]
        elif isinstance(cs, int):
            cs = [self._get_col_name_from_int(cs)]
        elif isinstance(cs, slice):
            sss: List[Optional[int]] = []
            for s in ['start', 'stop', 'step']:
                value: Optional[Union[str, int]] = getattr(cs, s)
                if value is None or isinstance(value, int):
                    sss.append(value)
                elif isinstance(value, str):
                    if s == 'step':
                        raise TypeError('Slice step must be None or int')
                    sss.append(self._find_col_location(value))
                else:
                    raise TypeError('Slice start, stop, and step values must '
                                    'be int, str, or None')
            if isinstance(cs.stop, str):
                if cs.step is None or cs.step > 0:
                    sss[1] += 1
                elif cs.step < 0:
                    sss[1] -= 1
            cs = self.columns[slice(*sss)]
        elif isinstance(cs, list):
            new_cols: List[str] = []
            for col in cs:
                # self.columns is a list to prevent numpy warning
                if isinstance(col, int):
                    new_cols.append(self._get_col_name_from_int(col))
                elif col not in self.columns:
                    raise ValueError(f'{col} is not in the columns')
                else:
                    new_cols.append(col)
            check_duplicate_list(new_cols)
            cs = new_cols
        else:
            raise TypeError('Selection must either be one of '
                            'int, str, list, or slice')
        return cs

    def _convert_row_selection(self, rs: RowSelection):
        if isinstance(rs, slice):
            def check_none_int(obj):
                return obj is None or isinstance(obj, int)

            all_ok: bool = (check_none_int(rs.start) and
                            check_none_int(rs.stop) and
                            check_none_int(rs.step))

            if not all_ok:
                raise TypeError('Slice start, stop, and step values must '
                                'be int or None')
        elif isinstance(rs, list):
            for row in rs:
                # self.columns is a list to prevent numpy warning
                if not isinstance(row, int):
                    raise TypeError('Row selection must consist '
                                    'only of integers')
        elif not isinstance(rs, int):
            raise TypeError('Selection must either be one of '
                            'int, list, or slice')

    def _getitem_scalar(self, rs, cs):
        if isinstance(cs, str):
            if cs not in self.columns:
                raise ValueError(f'{cs} is not a column')
        elif isinstance(cs, int):
            cs = self._get_col_name_from_int(cs)
        dtype, dtype_index = self._get_single_column_info(cs)
        return self._data[dtype][rs, dtype_index]

    # return the dtype and the position of that column
    def _get_single_column_info(self, col) -> Tuple[str, int]:
        dtype: str = self._column_dtype[col]
        dtype_index: int = self._dtype_column[dtype].index(col)
        return dtype, dtype_index

    def _construct_df_from_selection(self, rs, cs) -> 'DataFrame':
        new_col_attrs: Dict[str, List[str]] = {'U': [], 'b': [],
                                               'f': [], 'i': []}
        new_data: Block = {'U': None, 'b': None, 'f': None, 'i': None}
        dtype_index_map: Dict[str, List[int]] = {'U': [], 'b': [],
                                                 'f': [], 'i': []}

        for col in cs:
            dtype, dtype_index = self._get_single_column_info(col)
            new_col_attrs[dtype].append(col)
            dtype_index_map[dtype].append(dtype_index)

        for dt, index in dtype_index_map.items():
            if index:
                if isinstance(rs, list) and isinstance(index, list):
                    arr = self._data[dt][np.ix_(rs, index)].copy()
                else:
                    arr = self._data[dt][rs, index].copy()
                if arr.ndim == 1:
                    arr = arr[np.newaxis, :]
                new_data[dt] = arr

        df_new: DataFrame = DataFrame.__new__(DataFrame)
        df_new._dtype_column = new_col_attrs
        df_new._data = new_data
        df_new._columns = np.array(cs)
        df_new._map_columns_to_types()
        return df_new

    def __getitem__(self, value: Tuple[RowSelection,
                                       ColumnSelection]) -> 'DataFrame':
        if not isinstance(value, tuple):
            raise TypeError('You must provide both a row and column '
                            'selection separated by a comma')
        if len(value) != 2:
            raise TypeError('You must provide exactly one row selection '
                            'and one column selection')

        row_selection, col_selection = value
        if (isinstance(row_selection, int) and
                isinstance(col_selection, (int, str))):
            return self._getitem_scalar(row_selection, col_selection)

        col_selection = self._convert_col_selection(col_selection)
        self._convert_row_selection(row_selection)

        return self._construct_df_from_selection(row_selection, col_selection)

    def to_dict(self, orient: str='array') -> Dict[str, Union[np.ndarray, List]]:
        '''
        Conver DataFrame to dictionary of 1-dimensional arrays or lists

        Parameters
        ----------
        orient : str {'array' or 'list'}
        Determines the type of the values of the dictionary.
        '''
        if orient not in ['array', 'list']:
            raise ValueError('orient must be either "array" or "list"')
        data = {}
        for col in self.columns:
            dt, idx = self._get_single_column_info(col)
            if orient == 'array':
                data[col] = self._data[dt][:, idx]
            else:
                data[col] = self._data[dt][:, idx].tolist()
        return data
