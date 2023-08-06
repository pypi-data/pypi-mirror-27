from __future__ import print_function
import os
import sys
import numpy as np
import underworld as uw
import underworld.function as fn
import UWGeodynamics.scaling as sca
import UWGeodynamics.shapes as shapes
import UWGeodynamics.surfaceProcesses as surfaceProcesses
from .scaling import nonDimensionalize as nd
from .lithopress import LithostaticPressure
from .utils import PressureSmoother, PassiveTracers
from .rheology import ViscosityLimiter
from .Material import Material
from .Plots import Plots
from .visugrid import Visugrid
from .VelocityBoundaries import VelocityBCs
from .ThermalBoundaries import TemperatureBCs
from .rcParams import rcParams
from ._mesh_advector import _mesh_advector
from ._frictional_boundary import FrictionBoundaries

u = UnitRegistry = sca.UnitRegistry

class Model(Material):
    """ This class provides the main UWGeodynamics Model

    Attributes
    ----------

    materialField:
    pressureField:
    velocityField:
    temperature:
    tractionField:

    """

    def __init__(self, elementRes, minCoord, maxCoord,
                 name = "undefined",
                 gravity=(0.0, -9.81 * u.meter / u.second**2),
                 periodic=None, elementType="Q1/dQ0",
                 Tref=273.15 * u.degK):

        """
        Parameters
        ----------
        elementRes:
            Resolution of the mesh in number of elements for each axis (degree
            of freedom)
        minCoord:
            Minimum coordinates for each axis.
        maxCoord:
            Maximum coordinates for each axis.
        name:
            The Model name.
        gravity:
            Acceleration due to gravity vector.
        periodic:
            Mesh periodicity.
        elementType:
            Type of finite element used (Only Q1/dQ0 are currently supported

        Returns
        --------
        Model Class Object

        Examples
        --------
        >>> import UWGeodynamics as GEO
        >>> u = GEO.UnitRegistry
        >>> Model = Model = GEO.Model(elementRes=(64, 64),
                                      minCoord=(-1. * u.meter, -50. * u.centimeter),
                                      maxCoord=(1. * u.meter, 50. * u.centimeter))

        """

        super(Model, self).__init__()

        self.name = name
        self.top = maxCoord[-1]
        self.bottom = minCoord[-1]

        self.outputDir = rcParams["output.directory"]
        self.checkpointID = 0
        self._checkpoint = None

        self.minViscosity = 1e19*u.pascal*u.second
        self.maxViscosity = 1e25*u.pascal*u.second
        self.viscosityLimiter = ViscosityLimiter(self.minViscosity,
                                                 self.maxViscosity)

        self.gravity = gravity
        self.Tref = Tref
        self.elementType = elementType
        self.elementRes = elementRes
        self.minCoord = minCoord
        self.maxCoord = maxCoord
        self.height = maxCoord[-1] - minCoord[-1]

        if not periodic:
            self.periodic = tuple([False for val in range(len(self.elementRes))])
        else:
            self.periodic = periodic

        minCoord = tuple([nd(val) for val in self.minCoord])
        maxCoord = tuple([nd(val) for val in self.maxCoord])

        self.mesh = uw.mesh.FeMesh_Cartesian(elementType=self.elementType,
                                             elementRes=self.elementRes,
                                             minCoord=minCoord,
                                             maxCoord=maxCoord,
                                             periodic=self.periodic)

        # Add common fields
        self.temperature = None
        self.pressureField = uw.mesh.MeshVariable(mesh=self.mesh.subMesh, nodeDofCount=1)
        self.velocityField = uw.mesh.MeshVariable(mesh=self.mesh, nodeDofCount=self.mesh.dim)
        self.tractionField = uw.mesh.MeshVariable(mesh=self.mesh, nodeDofCount=self.mesh.dim)
        self._strainRateField = uw.mesh.MeshVariable(mesh=self.mesh, nodeDofCount=1)
        self.pressureField.data[...] = 0.
        self.velocityField.data[...] = 0.
        self.tractionField.data[...] = 0.

        # symmetric component of the gradient of the flow velocityField.
        self.strainRate_default = 1e-30 / u.second
        self.solutionExist = False
        self.strainRate = fn.tensor.symmetric(self.velocityField.fn_gradient)
        self.strainRate_2ndInvariant = fn.tensor.second_invariant(self.strainRate)

        # Create the material swarm
        self.swarm = uw.swarm.Swarm(mesh=self.mesh, particleEscape=True)
        self.swarmLayout = None
        self.population_control = None

        self.materials = [self]
        self._defaultMaterial = 0

        if self.mesh.dim == 2:
            # Create a series of aliases for the boundary sets
            self.leftWall   = self.mesh.specialSets["MinI_VertexSet"]
            self.topWall    = self.mesh.specialSets["MaxJ_VertexSet"]
            self.bottomWall = self.mesh.specialSets["MinJ_VertexSet"]
            self.rightWall  = self.mesh.specialSets["MaxI_VertexSet"]

        if self.mesh.dim == 3:
            self.leftWall   = self.mesh.specialSets["MinI_VertexSet"]
            self.rightWall  = self.mesh.specialSets["MaxI_VertexSet"]
            self.frontWall  = self.mesh.specialSets["MinJ_VertexSet"]
            self.backWall   = self.mesh.specialSets["MaxJ_VertexSet"]
            self.topWall    = self.mesh.specialSets["MaxK_VertexSet"]
            self.bottomWall = self.mesh.specialSets["MinK_VertexSet"]

        # Boundary Conditions
        self.velocityBCs = None
        self.temperatureBCs = None

        self.time = 0.0 * u.megayears
        self.step = 0
        self._dt = None
        self.Isostasy = None

        self.pressSmoother = PressureSmoother(self.mesh, self.pressureField)
        self.surfaceProcesses = None

        self._solver = rcParams["default.solver"]
        self.nonLinearTolerance = 1.0e-2

        # Passive Tracers
        self.passiveTracers = []

        # Plots
        self.plot = Plots(self)

        # Visugrid
        self._visugrid = None

        # Mesh advector
        self._advector = None

        # Frictional boundaries
        self.frictionalBCs = None

        self._material_drawing_order = None

        self._initialize()

    def _initialize(self):

        self.swarm_advector = uw.systems.SwarmAdvector(swarm=self.swarm,
                                  velocityField=self.velocityField,
                                  order=2)

        # Add Common Swarm Variables
        self.materialField = self.swarm.add_variable(dataType="int", count=1)
        self.plasticStrain = self.swarm.add_variable(dataType="double", count=1)
        self._viscosityField = self.swarm.add_variable(dataType="double", count=1)
        self._densityField = self.swarm.add_variable(dataType="double", count=1)
        self.meltField = self.swarm.add_variable(dataType="double", count=1)

        # Initialise materialField to Model material
        self.materialField.data[:] = self.index
        # Initialise remaininf fields to 0.
        self.plasticStrain.data[:] = 0.0
        self._viscosityField.data[:] = 0.
        self._densityField.data[:] = 0.
        self.meltField.data[:] = 0.

        # Create a bunch of tools to project swarmVariable onto the mesh
        self._projMaterialField  = uw.mesh.MeshVariable(mesh=self.mesh, nodeDofCount=1)
        self._materialFieldProjector = uw.utils.MeshVariable_Projection(self._projMaterialField, self.materialField, type=0)

        self._projViscosityField = uw.mesh.MeshVariable(mesh=self.mesh, nodeDofCount=1)
        self._viscosityFieldProjector = uw.utils.MeshVariable_Projection(self._projViscosityField, self._viscosityField, type=0)

        self._projPlasticStrain = uw.mesh.MeshVariable(mesh=self.mesh, nodeDofCount=1)
        self._plasticStrainProjector = uw.utils.MeshVariable_Projection(self._projPlasticStrain,
                                                                     self.plasticStrain, type=0)

        self._projDensityField = uw.mesh.MeshVariable(mesh=self.mesh, nodeDofCount=1)
        self._densityFieldProjector = uw.utils.MeshVariable_Projection(self._projDensityField, self._densityField, type=0)

    @property
    def x(self):
        return fn.input()[0]

    @property
    def y(self):
        return fn.input()[1]

    @property
    def z(self):
        return fn.input()[2]

    @property
    def solver(self):
        return self._solver

    @solver.setter
    def solver(self, value):
        solvers = ["mumps", "lu", "mg", "superlu", "superludist", "nomg"]

        if value not in solvers:
            raise ValueError("Invalid Solver")

        self._solver = value

    @property
    def outputDir(self):
        """ Output Directory """
        return self._outputDir
    
    @outputDir.setter
    def outputDir(self, value):
        if uw.rank() == 0:
            if not os.path.exists(value):
                os.makedirs(value)
        self._outputDir = value

    def restart(self, restartDir=None, step=None):
        """ Restart a Model
        
        parameters:
        -----------
            restartDir: (string)
                Directory that contains the outputs of the model
                you want to restart
            step: (int)
                Step from which you want to restart the model.
        
        """
        if not restartDir:
            restartDir = self._outputDir
        if not step:
            step = max([int(os.path.splitext(filename)[0].split("-")[-1])
                        for filename in os.listdir(restartDir) if "-" in
                        filename])

        self.checkpointID = step
        self.mesh.load(os.path.join(restartDir, "mesh.h5"))
        self.swarm = uw.swarm.Swarm(mesh=self.mesh, particleEscape=True)
        self.swarm.load(os.path.join(restartDir, 'swarm-%s.h5' % step))
        self._initialize()
        self.materialField.load(os.path.join(restartDir, "materialField-%s.h5" % step))
        self.temperature.load(os.path.join(restartDir, 'temperature-%s.h5' % step))
        self.pressureField.load(os.path.join(restartDir, 'pressureField-%s.h5' % step))
        self.plasticStrain.load(os.path.join(restartDir, 'plasticStrain-%s.h5' % step))
        self.velocityField.load(os.path.join(restartDir, 'velocityField-%s.h5' % step))

    @property
    def projMaterialField(self):
        """ Material field projected on the mesh """
        self._materialFieldProjector.solve()
        return self._projMaterialField

    @property
    def projPlasticStrain(self):
        """ Plastic Strain Field projected on the mesh """
        self._plasticStrainProjector.solve()
        return self._projPlasticStrain

    @property
    def strainRateField(self):
        """ Strain Rate Field """
        self._strainRateField.data[:] = self.strainRate_2ndInvariant.evaluate(self.mesh)
        return self._strainRateField

    @property
    def projViscosityField(self):
        """ Viscosity Field projected on the mesh """
        self.viscosityField.data[...] = self.viscosityFn.evaluate(self.swarm)
        self._viscosityFieldProjector.solve()
        return self._projViscosityField

    @property
    def viscosityField(self):
        """ Viscosity Field on particles """
        self._viscosityField.data[:] = self.viscosityFn.evaluate(self.swarm)
        return self._viscosityField

    @property
    def projDensityField(self):
        """ Density Field projected on the mesh """
        self.densityField.data[...] = self.densityFn.evaluate(self.swarm)
        self._densityFieldProjector.solve()
        return self._projDensityField

    @property
    def densityField(self):
        """ Density Field on particles """
        self._densityField.data[:] = self.densityFn.evaluate(self.swarm)
        return self._densityField
    
    @property
    def surfaceProcesses(self):
        """ Surface processes handler """ 
        return self._surfaceProcesses

    @surfaceProcesses.setter
    def surfaceProcesses(self, value):
        self._surfaceProcesses = value
        if isinstance(value, surfaceProcesses.Badlands):
            self._surfaceProcesses.Model = self

    @property
    def swarmLayout(self):
        """ Swarm Layout underworld object """
        return self._swarmLayout

    @swarmLayout.setter
    def swarmLayout(self, value):

        if value is not None:
            self._swarmLayout = value
        else:
            self._swarmLayout = uw.swarm.layouts.GlobalSpaceFillerLayout(
                                                 swarm=self.swarm,
                                                 particlesPerCell=50)

        self.swarm.populate_using_layout(layout=self._swarmLayout)

    @property
    def population_control(self):
        """ Population control underworld object """
        return self._population_control

    @population_control.setter
    def population_control(self, value):
        if isinstance(value, uw.swarm.PopulationControl):
            self._population_control = value
        else:
            self._population_control = uw.swarm.PopulationControl(
                     self.swarm,
                     aggressive=True, splitThreshold=0.15,
                     maxSplits=10,
                     particlesPerCell=50
                )

    def set_temperatureBCs(self, left=None, right=None, top=None, bottom=None,
                           front=None, back=None,
                           indexSets=None, materials=None):
        """ Set Model thermal conditions
         
        Parameters:
            left:
                Temperature or flux along the left wall.
                Default is 'None' 
            right:
                Temperature or flux along the right wall.
                Default is 'None' 
            top:
                Temperature or flux along the top wall.
                Default is 'None' 
            bottom:
                Temperature or flux along the bottom wall.
                Default is 'None' 
            front:
                Temperature or flux along the front wall.
                Default is 'None' 
            back:
                Temperature or flux along the back wall.
                Default is 'None' 
            indexSets: (set, temperature)
                underworld mesh index set and associate temperature
            materials:
                list of materials for which temperature need to be
                fixed. [(material, temperature)]
        
        """


        if not self.temperature:
            self.temperature = uw.mesh.MeshVariable(mesh=self.mesh,
                                                    nodeDofCount=1)
            self._temperatureDot = uw.mesh.MeshVariable(mesh=self.mesh,
                                                    nodeDofCount=1)
            self.temperature.data[...] = nd(self.Tref)
            self._temperatureDot.data[...] = 0.

        self.temperatureBCs = TemperatureBCs(self, left=left, right=right,
                                             top=top, bottom=bottom,
                                             back=back, front=front,
                                             indexSets=indexSets,
                                             materials=materials)
        return self.temperatureBCs.get_conditions()

    @property
    def temperature(self):
        """ Temperature Field """
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @property
    def _temperatureBCs(self):
        if not self.temperatureBCs:
            raise ValueError("Set Boundary Conditions")
        return self.temperatureBCs.get_conditions()

    @property
    def advdiffSystem(self):
        """ Advection Diffusion System """

        DiffusivityMap = {}
        for material in self.materials:
            DiffusivityMap[material.index] = nd(material.diffusivity)

        self.DiffusivityFn = fn.branching.map(fn_key=self.materialField,
                                              mapping=DiffusivityMap)

        HeatProdMap = {}
        for material in self.materials:
            if all([material.density, material.capacity, material.radiogenicHeatProd]):
                HeatProdMap[material.index] = (nd(material.radiogenicHeatProd) /
                                               (nd(material.density) *
                                                nd(material.capacity)))
            else:
                HeatProdMap[material.index] = 0.

            # Melt heating
            if material.latentHeatFusion and self._dt:
                dynamicHeating = self._get_dynamic_heating(material)
                HeatProdMap[material.index] += dynamicHeating

        self.HeatProdFn = fn.branching.map(fn_key=self.materialField,
                                           mapping=HeatProdMap)

        self._advdiffSystem = uw.systems.AdvectionDiffusion(
                self.temperature,
                self._temperatureDot,
                velocityField=self.velocityField,
                fn_diffusivity=self.DiffusivityFn,
                fn_sourceTerm=self.HeatProdFn,
                conditions=[self._temperatureBCs]
            )
        return self._advdiffSystem

    @property
    def stokes(self):
        """ Stokes solver """

        gravity = tuple([nd(val) for val in self.gravity])
        self.buoyancyFn = self.densityFn * gravity

        if any([material.viscosity for material in self.materials]):

            stokes = uw.systems.Stokes(velocityField=self.velocityField,
                                       pressureField=self.pressureField,
                                       conditions=self._velocityBCs,
                                       fn_viscosity=self.viscosityFn,
                                       fn_bodyforce=self.buoyancyFn,
                                       fn_one_on_lambda = None)

            self._stokes = uw.systems.Solver(stokes)
            self._stokes.set_inner_method(self.solver)

        return self._stokes

    def _init_melt_fraction(self):
        """ Initialize the Melt Fraction Field """

        # Initialize Melt Fraction to material property
        meltFractionMap = {}
        for material in self.materials:
            if material.meltFraction:
                meltFractionMap[material.index] = material.meltFraction

        if meltFractionMap:
            InitFn = fn.branching.map(fn_key=self.materialField, mapping=meltFractionMap, fn_default=0.0)
            self.meltField.data[:] = InitFn.evaluate(self.swarm)

    def set_velocityBCs(self, left=None, right=None, top=None, bottom=None,
                        front=None, back=None, indexSets=None):
        """ Set Model kinematic conditions
         
        Parameters:
            left:
                Velocity along the left wall.
                Default is 'None' 
            right:
                Velocity along the right wall.
                Default is 'None' 
            top:
                Velocity along the top wall.
                Default is 'None' 
            bottom:
                Velocity along the bottom wall.
                Default is 'None' 
            front:
                Velocity along the front wall.
                Default is 'None' 
            back:
                Velocity along the back wall.
                Default is 'None' 
            indexSets: (set, velocity)
                underworld mesh index set and associate velocity
        """

        self.velocityBCs = VelocityBCs(self, left=left,
                                       right=right, top=top,
                                       bottom=bottom, front=front,
                                       back=back, indexSets=indexSets)
        return self.velocityBCs.get_conditions()

    @property
    def _velocityBCs(self):
        """ Retrieve kinematic boundary conditions """
        if not self.velocityBCs:
            raise ValueError("Set Boundary Conditions")
        return self.velocityBCs.get_conditions()

    def add_material(self, shape, name="unknown", reset=False):
        """ Add Material to the Model

        Parameters:
        -----------
            shape:
                Shape of the material. See UWGeodynamics.shape
            name:
                Material name
            reset: (bool)
                Reset the material Field before adding the new
                material. Default is False.
        """

        if reset:
            self.materialField.data[...] = 0
            self.materials = [self]

        mat = Material()

        mat.name = name

        ### Initialize some properties to Model property
        mat.diffusivity        = self.diffusivity
        mat.capacity           = self.capacity
        mat.thermalExpansivity = self.thermalExpansivity
        mat.radiogenicHeatProd = self.radiogenicHeatProd

        if isinstance(shape, shapes.Layer):
            mat.top = shape.top
            mat.bottom = shape.bottom

            if self.mesh.dim == 3:
                shape.minY = self.minCoord[1]
                shape.maxY = self.maxCoord[1]

        mat.shape              = shape
        mat.indices = self._get_material_indices(mat)
        self.materials.reverse()
        self.materials.append(mat)
        self.materials.reverse()
        self._fill_model()

        return mat

    def _fill_model(self):
        """ Initialize the Material Field from the list of materials"""

        conditions = [(obj.shape.fn, obj.index)
                      for obj in self.materials if obj.shape is not None]

        conditions.append((True, self._defaultMaterial))
        self.materialField.data[:] = fn.branching.conditional(conditions).evaluate(self.swarm)

    @property
    def material_drawing_order(self):
        """ Order of material drawing. Overlapping shapes reset the material"""
        return self._material_drawing_order

    @material_drawing_order.setter
    def material_drawing_order(self, value):
        if value:
            self.materials = value
            self._material_drawing_order = value
            self._fill_model()

    @property
    def densityFn(self):
        """ Density function """
        return self._densityFn()

    def _densityFn(self):
        densityMap = {}
        for material in self.materials:

            if self.temperature:
                densityMap[material.index] = nd(material.density) * (1.0 -
                                             nd(material.thermalExpansivity)
                                             * (self.temperature - nd(self.Tref)))
            else:
                densityMap[material.index] = nd(material.density)

            if material.meltExpansion:
                fact = material.meltExpansion * self.meltField
                densityMap[material.index] = densityMap[material.index] * (1.0 - fact)

        return fn.branching.map(fn_key=self.materialField, mapping=densityMap)

    def set_frictional_boundary(self, right=False, left=False,
                                  top=False, bottom=False,
                                  thickness=2, friction=0.0):
        """ Set Frictional Boundary conditions 
        
        Frictional boundaries are implemented as a thin layer of frictional
        material along the chosen boundaries.

        Parameters:
        -----------

            right: (bool)
                if True create a frictional boundary.
            left: (bool)
                if True create a frictional boundary.
            top: (bool)
                if True create a frictional boundary.
            bottom: (bool)
                if True create a frictional boundary.
            thickness: (int)
                thickness of the boundaries (in number of
                elements)
            friction: (float)
                Friction coefficient at the boundaries.

        Returns:
        --------
            Underworld mesh variable that maps the boundaries.
            (Values are set to 1 if the mesh element applies
            a frictional condition, 0 otherwise).
        """

        self.frictionalBCs = FrictionBoundaries(self, right=right,
                                                      left=left,
                                                      top=top,
                                                      bottom=bottom,
                                                      thickness=thickness,
                                                      friction=friction)

        return self.frictionalBCs

    @property
    def viscosityFn(self):
        """ Effective Viscosity Function """
        return self._viscosityFn()

    def _viscosityFn(self):
        """ Create the Viscosity Function """

        ViscosityMap = {}
        BGViscosityMap = {}

        # Viscous behavior
        for material in self.materials:
            if material.viscosity:
                ViscosityHandler = material.viscosity
                ViscosityHandler.pressureField = self.pressureField
                ViscosityHandler.strainRateInvariantField = self.strainRate_2ndInvariant
                ViscosityHandler.temperatureField = self.temperature
                ViscosityHandler.viscosityLimiter = self.viscosityLimiter
                ViscosityMap[material.index] = ViscosityHandler.muEff


        # Melt Modifier
        for material in self.materials:
            if material.viscosity and material.viscosityChange > 1.0:
                X1 = material.viscosityChangeX1
                X2 = material.viscosityChangeX2
                change =  1.0 + (material.viscosityChange - 1.0) / (X2 - X1) * (self.meltField - X1)
                conditions = [(self.meltField < X1, 1.0),
                              (self.meltField > X2, material.viscosityChange),
                              (True, change)]
                ViscosityMap[material.index] *= fn.branching.conditional(conditions)

        # Plasticity
        PlasticityMap = {}
        for material in self.materials:

            if material.plasticity:

                YieldHandler = material.plasticity
                YieldHandler.pressureField = self.pressureField
                YieldHandler.plasticStrain = self.plasticStrain
                if self.mesh.dim == 2:
                    yieldStress = YieldHandler._get_yieldStress2D()
                if self.mesh.dim == 3:
                    yieldStress = YieldHandler._get_yieldStress3D()
                eijdef =  nd(self.strainRate_default)
                eij = fn.branching.conditional([(self.strainRate_2ndInvariant < sys.float_info.epsilon, eijdef),
                                              (True, self.strainRate_2ndInvariant)])
                muEff = 0.5 * yieldStress / eij
                muEff = self.viscosityLimiter.apply(muEff)
                PlasticityMap[material.index] = muEff

            if self.frictionalBCs is not None:
                from copy import copy

                # Only affect plastic materials
                if material.plasticity:

                    YieldHandler = copy(material.plasticity)
                    YieldHandler.frictionCoefficient = self.frictionalBCs.friction
                    YieldHandler.pressureField = self.pressureField
                    YieldHandler.plasticStrain = self.plasticStrain
                    if self.mesh.dim == 2:
                        yieldStress = YieldHandler._get_yieldStress2D()
                    if self.mesh.dim == 3:
                        yieldStress = YieldHandler._get_yieldStress3D()
                    eijdef =  nd(self.strainRate_default)
                    eij = fn.branching.conditional([(self.strainRate_2ndInvariant < sys.float_info.epsilon, eijdef),
                                                  (True, self.strainRate_2ndInvariant)])
                    muEff = 0.5 * yieldStress / eij
                    muEff = self.viscosityLimiter.apply(muEff)

                    conditions = [(self.frictionalBCs._mask == 1, muEff),
                                  (True, PlasticityMap[material.index])]

                    PlasticityMap[material.index] = fn.branching.conditional(conditions)


        # Combine rheologies
        EffViscosityMap = {}
        PlasticMap = {}
        for material in self.materials:
            idx = material.index
            if material.viscosity and material.plasticity:
                EffViscosityMap[idx] = fn.misc.min(PlasticityMap[idx], ViscosityMap[idx])
                BGViscosityMap[idx] = ViscosityMap[idx]
                PlasticMap[idx] = 0.
            elif material.viscosity:
                EffViscosityMap[idx] = ViscosityMap[idx]
                BGViscosityMap[idx] = ViscosityMap[idx]
                PlasticMap[idx] = 0.
            elif material.plasticity:
                EffViscosityMap[idx] = PlasticityMap[idx]
                BGViscosityMap[idx] = PlasticityMap[idx]
                PlasticMap[idx] = 1.0


        viscosityFn = fn.branching.map(fn_key=self.materialField, mapping=EffViscosityMap)
        backgroundViscosityFn = fn.branching.map(fn_key=self.materialField, mapping=BGViscosityMap)

        isPlastic = fn.branching.map(fn_key=self.materialField, mapping=PlasticMap)
        yieldConditions = [(viscosityFn < backgroundViscosityFn, 1.0),
                           (isPlastic > 0.5, 1.0),
                           (True, 0.0)]

        # Do not yield at the very first solve
        if self.solutionExist:
            self.isYielding = fn.branching.conditional(yieldConditions) * self.strainRate_2ndInvariant
        else:
            self.isYielding = fn.misc.constant(0.0)

        return viscosityFn

    @property
    def yieldStressFn(self):
        """ Yield Stress function """
        return self._yieldStressFn()

    def _yieldStressFn(self):
        """ Calculate Yield stress function from viscosity and strain rate"""
        eij = self.strainRate_2ndInvariant
        eijdef =  nd(self.strainRate_default)
        return 2.0 * self.viscosityFn * fn.misc.max(eij, eijdef)

    def solve_temperature_steady_state(self):
        """ Solve for steady state temperature 
        
        Returns:
        --------
            Updated temperature Field
        """

        if self.materials:
            DiffusivityMap = {}
            for material in self.materials:
                DiffusivityMap[material.index] = nd(material.diffusivity)

            self.DiffusivityFn = fn.branching.map(fn_key = self.materialField, mapping = DiffusivityMap)

            HeatProdMap = {}
            for material in self.materials:
                if all([material.density, material.capacity, material.radiogenicHeatProd]):
                    HeatProdMap[material.index] = (nd(material.radiogenicHeatProd) /
                                                   (nd(material.density) *
                                                    nd(material.capacity)))
                else:
                    HeatProdMap[material.index] = 0.

            self.HeatProdFn = fn.branching.map(fn_key = self.materialField, mapping = HeatProdMap)
        else:
            self.DiffusivityFn = fn.misc.constant(nd(self.diffusivity))
            self.HeatProdFn = fn.misc.constant(nd(self.radiogenicHeatProd))

        conditions = self._temperatureBCs
        heatequation = uw.systems.SteadyStateHeat(temperatureField=self.temperature,
                                                  fn_diffusivity=self.DiffusivityFn,
                                                  fn_heating=self.HeatProdFn,
                                                  conditions=conditions)
        heatsolver = uw.systems.Solver(heatequation)
        heatsolver.solve(nonLinearIterate=True)

        return self.temperature

    def get_lithostatic_pressureField(self):
        """ Calculate the lithostatic Pressure Field

        Returns:
        --------
            Pressure Field, array containing the pressures
            at the bottom of the Model
        """

        gravity = np.abs(nd(self.gravity[-1]))  # Ugly!!!!!
        lithoPress = LithostaticPressure(self.mesh, self.densityFn, gravity)
        self.pressureField.data[:], LPressBot = lithoPress.solve()
        self.pressSmoother.smooth()

        return self.pressureField, LPressBot

    def _calibrate_pressureField(self):
        """ Pressure Calibration callback function """

        surfaceArea = uw.utils.Integral(fn=1.0, mesh=self.mesh,
                                        integrationType='surface',
                                        surfaceIndexSet=self.topWall)
        surfacepressureFieldIntegral = uw.utils.Integral(
                fn=self.pressureField,
                mesh=self.mesh,
                integrationType='surface',
                surfaceIndexSet=self.topWall
            )
        area, _ = surfaceArea.evaluate()
        p0, _ = surfacepressureFieldIntegral.evaluate()
        offset = p0/area
        self.pressureField.data[:] -= offset
        self.pressSmoother.smooth()

        for material in self.materials:
            if material.viscosity:
                material.viscosity.firstIter = False

    def _get_material_indices(self, material):
        """ Get mesh indices of a Material 
        
        Parameter:
        ----------
            material:
                    The Material of interest
        Returns;
        --------
            underworld IndexSet
        
        """
        nodes = np.arange(0, self.mesh.nodesLocal)[self.projMaterialField.evaluate(self.mesh.data[0:self.mesh.nodesLocal])[:, 0] == material.index]
        return uw.mesh.FeMesh_IndexSet(self.mesh, topologicalIndex=0, size=self.mesh.nodesGlobal, fromObject=nodes)

    def solve(self):
        """ Solve Stokes """
        self.stokes.solve(nonLinearIterate=True,
                          callback_post_solve=self._calibrate_pressureField,
                          nonLinearTolerance=self.nonLinearTolerance)
        self.solutionExist = True

    def init_model(self, temperature=True, pressureField=True):
        """ Initialize the Temperature Field as steady state,
            Initialize the Pressure Field as Lithostatic

        Parameters:
        -----------
            temperature: (bool) default to True
            pressure: (bool) default to True
        """

        # Init Temperature Field
        if self.temperature and temperature:
            self.solve_temperature_steady_state()

        # Init pressureField Field
        if self.pressureField and pressureField:
            self.get_lithostatic_pressureField()
        return

    def run_for(self, duration=None, checkpoint=None, timeCheckpoints=None):
        """ Run the Model

        Parameters:
        -----------
        
            duration: duration of the Model in Time units or nb of steps
            checkpoint: checkpoint interval
            timeCheckpoints: Additional checkpoints
        """

        step = self.step
        time = nd(self.time)
        units = duration.units
        duration = time + nd(duration)

        next_checkpoint = None

        if timeCheckpoints:
            timeCheckpoints = [nd(val) for val in timeCheckpoints]

        if checkpoint:
            next_checkpoint = time + nd(checkpoint)

        while time < duration:
            self.solve()

            # Whats the longest we can run before reaching the end of the model
            # or a checkpoint?
            # Need to generalize that
            dt = self.swarm_advector.get_max_dt()

            if self.temperature:
                dt = min(dt, self.advdiffSystem.get_max_dt())

            if checkpoint:
                dt = min(dt, next_checkpoint - time)

            self._dt = min(dt, duration - time)

            uw.barrier()

            self.update()

            step += 1
            self.time += sca.Dimensionalize(self._dt, units)
            time += self._dt

            if time == next_checkpoint:
                self.checkpointID += 1
                self.checkpoint()
                self.output_glucifer_figures(self.checkpointID)
                next_checkpoint += nd(checkpoint)

            if checkpoint or step % 1 == 0:
                if uw.rank() == 0:
                    print("Time: ", str(self.time.to(units)),
                          'dt:', str(sca.Dimensionalize(self._dt, units)))
        return 1

    def update(self):
        """ Update Function 
        
        The following function processes the mesh and swarm variables
        between two solves. It takes care of mesh, swarm advection and
        update the fields according to the Model state.

        """

        dt = self._dt
        # Increment plastic strain
        plasticStrainIncrement = dt * self.isYielding.evaluate(self.swarm)
        self.plasticStrain.data[:] += plasticStrainIncrement

        if any([material.melt for material in self.materials]):
            # Calculate New meltField
            meltFraction = self._get_melt_fraction()
            self.meltField.data[:] = meltFraction.evaluate(self.swarm)

        # Solve for temperature
        if self.temperature:
            self.advdiffSystem.integrate(dt)

        # Integrate Swarms in time
        self.swarm_advector.integrate(dt, update_owners=True)

        if self.passiveTracers:
            for tracers in self.passiveTracers:
                tracers.integrate(dt)

        if self._advector:
            self._advector.advect_mesh(dt)

        # Do pop control
        self.population_control.repopulate()

        if self.surfaceProcesses:
            self.surfaceProcesses.solve(dt)

        if self.Isostasy:
            self.Isostasy.solve()

        if self._visugrid:
            self._visugrid.advect(dt)

    def set_meshAdvector(self, axis):
        """ Initialize the mesh advector 
        
        Parameters:
        -----------
            axis:
                list of axis (or degree of freedom) along which the
                mesh is allowed to deform
        """
        self._advector = _mesh_advector(self, axis)

    def add_passive_tracers(self, name=None, vertices=None, particleEscape=True):
        """ Add a swarm of passive tracers to the Model

        Parameters:
        -----------
            name:
                Name of the swarm of tracers.
            vertices:
                Numpy array that contains the coordinates of the tracers.
            particleEscape: (bool)
                Allow or prevent tracers from escaping the boundaries of the
                Model (default to True)
        """
        tracers = PassiveTracers(self.mesh,
                                 self.velocityField,
                                 name=name,
                                 vertices=vertices,
                                 particleEscape=particleEscape)

        self.passiveTracers.append(tracers)

        return tracers

    def _get_melt_fraction(self):
        """ Melt Fraction function 
        
        Returns:
        -------
            Underworld function that calculates the Melt fraction on the 
            particles.
        
        """
        meltMap = {}
        for material in self.materials:
            if material.melt:
                T_s = material.solidus.temperature(self.pressureField)
                T_l = material.liquidus.temperature(self.pressureField)
                T_ss = (self.temperature - 0.5 * (T_s + T_l)) / (T_l - T_s)
                value =  0.5 + T_ss + (T_ss * T_ss - 0.25) * (0.4256 + 2.988 * T_ss)
                conditions = [((-0.5 < T_ss) & (T_ss < 0.5), fn.misc.min(value, material.meltFractionLimit)),
                              (True, 0.0)]
                meltMap[material.index] = fn.branching.conditional(conditions)

        return fn.branching.map(fn_key=self.materialField, mapping=meltMap, fn_default=0.0)

    def _get_dynamic_heating(self, material):
        """ Calculate additional heating source due to melt 
        
        Returns:
        --------
            Underworld function

        """

        ratio = material.latentHeatFusion / material.capacity

        if not ratio.dimensionless:
            raise ValueError("Unit Error in either Latent Heat Fusion or Capacity (Material: "+material.name)
        ratio = ratio.magnitude

        dF = (self._get_melt_fraction() - self.meltField) / self._dt
        return (ratio * dF) * self.temperature

    @property
    def lambdaFn(self):
        """ Initialize compressibility """

        materialMap = {}
        if any([material.compressibility for material in self.materials]):
            for material in self.materials:
                if material.compressibility:
                    materialMap[material.index] = material.compressibility

            return uw.function.branching.map(fn_key=self.materialField,
                   mapping=materialMap, fn_default=0.0)
        return

    def checkpoint(self, variables=None, checkpointID=None):
        """ Do a checkpoint (Save fields)
        
        Parameters:
        -----------
            variables:
                list of fields/variables to save
            checkpointID:
                checkpoint ID.

        """
        if not variables:
            variables = rcParams["default.outputs"]

        if not checkpointID:
            checkpointID = self.checkpointID

        for variable in variables:
            if variable == "temperature" and not self.temperature:
                continue
            self._save_field(variable, checkpointID)

        if checkpointID > 2:
            for field in rcParams["swarm.variables"]:
                try:
                    os.remove(os.path.join(self.outputDir, field+"-%s" %  checkpointID - 2))
                except:
                    pass

    def output_glucifer_figures(self, step):
        """ Output glucifer Figures to the gldb store """

        import glucifer
        GluciferStore = glucifer.Store(os.path.join(self.outputDir, "glucifer"))
        GluciferStore.step = step

        pressure = self.plot.pressureField(store=GluciferStore, show=False)
        pressure.save()

        temperature = self.plot.temperature(store=GluciferStore, show=False)
        temperature.save()

        velocity = self.plot.velocityField(store=GluciferStore, show=False)
        velocity.save()

        strainrate = self.plot.strainRate(store=GluciferStore, show=False)
        strainrate.save()

        material = self.plot.material(projected=True, store=GluciferStore, show=False)
        material.save()

        strain = self.plot.strain(projected=True, store=GluciferStore, show=False)
        strain.save()

        density = self.plot.density(projected=True, store=GluciferStore, show=False)
        density.save()

        viscosity = self.plot.viscosity(projected=True, store=GluciferStore, show=False)
        viscosity.save()

    def add_visugrid(self, elementRes, minCoord=None, maxCoord=None):
        """ Add a tracking grid to the Model 
        
        This is essentially a lagrangian grid that deforms with the materials.

        Parameters:
        -----------
            elementRes:
                Grid resolution in number of elements along each axis (x, y, z).
            minCoord:
                Minimum coordinate for each axis.
                Used to define the extent of the grid,
            maxCoord:
                Maximum coordinate for each axis.
                Used to define the extent of the grid,
        """


        if not maxCoord:
            maxCoord = self.maxCoord

        if not minCoord:
            minCoord = self.minCoord

        self._visugrid = Visugrid(self, elementRes, minCoord, maxCoord, self.velocityField)

    def _save_field(self, field, checkpointID, units=None):
        """ Save Field """

        if field in rcParams["mesh.variables"]:
            if not units:
                units = rcParams[field+".SIunits"]
            mH = self.mesh.save(os.path.join(self.outputDir, "mesh.h5"), units=u.kilometers)
            file_prefix = os.path.join(self.outputDir, field+'-%s' % checkpointID)
            obj = getattr(self, field)
            handle = obj.save('%s.h5' % file_prefix, units=units)
            obj.xdmf('%s.xdmf' % file_prefix, handle, field, mH, 'mesh', modeltime=self.time.magnitude)

        elif field in rcParams["swarm.variables"]:
            if not units:
                units = rcParams[field+".SIunits"]
            sH = self.swarm.save(os.path.join(self.outputDir, 'swarm-%s.h5' % checkpointID), units=u.kilometers)
            file_prefix = os.path.join(self.outputDir, field+'-%s' % checkpointID)
            obj = getattr(self, field)
            handle = obj.save('%s.h5' % file_prefix)
            obj.xdmf('%s.xdmf' % file_prefix, handle, field, sH, 'swarm', modeltime=self.time.magnitude)
        else:
            raise ValueError(field, ' is not a valid variable name \n')
