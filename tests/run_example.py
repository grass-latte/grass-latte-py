import grass_latte
import time

grass_latte.set_port_range((3030, 3030))
grass_latte.serve_webpage()

time.sleep(1)

i = 0
while True:
    grass_latte.send_text(["a", "b", "c"], f"hello - {i}", True)
    time.sleep(1)
    i += 1