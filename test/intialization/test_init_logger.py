# The script is to test the behavor of our gloabl get_logger() method.
#
import sys

import myproject
l1 = myproject.get_logger()
l1.info(f"'__name__' is this script is {__name__}")
l1.info(f"The log file defaulted to 'test_init_logger' for its filename.")
l1.info(f"Environment is configured for '{myproject.config['env']}'.")
l1.info("")


# The following output a duplicated line.
from myproject import get_logger
get_logger().info(f"The log file defaulted to 'test_init_logger' for its filename just as above.")
l1.info("")


# Get another logger.
l2 = myproject.get_logger( "second_logger" )
l2.info(f"The log file defaulted to 'second_logger'    for its filename.")
l2.info("")


# Get another logger.
l2 = myproject.get_logger( myproject.__name__ )
l2.info(f"The log file defaulted to '{myproject.__app__:16}  for its filename.")
l2.info("")


# See what other class behave.
from myproject.subdir1.class1 import Class1
c1 = Class1()
c1.run()


from myproject.subdir1.subdir2.class2 import Class2
c2 = Class2()
c2.run()

pass

# Sample output.
# --------------
# 20230616Fri 154445.244 (0a0000E0.23484)[INFO test_init_logger] '__name__' is this script is __main__
# 20230616Fri 154445.244 (0a0000E0.23484)[INFO test_init_logger] The log file defaulted to 'test_init_logger' for its filename.
# 20230616Fri 154445.244 (0a0000E0.23484)[INFO test_init_logger] Environment is configured for 'dev'.
# 20230616Fri 154445.244 (0a0000E0.23484)[INFO test_init_logger] 
# 20230616Fri 154445.244 (0a0000E0.23484)[INFO test_init_logger] The log file defaulted to 'test_init_logger' for its filename just as above.
# 20230616Fri 154445.244 (0a0000E0.23484)[INFO test_init_logger] 
# 20230616Fri 154445.245 (0a0000E0.23484)[INFO test_init_logger] The log file defaulted to 'second_logger'    for its filename.
# 20230616Fri 154445.245 (0a0000E0.23484)[INFO test_init_logger] 
# 20230616Fri 154445.246 (0a0000E0.23484)[INFO test_init_logger] The log file defaulted to 'myproject         for its filename.
# 20230616Fri 154445.248 (0a0000E0.23484)[INFO test_init_logger] 
