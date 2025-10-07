### Spark SQL: Relational Data Processing in Spark (Michael Armbrust, Reynold Xin, Cheng Lian, Yin Huai, Davies Liu, Joseph K. Bradley, Xiangrui Meng, Tomer Kaftan, M. Franklin, A. Ghodsi, M. Zaharia, 2015)

**Problem Statement:**  
The paper addresses the challenge of transforming computing into a utility service — making IT resources as accessible and scalable as electricity. It explores how cloud computing can solve problems of over- and under-provisioning, cost inefficiency, and limited scalability in traditional datacenter models.

**Objectives:**  
The authors aim to define Cloud Computing clearly, compare it with prior paradigms, and analyze the economic and technical foundations that make it viable. They also seek to identify obstacles and opportunities for cloud growth and adoption.

**Proposed Solution:**  
The paper proposes viewing Cloud Computing as the combination of Software as a Service (SaaS) and Utility Computing, focusing on elasticity, on-demand self-service, and pay-per-use economics.
It highlights the enabling role of large-scale, commodity hardware datacenters (e.g., Amazon EC2, Google AppEngine, Microsoft Azure) and introduces a taxonomy for cloud service abstraction levels — from low-level virtual machines (IaaS) to high-level application frameworks (PaaS).

**Evaluation:**  
The evaluation is conceptual and economic rather than experimental. The authors present cost analyses showing how elasticity reduces both over- and under-provisioning risks, and they quantify scenarios comparing fixed datacenter costs vs. pay-as-you-go cloud pricing. They also list the top 10 obstacles and corresponding opportunities for cloud growth (e.g., data lock-in, confidentiality, scalability, software licensing).

**Key Contributions:**  
- [List the most important findings or innovations]  
- [Mention any unique aspect compared to prior work]

**Limitations and Future Work:**  
The study notes that [limitations]. Future directions include [suggested work].

**Relevance to Current Project:**  
This paper provides the conceptual and historical foundation for the DI cloud infrastructure project, defining key principles such as elasticity, on-demand provisioning, and resource pooling.
While its economic perspective focused on the public-cloud model and utility pricing — less relevant to today’s academic private-cloud environments — its architectural insights remain crucial.
The notions of scalable resource abstraction, automated provisioning, and service layering (IaaS, PaaS, SaaS) directly inform the design and management of the DI’s internal cloud infrastructure, guiding how resources can be dynamically allocated and monitored.

**DOI / Link:** [None]
