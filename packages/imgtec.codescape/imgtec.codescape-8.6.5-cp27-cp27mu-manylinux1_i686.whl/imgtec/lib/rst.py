###############################################################################
#
# Disclaimer of Warranties and Limitation of Liability
#
# This software is available under the following conditions:
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL IMAGINATION TECHNOLOGIES LLC OR IMAGINATION
# TECHNOLOGIES LIMITED BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2016, Imagination Technologies Limited and/or its affiliated
# group companies ("Imagination").  All rights reserved.
# No part of this content, either material or conceptual may be copied or
# distributed, transmitted, transcribed, stored in a retrieval system or
# translated into any human or computer language in any form by any means,
# electronic, mechanical, manual, or otherwise, or disclosed to third parties
# without the express written permission of Imagination.
#
###############################################################################

import itertools
import re


def title(s, ch="=", document_title=False):
    r"""Create a title.

    >>> print title('Hello World', '-')
    Hello World
    -----------

    >>> print title('Hello World', document_title=True)
    ===========
    Hello World
    ===========

    """
    dashes = ch * len(s)
    top = dashes + '\n' if document_title else ''
    return "%s%s\n%s" % (top, s, dashes)


def table(header, rows):
    r"""Create a simple rst table if possible, else a grid table.

        >>> print table(['wibble', 'wibblery', 'wob'],
        ...                    [['aabbcc', '', 'wob']])
        ====== ======== ===
        wibble wibblery wob
        ====== ======== ===
        aabbcc          wob
        ====== ======== ===
        >>> print table(['wibble', 'wib\nble\nry', 'wob'],
        ...                    [['aa\nbb\ncc\n', '', 'wob']])
        +--------+-----+-----+
        | wibble | wib | wob |
        |        | ble |     |
        |        | ry  |     |
        +========+=====+=====+
        | aa     |     | wob |
        | bb     |     |     |
        | cc     |     |     |
        |        |     |     |
        +--------+-----+-----+
    """
    has_new_lines = _check_for_new_lines(header) or _check_for_new_lines(rows)
    tabler = grid_table if has_new_lines else simple_table
    return tabler(header, rows)


def headerless_table(rows):
    """Create a columned table.

    This is not really an rst thing but produces a nicely formatted table
    with all of the data in columns.

    >>> print headerless_table([['a'], ['b', 'c']])
    a
    b c
    >>> print headerless_table([('muchlonger',), ['b', 'c']] * 6)
    muchlonger
    b          c
    muchlonger
    b          c
    muchlonger
    b          c
    muchlonger
    b          c
    muchlonger
    b          c
    muchlonger
    b          c
    """
    num_cols = max(len(row) for row in rows)
    header = [''] * num_cols
    rows = [list(row) + [''] * (num_cols - len(row)) for row in rows]
    table = simple_table(header, rows).splitlines()[3:-1]
    return '\n'.join(line.rstrip() for line in table)


def _check_for_new_lines(rows):
    r"""Return True if any of the cells have new line.

    >>> _check_for_new_lines(['wibble', 'wib\nble\nry', 'wob'])
    True
    >>> _check_for_new_lines(['wibble', 'wibblery', 'wob'])
    False
    """
    newlines = False
    for rown, row in enumerate(rows):
        for coln, cell in enumerate(row):
            try:
                newlines = ('\n' in cell) or newlines
            except TypeError:
                raise ValueError('Cell(row={0}, col={1}) {2!r} is not a string.'.format(rown, coln, cell))
    return newlines


def _widths(rows):
    r"""Calculate the widths of the given cells, taking into account lines with new lines.

    >>> _widths([['wibble', 'wib\nble\nry', 'wob'],
    ...          ['aa\nbb\ncc\n', '', 'wob']])
    [6, 3, 3]
    """
    header = rows[0]
    return [max(max(len(cell) for cell in row[n].split('\n')) for row in rows) for n in range(len(header))]


