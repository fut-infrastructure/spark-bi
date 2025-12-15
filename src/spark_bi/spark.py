import enum
import logging
import os

import pydantic
from pathling import PathlingContext  # pyright: ignore[reportMissingTypeStubs]
from pyspark.sql import SparkSession

log = logging.getLogger(__name__)


def is_jupyter_hub() -> bool:
    return any("JUPYTERHUB" in key for key in list(os.environ))


class S3Credentials(pydantic.BaseModel):
    region: str
    access_key: str
    secret_key: str

    def __post_init__(self):
        # The S3Credentials are not used if not on JupyterHub, so don't need to strictly validate them
        if is_jupyter_hub() and ("DUMMY" in self.access_key or "DUMMY" in self.secret_key):
            raise ValueError(
                "S3Credentials contain dummy values. Contact FUT-S or TRIFORK to get real ones."
            )

    def to_hadoop_config(self) -> dict[str, str]:
        return {
            "fs.s3a.endpoint.region": self.region,
            "fs.s3a.access.key": self.access_key,
            "fs.s3a.secret.key": self.secret_key,
        }


class LogLevel(enum.Enum):
    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"
    TRACE = "TRACE"


class FutPathlingContext:
    FORBIDDEN_SPARK_KEY = {  # noqa: RUF012
        "spark.deploy.defaultCores": "can hog all cores in the cluster",
        "spark.dynamicAllocation.enabled": "will never release resources",
        "spark.dynamicAllocation.shuffleTracking.enabled": "can block dynamic resource allocation",
        "spark.dynamicAllocation.initialExecutors": "can hog all resources in the cluster",
    }

    SHARED_SPARK_CONFIG = {  # noqa: RUF012
        "spark.jars.packages": ",".join(
            ["au.csiro.pathling:library-runtime:9.1.0", "io.delta:delta-spark_2.13:4.0.0"]
        ),
        "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        "spark.driver.memory": "4g",
    }

    @staticmethod
    def create(
        app_name: str,
        spark_master_url: str = "spark://spark-master-svc.bi-tools.svc.cluster.local:7077",
        spark_additional_config: dict[str, str] | None = None,
        hadoop_config: dict[str, str] | None = None,
        spark_log_level: LogLevel = LogLevel.ERROR,
    ) -> PathlingContext:
        import socket

        ip = socket.gethostbyname(socket.gethostname()) if is_jupyter_hub() else "0.0.0.0"
        return FutPathlingContext._create(
            app_name,
            spark_driver_host=ip,
            spark_master_url=spark_master_url,
            spark_additional_config=spark_additional_config,
            hadoop_config=hadoop_config,
            spark_log_level=spark_log_level,
        )

    @staticmethod
    def _create(
        app_name: str,
        spark_driver_host: str,
        spark_master_url: str = "spark://spark-master-svc.bi-tools.svc.cluster.local:7077",
        spark_additional_config: dict[str, str] | None = None,
        hadoop_config: dict[str, str] | None = None,
        spark_log_level: LogLevel = LogLevel.ERROR,
    ) -> PathlingContext:
        sparkConfig = SparkSession.builder.appName(app_name)

        if spark_additional_config is None:
            spark_additional_config = {}

        if hadoop_config is None:
            hadoop_config = {}

        if is_jupyter_hub():
            sparkConfig.master(spark_master_url)

            default_spark_config = {
                **FutPathlingContext.SHARED_SPARK_CONFIG,
                "spark.driver.host": spark_driver_host,
                "spark.driver.bindAddress": "0.0.0.0",
            }
        else:
            log.info("Not in JupyterHub, disregarding spark_driver_host and spark_master_url")

            default_spark_config = FutPathlingContext.SHARED_SPARK_CONFIG

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

        pc.spark.sparkContext.setLogLevel(spark_log_level.value)
        return pc
