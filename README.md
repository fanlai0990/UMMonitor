Requirement
=====================
1. Make sure that you've implemented the Python 2.7, and successfully add the path to the environment. For more details, please check:
https://www.cnblogs.com/dangeal/p/5455005.html

2. Please record the path of document, e.g., C:/user/local/UMHousing. In the rest of this README, we denote this Path as PATH.

Install
=====================
(1) open cmd

(2) type in: git clone git@github.com:fanlai0990/UMMonitor.git

(3) type in: cd UMMonitor

(4) type in: python pre_install.py

Then it will automatically download the dependency for you. Please note that you only need install all the dependency once.

Configuration
=====================
Please config the following part in "HousingMonitor.py":

    payload = {
        'fld28053': 'Unfurnished',  # Furnishings: {Furnished, Unfurnished}
        'fld28051': 'August 16',  # Contract start date: {July 1, July 16, August 1, August 16, September 1, September 16}
        'dateflddtArrival': '8/1/2018',  # Arrival date: %-m/%-d/%Y (e.g., 8/15/2017)
        'dateValueflddtArrival': '',
        'fldFunction': 6952,
        'btnSubmit': 'Search',
        'fld28052': 49,
        #'chkRoommate134660':'on' 
    }
Current version doesn't support the roommate selection.

Start Searching
=====================

(1) open cmd

(2) type in: cd PATH

(3) type in: python HousingMonitor.py

PS: please note that the current codes use my email as the sender, but this will be stale soon. Instead, you should use your own email to replace the current one. i.e., line 40 in HousingMonitor.py and the corresponding validation codes (line 41).
