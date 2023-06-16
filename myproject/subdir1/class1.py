from myproject import get_logger

# Module level logger
ml = get_logger()
ml.info(f"Class1.Module level: The log file defaulted to 'class1' for its filename just as above.")
ml.info("")


class Class1:
    #Class level logger
    cl = get_logger()

    def __init__(self):
        ml.info(        f"Init: Class1.Module level: The log file defaulted to 'class1'.")
        self.cl.error(  f"Init: Class1.Clazz  level: The log file defaulted to 'class1'.")
        self.cl.info("")

    def run(self):
        rl = get_logger("clz1")
        ml.info(        f"Run:  Class1.Module level: The log file defaulted to 'class1'.")
        rl.info(        f"Run:  Class1.Clazz  level: The log file defaulted to 'clz1'.")
        self.cl.warn(   f"Run:  Class1.Clazz  level: The log file defaulted to 'class1'.")
        self.cl.info("")


# Sample output.
# --------------
# 20230616Fri 154445.252 (0a0000E0.23484)[INFO class1] Class1.Module level: The log file defaulted to 'class1' for its filename just as above.
# 20230616Fri 154445.253 (0a0000E0.23484)[INFO class1] 
# 20230616Fri 154445.254 (0a0000E0.23484)[INFO class1] Init: Class1.Module level: The log file defaulted to 'class1'.
# 20230616Fri 154445.254 (0a0000E0.23484)[ERR  class1] Init: Class1.Clazz  level: The log file defaulted to 'class1'.
# 20230616Fri 154445.255 (0a0000E0.23484)[INFO class1] 
# 20230616Fri 154445.256 (0a0000E0.23484)[INFO class1] Run:  Class1.Module level: The log file defaulted to 'class1'.
# 20230616Fri 154445.256 (0a0000E0.23484)[INFO class1] Run:  Class1.Clazz  level: The log file defaulted to 'clz1'.
# 20230616Fri 154445.257 (0a0000E0.23484)[WARN class1] Run:  Class1.Clazz  level: The log file defaulted to 'class1'.
# 20230616Fri 154445.257 (0a0000E0.23484)[INFO class1]
