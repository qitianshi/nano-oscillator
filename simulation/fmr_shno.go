Nx := 512
Ny := 512
cSize := 6e-9

setGridsize(Nx, Ny, 1)
setCellsize(cSize, cSize, 5e-9)

// Geometry
NC_image := imageShape("Geometries/nanoconstriction.png").inverse()
setGeom(NC_image)
defRegion(1, NC_image)
edgesmooth = 8

// Set Simulation time
tSim := 40e-9

// Material parameter (Ni-Fe)
// Values taken from M.Dvornik et al., PHYSICAL REVIEW APPLIED 9, 014017 (2018)
Msat   = 600e3//589e3
Aex    = 10e-12//13e-12
alpha  = 0.02 //damping constant
gammaLL = 1.855e11

// Absorbing BC
// Set up Absorbing boundary layers (ABL).
// to mimic the real world conditions. In actuality, the real physical dimension is around 10 microns by 5 microns
// but since the dimension we use for the simulation is smaller, spin waves will reflect off the boundary and mess with the nanoconstriction
//the ABLs help to mimic the real nanoconstriction as it contains of around 30 layers with an increasing damping constant so that the spin waves dont reflect off
xEnd := Nx*cSize/2
yEnd := Ny*cSize/2
alStart := 0.02
alStop := 1.
NB := 30
dx := cSize
dy := cSize
xStart := xEnd-NB*cSize
xStop := xEnd
yStart := yEnd-NB*cSize
yStop := yEnd
n := 2 //Polynomial order
a := (alStop - alStart)/pow((xStop-xStart)*1e9,n)
print(NB)

//Set the damping in ABL
lR1 := 2*xStart
wR1 := 2*yStart

for i:=1; i<NB+1; i++{
    lR2 := lR1 + 2*dx
    wR2 := wR1 + 2*dy
    rectCurr := rect(lR2,wR2).sub(rect(lR1,wR1))
    DefRegion(i+2, rectCurr)
    alp := a*pow(i*(dx+dy)*1e9*0.5, n)
    alpha.setRegion(i+3, alStart+alp)
    lR1 = lR2
    wR1 = wR2
}

//initial uniform magnetic field
m = uniform(1, 0, 0)
save(geom)

// External field in T
fieldMag := 0.03
phi := 0.

// RF Field
f := 4.0e9
hAmp := 0.0005

// rf field should be perpendicular to the external magnetic field so that it will precess

// Save output
tableAdd(maxAngle)
tableAddVar(phi, "phi", "degree")
tableAddVar(f, "f_RF", "GHz")
tableAutosave(5e-12)

for phi = 0; phi <= 360; phi += 5{
  for f = 3.0e9; f <= 7.0e9;  f+= 0.5e9 {

      B_ext = vector(fieldMag*cos(phi*pi/180), fieldMag*sin(phi*pi/180) + hAmp*sin(2*pi*f*t), 0)
      run(3e-9)

  }
}
