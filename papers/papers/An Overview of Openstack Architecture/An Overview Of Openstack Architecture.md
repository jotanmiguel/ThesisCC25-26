### An overview of openstack architecture (Tiago Rosado, Jorge Bernardino, 2014)

**Problem Statement:**  
The paper addresses the need for a clear and structured understanding of the OpenStack architecture, an increasingly complex open-source IaaS framework.
As cloud adoption grew, OpenStack became one of the most adopted solutions for both private and public infrastructures. However, its modular nature and the number of interacting components created challenges in design, deployment, and management.

**Objectives:**  
The authors aim to:
- Present an updated and concise overview of OpenStack’s software components and their interactions.
- Classify and describe the roles of each service (compute, networking, storage, shared, and supporting).
- Demonstrate OpenStack’s scalability and adaptability to diverse hardware configurations — from enterprise to entry-level setups.

**Proposed Solution:**  
The paper organizes OpenStack’s components into five functional domains:

- Computing
  - Nova: Orchestrates and manages virtual machine instances through various hypervisors (KVM, Xen, VMware, Hyper-V).
  - Glance: Manages VM images, supporting discovery, registration, and retrieval through APIs.

- Networking
  - Neutron: Provides “networking as a service” — managing IP addressing, VLANs, VPNs, and other advanced topologies. Integrates with frameworks like load balancing or intrusion detection systems.

- Storage
  - Swift: Object storage for scalable, distributed file management.
  - Cinder: Block storage for persistent VM volumes, interoperable with Swift for backups.

- Shared Services
  - Keystone: Authentication and authorization service central to all component communication.
  - Horizon: Web dashboard for unified management.
  - Ceilometer: Telemetry and metering service for billing and usage tracking.

- Supporting Services
  - Database (MySQL): Stores configuration and state data for core services.
  - AMQP (RabbitMQ, Qpid, ZeroMQ): Manages inter-process communication between services.

**Evaluation:**  
The paper is descriptive and architectural rather than experimental.
It includes a conceptual diagram of OpenStack’s components and explains their interdependencies.
It highlights how the modular design allows flexible installations depending on the organization’s needs (minimal core or full deployment).
**Key Contributions:**  
- Presents a clear classification of OpenStack services by functional layer.
- Emphasizes modularity, scalability, and open-source adaptability as key advantages.
- Identifies core services required for a minimal deployment (Nova, Glance, Keystone, Horizon, MySQL, RabbitMQ).

**Limitations and Future Work:**  
The paper does not present experimental performance data or deployment results.
It remains a conceptual study based on documentation and previous literature.
Future work proposed includes usability improvements, better monitoring tools, and enhanced administration interfaces for OpenStack.

**Relevance to Current Project:**  
This paper is highly relevant to the DI Cloud Infrastructure Project.
It provides a structural reference for setting up a private IaaS using OpenStack, detailing how each service interacts and how to compose a minimal functional system.
It also supports the design of authentication integration (Keystone with Active Directory), storage management (Cinder/Swift), and network orchestration (Neutron).
Moreover, it validates the use of OpenStack as a scalable solution adaptable to the department’s mixed hardware environment.

**DOI / Link:**
https://dl.acm.org/doi/10.1145/2628194.2628195
