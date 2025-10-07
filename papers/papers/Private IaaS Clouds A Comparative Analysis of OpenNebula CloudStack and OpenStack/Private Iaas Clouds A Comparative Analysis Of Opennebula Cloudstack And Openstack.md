### Private IaaS Clouds: A Comparative Analysis of OpenNebula, CloudStack and OpenStack (Adriano Vogel, Dalvan Griebler, Carlos A. F. Maron, C. Schepke, L. G. Fernandes, 2016)

**Problem Statement:**  
The paper addresses the challenge of **selecting and evaluating IaaS management tools** (OpenNebula, CloudStack, and OpenStack) for **private cloud deployments**.  
While cloud computing is widely adopted, there was limited empirical research comparing open-source IaaS frameworks in terms of **flexibility, resiliency, and performance**—key factors for both academic and enterprise environments.

**Objectives:**  
The study aims to:  
- Evaluate the **flexibility** and **resiliency** of three open-source IaaS tools.  
- Compare their **performance** under identical hardware and hypervisor (KVM) conditions.  
- Provide an empirical basis for choosing an IaaS framework suited for **scientific workloads** and **private infrastructures**.  
- Extend previous taxonomies (e.g., Dukaric & Juric, 2013) by including resiliency as a measurable attribute.
- 
**Proposed Solution:**  
The authors built and tested three **private cloud environments** (OpenNebula, CloudStack, and OpenStack), each deployed with the **same hardware and hypervisor (KVM)** to ensure fairness.  
Their comparison framework includes:  

- **Flexibility analysis** using seven taxonomy layers (core service, support, management, control, security, abstraction, and value-added services).  
- **Resiliency evaluation** based on supported virtualization, storage, networking, and fault-tolerance technologies.  
- **Performance benchmarking** through both micro-benchmarks (CPU, memory, storage, and network) and scientific workloads (NAS parallel benchmarks).  

**Test setup:**  
- Hardware: 4× Supermicro blades (Xeon X5560, 24 GB RAM, RAID5, Ubuntu Server 14.04).  
- Hypervisor: KVM/QEMU 2.0.  
- Tools: OpenNebula 4.12, CloudStack 4.5.2, OpenStack Kilo.  
- Benchmarks: LINPACK, STREAM, IOzone, IPerf, NAS-OMP, and NAS-MPI.

**Evaluation:**  
- **Flexibility:** CloudStack showed the **broadest support** for APIs, integration layers, and external components; OpenStack followed closely with modularity advantages; OpenNebula was simpler but less customizable.  
- **Resiliency:** OpenStack demonstrated the **highest resiliency**, supporting more hypervisors, storage formats, and networking technologies.  
- **Performance:**  
  - OpenStack had **stable performance** with low variation across workloads.  
  - CloudStack was **more flexible** but consumed extra resources due to system VMs.  
  - OpenNebula had **slightly poorer I/O throughput** in disk-intensive tasks.  
  - For scientific applications, all tools performed **close to native environments** (minimal virtualization overhead).  

**Key Contributions:**  
- First unified comparison of OpenNebula, CloudStack, and OpenStack in identical conditions.  
- Integration of **flexibility and resiliency metrics** into the IaaS evaluation framework.  
- Empirical insights showing that **private clouds can handle scientific workloads** efficiently, contrary to prior assumptions from public cloud studies.  
- Quantified trade-offs:  
  - **OpenStack** → most resilient, modular, stable.  
  - **CloudStack** → most flexible, simpler to deploy.  
  - **OpenNebula** → lightweight but limited in scalability.

**Limitations and Future Work:**  
- evaluate more applications and benchmarks for VM scheduling, deployment, and image transfer
- customize the deployed clouds for testing different network and storage options;
- continue deploying and analyzing private IaaS cloud tools using our
methodology.

**Relevance to Current Project:**  
This paper provides insights applicable to the cloud infrastructure project at DI, particularly [authentication / virtualization / orchestration / etc.].

**DOI / Link:** [None]
