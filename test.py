import myproject
l = myproject.get_logger()
l.info(f"I am in {__name__} 1")


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
# 20230615Thu 211430.252 (23540.14528)[INFO __init__] Environment is to be configured for 'dev'.
# 20230615Thu 212237.726 (16200.12888)[INFO test] I am in __main__ 1
# 20230615Thu 212237.727 (16200.12888)[INFO test] I am in __main__ 2
# 20230615Thu 212237.727 (16200.12888)[INFO test] I am in __main__ 2
