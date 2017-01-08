use std;
use super::integrator::IntegratorType;

//// Simulation
pub const TIME_STEP: f64 = 0.08; // in days
//pub const TIME_STEP: f64 = 0.003; // in days
//pub const TIME_LIMIT: f64 = 365.25 * 1.0e8;
//pub const TIME_LIMIT: f64 = 365.25 * 1.0e3;
pub const TIME_LIMIT: f64 = TIME_STEP*4.;
pub const PRINT_EVERY_N_DAYS: f64 = 100.*365.25;
//pub const PRINT_EVERY_N_DAYS: f64 = TIME_STEP;
pub const INITIAL_TIME: f64 = 1.0e6*365.25; // time [days] where simulation starts
//pub const INITIAL_TIME: f64 = 2.5e6*365.25; // time [days] where simulation starts (value for SolarLike or MathisSolarLike)

//// Integrator
pub const INTEGRATOR: IntegratorType = IntegratorType::LeapFrog;
//pub const INTEGRATOR: IntegratorType = IntegratorType::Ias15;
//pub const INTEGRATOR: IntegratorType = IntegratorType::WHFastHelio;

//// Constants for IAS15 integrator (to be ignored for others)
pub const INTEGRATOR_FORCE_IS_VELOCITYDEPENDENT : bool = true;	// Turn this off to safe some time if the force is not velocity dependent (i.e. radiation forces, tides depend on vel.).
pub const INTEGRATOR_EPSILON_GLOBAL : bool = true;  // if true: estimate the fractional error by max(acceleration_error)/max(acceleration), where max is take over all particles.
                                                    // if false: estimate the fractional error by max(acceleration_error/acceleration).
pub const INTEGRATOR_EPSILON : f64 = 1e-6;          // Precision parameter (default: 1e-9)
    							                    // If it is zero, then a constant timestep is used. 
pub const INTEGRATOR_MIN_DT : f64 = 0.;             // Minimum timestep used as a floor when adaptive timestepping is enabled (default: 0.).
pub const SAFETY_FACTOR : f64 = 0.25;               // Maximum increase/deacrease of consecutve timesteps (default: 0.25).

///// Constants for WHFastHelio
pub const WHFAST_NMAX_QUART : usize = 64;               // Maximum number of iterations for quartic solver
pub const WHFAST_NMAX_NEWT : usize = 32;               // Maximum number of iterations for Newton's method


//// Physical constants
// These are the same units as used by the mercury6 code.
const K  : f64 = 0.01720209895;    // Gaussian constant 
pub const K2 : f64 = K*K; 
pub const G  : f64 = K2;  // Gravitational constant
pub const PI : f64 = std::f64::consts::PI;
pub const TWO_PI : f64 = std::f64::consts::PI * 2.;
pub const DEG2RAD : f64 = std::f64::consts::PI / 180.; // conversion factor from degrees to radians
pub const M2AU  : f64 = 6.684587153547e-12; // 1 meter in AU
pub const AU : f64 = 1.49598e11; // m
pub const HR: f64 = 3600.; // s

// Solar system
pub const M_SUN : f64 =  1.98892e30; // Kg
pub const R_SUN : f64 = 4.67920694e-3;  // AU
pub const SUN_DYN_FREQ : f64 = K2/(R_SUN*R_SUN*R_SUN); // Needed for MathisSolarLike
pub const R_EARTH : f64 = 4.25874677e-5; // AU
pub const M_EARTH : f64 = 3.0e-6; // M_SUN
pub const M2EARTH : f64 = (1.9891e6/5.9794); // Factor for mass-radius relation (valid only for earth type planets)

// Speed of light in AU/day
pub const SPEED_OF_LIGHT : f64 = 173.1444830225;
pub const SPEED_OF_LIGHT_2 : f64 = SPEED_OF_LIGHT*SPEED_OF_LIGHT;

//// Others
pub const CONSIDER_EVERY_BODY_COMBINATIONS: bool = false;
pub const TIDES: bool = true;
pub const ROTATIONAL_FLATTENING: bool = true;
pub const GENERAL_RELATIVITY: bool = true;
