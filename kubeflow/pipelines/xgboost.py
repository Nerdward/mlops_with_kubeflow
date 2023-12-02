import kfp
from kfp import components


chicago_taxi_dataset_op = components.load_component_from_file("/home/azureuser/kubeflow/components/datasets/ChicagoTaxi/component.yaml")
convert_csv_to_apache_parquet_op = components.load_component_from_file("/home/azureuser/kubeflow/components/converters/ApacheParquet/from_CSV/component.yaml")
xgboost_train_on_parquet_op = components.load_component_from_file("/home/azureuser/kubeflow/components/XGBoost/Train/from_ApacheParquet/component.yaml")
xgboost_predict_on_parquet_op = components.load_component_from_file("/home/azureuser/kubeflow/components/XGBoost/Predict/from_ApacheParquet/component.yaml")

@kfp.dsl.pipeline(name='xgboost')
def xgboost_pipeline():
    training_data_csv = chicago_taxi_dataset_op(
        where='trip_start_timestamp >= "2019-01-01" AND trip_start_timestamp < "2019-02-01"',
        select='tips,trip_seconds,trip_miles,pickup_community_area,dropoff_community_area,fare,tolls,extras,trip_total',
        limit=10000,
    ).output

    # Training and prediction on dataset in Apache Parquet format
    training_data_parquet = convert_csv_to_apache_parquet_op(
        data=training_data_csv
    ).output

    model_trained_on_parquet = xgboost_train_on_parquet_op(
        training_data=training_data_parquet,
        label_column_name='tips',
        objective='reg:squarederror',
        num_iterations=200,
    ).outputs['model']

    xgboost_predict_on_parquet_op(
        data=training_data_parquet,
        model=model_trained_on_parquet,
        label_column_name='tips',
    )


if __name__ == '__main__':
    # kfp_endpoint="http://localhost:8080"
    # kfp.Client(host=kfp_endpoint).create_run_from_pipeline_func(xgboost_pipeline,
    #                                                             mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
    #                                                             arguments={})
    kfp.compiler.Compiler().compile(
    pipeline_func=xgboost_pipeline,
    package_path='pipeline.yaml')