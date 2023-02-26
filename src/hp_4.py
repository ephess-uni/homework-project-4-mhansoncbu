# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict
from pathlib import Path


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    format_string_old = '%Y-%m-%d'
    format_string_new = '%d %b %Y'
    dates_old = [datetime.strptime(date, format_string_old)for date in old_dates]
    dates_new = [datetime.strftime(date, format_string_new) for date in dates_old]
    return dates_new
      
def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if isinstance(start, str) == False:
        raise TypeError('start is not a string.')
    if isinstance(n, int) == False:
        raise TypeError('n is not an integer.')
    start_date_object = datetime.fromisoformat(start)
    date_list = list()
    for x in range(n):
        add_day = timedelta(days=+x)
        next_day = start_date_object + add_day
        date_list.append(next_day)
    return date_list

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    dates_to_add = date_range(start_date, len(values))
    dates_and_values = zip(dates_to_add, values)
    return list(dates_and_values)
        
def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""

    book_dict = defaultdict(list)
    format_book_date = '%m/%d/%Y'
    
    with open(infile) as book_file:
        reader = DictReader(book_file)
        book_list = [row for row in reader]
        for record in book_list:
            date_due_object = datetime.strptime(record['date_due'], format_book_date) 
            date_returned_object = datetime.strptime(record['date_returned'], format_book_date)
            days_overdue_object = date_returned_object - date_due_object
            days_overdue = int(days_overdue_object.days)
            if days_overdue > 0:
                charges = days_overdue * .25
            else: charges = 0
            record['fine'] = charges
            book_dict[record['patron_id']].append(record['fine'])
        book_dict_not_default = dict(book_dict)
        book_fees = list()
        book_fees = [{'patron_id': patron, 'late_fees': '{:.2f}'.format(sum(fines))} for patron, fines in book_dict_not_default.items()]
           
    file_path = Path(outfile)
    file = file_path.open(mode = 'w')
    writer = DictWriter(file, fieldnames = ['patron_id', 'late_fees'])
    writer.writeheader()
    writer.writerows(book_fees)
    file.close()
 
# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
