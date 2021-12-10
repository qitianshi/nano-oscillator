// Config file for mumax3 simulation.

// mumax3 uses a variant of Go to configure the simulation. This file does not
// follow typical Go syntax, and cannot be compiled as a standalone file.


// Cell and grid parameters
Nx := 512         // Number of cells in the x-axis
Ny := 512         // Number of cells in the y-axis
cSize := 6e-9     // Cell size (side of square)
setGridsize(Nx, Ny, 1)
setCellsize(cSize, cSize, 5e-9)

// Geometry
NC_image := imageShape("Geometries/nanoconstriction.png").inverse()
setGeom(NC_image)
defRegion(1, NC_image)
edgesmooth = 8            // Smoothening factor for raster images (max 8)

// Material parameters (Ni-Fe permalloy)
// Values taken from M. Dvornik et al., PHYSICAL REVIEW APPLIED 9, 014017 (2018)
Msat = 600e3              // Magnetic saturation
Aex = 10e-12              // Exchange stiffness
alpha = 0.02              // Damping constant
gammaLL = 1.855e11        // Gyromagnetic ratio

// Absorbing boundary conditions
// To reduce simulation time and complexity, only a central region of the
// device is simulated, measuring 2μm by 2μm; the real device is several times
// the area of the simulated portion.
// To simulate the behavior of a larger sample while only actually running on
// a small portion, this section of code sets up the boundary layers of the
// simulated geometry to absorb spin waves (Absorbing Boundary Layer, ABL).
// Otherwise, spin waves would normally reflect off the edges of the geometry
// and interfere with results.
xEnd := Nx * cSize / 2
yEnd := Ny * cSize / 2
alStart := 0.02
alStop := 1.
NB := 30
dx := cSize
dy := cSize
xStart := xEnd - NB * cSize
xStop := xEnd
yStart := yEnd - NB * cSize
yStop := yEnd
n := 2                                                      // Polynomial order
a := (alStop - alStart) / pow((xStop - xStart) * 1e9, n)

// Set the damping in ABL
lR1 := 2 * xStart
wR1 := 2 * yStart
for i := 1; i < NB + 1; i ++ {

  lR2 := lR1 + 2 * dx
  wR2 := wR1 + 2 * dy
  rectCurr := rect(lR2, wR2).sub(rect(lR1, wR1))
  DefRegion(i + 2, rectCurr)
  alp := a * pow(i * (dx + dy) * 1e9 * 0.5, n)
  alpha.setRegion(i + 3, alStart + alp)
  lR1 = lR2
  wR1 = wR2

}

// Initializes with uniform magnetic field
m = uniform(1, 0, 0)
save(geom)

// External field, in T
fieldMag := 0.03
phi := 0.

// RF Field
f := 4.0e9
hAmp := 0.0005

// Configures table output
tableAdd(maxAngle)
tableAddVar(phi, "phi", "degree")
tableAddVar(f, "f_RF", "GHz")
tableAutosave(5e-12)

for phi = 0; phi <= 360; phi += 5{
  for f = 3.0e9; f <= 7.0e9;  f += 0.5e9 {

    B_ext = vector(fieldMag * cos(phi * pi / 180), fieldMag * sin(phi * pi / 180) + hAmp * sin(2 * pi * f * t), 0)
    run(3e-9)

  }
}
