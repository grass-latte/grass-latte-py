_port_range = (3030, 3035)
_port_range_used = False

def get_port_range():
    global _port_range_used
    _port_range_used = True
    return _port_range

def set_port_range(new_range: (int, int)):
    global _port_range
    if _port_range_used:
        raise Exception("Attempted to change port range after port range was accessed")
    _port_range = new_range