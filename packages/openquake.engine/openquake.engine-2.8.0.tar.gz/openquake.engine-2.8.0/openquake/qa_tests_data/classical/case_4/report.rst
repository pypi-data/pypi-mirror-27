Classical Hazard QA Test, Case 4
================================

============== ===================
checksum32     796,188,147        
date           2017-11-08T18:07:12
engine_version 2.8.0-gite3d0f56   
============== ===================

num_sites = 1, num_imts = 1

Parameters
----------
=============================== ==================
calculation_mode                'classical'       
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         1                 
truncation_level                0.0               
rupture_mesh_spacing            0.1               
complex_fault_mesh_spacing      0.1               
width_of_mfd_bin                1.0               
area_source_discretization      10.0              
ground_motion_correlation_model None              
random_seed                     1066              
master_seed                     0                 
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gsim_logic_tree.xml <gsim_logic_tree.xml>`_                
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
====== ================ ========= ========== ==========
grp_id gsims            distances siteparams ruptparams
====== ================ ========= ========== ==========
0      SadighEtAl1997() rrup      vs30       mag rake  
====== ================ ========= ========== ==========

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=1, rlzs=1)
  0,SadighEtAl1997(): [0]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== =========== ============ ============
source_model     grp_id trt                  num_sources eff_ruptures tot_ruptures
================ ====== ==================== =========== ============ ============
source_model.xml 0      Active Shallow Crust 1           91           91          
================ ====== ==================== =========== ============ ============

Informational data
------------------
=========================== ========================================================================
count_eff_ruptures.received tot 615 B, max_per_task 615 B                                           
count_eff_ruptures.sent     sources 1.06 KB, srcfilter 684 B, param 592 B, monitor 328 B, gsims 91 B
hazard.input_weight         91.0                                                                    
hazard.n_imts               1                                                                       
hazard.n_levels             3                                                                       
hazard.n_realizations       1                                                                       
hazard.n_sites              1                                                                       
hazard.n_sources            1                                                                       
hazard.output_weight        3.0                                                                     
hostname                    tstation.gem.lan                                                        
require_epsilons            False                                                                   
=========================== ========================================================================

Slowest sources
---------------
====== ========= ================= ============ ========= ========= =========
grp_id source_id source_class      num_ruptures calc_time num_sites num_split
====== ========= ================= ============ ========= ========= =========
0      1         SimpleFaultSource 91           0.003     1         1        
====== ========= ================= ============ ========= ========= =========

Computation times by source typology
------------------------------------
================= ========= ======
source_class      calc_time counts
================= ========= ======
SimpleFaultSource 0.003     1     
================= ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ===== ====== ===== ===== =========
operation-duration mean  stddev min   max   num_tasks
count_eff_ruptures 0.004 NaN    0.004 0.004 1        
================== ===== ====== ===== ===== =========

Slowest operations
------------------
============================== ========= ========= ======
operation                      time_sec  memory_mb counts
============================== ========= ========= ======
reading composite source model 0.020     0.0       1     
total count_eff_ruptures       0.004     0.0       1     
store source_info              0.003     0.0       1     
prefiltering source model      0.002     0.0       1     
managing sources               0.002     0.0       1     
reading site collection        4.411E-05 0.0       1     
saving probability maps        2.909E-05 0.0       1     
aggregate curves               1.884E-05 0.0       1     
============================== ========= ========= ======