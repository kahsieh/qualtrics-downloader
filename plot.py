#!/usr/bin/env python3

"""
plot.py
"""

import csv
from collections import Counter
from typing import List, Tuple

from matplotlib import pyplot as plt
from matplotlib.figure import Figure

def plottable(cell: str) -> bool:
  """
  Determines whether a cell is plottable. Currently, a cell is considered
  plottable if its contents can be interpreted as a floating-point number.

  Args:
    cell (str): cell contents

  Returns:
    bool: whether the cell is plottable
  """
  try:
    float(cell)
    return True
  except ValueError:
    return False


def listPlottableColumnsInCsv(path: str) -> List[str]:
  """
  Get a list of descriptions of of plottable columns in the .csv file.

  Args:
    path (str): path to .csv file

  Returns
    List[str]: list of column descriptions
  """
  plottableColumns: List[str] = []
  with open(path, 'r') as csvfile:
    for column in map(list, zip(*csv.reader(csvfile))):
      # A column is considered plottable if the contents of all its cells
      # (ignoring rows 0, 1, and 2) are plottable.
      if all(plottable(cell) for cell in column[3:]):
        plottableColumns.append('{}: {}'.format(column[0], column[1]))
  return plottableColumns


def plotColumn(column: List[str]):
  """
  Displays a bar chart for a column of survey response data.

  Args:
    column (List[str]): A column of survey response data, where column[0] and
      column[1] make up the title and data start at column[3].

  Raises:
    ValueError: If the column cannot be plotted because a value couldn't be
      interpreted as a floating-point number.
  """
  # Produce a value-frequency table, ignoring headers (rows 0-2).
  table: List[Tuple[str, int]] = list(Counter(column[3:]).items())
  # Sort by the values' floating-point interpretations.
  table.sort(key=lambda pair: float(pair[0]))
  # Transpose to separate the value list from the frequency list.
  values, frequencies = zip(*table)
  # Create a bar chart.
  figure: Figure = plt.figure()
  plt.bar(values, frequencies)
  # Add title and axis labels.
  plt.title('{}: {}'.format(column[0], column[1]))
  plt.xlabel('Response')
  plt.ylabel('Count')
  # Set y-axis to use integers only.
  figure.gca().yaxis.get_major_locator().set_params(integer=True)
  # Display the chart.
  plt.show()


def plotColumnByDescription(path: str, description: str):
  """
  Displays bar charts for columns in the .csv file matching the given
  description.

  Args:
    path (str): path to .csv file
    description (str): column description
  """
  # Open the file specified.
  with open(path, 'r') as csvfile:
    # Read the file as a CSV (csv.reader(...)), transpose it so that we can
    # iterate by column (zip(*...)), and convert each column to a list
    # (map(list, ...)) for easy use.
    for column in map(list, zip(*csv.reader(csvfile))):
      # Try plotting the column. If successful, also print a message.
      if description == '{}: {}'.format(column[0], column[1]):
        try:
          plotColumn(column)
          print('Plotted: {}: {}'.format(column[0], column[1]))
        # If plotting fails because a value couldn't be interpreted as a floating-
        # point number, print a message to that effect.
        except ValueError:
          print('Not plottable: {}: {}'.format(column[0], column[1]))
