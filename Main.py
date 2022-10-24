import urllib.request, sched, time, logging, config
from datetime import date
from concurrent.futures import ThreadPoolExecutor


def schedule(t):
    """Creates a scheduler that calls our get() function at a specified time t.

    :param t: the time in which to execute get()
    :type t: floating point number
    :return: None
    """

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enterabs(t, 0, get)
    scheduler.run()
    return


def get():
    """Sends a request to the URL specified in config.py and logs the response.

    :return: None
    """

    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    request = urllib.request.Request(url = config.URL, headers = header)
    response = urllib.request.urlopen(request).read()
    logging.info(response)
    return


if __name__ == "__main__":
    """First gets the input from CLI as a list and creates a ThreadPoolExecutor().
    Iterates through the timestamps and uses the ThreadPoolExecutor to schedule each request.
    This ensures that if there are duplicate time stamps that they are executed at the same time.
    """

    logging.basicConfig(filename = 'log.txt', encoding = 'utf-8', level = logging.DEBUG)
    executor = ThreadPoolExecutor()

    time_list = input("Timestamps: ").split(',')
    time_list.sort()
    today = date.today()
    todayString = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + " "

    for timeString in time_list:
        timeString = todayString + timeString
        try:
            t = time.mktime(time.strptime(timeString, "%Y-%m-%d %H:%M:%S"))
        except:
            logging.error("Error with CLI input, skipping this timestamp: " + timeString)
            continue
        logging.info(timeString)
        executor.submit(schedule, t)
