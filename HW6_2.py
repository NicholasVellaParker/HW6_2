# region imports
from Fluid import Fluid
from Pipe import Pipe
from Loop import Loop
from PipeNetwork import PipeNetwork
# endregion

# region function definitions
def main():
    '''
    This program analyzes flows in a given pipe network based on the following:
    1. The pipe segments are named by their endpoint node names:  e.g., a-b, b-e, etc.
    2. Flow from the lower letter to the higher letter of a pipe is considered positive.
    3. Pressure decreases in the direction of flow through a pipe.
    4. At each node in the pipe network, mass is conserved.
    5. For any loop in the pipe network, the pressure loss is zero
    Approach to analyzing the pipe network:
    Step 1: build a pipe network object that contains pipe, node, loop and fluid objects
    Step 2: calculate the flow rates in each pipe using fsolve
    Step 3: output results
    Step 4: check results against expected properties of zero head loss around a loop and mass conservation at nodes.
    :return:
    '''
    #instantiate a Fluid object to define the working fluid as water
    water= Fluid()#$JES MISSING CODE$  #
    r1 = 0.00085  # in feet
    r2 = 0.003  #in feet

    #instantiate a new PipeNetwork object
    PN=PipeNetwork() #$JES MISSING CODE$  #
    #add Pipe objects to the pipe network (see constructor for Pipe class)
    PN.pipes.append(Pipe('a','h', 1000, 24, r2, water))
    PN.pipes.append(Pipe('a','b', 1000, 18, r2, water))
    PN.pipes.append(Pipe('b','c', 500, 18, r2, water))
    PN.pipes.append(Pipe('c','d', 500, 18, r2, water))
    PN.pipes.append(Pipe('c','f', 800, 16, r1, water))
    PN.pipes.append(Pipe('d','g', 800, 16, r1, water))
    PN.pipes.append(Pipe('b','e', 800, 16, r1, water))
    PN.pipes.append(Pipe('e','f', 500, 12, r1, water))
    PN.pipes.append(Pipe('f','g', 500, 12, r1, water))
    PN.pipes.append(Pipe('g','j', 800, 18, r2, water))
    PN.pipes.append(Pipe('e','i', 800, 18, r2, water))
    PN.pipes.append(Pipe('h','i', 1000, 24, r2, water))
    PN.pipes.append(Pipe('i','j', 1000, 24, r2, water))
    #add Node objects to the pipe network by calling buildNodes method of PN object
    PN.buildNodes()

    #update the external flow of certain nodes
    PN.getNode('h').extFlow= 10
    PN.getNode('e').extFlow= -3
    PN.getNode('f').extFlow= -5
    PN.getNode('d').extFlow= -2

    #add Loop objects to the pipe network
    PN.loops.append(Loop('A',[PN.getPipe('a-b'), PN.getPipe('b-e'),PN.getPipe('e-i'), PN.getPipe('h-i'), PN.getPipe('a-h')]))
    PN.loops.append(Loop('B',[PN.getPipe('b-c'), PN.getPipe('c-f'),PN.getPipe('e-f'), PN.getPipe('b-e')]))
    PN.loops.append(Loop('C',[PN.getPipe('c-d'), PN.getPipe('d-g'),PN.getPipe('f-g'), PN.getPipe('c-f')]))
    PN.loops.append(Loop('D',[PN.getPipe('e-f'), PN.getPipe('f-g'),PN.getPipe('g-j'), PN.getPipe('i-j')]))

    #call the findFlowRates method of the PN (a PipeNetwork object)
    PN.findFlowRates()

    #get output
    PN.printPipeFlowRates()
    print()
    print('Check node flows:')
    PN.printNetNodeFlows()
    print()
    print('Check loop head loss:')
    PN.printLoopHeadLoss()
    print('\nPressure at each node:')

gamma = 62.3  # lb/ft³
known_pressure_psi = 80.0
known_node = 'h'

# Convert psi to feet of head
nodeHeads = {known_node: known_pressure_psi * 144 / gamma}

# Walk pipes until all nodes are assigned
for _ in range(len(PN.pipes)):
    for p in PN.pipes:
        n1 = p.startNode
        n2 = p.endNode
        hl = p.frictionHeadLoss()

        if n1 in nodeHeads and n2 not in nodeHeads:
            if p.Q >= 0:
                nodeHeads[n2] = nodeHeads[n1] - hl
            else:
                nodeHeads[n2] = nodeHeads[n1] + hl

        elif n2 in nodeHeads and n1 not in nodeHeads:
            if p.Q >= 0:
                nodeHeads[n1] = nodeHeads[n2] + hl
            else:
                nodeHeads[n1] = nodeHeads[n2] - hl

# Print results
print(f'  {"Node":<8} {"Head (ft)":>12} {"Pressure (psi)":>16}')
for name, head in sorted(nodeHeads.items()):
    psi = head * gamma / 144  #convert back to psi
    print(f'  {name:<8} {head:>12.2f} {psi:>16.2f}')
    #PN.printPipeHeadLosses()
# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregions

