# play SRT file 
import sys
import time
import os

from kbhit import KBHit
import thread, threading
import datetime

import srtgetter


subtitles = []

class Subtitle(object):
    pass


def parse_time(timestr):
    tokens = timestr.split(",")
    ms = int(tokens[1])
    tokens = map(int,tokens[0].split(":"))
    
    return datetime.timedelta(
        hours=tokens[0],
        minutes=tokens[1],
        seconds=tokens[2],
        milliseconds=ms)


def read_subtitles(lines):
    lines.reverse()
    while lines:
        s = Subtitle()
        line = lines.pop()

        if not line.strip():
            continue

        id = int(line)
        s.id = id

        timing = lines.pop()
        # timing looks like:
        # 00:00:56,050 --> 00:00:57,558
        tokens = timing.split("-->")



        s.start = parse_time(tokens[0])
        s.end = parse_time(tokens[1])

        s.displayed = []
        while line.strip() != "" and lines:
            line = lines.pop()
            s.displayed.append(line)

        subtitles.append(s)

    return subtitles

def display_lines(sub):
    slept = 0

    for line in sub.displayed:
        line = line.strip()
        if not line:
            continue


        
        print "%04i" % sub.id,
        hours, remainder = divmod(sub.start.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print '%02i:%02i:%02i ' % (hours, minutes, seconds),

        sys.stdout.flush()
        if line[0] == "'":
            line = "[%s]" % (line.strip("'"))

        words = line.split()

        for word in words:
            sys.stdout.write(word)
            sys.stdout.write(" ")
            sys.stdout.flush()
            # 110 baud:
            if not RESET:
                time.sleep( 4./110 )
                slept += 4./110

        sys.stdout.write("\n")
    return slept


OVER = False
RESET = False
PAUSE = False
SUB_ID = 0
def subtitle_runner(subs):
    global SUB_ID, RESET
    cur = datetime.timedelta(0)

    incr = 0.05

    last_call = time.time()
    while SUB_ID < len(subs) and not OVER:
        RESET = False

        sub = subs[SUB_ID]
        display_in = sub.start - cur
        display_at = time.time() + display_in.seconds
        time_left = 1
        while time_left > 0 and not RESET:
            t = time.time()
            delta = t - last_call
            time_left = display_at - t
            last_call = t

            suf = "         "
            if PAUSE:
                display_at += delta
                suf = " (paused)"

            print "t-%02i%s" % (time_left, suf),
            sys.stdout.flush()
            time.sleep(incr)
            sys.stdout.write("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
            sys.stdout.flush()

        if OVER:
            break

        if RESET:
            cur = subs[SUB_ID].start
            continue

        cur = sub.start
        cur += datetime.timedelta(seconds=display_lines(sub))
        SUB_ID += 1

    if not OVER:
        thread.interrupt_main()

def incr_subtitle(amt):
    global SUB_ID, RESET
    SUB_ID += amt

    RESET = True
    if SUB_ID <= 0:
        SUB_ID = 0

escape_handlers = {
    0: lambda: incr_subtitle(5),
    1: lambda: incr_subtitle(-5),
    2: lambda: incr_subtitle(0),
    3: lambda: incr_subtitle(-2)
}
def handle_escape_code(c, d):
    if c == "[":
    # up, right, down, left
    # 'A', 'C', 'B', 'D'
    # 0, 2, 1, 3
        o = ord(d) - ord('A')
        if o in escape_handlers:
            escape_handlers[o]()




    
def _main():
    global OVER, RESET,PAUSE
    if len(sys.argv) < 2:
        bin_path = os.path.normpath(sys.argv[0])
        print("Please supply a query on the command line: %s [query terms] [language]" % bin_path)
        print("ex: %s law and order svu 01x01 english" % bin_path)
        sys.exit(0)

    lines = srtgetter.run_query(*sys.argv[1:])
    subs = read_subtitles(lines)

    print('Hit any key, or q to exit')

    t = threading.Thread(target=subtitle_runner, args=[subs])
    t.start()

    kb = KBHit()



    p = None

    
    try:
	while True:
	    if kb.kbhit():
		c = kb.getch()
                if c == 'q':
                    break

                if ord(c) == 27: # ESC
                    c = kb.getch()
                    d = kb.getch()
                  
                    handle_escape_code(c, d)

                if c == ' ':
                    PAUSE = not PAUSE

            time.sleep(0.05)
    except Exception, e:
        print "EXCEPTION", e
    finally:
        RESET=True
        OVER=True

class CursorOff(object):
    def __enter__(self):
        os.system('setterm -cursor off')
         
    def __exit__(self, *args):
        os.system('setterm -cursor on')


def main():
    with CursorOff():
        _main()
