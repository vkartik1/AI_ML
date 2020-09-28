set serveroutput on
set echo off
set verify off
-- 
-- Create the Settings table for the model
--

DECLARE
 
BEGIN -- test1

  -- SVM Settings
  insert into AIML_SVM_PS_SETTINGS values (dbms_data_mining.algo_name, dbms_data_mining.algo_support_vector_machines);
  insert into AIML_SVM_PS_SETTINGS values (dbms_data_mining.svms_kernel_function, dbms_data_mining.svms_linear);
  insert into AIML_SVM_PS_SETTINGS values (dbms_data_mining.prep_auto, dbms_data_mining.prep_auto_on);

  -- Random Forest Settings
  insert into AIML_RF_PS_SETTINGS values (dbms_data_mining.algo_name, dbms_data_mining.algo_random_forest);
  insert into AIML_RF_PS_SETTINGS values (dbms_data_mining.rfor_num_trees, 25);

  -- Naive Bayes
  insert into AIML_NB_PS_SETTINGS values (dbms_data_mining.algo_name, dbms_data_mining.algo_naive_bayes);
   
  -- Create the model in parallel mode ?
  if ('&1' = 'PARALLEL') then
    insert into AIML_SVM_PS_SETTINGS values (dbms_data_mining.odms_partition_columns, 'CATEGORY');
    insert into AIML_RF_PS_SETTINGS  values (dbms_data_mining.odms_partition_columns, 'CATEGORY');
    insert into AIML_NB_PS_SETTINGS  values (dbms_data_mining.odms_partition_columns, 'CATEGORY');
    dbms_output.put_line('Parallel (Partition)   = True'); 
  else
    dbms_output.put_line('Parallel (Partition)   = False'); 
  end if;

END;

/
  
quit;
