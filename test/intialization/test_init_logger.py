# The script is to test the behavor of our gloabl config, CaseInsensitiveDict, get_logger() method.
#
from  myproject import CaseInsensitiveDict as cidict

cid = cidict()
cid[ 1 ] = '123456'
print(f"cid[ 1 ] is {cid[ 1 ]}")
cid[ 1 ] = 'abcdef'
print(f"cid[ 1 ] is {cid[ 1 ]}")
cid['a'] = 'aAbBcB'
print(f"cid['a'] is {cid['a']}")
cid['A'] = '123345'
print(f"cid['a'] is {cid['a']}")
print(f"cid['A'] is {cid['a']}")

if 'A' in cid:
    print(f"'A' is     in cid.")
else:
    print(f"'A' is NOT in cid.")

cid['b'] = 'xyz'
if 'B' in cid:
    print(f"'B' is     in cid.")
    cid.pop('B')
if 'B' not in cid:
    print(f"'B' is NOT in cid.")

# Sample output.
# --------------
# cid[ 1 ] is 123456
# cid[ 1 ] is abcdef
# cid['a'] is aAbBcB
# cid['a'] is 123345
# cid['A'] is 123345
# 'A' is     in cid.
# 'B' is     in cid.
# 'B' is NOT in cid.


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
