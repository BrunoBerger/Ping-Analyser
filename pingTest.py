import argparse
import time
import statistics

# from pythonping import ping
import pythonping
import matplotlib.pyplot as plt

# Progressbar from https://stackoverflow.com/a/34325723
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
    filename = time.strftime("PingTestResult_%d-%m-%Y_%Hh%Mm%Ss", time.localtime())
    plt.figure(filename)

    plt.xlim(0, len(pings))
    plt.plot(pings)
    ylabel = "Ping to {} in ms".format(args["adress"])
    plt.ylabel(ylabel)
    plt.xlabel("Pings, with a "+ str(args["interval"]) + "s interval")
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
    try:
        while time.time() <= timeout:
            response_list = pythonping.ping(args["adress"], size=40, count=1)
            pings.append(response_list.rtt_avg_ms)
            # Update Progress Bar
            timeleft = int((timeout - time.time())*100)
            printProgressBar(plannedTime-timeleft, plannedTime,
                             prefix = 'Progress:', suffix = 'Complete', length = 50)
            time.sleep(args["interval"])
        printProgressBar(plannedTime, plannedTime,
                         prefix = 'Progress:', suffix = 'Complete', length = 50)
    except KeyboardInterrupt:
        print("\nTest aborted")

    print("\nPinged", args["adress"], len(pings) , "times")
    print("Avarage ping: {:.2f}ms".format(statistics.mean(pings)))

    endT = time.time()
    print("Elapsed Time: {:.2f} seconds".format(endT-startT))
    plotData(args, pings)

# TODO: Make a list of std.-adresses available
if __name__ == "__main__":
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("-t", "--testTime", type=int, default=10,
                            help="Test duration in seconds")
        parser.add_argument("-i", "--interval", type=float, default=0.1,
                            help="Time between each ping")
        parser.add_argument("-a", "--adress", default='google.com',
                            help="Sever Adress")
        args = vars(parser.parse_args())
        main(args)
