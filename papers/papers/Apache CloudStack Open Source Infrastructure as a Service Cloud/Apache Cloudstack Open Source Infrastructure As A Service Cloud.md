### Apache CloudStack : Open Source Infrastructure as a Service Cloud Computing Platform (R. Kumar, Kanishk Jain, Hitesh Maharwal, N. Jain, A. Dadhich, 2014)

**Problem Statement:**  
In this research paper, the authors are discussing, introduction, benefits, background, features, use cases and purposes of Apache CloudStack. Further discussing
deployment architecture, components, API, pros and cons of Apache CloudStack and lastly discuss about some new features supported by the release of Apache CloudStack 4.4. This paper shows the importance of Apache CloudStack as a Cloud provider and gives the best solution for service providers, web content providers, SaaS providers, and
enterprises.

**Objectives:**  
The main objectives of the paper are to:
- Present Apache CloudStack as a comprehensive open-source IaaS solution.
- Describe its architecture, components, and APIs that enable large-scale deployment of virtual machines and networking resources.
- Demonstrate its benefits, features, and common use cases for enterprises, SaaS providers, and web hosting services.
- Discuss the advantages and challenges of using CloudStack in production environments.

**Proposed Solution:**  
The paper outlines **Apache CloudStack** as a **turnkey platform** that provides compute, storage, and networking orchestration through a centralized management server.  
Its architecture includes the following key elements:

1. **Management Server:** Central controller that manages all physical and virtual resources.  
2. **Hosts and Clusters:** Each host provides compute resources via hypervisors (KVM, XenServer, VMware, or Hyper-V). Hosts are grouped into clusters and pods within zones (data centers).  
3. **Storage System:**  
   - *Primary Storage* — stores VM volumes (coupled with clusters).  
   - *Secondary Storage* — stores VM templates, ISOs, and snapshots.  
4. **Networking:** Supports *Basic* (AWS-style) and *Advanced* (VLAN/VPN-based) models.  
5. **API Layers:** Three API roles — root admin, domain admin, and user — allowing fine-grained control over both physical and virtual resources.  
6. **Hypervisor Integration:** Broad compatibility (XenServer, VMware, Oracle VM, KVM) enabling flexibility across hardware and virtualization setups.  

**Evaluation:**  
The paper is descriptive, not experimental. It focuses on explaining the **deployment model**, **management interfaces**, and **API structure**.  It provides examples of enterprise and academic use cases and mentions the **version 4.4 updates** (e.g., improved Hyper-V support, distributed routing, VMware DRS integration, root disk resizing).

**Key Contributions:**  
- Detailed architectural overview of Apache CloudStack and its layered management model (zones, pods, clusters, hosts).  
- Identification of CloudStack’s core strengths:  
  - Simple web and RESTful API interfaces.  
  - AWS EC2/S3 API compatibility for hybrid deployments.  
  - Automated provisioning and elastic scalability.  
- Clear explanation of administrative hierarchy and API access roles.  
- Summary of major enhancements introduced in CloudStack 4.4.  
- Positioning CloudStack as a **mature, enterprise-ready open-source alternative** for IaaS deployment.


**Limitations and Future Work:**  
The authors note that CloudStack’s **modularity is less customizable** than other frameworks like OpenStack.  
Backup and restore mechanisms are limited, and Fiber Channel storage is the only fully supported option through hypervisors.  
Future work is directed toward improving **dynamic reconfiguration**, **data security**, and **system performance**, as well as addressing flexibility through plug-ins and advanced monitoring tools.

**Relevance to Current Project:**  
Although all of this, this paper is kind of old and some of the problems pointed before could now be solved.

**DOI / Link:** [None]