def row_justifier(x, *args):
    return x.ljust(*args)


def _row(lead, sep, cells, widths, follow, process_new_lines=True, justifier=row_justifier):
    r"""

    >>> _row('<', '|', list('abc'), [1, 1, 1], '>')
    '<a|b|c>'
    >>> print _row('<', '|', ['a\na', 'b', 'c\nc\nc'], [1, 1, 1], '>')
    <a|b|c>
    <a| |c>
    < | |c>
    >>> print _row('<', '|', ['a\na', 'b', 'c\nc\nc'], [1, 1, 1], '>', False)
    <a
    a|b|c
    c
    c>
    """
    if process_new_lines:
        cols = [cell.split('\n') for cell in cells]
        rows = list(itertools.izip_longest(*cols, fillvalue=''))
        lines = [lead + sep.join(justifier(c, w) for c, w in zip(row, widths)) + follow for row in rows]
        return '\n'.join(lines)
    else:
        return lead + sep.join(cells) + follow


def _table(header, rows, cl, cm, cr, cs,
                         tl, tm, tr, ts,
                         rl, rm, rr, rs, process_new_lines=True, trim_ws=True):
    """Draw a table with the following borders:

        rl rs rs rs rm rs rs ts rr   * if rs is '' then tl, rm, tr are used here, if cs is '' then this line is skipped
        cl text  cs cm text  cs cr   * if cs is '' then tl, tm, tr are used here
        tl ts ts ts tm ts ts ts tr   * if cs is '' then this line is skipped
        cl text  cs cm text  cs cr
        rl rs rs rs rm rs rs ts rr   * if rs is '' then this line is skipped
        cl text  cs cm text  cs cr
        rl rs rs rs rm rs rs ts rr   * if rs is '' then tl, rm, tr are used here, if cs is '' then this line is skipped
    """
    num_cols = max(len(row) for row in [header] + rows)
    header = list(header) + [''] * (num_cols - len(header))
    rows = [list(row) + [''] * (num_cols - len(row)) for row in rows]
    widths = _widths([header] + rows)
    if cs:
        header = _row(cl, cm, header, widths, cr, process_new_lines)
    else:
        header = _row(tl, tm, header, widths, tr, process_new_lines)
    padded = [_row(cl, cm, row, widths, cr, process_new_lines) for row in rows]
    tsep = tl + tm.join(ts * width for width in widths) + tr
    rsep = ''
    if rs:
        rsep = '\n' + _row(rl, rm, (rs * width for width in widths), widths, rr, process_new_lines)
    lines = []
    if cs:
        lines.append((rsep or tsep).strip())
    lines.append(header)
    if cs:
        lines.append(tsep)
    lines.extend((line + rsep for line in padded))
    if cs and not rs:
        lines.append(tsep)
    if trim_ws:
        lines = [x.rstrip() for x in lines]
    return '\n'.join(lines)


def grid_table(header, rows):
    r"""Create a grid rst table.  header is a list of cells to go in
    the header row. rows is a list of list of cells for the body of the
    table.

    >>> print grid_table(['wibble', 'wibblery', 'wob'],
    ...                    [['aabbcc', '', 'wob']])
    +--------+----------+-----+
    | wibble | wibblery | wob |
    +========+==========+=====+
    | aabbcc |          | wob |
    +--------+----------+-----+
    >>> print grid_table(['wibble', 'wib\nble\nry', 'wob'],
    ...                    [['aa\nbb\ncc\n', '', 'wob']])
    +--------+-----+-----+
    | wibble | wib | wob |
    |        | ble |     |
    |        | ry  |     |
    +========+=====+=====+
    | aa     |     | wob |
    | bb     |     |     |
    | cc     |     |     |
    |        |     |     |
    +--------+-----+-----+
    """
    _check_for_new_lines(header)  # hacky way to check for non-str things in the table
    _check_for_new_lines(list(itertools.chain.from_iterable(rows)))
    return _table(header, rows, '| ', ' | ', ' |', ' ',
                  '+=', '=+=', '=+', '=',
                  '+-', '-+-', '-+', '-')


