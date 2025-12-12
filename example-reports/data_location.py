from pathlib import Path

from spark_bi.spark import is_jupyter_hub

LOCAL_DELTA = str(Path.home() / "data" / "fut-bi-delta-lake")
CLOUD_DELTA = "s3a://fut-trifork-bi-export/delta-lake"

DELTA_LOCATION = CLOUD_DELTA if is_jupyter_hub() else LOCAL_DELTA
