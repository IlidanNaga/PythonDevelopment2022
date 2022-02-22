from figdate import date

import sys
import locale


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "RU_ru")
    
    if sys.argv.__len__() == 2:
        print(date(format=sys.argv[1]))
    
    elif sys.argv.__len__() > 2:
        print(date(format=sys.argv[1], font=sys.argv[2]))

    else:
        print(date())

    