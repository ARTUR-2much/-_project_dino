import unittest
import DinoGame as Dng


class FunctionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nTest of functions")
        print("=======================================")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_collusion(self):
        # """Test collusion function."""
        # Run into small cactus
        cactus_arr = [Dng.Object(Dng.usr_x, 449, 64, None, 5),
                      Dng.Object(300, 449, 64, None, 5),
                      Dng.Object(600, 449, 64, None, 5)]
        self.assertTrue(Dng.check_collision(cactus_arr))

        cactus_arr = [Dng.Object(Dng.usr_x + 50, 449, 64, None, 5),
                      Dng.Object(300, 449, 64, None, 5),
                      Dng.Object(600, 449, 64, None, 5)]
        self.assertFalse(Dng.check_collision(cactus_arr))

        cactus_arr = [Dng.Object(Dng.usr_x + 50, 410, 37, None, 5),
                      Dng.Object(300, 410, 37, None, 5),
                      Dng.Object(600, 410, 37, None, 5)]
        self.assertFalse(Dng.check_collision(cactus_arr))

        cactus_arr = [Dng.Object(Dng.usr_x + 50, 420, 40, None, 5),
                      Dng.Object(300, 420, 40, None, 5),
                      Dng.Object(600, 420, 40, None, 5)]
        self.assertFalse(Dng.check_collision(cactus_arr))

    def test_health(self):
        # """Test check_health function."""
        Dng.health = 5

        self.assertTrue(Dng.check_health())
        self.assertEqual(4, Dng.health)

        Dng.health = 1
        self.assertFalse(Dng.check_health())

    # @unittest.skip("Skipping Jumps")
    def test_jump(self):
        # """Test jump() func."""
        jump_tries = {
            30: 400.0, 29: 388.0, 28: 376.4, 27: 365.2, 26: 354.4,
            25: 344.0, 24: 334.0, 23: 324.4, 22: 315.2, 21: 306.4,
            20: 298.0, 19: 290.0, 18: 282.4, 17: 275.2, 16: 268.4,
            15: 262.0, 14: 256.0, 13: 250.4, 12: 245.20000000000002, 11: 240.4,
            10: 236.0, 9: 232.0, 8: 228.4, 7: 225.20000000000002, 6: 222.4,
            5: 220.0, 4: 218.0, 3: 216.4, 2: 215.20000000000002, 1: 214.4,
            0: 214.0, -1: 214.0, -2: 214.4, -3: 215.20000000000002, -4: 216.4,
            -5: 218.0, -6: 220.0, -7: 222.4, -8: 225.20000000000002, -9: 228.4,
            -10: 232.0, -11: 236.0, -12: 240.4, -13: 245.20000000000002,
            -14: 250.4,
            -15: 256.0, -16: 262.0, -17: 268.4, -18: 275.2, -19: 282.4,
            -20: 290.0, -21: 298.0, -22: 306.4, -23: 315.2, -24: 324.4,
            -25: 334.0, -26: 344.0, -27: 354.4, -28: 365.2, -29: 376.4,
            -30: 388.0, -31: 400.0
        }

        while Dng.make_jump:
            Dng.jump()
            self.assertEqual(jump_tries[Dng.jump_counter], Dng.usr_y)
            test_a = Dng.usr_y + 10
            self.assertNotEqual(jump_tries[Dng.jump_counter], test_a)

    def test_scores(self):
        # """ Test scores count """

        Dng.scores = 4
        Dng.usr_y = 214
        Dng.jump_counter = -30
        cactus_arr = [Dng.Object(Dng.usr_x - 20, 449, 64, None, 5),
                      Dng.Object(300, 449, 64, None, 5),
                      Dng.Object(600, 449, 64, None, 5)]
        Dng.count_scores(cactus_arr)
        self.assertEqual(6, Dng.scores)
