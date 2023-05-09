import threading

thread_ids = {}

def start(id, function):
    thread_ids[id] = {}
    thread_ids[id]["running"] = [True] # needed for python to pass by reference / not value, see https://stackoverflow.com/questions/3648473/python-how-to-pass-a-reference-to-a-function
    thread_ids[id]["thread"] = threading.Thread(target=function, args=(thread_ids[id]["running"],))
    thread_ids[id]["thread"].start()

def stop(id):
    thread_ids[id]["running"][0] = False # see above for container need
    thread_ids[id]["thread"].join()