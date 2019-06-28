import posidonius
import numpy as np
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('output_filename', action='store', help='Filename where the initial snapshot will be stored (e.g., universe_integrator.json)')

    args = parser.parse_args()
    filename = args.output_filename
    #filename = posidonius.constants.BASE_DIR+"target/example.json"

    initial_time = 1.0e6*365.25 # time [days] where simulation starts
    time_step = 0.08 # days
    #time_limit   = 4*time_step # days
    time_limit   = 365.25 * 1.0e7 # days
    historic_snapshot_period = 100.*365.25 # days
    recovery_snapshot_period = 100.*historic_snapshot_period # days
    consider_tides = True
    consider_type_two_migration = True
    consider_rotational_flattening = False
    consider_general_relativity = False
    #consider_general_relativity = "Kidder1995" # Assumes one central massive body
    #consider_general_relativity = "Anderson1975" # Assumes one central massive body
    #consider_general_relativity = "Newhall1983" # Considers all bodies
    universe = posidonius.Universe(initial_time, time_limit, time_step, recovery_snapshot_period, historic_snapshot_period, consider_tides, consider_type_two_migration, consider_rotational_flattening, consider_general_relativity)

    star_mass = 1.0 # Solar masses
    star_radius_factor = 1.0
    star_radius = star_radius_factor * posidonius.constants.R_SUN

    star_dissipation_factor = 4.992*3.845764e-2 # -66+64
    star_dissipation_factor_scale = 1.0
    star_radius_of_gyration_2 = 5.9e-2 # Sun
    star_love_number = 0.03
    star_fluid_love_number = star_love_number
    star_disk_inner_edge_distance = 0.0
    star_disk_outer_edge_distance = 0.0
    star_disk_lifetime = 0.0
    star_alpha_disk = 0.0
    star_disk_surface_density_normalization = 0.0
    star_disk_mean_molecular_weight =  0.0
    #star_type_two_migration_time = 0. # days
    #star_type_two_migration_inner_disk_edge_distance = 0.0 # AU
    star_position = posidonius.Axes(0., 0., 0.)
    star_velocity = posidonius.Axes(0., 0., 0.)

    # Initialization of stellar spin
    star_rotation_period = 24.0 # hours
    star_angular_frequency = posidonius.constants.TWO_PI/(star_rotation_period/24.) # days^-1
    star_spin = posidonius.Axes(0., 0., star_angular_frequency)
    star_evolution_type = posidonius.GalletBolmont2017(star_mass) # mass = 0.30 .. 1.40
    #star_evolution_type = posidonius.BolmontMathis2016(star_mass) # mass = 0.40 .. 1.40
    #star_evolution_type = posidonius.Baraffe2015(star_mass) # mass = 0.01 .. 1.40
    #star_evolution_type = posidonius.Leconte2011(star_mass) # mass = 0.01 .. 0.08
    #star_evolution_type = posidonius.Baraffe1998(star_mass) # Sun (mass = 1.0) or M-Dwarf (mass = 0.1)
    #star_evolution_type = posidonius.LeconteChabrier2013() # Jupiter
    #star_evolution_type = posidonius.LeconteChabrier2013dissip() # Jupiter with dynamical tide dissipation as in BolmontMathis2016 and GalletBolmont2017
    #star_evolution_type = posidonius.NonEvolving()
    universe.add_particle(star_mass, star_radius, star_dissipation_factor, star_dissipation_factor_scale, star_radius_of_gyration_2, star_love_number, star_fluid_love_number \
                          , star_disk_inner_edge_distance, star_disk_outer_edge_distance, star_disk_lifetime, star_alpha_disk, star_disk_surface_density_normalization, star_disk_mean_molecular_weight \
                          , star_position, star_velocity, star_spin, star_evolution_type)


    ############################################################################
    planet_mass = 0.000954265748
    planet_radius_factor = 0.845649342247916
    planet_radius = planet_radius_factor * posidonius.constants.R_SUN

    planet_dissipation_factor = 2.006*3.845764e4 # -60+64
    planet_dissipation_factor_scale = 1.0
    planet_radius_of_gyration_2 = 0.2376400515700609
    planet_love_number = 0.307
    planet_fluid_love_number = planet_love_number
    #planet_type_two_migration_time = 1.0e5*365.25 # days
    #planet_type_two_migration_inner_disk_edge_distance = 0.01 # AU
    planet_disk_inner_edge_distance = 0.01  # AU
    planet_disk_outer_edge_distance = 100.0 # AU
    planet_disk_lifetime = 1.0e5 * 365.25e0 # days
    planet_alpha_disk = 1.0e-2
    disk_surface_density_normalization_gcm = 1000. # g.cm^-2
    disk_surface_density_normalization_SI = disk_surface_density_normalization_gcm * 1.0e-3 * 1.0e4 # kg.m^-2
    planet_disk_surface_density_normalization = disk_surface_density_normalization_SI * (1.0/posidonius.constants.M_SUN) * np.power(posidonius.constants.AU, 2) # Msun.AU^-2
    planet_disk_mean_molecular_weight =  2.4

    #////////// Specify initial position and velocity for a stable orbit
    #////// Keplerian orbital elements, in the `asteroidal' format of Mercury code
    a = 1.000;                             # semi-major axis (in AU)
    e = 0.1;                               # eccentricity
    i = 5. * posidonius.constants.DEG2RAD;                      # inclination (degrees)
    p = 0. * posidonius.constants.DEG2RAD;                                # argument of pericentre (degrees)
    n = 0. * posidonius.constants.DEG2RAD;                      # longitude of the ascending node (degrees)
    l = 0. * posidonius.constants.DEG2RAD;                      # mean anomaly (degrees)
    p = (p + n);                 # Convert to longitude of perihelion !!
    q = a * (1.0 - e);                     # perihelion distance
    gm = posidonius.constants.G*(planet_mass+star_mass);
    x, y, z, vx, vy, vz = posidonius.calculate_cartesian_coordinates(gm, q, e, i, p, n, l);
    planet_position = posidonius.Axes(x, y, z)
    planet_velocity = posidonius.Axes(vx, vy, vz)

    #////// Initialization of planetary spin
    planet_obliquity = 11.459156 * posidonius.constants.DEG2RAD # 0.2 rad
    planet_rotation_period = 13. # hours
    planet_angular_frequency = posidonius.constants.TWO_PI/(planet_rotation_period/24.) # days^-1
    # Pseudo-synchronization period
    #planet_keplerian_orbital_elements = posidonius.calculate_keplerian_orbital_elements(posidonius.constants.G*star_mass*planet_mass, planet_position, planet_velocity)
    #planet_semi_major_axis = planet_keplerian_orbital_elements[0]
    #planet_eccentricity = planet_keplerian_orbital_elements[2]
    #planet_semi_major_axis = a
    #planet_eccentricity = e
    #planet_pseudo_synchronization_period = posidonius.calculate_pseudo_synchronization_period(planet_semi_major_axis, planet_eccentricity, star_mass, planet_mass)
    #planet_angular_frequency = posidonius.constants.TWO_PI/(planet_pseudo_synchronization_period/24.) # days^-1
    planet_keplerian_orbital_elements = posidonius.calculate_keplerian_orbital_elements(posidonius.constants.G*star_mass*planet_mass, planet_position, planet_velocity)
    planet_inclination = planet_keplerian_orbital_elements[3]
    planet_spin = posidonius.calculate_spin(planet_angular_frequency, planet_inclination, planet_obliquity)

    planet_evolution_type = posidonius.LeconteChabrier2013dissip() # Jupiter with dynamical tide dissipation as in BolmontMathis2016 and GalletBolmont2017
    #planet_evolution_type = posidonius.NonEvolving()
    universe.add_particle(planet_mass, planet_radius, planet_dissipation_factor, planet_dissipation_factor_scale, planet_radius_of_gyration_2, planet_love_number, planet_fluid_love_number, planet_disk_inner_edge_distance, planet_disk_outer_edge_distance, planet_disk_lifetime, planet_alpha_disk, planet_disk_surface_density_normalization, planet_disk_mean_molecular_weight, planet_position, planet_velocity, planet_spin, planet_evolution_type)

    whfast_alternative_coordinates="DemocraticHeliocentric"
    #whfast_alternative_coordinates="WHDS"
    #whfast_alternative_coordinates="Jacobi"
    universe.write(filename, integrator="WHFast", whfast_alternative_coordinates=whfast_alternative_coordinates)
    #universe.write(filename, integrator="IAS15")
    #universe.write(filename, integrator="LeapFrog")


