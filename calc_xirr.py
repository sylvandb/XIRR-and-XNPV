#!/usr/bin/env python3

import datetime
import sys
from xirr import xirr



VALIDNUMBER = '1234567890.-'


cashflows = []

def read_flows():
    while True:
        l = sys.stdin.readline()
        if not l:
            print("EOF.")
            break
        l = l.strip()
        if l == '.':
            print("End.")
            break
        cashflows.append(l)


def parse_flows():
    dates = []
    flows = []
    for l in cashflows:
        while l:
            try:
                l = l.split()
            except AttributeError:
                pass
            date, flow = l[:2]
            l = l[2:]
            # print(date, flow, l)

            try:
                if len(date) == 8:
                    year = int(date[0:4])
                    month = int(date[4:6])
                    day = int(date[6:8])
                elif len(date) == 10:
                    year = int(date[0:4])
                    month = int(date[5:7])
                    day = int(date[8:10])
                else:
                    raise ValueError("Date wrong length %d not YYYYMMDD" % (len(date),))
                dates.append(datetime.date(year, month, day))
            except (ValueError, TypeError) as e:
                print("Not valid date, {YYYYMMDD} {amount}: %s %s\n%s" % (date, flow, e))
                continue

            try:
                flows.append(float(''.join(f for f in flow if f in VALIDNUMBER)))
            except (ValueError, TypeError) as e:
                print("Not valid amount, {YYYYMMDD} {amount}: %s %s\n%s" % (date, flow, e))
                del date[-1]
                continue

    del cashflows[:]
    cashflows.extend(zip(dates, flows))
    return bool(cashflows)




def main(argv=None):

    if argv:
        cashflows.append(' '.join(argv))
    else:
        read_flows()
    if not parse_flows():
        return 1

    print('\n------ Cashflow ------')
    fmt = '%s %0.2f' if any(not f == int(f) for d, f in cashflows) else '%s %d'
    for d, f in cashflows:
        print(fmt % (d, f))
    print('----------------------')
    print('%d flows' % (len(cashflows),))
    print('----------------------')

    print('xIRR: %0.2f%%' % (100 * xirr(cashflows),))

    return 0


if __name__ == '__main__':
    usage = """
    Enter cashflow series of {date} {amount} ...
      {date}: YYYYMMDD - a 4 digit Year (YYYY), 2 digit Month (MM), and 2 digit Day (DD)
         so that 2 October 2019 would be: 20191002
      {amount}: negative for deposit, positive for withdrawals
    will read until End of File or a '.' as the only character on a line."""

    if '-h' in sys.argv or '--help' in sys.argv:
        print(usage)
        sys.exit(0)

    if '--hack' in sys.argv:
        sys.argv.remove('--hack')
        xirr.DO_HACK = True

    if '--nohack' in sys.argv:
        sys.argv.remove('--nohack')
        xirr.DO_HACK = False

    if sys.argv[1:]:
        if main(sys.argv[1:]):
            print(usage)
            sys.exit(1)
    else:
        print(usage)
        sys.exit(main())
