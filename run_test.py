import unittest
import tests.funct_test as ggwp

MainTestSuite = unittest.TestSuite()
MainTestSuite.addTest(unittest.makeSuite(ggwp.FunctionsTests))
# MainTestSuite.addTest(unittest.makeSuite(middleware_test.MiddlewareSaveTests))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(MainTestSuite)
