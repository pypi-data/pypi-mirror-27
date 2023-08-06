# pandas_lite
A simpler alternative to pandas

# Main Goals
* A very minimal set of features 
* Be as explicit as possible

## Data Structures
* Only DataFrames
* No Series

## Data Types
* Only primitive types - int, float, boolean, numpy.unicode
* No object data types

## Row and Column Labels
* No index, meaning no row labels
* No hierarchical index
* Column names must be strings
* Column names must be unique
* Columns stored in a numpy array

## Subset Selection
* Only one way to select data - `[ ]`
* Subset selection will be explicit and necessitate both rows and columns
* Rows will be selected only by integer location
* Columns will be selected by either label or integer location. Since columns must be strings, this will not be amibguous

## All selections and operations copy
* All selections and operations provide new copies of the data
* This will avoid any chained indexing confusion

## Development
* Must use type hints
* Must use 3.6 - fstrings