def simple_table(header, rows):
    r"""Create a simple rst table.  header is a list of cells to go in
    the header row. rows is a list of list of cells for the body of the
    table.

    .. note :: If the cells might contain new lines then use :func:`grid_table`.

    >>> print simple_table(['wibble', 'wibblery', 'wob'],
    ...                    [['aabbcc', '', 1], ['short']])
    Traceback (most recent call last):
      ...
    ValueError: Cell(row=0, col=2) 1 is not a string.
    >>> print simple_table(['wibble', 'wibblery', 'wob'],
    ...                    [['aabbcc', '', 'wo'], ['short']])
    ====== ======== ===
    wibble wibblery wob
    ====== ======== ===
    aabbcc          wo
    short
    ====== ======== ===
    >>> print simple_table(['wibble', 'wib\nble\nry', 'wob'],
    ...                    [['aa\nbb\ncc\n', '', 'wob']])
    Traceback (most recent call last):
      ...
    ValueError: One or more cells contain new lines, this would produce invalid ReST
    """
    for row in rows:
        if row[0] == "":
            row[0] = "\\ "
    _check_for_new_lines(rows)
    if _check_for_new_lines([header]) or _check_for_new_lines([r[0] for r in rows]):
        raise ValueError("One or more cells contain new lines, this would produce invalid ReST")

    return _table(header, rows, '', ' ', '', ' ',
                         '', ' ', '', '=',
                         '', '', '', '', trim_ws=True)


def html_table(header, rows):
    r"""Create a html table, using the same parameter list as :func:`simple_table`.

    This is not really an rst function but it shares the same implementation as the
    other table creation functions.

        >>> print html_table(['wibble', 'wibblery', 'wob'],
        ...                    [['aabbcc', '', 'wob']])
        <table>
          <thead>
            <tr><th>wibble</th><th>wibblery</th><th>wob</th></tr>
          </thead>
          <tbody>
            <tr><td>aabbcc</td><td></td><td>wob</td></tr>
          </tbody>
        </table>

    .. note :: no html escaping of cell contents is performed.

    """
    return ("<table>\n" +
            _table(header, rows, '    <tr><td>', '</td><td>', '</td></tr>', '',
                   '  <thead>\n    <tr><th>', '</th><th>', '</th></tr>\n  </thead>\n  <tbody>', ' ',
                   '', '', '', '', process_new_lines=False)
            + "\n  </tbody>\n</table>")


def parse_simple_table(rst):
    r'''Parse a simple rst table.

    >>> parse_simple_table("""\
    ... ============== ======= ==========
    ... path           version flash_code
    ... ============== ======= ==========
    ... n705050700.fsh 5.5.7   37
    ... sp00050000.fsh 0.5.0   55
    ... ============== ======= ==========""")
    (['path', 'version', 'flash_code'], [['n705050700.fsh', '5.5.7', '37'], ['sp00050000.fsh', '0.5.0', '55']])
    '''
    regex = re.compile(r'''
        ^((?:=+\ )*=+$)\n
        ([^\n]*)\n
        ^((?:=+\ )*=+$)\n
        (.*)
        ^((?:=+\ )*=+$)
    ''', flags=re.MULTILINE | re.VERBOSE | re.DOTALL)
    m = regex.match(rst)
    headers = m.group(1, 3, 5)
    if not all(h == headers[0] for h in headers[1:]):
        print 'mismatched headers in rst output.'
    columns = [len(x) + 1 for x in re.findall('=+', headers[0])]
    rows = [m.group(2)] + m.group(4).splitlines()
    columns = [(sum(columns[:n]), sum(columns[:n]) + l - 1) for n, l in enumerate(columns)]
    cells = []
    for row in rows:
        cells.append([row[a:b].strip() for a, b in columns])
    return cells[0], cells[1:]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
