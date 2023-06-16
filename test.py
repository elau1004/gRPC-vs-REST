import myproject
l1 = myproject.get_logger()
l1.info(f"I am in {__name__} 1")


# The following output a duplicated line.
from myproject import get_logger
get_logger().info(f"I am in {__name__} 2")


from myproject.subdir1.class1 import Class1
c1 = Class1()
c1.run()


from myproject.subdir1.subdir2.class2 import Class2
c2 = Class2()
c2.run()

pass

# Sample output.
# --------------
# 20230616Fri 140237.324 (0a0000E0.23596)[INFO __init__] Environment is to be configured for 'dev'.
# 20230616Fri 140239.572 (0a0000E0.23596)[INFO test] I am in __main__ 1
# 20230616Fri 140239.572 (0a0000E0.23596)[INFO test] I am in __main__ 2
