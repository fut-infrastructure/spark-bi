from pathling import PathlingContext  # pyright: ignore[reportMissingTypeStubs]
from pyspark.sql import SparkSession


class FutPathlingContext:
    FORBIDDEN_SPARK_KEY = {  # noqa: RUF012
        "spark.deploy.defaultCores": "can hog all cores in the cluster",
        "spark.dynamicAllocation.enabled": "will never release resources",
        "spark.dynamicAllocation.shuffleTracking.enabled": "can block dynamic resource allocation",
        "spark.dynamicAllocation.initialExecutors": "can hog all resources in the cluster",
    }

    @staticmethod
    def create(
        app_name: str,
        spark_master_url: str = "spark://spark-master-svc.bi-tools.svc.cluster.local:7077",
        spark_additional_config: dict[str, str] | None = None,
        hadoop_config: dict[str, str] | None = None,
    ) -> PathlingContext:
        import socket

        ip = socket.gethostbyname(socket.gethostname())
        return FutPathlingContext._create(
            app_name,
            spark_driver_host=ip,
            spark_master_url=spark_master_url,
            spark_additional_config=spark_additional_config,
            hadoop_config=hadoop_config,
        )

    @staticmethod
    def _create(
        app_name: str,
        spark_driver_host: str,
        spark_master_url: str = "spark://spark-master-svc.bi-tools.svc.cluster.local:7077",
        spark_additional_config: dict[str, str] | None = None,
        hadoop_config: dict[str, str] | None = None,
    ) -> PathlingContext:
        sparkConfig = SparkSession.builder.appName(app_name).master(spark_master_url)

        if spark_additional_config is None:
            spark_additional_config = {}

        # XXX: Monkey-patch the ip-address so users don't need to pass it
        if hadoop_config is None:
            hadoop_config = {}

        default_spark_config = {
            "spark.jars.packages": ",".join(
                ["au.csiro.pathling:library-runtime:9.1.0", "io.delta:delta-spark_2.13:4.0.0"]
            ),
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.driver.host": spark_driver_host,
            "spark.driver.bindAddress": "0.0.0.0",
            "spark.deploy.defaultCores": "1",
            "spark.dynamicAllocation.enabled": "true",
            "spark.dynamicAllocation.shuffleTracking.enabled": "true",
            "spark.dynamicAllocation.initialExecutors": "1",
        }

        for key, value in default_spark_config.items():
            sparkConfig.config(key, value)

        for key, value in spark_additional_config.items():
            for forbidden_key, reason in FutPathlingContext.FORBIDDEN_SPARK_KEY.items():
                if key.lower() == forbidden_key.lower():
                    raise ValueError(
                        f"Overriding '{forbidden_key}' is forbidden. Changing it {reason}."
                    )

            sparkConfig.config(key, value)

        spark = sparkConfig.getOrCreate()

        for key, value in (hadoop_config or {}).items():
            spark._jsc.hadoopConfiguration().set(key, value)  # type: ignore

        pc = PathlingContext.create(spark)
        return pc
