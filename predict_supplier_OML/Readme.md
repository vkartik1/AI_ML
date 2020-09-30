# Prediction Using Oracle Machine Language (OML)

### Overview 
This project
1. Creates a model using the DBMS_DATA_MINING.CREATE_MODEL procedure and. 
2. Recommends the supplier and its probability using the 2 OML plsql functions: PREDICTION and PREDICTION_PROBABILITY. 


### How to run  

1. Update the TNS info in the db_info file 

2. Run the command "./run" to create model, do prediction. 
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
 
     Parameter position doesnt matter. 
     Below command uses Random Forest model for 10K rows and with trace off and parallel=off.   
       ./run trace_off 10000 
  
3. The ./run will print predicted supplier and will also print 2 trace filenames (, if trace_on,) of the below format. 
&ensp;     Model creation trace filename : *AIML_MODEL.trc. 
&ensp;     Prediction trace filename     : *AIML_PREDICT.trc. 

###  Optional Read from here on - Feel free to skip

#### Files 
1. db_info                : Override the db/tns info here.   
2. run                    : Main script to be run to create model and do supplier prediction.    
                            The run script uses the below files.   
3. create_tables.sql      : Create the 2 tables needed for model creation to work.   
4. populate_settings.sql  : Populate the settings tables.    
5. input_data.txt         : Trend data to be loaded, based on which prediction will be done.   
6. input_data.ctl         : Sqlldr Control file for the input_data.txt.    
7. model_and_predict.sql  : Creates the model and calls the prediction sql to predict the supplier for item='manila booklet envelope' and category='Office Equipment, Accessories and Supplies'. This prints the predicted supplier, probability and the trace files for the model creation API and prediction SQL.   

#### Methods for which the SQL trace is being collected 
Copied from the model_and_predict.sql

1> Model creation API for whch Tracing is being done.     
&ensp;    DBMS_DATA_MINING.CREATE_MODEL(. 
&ensp;      model_name          => 'SVM_PREDICT_SUPPLIER',  
&ensp;      mining_function     => dbms_data_mining.classification,  
&ensp;      data_table_name     => 'AIML_SUPPLIER_TREND',  
&ensp;      case_id_column_name => NULL,  
&ensp;      target_column_name  => 'supplier',  
&ensp;      settings_table_name => 'SVM_MODEL_SETTINGS');  
  
2> Prediction SQL for which tracing is being done.   
&ensp;    SELECT. 
&ensp;      item_description,  
&ensp;      category,  
&ensp;      PREDICTION(SVM_PREDICT_SUPPLIER USING *) predicted_supplier,  
&ensp;      PREDICTION_PROBABILITY(SVM_PREDICT_SUPPLIER USING *) predicted_supplier. 
&ensp;   INTO. 
&ensp;      l_item,  
&ensp;      l_category,  
&ensp;      l_supplier,  
&ensp;      l_prob
&ensp;    FROM  
&ensp;      (select 'manila booklet envelope' ITEM_DESCRIPTION, 'Office Equipment, Accessories and Supplies' CATEGORY. 
&ensp;      from dual);  
                          
