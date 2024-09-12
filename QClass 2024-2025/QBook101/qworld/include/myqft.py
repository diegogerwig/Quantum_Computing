import cirq
from cirq import H, SWAP
from cirq.circuits import InsertStrategy
from math import pi

def myQFT(qubits):

    circuit = cirq.Circuit() # create a circuit
    
    n = len(qubits)
    for i in range(n):
        #Apply Hadamard
        circuit.append(H(qubits[i]), strategy = InsertStrategy.NEW) # strategy is for the circuit to look neat
        
        # apply Controlled-PhaseShift 
        phase_divisor = 4 # 4,8,16,...
        for j in range(i+1,n):
            circuit.append(cirq.CZPowGate(exponent = 2/phase_divisor).on(qubits[j],qubits[i]))
            phase_divisor = 2 * phase_divisor
 
    # swap the qubits
    for j in range(n//2): # integer division
        circuit.append(SWAP.on(qubits[j],qubits[n-j-1]), strategy = InsertStrategy.NEW)  
    
    return circuit