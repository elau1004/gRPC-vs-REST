from myproject import get_logger

# class2_logger = get_logger()


class Class2:
    logger = get_logger()

    def __init__(self):
        Class2.logger.info(f"I am in {__name__} using the class  logger")
    
    def run(self):
        Class2.logger.warn(f"I am running in {__name__}.run() using the class  logger")


# Sample output.
# --------------
# 20230615Thu 211441.939 (23540.14528)[INFO class2] I am in myproject.subdir1.subdir2.class2 using the class  logger
# 20230615Thu 211441.940 (23540.14528)[WARN class2] I am running in myproject.subdir1.subdir2.class2.run() using the class  logger  