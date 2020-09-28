set serveroutput on
set verify off

DECLARE
  data_table_name               VARCHAR2(100) := 'AIML_SUPPLIER_TREND';
  target_column_name            VARCHAR2(100) := 'SUPPLIER';

  svm_model_name                VARCHAR2(100) := 'AIML_SVM_PS';
  rand_forest_model_name        VARCHAR2(100) := 'AIML_RF_PS';
  naive_bayes_model_name        VARCHAR2(100) := 'AIML_NB_PS';

  create_model_trace_file_id    VARCHAR2(100) := 'AIML_MODEL';
  predict_trace_file_id         VARCHAR2(100) := 'AIML_PREDICT';
  item                          VARCHAR2(100) := 'manila booklet envelope' ;
  category                      VARCHAR2(100) := 'Office Equipment, Accessories and Supplies';
  trace_on                      BOOLEAN:=false;

  algorithm_short_form          VARCHAR2(100);
  model_name                    VARCHAR2(100);
  settings_table_name           VARCHAR2(100);

  -- 
  -- Get the model name for a given short form: Defalt value is RF (Random Forest)
  --
  FUNCTION get_model_name(p_algorithm_short_form VARCHAR2) RETURN VARCHAR2 IS
    l_model_name          VARCHAR2(100);
  BEGIN
    SELECT 
    CASE
      WHEN p_algorithm_short_form = 'SVM' THEN svm_model_name
      WHEN p_algorithm_short_form = 'RF'  THEN rand_forest_model_name
      WHEN p_algorithm_short_form = 'NB'  THEN naive_bayes_model_name
      ELSE rand_forest_model_name
    END
    INTO l_model_name
    FROM DUAL;

    RETURN l_model_name;
  END;

  --
  -- This Creates the model for the predict_supplier functionality.
  --
  PROCEDURE create_model(p_model_name VARCHAR2, p_settings_table_name VARCHAR2) IS
    l_trace_file   varchar2(200);
    l_start_time   TIMESTAMP;
  BEGIN
    select sysdate into l_start_time from dual;
    dbms_output.put_line('Model                 = ' || p_model_name);
    dbms_output.put_line('Settings table name   = ' || p_settings_table_name);
    dbms_output.put_line('Creating Model..');
  
    BEGIN
      DBMS_DATA_MINING.DROP_MODEL (model_name          => p_model_name, FORCE => true);
    EXCEPTION WHEN OTHERS THEN
      NULL;
    END;

    if (trace_on) then
      EXECUTE IMMEDIATE 'ALTER SESSION SET sql_trace = true';
      EXECUTE IMMEDIATE 'ALTER SESSION SET tracefile_identifier = ' || create_model_trace_file_id;
      SELECT value into l_trace_file FROM V$DIAG_INFO WHERE NAME = 'Default Trace File';
    END IF;

    DBMS_DATA_MINING.CREATE_MODEL(
      model_name          => p_model_name,
      mining_function     => dbms_data_mining.classification,
      data_table_name     => data_table_name,
      case_id_column_name => NULL,
      target_column_name  => target_column_name,
      settings_table_name => p_settings_table_name);

    if (trace_on) then
      EXECUTE IMMEDIATE 'ALTER SESSION SET sql_trace = false';
      dbms_output.put_line('-------  Trace Files -------');
      dbms_output.put_line('1> Build Model Trace file: '|| l_trace_file);
    END IF;

    dbms_output.put_line('Model creation Done. Time taken (HH:MI:SS): '|| extract( Hour from sysdate - l_start_time ) ||':'|| extract( minute from sysdate - l_start_time ) ||':'||extract( second from sysdate - l_start_time ));

  END;

  -- 
  -- Predicts the supplier for a given item and categor. 
  -- create_model should have been invoked before predict is called
  --
  PROCEDURE PREDICT(p_model_name VARCHAR2, p_item VARCHAR2, p_category VARCHAR2) IS
    l_item              varchar2(2000);
    l_category          varchar2(512);
    l_supplier          varchar2(512);
    l_probability       NUMBER;
    l_trace_file        varchar2(200);
    l_start_time        timestamp;
    l_predict_sql_stmt  varchar2(1000);
  BEGIN
    select sysdate into l_start_time from dual;

    if (trace_on) then
      EXECUTE IMMEDIATE 'ALTER SESSION SET sql_trace = true';
      EXECUTE IMMEDIATE 'ALTER SESSION SET tracefile_identifier = ' || predict_trace_file_id ;
      SELECT value into l_trace_file FROM V$DIAG_INFO WHERE NAME = 'Default Trace File';
    END IF;
  
    l_predict_sql_stmt := 'SELECT
      item_description,
      category,
      PREDICTION('|| p_model_name || ' USING *) predicted_supplier,
      PREDICTION_PROBABILITY(' || p_model_name || ' USING *) predicted_supplier
    FROM
      (select ''' || p_item || ''' ITEM_DESCRIPTION, '''|| p_category || ''' CATEGORY 
      from dual)' ;

    EXECUTE IMMEDIATE l_predict_sql_stmt into       l_item, l_category, l_supplier, l_probability    ;

    if (trace_on) then
      EXECUTE IMMEDIATE 'ALTER SESSION SET sql_trace = false';
      dbms_output.put_line('2> Prediction Trace file: '|| l_trace_file);
    END IF;
  
    dbms_output.put_line('-------  Input -------');
    dbms_output.put_line('Item                  = ' || l_item);
    dbms_output.put_line('Category              = ' || l_category);
    dbms_output.put_line('-------  Prediction -------');
    dbms_output.put_line('Predicted Supplier    = ' || l_supplier);
    dbms_output.put_line('Probability           = ' || l_probability);
    dbms_output.put_line('-------  End -------');
  END;


  --
  -- Read Model name and sql tracin (true/false) are optional command line parameters
  --
  PROCEDURE get_cmd_line_params(p_algorithm_short_form VARCHAR2, p_trace_on VARCHAR2) IS
  BEGIN
    algorithm_short_form := p_algorithm_short_form;
    if (p_trace_on = 'TRACE_OFF') then
      trace_on := false;
      dbms_output.put_line('sql_trace             = False'); 
    else
      trace_on := true;
      dbms_output.put_line('sql_trace             = True');
    end if;

    dbms_output.put_line('Algorithm Short Code  = ' || algorithm_short_form);
  END;

--
-- Main Logic starts here
--
BEGIN
  get_cmd_line_params('&1', '&2');
  model_name          := get_model_name(algorithm_short_form);
  settings_table_name := model_name||'_SETTINGS';

  create_model(model_name, settings_table_name);
  predict(model_name, item, category);
END;
/
quit;
