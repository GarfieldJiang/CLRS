import unittest


def seam_carve(disruptivity_image):
    """
    DP algorithm to calculate the seam to carve from the original image for the optimal compression.
    :param disruptivity_image: disruptivity values of each pixel of the original image.
    :return: optimal disruptivity value of the seam plus the seam itself.
    """

    m = len(disruptivity_image)
    n = len(disruptivity_image[0])
    for row in disruptivity_image:
        assert len(row) == n, 'Image must be rectangular'
        for disruptivity in row:
            assert isinstance(disruptivity, int) or isinstance(disruptivity, float), 'Disruptivity must be int or float'

    opt_disruptivities = [[float('inf') for _ in xrange(0, n + 2)] for _ in xrange(0, m)]

    for j in xrange(0, n):
        opt_disruptivities[m - 1][j + 1] = disruptivity_image[m - 1][j]

    for i in xrange(m - 2, -1, -1):
        for j in xrange(0, n):
            opt_disruptivities[i][j + 1] = disruptivity_image[i][j] + min(
                opt_disruptivities[i + 1][j], opt_disruptivities[i + 1][j + 1], opt_disruptivities[i + 1][j + 2]
            )

    start_j = -1
    opt_disruptivity = float('inf')
    for j in xrange(0, n):
        if opt_disruptivities[0][j + 1] < opt_disruptivity:
            start_j = j
            opt_disruptivity = opt_disruptivities[0][j + 1]

    opt_seam = [start_j]
    for i in xrange(0, m - 1):
        for j in (start_j - 1, start_j, start_j + 1):
            if opt_disruptivities[i][start_j + 1] == disruptivity_image[i][start_j] + opt_disruptivities[i + 1][j + 1]:
                start_j = j
                opt_seam.append(j)
                break

    return opt_disruptivity, tuple(opt_seam)


class TestSeamCarving(unittest.TestCase):
    def test_seam_carving(self):
        cases = (
            (
                '1x1', ((1,),), 1, (0,)
            ),
            (
                '2x2 #0',
                (
                    (1, 2),
                    (2, 1),
                ),
                2, (0, 1),
            ),
            (
                '2x2 #1',
                (
                    (2, 1),
                    (1, 2),
                ),
                2, (1, 0),
            ),
            (
                '3x3 Simple',
                (
                    (1, 2, 3),
                    (3, 1, 2),
                    (1, 3, 2),
                ),
                3, (0, 1, 0),
            ),
            (
                '3x3 Not that simple',
                (
                    (2, 1, 3),
                    (1, 2, 3),
                    (3, 2, 1),
                ),
                4, (1, 0, 1),
            ),
            (
                '3x5',
                (
                    (4, 2, 3, 1, 5),
                    (5, 4, 1, 2, 3),
                    (5, 1, 2, 3, 4),
                ),
                3, (3, 2, 1),
            ),
            (
                '3x1',
                (
                    (100,),
                    (200,),
                    (300,),
                ),
                600, (0, 0, 0),
            ),
        )

        for desc, disruptivity_image, expected_disruptivity, expected_seam in cases:
            disruptivity, seam = seam_carve(disruptivity_image)
            self.assertAlmostEqual(disruptivity, expected_disruptivity,
                                   msg='%s, disruptivity %.2f != %.2f' % (desc, disruptivity, expected_disruptivity))
            self.assertEqual(seam, expected_seam,
                             msg='%s, seam %s != %s' % (desc, seam, expected_seam))
