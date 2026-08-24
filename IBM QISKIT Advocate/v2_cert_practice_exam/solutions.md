# Answer Key & Technical Explanations

**Q1: B**
> The recommended approach in v2.x is to instantiate a pass manager using generate_preset_pass_manager(backend=backend) and then call pm.run(circuit).

**Q2: B**
> V2 Primitives strictly require ISA circuits and do not perform implicit transpilation. Submitting a non-ISA circuit will throw a validation error.

**Q3: A**
> SamplerV2 PUBs are tuples. They take the circuit and optionally the parameter values. Observables are not used in SamplerV2.

**Q4: B**
> EstimatorV2 PUBs require an observable as the second element of the tuple, followed optionally by parameter values.

**Q5: C**
> SparsePauliOp is the standard class in Qiskit v2.x for representing and manipulating Pauli observables. PauliSumOp (from opflow) was deprecated and removed.

**Q6: C**
> The compose() method is the standard way to merge circuits in Qiskit.

**Q7: B**
> In V2 Primitives, results are accessed via the DataBin. If your classical register is named 'meas' (or default), you access it via result[0].data.meas.get_counts().

**Q8: A**
> EstimatorV2 results store the expectation values in the 'evs' attribute of the PUB result data.

**Q9: B**
> ParameterVector creates an array of Parameter objects that share a common string prefix and are indexed automatically.

**Q10: A**
> The state_fidelity function from qiskit.quantum_info is used to compute the fidelity between two quantum states.

**Q11: C**
> The optimization levels range from 0 (no optimization, just mapping) to 3 (heavy optimization for circuit depth and gate count).

**Q12: B**
> The if_test context manager is the standard and most robust way to build dynamic circuits in Qiskit v2.x, replacing the older c_if method.

**Q13: C**
> measure_all() always creates a new ClassicalRegister and adds it to the circuit to store the measurement outcomes of all qubits.

**Q14: D**
> While passing shots to run() is valid in some runtime environments, configuring the primitive options (e.g., sampler.options.default_shots) or passing it directly to the run() method in Runtime V2 is the standard approach.

**Q15: A**
> Passing a QuantumCircuit to the Operator class from qiskit.quantum_info evaluates the circuit and returns its unitary matrix.

**Q16: A**
> qc.count_ops() returns an OrderedDict with the names of the operations as keys and their frequencies as values.

**Q17: A**
> You can calculate the purity of a DensityMatrix object using its purity attribute or method. A state is pure if the purity is 1.0.

**Q18: B**
> basis_gates tells the transpiler which gates are physically executable on the target backend, forcing it to decompose all other gates into this set.

**Q19: B**
> Sessions allow multiple iterative workloads to be grouped together, minimizing queue times between related jobs on real hardware.

**Q20: B**
> X on |0> creates |1>. Applying H on |1> creates the |-> (minus) superposition state.

**Q21: B**
> QiskitRuntimeService from qiskit_ibm_runtime is the standard class for authenticating and accessing IBM hardware in v2.x.

**Q22: A**
> The tensor() method is used to compute the tensor product of two operators in the quantum_info module.