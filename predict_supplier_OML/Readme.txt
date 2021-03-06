# Prediction Using Oracle Machine Language (OML)

### Overview 
This project
1) Creates a model using the DBMS_DATA_MINING.CREATE_MODEL procedure and 
2) Predicts the supplier and its probability using the 2 OML plsql functions: PREDICTION and PREDICTION_PROBABILITY


### How to run  

1) Update the TNS info in the db_info file 

2) Run the command "./run" to create model, do prediction. 
      ./run [svm/rf/nb] [data set size] [trace_on/trace_off] [parallel]

   Default command line value 
   a) Algorithm     = Random Forest Algorithm, 
   b) Data set size = All
   c) SQL Trace     = Off
   d) Parallel      = Off

     e.g. 
      ./run svm 10000 trace_on parallel

     Below command will run the model creation + prediction for Random forest,entire input data set, trace OFF and parallel OFF  
       ./run 
 
     Parameter position doesnt matter 
     Below command uses Random Forest model for 10K rows and with trace off and parallel=off
       ./run trace_off 10000 
  
3) The ./run will print predicted supplier and will also print 2 trace filenames (, if trace_on,) of the below format
     Model creation trace filename: *AIML_MODEL.trc
     Prediction trace filename    : *AIML_PREDICT.trc

###  Optional Read from here on - Feel free to skip

#### Files 
db_info               : Override the db/tns info here
run                   : Main script to be run to create model and do supplier prediction. 
                        The run script uses the below files 
  create_tables.sql                  : Create the 2 tables needed for model creation to work
  populate_settings.sql              : Populate the settings tables (e.g. 
  input_data.txt                     : Trend data to be loaded, based on which prediction will be done
  input_data.ctl                     : sqlldr Control file for the input_data.txt 
  model_and_predict.sql              : creates the model and calls the prediction sql to predict the supplier for
                                       item='manila booklet envelope' and category='Office Equipment, Accessories and Supplies'
                                       This prints the predicted supplier, the trace files for 
                                       a) model creation API and b) prediction SQL
  predict.trc                        : Sample trace file for the PREDICTION and PREDICTION_PROBABILITY APIs
  create_model.trc                   : Sample trace file for the DBMS_DATA_MINING.CREATE_MODEL

#### Methods for which the SQL trace is being collected 
Copied from the model_and_predict.sql

1> Model creation API for whch Tracing is being done
    DBMS_DATA_MINING.CREATE_MODEL(
      model_name          => 'SVM_PREDICT_SUPPLIER',
      mining_function     => dbms_data_mining.classification,
      data_table_name     => 'AIML_SUPPLIER_TREND',
      case_id_column_name => NULL,
      target_column_name  => 'supplier',
      settings_table_name => 'SVM_MODEL_SETTINGS');

2> Prediction SQL for which tracing is being done
    SELECT
      item_description,
      category,
      PREDICTION(SVM_PREDICT_SUPPLIER USING *) predicted_supplier,
      PREDICTION_PROBABILITY(SVM_PREDICT_SUPPLIER USING *) predicted_supplier
   INTO
      l_item,
      l_category,
      l_supplier,
      l_prob
    FROM
      (select 'manila booklet envelope' ITEM_DESCRIPTION, 'Office Equipment, Accessories and Supplies' CATEGORY
      from dual);
                          
