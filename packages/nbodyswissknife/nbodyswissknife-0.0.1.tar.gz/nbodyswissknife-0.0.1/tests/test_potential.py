# coding=utf-8
"""test suite for testing the potential module"""
import numpy
import nbodyswissknife


def test_single_particle_potential_at_the_origin():

    pot = nbodyswissknife.potential.potential_native(
        coords=numpy.array([0.0, 0.0, 0.0]).reshape(3, 1),
        mass=1.0,
        soft=0.0,
        gauss=1.0,
        location=numpy.array([1.0, 0.0, 0.0])
    )

    pot_expected = - 1.0
    numpy.testing.assert_allclose(pot, pot_expected, rtol=1.0e-16)


def test_single_particle_potential_with_softening():

    pot = nbodyswissknife.potential.potential_native(
        coords=numpy.array([0.0, 0.0, 0.0]).reshape(3, 1),
        mass=1.0,
        soft=1.0,
        gauss=1.0,
        location=numpy.array([1.0, 0.0, 0.0])
    )

    pot_expected = - 1.0 / numpy.sqrt(2.0)
    numpy.testing.assert_allclose(pot, pot_expected, rtol=1.0e-16)


def test_potential_many_paricles_at_the_origin():
    n_part = 50

    origin = [3.1, -4.1, 0.23]
    mass = 0.2
    soft = 0.1
    gauss = 2.1
    r_loc = [1.0, 2.0, 3.0]

    pot = nbodyswissknife.potential.potential_native(
        coords=numpy.repeat(origin, n_part).reshape(3, n_part),
        mass=numpy.ones(n_part, 'f8')*mass,
        soft=soft,
        gauss=gauss,
        location=r_loc
    )

    pot_expected = - n_part * gauss * mass / numpy.sqrt(
        (origin[0] - r_loc[0]) ** 2 +
        (origin[1] - r_loc[1]) ** 2 +
        (origin[2] - r_loc[2]) ** 2 +
        soft**2
    )

    numpy.testing.assert_allclose(
        pot,
        pot_expected,
        rtol=1.0e-6,
        atol=0.0,
        verbose=True
    )


def test_that_potential_native_and_potential_cpu_agree():

    n = 1000
    b = 5.3
    G = 8.22
    r_loc = numpy.array([1.0, 2.0, 3.0]).reshape(3, 1)

    m = numpy.random.rand(n)
    x = numpy.random.rand(n)
    y = numpy.random.rand(n)
    z = numpy.random.rand(n)

    pot_native = nbodyswissknife.potential.potential_native(
        numpy.vstack((x, y, z)),
        m,
        soft=b,
        gauss=G,
        location=r_loc,
    )

    pot_cpu = nbodyswissknife.potential_cpu.potential(
        x, y, z,
        m,
        b,
        G,
        r_loc,
    )

    numpy.testing.assert_allclose(
        pot_cpu,
        pot_native,
        rtol=1.0e-14
    )


def test_that_potential_cpu_at_multiple_locations_is_computed_correctly():

    n = 100
    b = 5.3
    G = 8.22

    m = numpy.random.rand(n)
    x = numpy.random.rand(n)
    y = numpy.random.rand(n)
    z = numpy.random.rand(n)

    locations = numpy.meshgrid(
        numpy.linspace(-numpy.random.rand(), numpy.random.rand(), 5),
        numpy.linspace(-numpy.random.rand(), numpy.random.rand(), 8),
        numpy.linspace(-numpy.random.rand(), numpy.random.rand(), 3),
    )

    pot = numpy.zeros_like(locations[0]).flatten()

    nbodyswissknife.potential_cpu.potential_multiple_locations(
        x, y, z,
        m,
        b,
        G,
        locations[0].flatten(),
        locations[1].flatten(),
        locations[2].flatten(),
        pot
    )
    pot = pot.reshape(locations[0].shape)

    for pot_cpu, loc in zip(pot.flatten(),
                            numpy.vstack((locations[0].flatten(),
                                          locations[1].flatten(),
                                          locations[2].flatten())).T):

        pot_native = nbodyswissknife.potential.potential_native(
            numpy.vstack((x, y, z)),
            m,
            soft=b,
            gauss=G,
            location=loc,
        )

        numpy.testing.assert_allclose(
            pot_cpu,
            pot_native,
            rtol=1.0e-14
        )
        # print('{:e}\n{:e}\n{:e}\n----------'.format(
        #     pot_cpu,
        #     pot_native,
        #     1.0 - pot_cpu / pot_native)
        # )
