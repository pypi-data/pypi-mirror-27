QA test for blocksize independence (hazard)
===========================================

============== ===================
checksum32     1,989,351,768      
date           2017-11-08T18:07:34
engine_version 2.8.0-gite3d0f56   
============== ===================

num_sites = 2, num_imts = 1

Parameters
----------
=============================== ==================
calculation_mode                'event_based'     
number_of_logic_tree_samples    1                 
maximum_distance                {'default': 400.0}
investigation_time              5.0               
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            10.0              
complex_fault_mesh_spacing      10.0              
width_of_mfd_bin                0.5               
area_source_discretization      10.0              
ground_motion_correlation_model None              
random_seed                     42                
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source                  `source_model.xml <source_model.xml>`_                      
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ====== =============== ================
smlt_path weight gsim_logic_tree num_realizations
========= ====== =============== ================
b1        1.000  trivial(1)      1/1             
========= ====== =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ================= =========== ======================= =================
grp_id gsims             distances   siteparams              ruptparams       
====== ================= =========== ======================= =================
0      ChiouYoungs2008() rjb rrup rx vs30 vs30measured z1pt0 dip mag rake ztor
====== ================= =========== ======================= =================

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=1, rlzs=1)
  0,ChiouYoungs2008(): [0]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== =========== ============ ============
source_model     grp_id trt                  num_sources eff_ruptures tot_ruptures
================ ====== ==================== =========== ============ ============
source_model.xml 0      Active Shallow Crust 5           10,399       13,823      
================ ====== ==================== =========== ============ ============

Informational data
------------------
========================= ====================================================================================
compute_ruptures.received tot 36.62 KB, max_per_task 4.53 KB                                                  
compute_ruptures.sent     sources 485.48 KB, src_filter 10.43 KB, param 8.8 KB, monitor 4.78 KB, gsims 1.44 KB
hazard.input_weight       2583.4                                                                              
hazard.n_imts             1                                                                                   
hazard.n_levels           4                                                                                   
hazard.n_realizations     1                                                                                   
hazard.n_sites            2                                                                                   
hazard.n_sources          5                                                                                   
hazard.output_weight      0.1                                                                                 
hostname                  tstation.gem.lan                                                                    
require_epsilons          False                                                                               
========================= ====================================================================================

Slowest sources
---------------
====== ========= ============ ============ ========= ========= =========
grp_id source_id source_class num_ruptures calc_time num_sites num_split
====== ========= ============ ============ ========= ========= =========
0      2         AreaSource   2,334        0.0       2         0        
0      1         AreaSource   7,020        0.0       2         0        
0      9         AreaSource   897          0.0       2         0        
0      8         AreaSource   1,812        0.0       1         0        
0      3         AreaSource   1,760        0.0       2         0        
====== ========= ============ ============ ========= ========= =========

Computation times by source typology
------------------------------------
============ ========= ======
source_class calc_time counts
============ ========= ======
AreaSource   0.0       5     
============ ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
compute_ruptures   0.254 0.162  0.003 0.396 15       
================== ===== ====== ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
total compute_ruptures         3.804     0.0       15    
reading composite source model 1.642     0.0       1     
managing sources               0.737     0.0       1     
saving ruptures                0.011     0.0       15    
store source_info              0.006     0.0       1     
prefiltering source model      0.005     0.0       1     
setting event years            0.002     0.0       1     
filtering ruptures             8.533E-04 0.0       3     
reading site collection        4.458E-05 0.0       1     
============================== ========= ========= ======