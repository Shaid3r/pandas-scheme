# pandas-scheme

This is a Taurus scheme that provides access to the contents of files
as Taurus Attributes. It uses the [pandas](http://pandas.pydata.org/) module.

## Enabling
To enable it, install `taurus-pandas-scheme` and edit `<taurus>/tauruscustomsettings.py`
to add `taurus_pandas` to the `EXTRA_SCHEME_MODULES` list. For example:

```python
EXTRA_SCHEME_MODULES = ['taurus_pandas']
```

## Examples:

Once the new scheme is enabled in your taurus installation, you can:


- Recognize file extension and get all columns from 1-st sheet

    `pds:/path/to/file.xls::`

- Force xls handler and get all columns from "Sheet"

    `pds-xls:/path/to/file::"Sheet"`

- Get 1 column ("column1" must be in brackets)

    `pds-xls:/path/to/file::"Sheet",["column1"]`

- Get multiple columns

    `pds-xls:/path/to/file::"Sheet",["column1","column2"]`

- Get row 0, all columns

    `pds-xls:/path/to/file::"Sheet",[],[0]`

- Get all rows from 0 to 7 (excluding 7), all columns, 1-st sheet

    `pds-xls:/path/to/file::"",[],[0,7]`

- Pass parameters to pandas function

    `pds-xls:/path/to/file::{"parse_cols":"A:B"}`
