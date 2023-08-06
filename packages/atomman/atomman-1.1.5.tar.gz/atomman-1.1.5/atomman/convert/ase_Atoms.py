import atomman as am
import numpy as np

try:
    import ase
    has_ase = True
except:
    has_ase = False
    
def load(ase_atoms):
    """Convert an ase.Atoms into an atomman.System and list of elements."""
    
    assert has_ase, 'ase not imported'
    
    box = am.Box(vects = ase_atoms.get_cell())
    atoms = am.Atoms(natoms = len(ase_atoms))
    atoms.prop(key = 'pos', value = ase_atoms.get_positions())

    all_elements = np.array(ase_atoms.get_chemical_symbols())
    elements, atype = np.unique(all_elements, return_inverse = True)
    atype += 1
    
    atoms.prop(key='atype', value=atype)
    
    return am.System(atoms=atoms, box=box), elements

def dump(system, elements):
    """Convert an atomman.System and list of elements into an ase.Atoms."""
    
    assert has_ase, 'ase not imported'
    
    elements = np.asarray(elements)
    positions = system.atoms_prop(key='pos')
    cell = system.box.vects
    atype = system.atoms_prop(key='atype')
    symbols = elements[atype-1]
    pbc = system.pbc
    
    return ase.Atoms(symbols=symbols, positions=positions, pbc=pbc, cell=cell)
    
