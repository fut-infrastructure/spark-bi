from fut_bi.spark import FutPathlingContext

TEST_SPARK_HOST = "127.0.0.1"


def test_can_init():
    result = FutPathlingContext._create(
        spark_driver_host=TEST_SPARK_HOST, appName="TestApp", spark_master_url="local[4]"
    )  # type: ignore
    assert result is not None


def test_uses_additional_config():
    result = FutPathlingContext._create(
        spark_driver_host=TEST_SPARK_HOST,
        appName="TestApp",
        spark_master_url="local[4]",
        spark_additional_config={"spark.some.config": "some_value"},
    )  # type: ignore
    spark = result.spark
    assert spark.conf.get("spark.some.config") == "some_value"


def test_uses_hadoop_config():
    result = FutPathlingContext._create(
        spark_driver_host=TEST_SPARK_HOST,
        appName="TestApp",
        spark_master_url="local[4]",
        hadoop_config={"fs.defaultFS": "hdfs://namenode:8020"},
    )  # type: ignore
    spark = result.spark
    hadoop_conf = spark._jsc.hadoopConfiguration()  # type: ignore
    assert hadoop_conf.get("fs.defaultFS") == "hdfs://namenode:8020"  # pyright: ignore[reportUnknownMemberType]
