# Qiskit v2.x Certification Practice Exam

*Choose the best answer for each question.*

### Q1. Transpilation
In Qiskit v2.x, what is the standard method to transpile a generic circuit into an Instruction Set Architecture (ISA) circuit for a specific backend?
- A) qiskit.compiler.transpile
- B) generate_preset_pass_manager
- C) backend.compile
- D) QuantumCircuit.decompose

---

### Q2. V2 Primitives
What happens if you submit a non-ISA circuit (containing gates not supported by the backend) directly to SamplerV2?
- A) It transpiles automatically.
- B) It throws an ISA validation error.
- C) It runs on a simulator.
- D) It ignores the unsupported gates.

---

### Q3. PUBs (Sampler)
Which of the following is the correct structure for a Primitive Unified Bloc (PUB) when submitting a parameterized circuit to SamplerV2?
- A) (circuit, parameter_values)
- B) (circuit, observable, parameter_values)
- C) [circuit, parameter_values]
- D) {circuit: parameter_values}

---

### Q4. PUBs (Estimator)
Which of the following is the correct structure for a Primitive Unified Bloc (PUB) when submitting a parameterized circuit to EstimatorV2?
- A) (circuit, parameter_values)
- B) (circuit, observable, parameter_values)
- C) (observable, circuit, parameter_values)
- D) [circuit, observable]

---

### Q5. Quantum Info
Which class is recommended in Qiskit v2.x to represent Pauli observables efficiently?
- A) PauliSumOp
- B) Operator
- C) SparsePauliOp
- D) Observable

---

### Q6. Circuit Manipulation
How do you combine two quantum circuits, `qc1` and `qc2`, in Qiskit v2.x by appending `qc2` to the end of `qc1`?
- A) qc1.append(qc2)
- B) qc1 + qc2
- C) qc1.compose(qc2)
- D) qc1.merge(qc2)

---

### Q7. Data Extraction (Sampler)
After running a job with SamplerV2, how do you extract the measurement counts from the first PUB result?
- A) result.get_counts()
- B) result[0].data.meas.get_counts()
- C) result[0].counts
- D) result.data[0].get_counts()

---

### Q8. Data Extraction (Estimator)
After running a job with EstimatorV2, how do you extract the expected values?
- A) result[0].data.evs
- B) result.values()
- C) result[0].expectation_values
- D) result.get_evs()

---

### Q9. Parameters
If you need to create a list of 5 parameters for a circuit, what is the most efficient Qiskit class to use?
- A) ParameterList('theta', 5)
- B) ParameterVector('theta', 5)
- C) [Parameter('theta') for _ in range(5)]
- D) CircuitParameters(5)

---

### Q10. State Fidelity
Which function from `qiskit.quantum_info` calculates the fidelity between two Statevector objects?
- A) state_fidelity(sv1, sv2)
- B) calculate_fidelity(sv1, sv2)
- C) sv1.fidelity(sv2)
- D) entanglement_fidelity(sv1, sv2)

---

### Q11. Optimization Levels
In `generate_preset_pass_manager`, what is the maximum `optimization_level` available?
- A) 1
- B) 2
- C) 3
- D) 4

---

### Q12. Dynamic Circuits
In Qiskit v2.x, what is the recommended method to execute a conditional gate based on a classical bit measurement?
- A) qc.x(0).c_if(cr, 1)
- B) with qc.if_test((cr, 1)): qc.x(0)
- C) qc.conditional(cr, 1, 'x', 0)
- D) qc.if_c(cr, 1).x(0)

---

### Q13. Measurements
If `qc.measure_all()` is called on a circuit that already has classical bits, what happens?
- A) It overwrites the existing classical bits.
- B) It throws an error.
- C) It adds a new classical register containing the measurement results.
- D) It only measures the unmeasured qubits.

---

### Q14. Primitives Execution
How do you specify the number of shots when executing a job with SamplerV2?
- A) SamplerV2(shots=1024)
- B) sampler.run([pub], shots=1024)
- C) qc.set_shots(1024)
- D) sampler.options.default_shots = 1024; sampler.run([pub])

---

### Q15. Quantum Info
How can you convert a generic QuantumCircuit into a matrix representation to check its unitary operator?
- A) Operator(qc)
- B) qc.to_matrix()
- C) Unitary(qc)
- D) qc.get_unitary()

---

### Q16. Circuit Inspection
Which method returns a dictionary containing the count of each gate used in the circuit?
- A) qc.count_ops()
- B) qc.gate_counts()
- C) qc.get_gates()
- D) qc.summary()

---

### Q17. Density Matrices
How do you check if a DensityMatrix represents a pure quantum state?
- A) purity == 1.0
- B) is_pure()
- C) trace() == 1.0
- D) check_purity()

---

### Q18. Transpilation
What is the primary role of the `basis_gates` argument in a pass manager?
- A) To define the layout of the qubits.
- B) To specify the target instruction set architecture (ISA) gates.
- C) To optimize the circuit depth.
- D) To simulate hardware noise.

---

### Q19. Sessions
What is the main advantage of using a `Session` context manager when sending multiple jobs to IBM Quantum?
- A) It makes the jobs run on a simulator for free.
- B) It allows jobs to skip the queue and run sequentially without interruption.
- C) It automatically transpiles the circuits.
- D) It compresses the job payload.

---

### Q20. Bitwise Operations
What is the effect of applying an X gate followed by an H gate (X then H) on a qubit initialized in state |0>?
- A) |+> state
- B) |-> state
- C) |1> state
- D) |0> state

---

### Q21. Qiskit Runtime
Which class is used to authenticate and connect to IBM Quantum Platform to retrieve backends?
- A) IBMProvider
- B) QiskitRuntimeService
- C) QuantumService
- D) IBMQ

---

### Q22. Observables
How do you tensor two SparsePauliOp objects, `op1` and `op2`?
- A) op1.tensor(op2)
- B) op1 * op2
- C) op1 ^ op2
- D) op1.compose(op2)