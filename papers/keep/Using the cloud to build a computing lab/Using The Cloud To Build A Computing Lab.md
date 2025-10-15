### Using the cloud to build a computing lab (Samuel Alves, Paula Prata, 2014)

**Problem Statement:**  
Managing university computer laboratories is both costly and inflexible.  
In traditional setups, all machines must be pre-installed with operating systems and software in advance, which limits adaptability and increases maintenance overhead.  
IT teams are under pressure to provide the right resources at minimal cost, while ensuring that each class has the necessary computing environment.  
This static model restricts instructors to pre-defined software configurations, preventing experimentation or dynamic adaptation during the semester.  

The authors propose leveraging *cloud computing* to provision and release computing resources on demand, allowing teachers and students to create and manage customized laboratory environments dynamically, without the need for specialized technical knowledge.


**Objectives:**  
Develop **CSCLab (Computer Science Cloud Laboratory)** — a plataform that enables users without cloud knowledge to create, edit and manage virtual labs for classes. This soluction was implement in a Openstack*private cloud*. Also they had the idea to use multi-cloud enviroments. 

**Proposed Solution:**  
- **Architecture:** The CSCLab consists of a *private cloud* based on OpenStack (Havana version) and a web application with a database.  
  - **OpenStack services:** Keystone (authentication), Glance (image management), Nova (compute), Cinder (block storage), and Neutron (networking).  
  - The web application follows the MVC model (PHP/CodeIgniter) with a MySQL database and communicates with OpenStack through the *php-opencloud* SDK.  

- **Data model and roles:**  
  There are three main roles — **administrator**, **lab manager**, and **student** — each with different privileges.  
  The CSCLab database stores entities such as laboratories, images, classes, software, users, and associations, while directly referencing OpenStack’s internal tables (e.g., `glance.images`, `nova.instances`, `cinder.volumes`, `keystone.*`, `neutron.*`) to avoid data duplication.  

- **Laboratory creation:**  
  A laboratory is defined by an image, a number of virtual machines (VMs), networks, and optionally a pool of *floating IPs*.  
  Each class or lab is isolated using a “one router per *tenant*” topology in Neutron.  
  Access to VMs can be provided via *floating IPs* (SSH, VNC, RDP).  
  Lab managers can customize base images, create *snapshots*, and reuse them in future classes.  

- **Student persistence:**  
  Instead of keeping a dedicated VM running for each student, every student receives a personal Cinder volume to store their data.  
  These volumes can be attached or detached between labs and even transferred between *tenants* using the **`cinder-transfer`** command.  
  User-specific credentials and volume mounts are injected via *cloud-config/User-Data*.  

- **Monitoring:**  
  The *logging* system records predefined actions (such as program executions or VM restarts), enabling auditing by lab managers.  

**Evaluation:**  
A minimal two-node *private cloud* (controller + compute) was implemented using Ubuntu 13.10.  
Most backend services were validated — image creation, *flavors*, networks, *snapshots*, volume attach/detach/transfer — although the web interface was still under development.  
No quantitative performance metrics were provided; the evaluation focused on functional validation.  

**Key Contributions:**  
- A practical, role-based platform (CSCLab) for building educational virtual laboratories on OpenStack.  
- A data model integrated with OpenStack databases and a network topology isolated per *tenant*.  
- A lightweight per-user persistence model using detachable Cinder volumes and *tenant*-to-*tenant* transfer.  
- An initial analysis of multi-*cloud* management tools for this use case.  

**Limitations and Future Work:**  
- **Multi-cloud:** The tested tools presented several limitations.  
  - *CompatibleOne* could not be made fully operational.  
  - *Scalr* worked but disabled key OpenStack features (such as Neutron network details and Cinder volume transfer management).  
  As a result, multi-*cloud* support remained incomplete and was identified as an area for future work.  
- **Web Interface:** The web interface was still under development at the time of publication.  

**Relevance to Current Project:**  
This paper gives useful insights to build a Cloud Lab:  
1. Isolate every class/lab with a independent *tenant* OpenStack.  
2. Assign persistence volumes to every student instead of VM persistence.  
3. Use *snapshots* to create Images based on previously created images.  
4. Log every user activity.

**DOI / Link:** [None]  

