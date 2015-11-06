from queue_manager import QueueServer


if __name__ == "__main__":
    m = QueueServer()
    s = m.get_server()
    s.serve_forever()