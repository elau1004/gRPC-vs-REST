from myproject import get_logger

class Class2:
    #Class level logger
    cl = get_logger()

    def __init__(self):
        self.cl.error(  f"Init: Class2.Clazz  level: The log file defaulted to 'class2'.")
        self.cl.info("")

    def run(self):
        rl = get_logger("clz2")
        rl.info(        f"Run:  Class2.Clazz  level: The log file defaulted to 'clz2'.")
        self.cl.warn(   f"Run:  Class2.Clazz  level: The log file defaulted to 'class2'.")
        self.cl.info("")


# Sample output.
# --------------
# 20230616Fri 154445.261 (0a0000E0.23484)[ERR  class2] Init: Class2.Clazz  level: The log file defaulted to 'class2'.
# 20230616Fri 154445.262 (0a0000E0.23484)[INFO class2]
# 20230616Fri 154445.262 (0a0000E0.23484)[INFO class2] Run:  Class2.Clazz  level: The log file defaulted to 'clz2'.
# 20230616Fri 154445.263 (0a0000E0.23484)[WARN class2] Run:  Class2.Clazz  level: The log file defaulted to 'class2'.
# 20230616Fri 154445.263 (0a0000E0.23484)[INFO class2]
