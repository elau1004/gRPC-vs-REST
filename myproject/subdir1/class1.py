from myproject import get_logger

class1_logger = get_logger()


class Class1:
    logger = get_logger()

    def __init__(self):
        Class1.logger.info(f"I am in {__name__} using the class  logger")
        class1_logger.info(f"I am in {__name__} using the module logger")
    
    def run(self):
        Class1.logger.error(f"I am running in {__name__}.run() using the class  logger")
        class1_logger.error(f"I am running in {__name__}.run() using the module logger")


# Sample output.
# --------------
# 20230616Fri 140239.576 (0a0000E0.23596)[INFO class1] I am in myproject.subdir1.class1 using the class  logger
# 20230616Fri 140239.576 (0a0000E0.23596)[INFO class1] I am in myproject.subdir1.class1 using the module logger
# 0230616Fri 140239.577 (0a0000E0.23596)[ERR  class1] I am running in myproject.subdir1.class1.run() using the class  logger
# 20230616Fri 140239.579 (0a0000E0.23596)[ERR  class1] I am running in myproject.subdir1.class1.run() using the module logger
