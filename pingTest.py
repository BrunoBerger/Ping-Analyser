import argparse
import time
import statistics

from pythonping import ping
import matplotlib.pyplot as plt

# Progressbar from https://stackoverflow.com/a/34325723
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : positive number of decimals in percent complete (Int)
    length      - Optional  : character length of bar (Int)
    fill        - Optional  : bar fill character (Str)
    printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

# TODO: add more stuff
def plotData(args, pings):
    plt.xlim(0, len(pings))
    plt.plot(pings)
    plt.ylabel("Ping to: " + args["adress"]+"/ms")
    plt.xlabel("Pings")
    plt.show()

def main(args):
    # Measurement to get when to stop and completion%
    # multiply to get finer completion percentage
    startT = time.time()
    timeout = time.time() + args["testTime"]
    plannedTime = args["testTime"]*100
    printProgressBar(0, plannedTime,
                     prefix = 'Progress:', suffix = 'Complete', length = 50)

    pings = []
    while time.time() <= timeout:
        response_list = ping(args["adress"], size=40, count=1)
        pings.append(response_list.rtt_avg_ms)
        # Update Progress Bar
        timeleft = int((timeout - time.time())*100)
        printProgressBar(plannedTime-timeleft, plannedTime,
                         prefix = 'Progress:', suffix = 'Complete', length = 50)
        time.sleep(args["interval"])

    print("Pinged", args["adress"], len(pings) , "times")
    print("Avarage ping: {:.2f}ms".format(statistics.mean(pings)))

    endT = time.time()
    print("Elapsed Time: {:.2f} seconds".format(endT-startT))
    plotData(args, pings)

if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--testTime", type=int, default=10,
                            help="Test-time in seconds")
        parser.add_argument("-i", "--interval", type=float, default=0.1,
                            help="time between each ping")
        parser.add_argument("-a", "--adress", default='google.com',
                            help="Sever Adress")
        args = vars(parser.parse_args())
        main(args)
