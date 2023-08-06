class ListenPool(object):

    def __init__(self):
        self.listeners = []

    def deploy_listener(self, listener, sleep_time=5):
        listener.mount()
        listener.run(sleep_time=sleep_time)
        self.listeners.append(listener)
