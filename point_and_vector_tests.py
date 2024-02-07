import unittest

loader = unittest.TestLoader()

# Discover all test files
all_tests = loader.discover('unit_tests', pattern='test_*.py')

# Filter out unwanted test files
selected_tests = unittest.TestSuite()
#print(all_tests)
print('-------------------')
for test in all_tests:
    #print(test)
    if test._tests[0]._tests[0].__class__.__name__ in ['PointTest', 'VectorTest']:
        print(test._tests[0]._tests[0].__class__.__name__)
        selected_tests.addTest(test)

# Run the selected tests
runner = unittest.TextTestRunner()
runner.run(selected_tests)


