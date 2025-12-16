import pyspark
import pyspark.sql
from pathling import DataSource
from pyspark.sql.functions import col, when

from spark_bi.constants import ColNames, Extensions


def compute_patient2municipality(delta_lake: DataSource) -> pyspark.sql.DataFrame:
    patients_with_municipality = delta_lake.view(
        resource="Patient",
        select=[
            {
                "column": [
                    {"name": "patient_id", "path": "getResourceKey()"},
                    {
                        "name": ColNames.MUNICIPALITY_CODE.value,
                        "path": "address.where(use = 'home').extension('http://hl7.dk/fhir/core/StructureDefinition/dk-core-municipalityCodes').valueCodeableConcept.coding.code",
                    },
                ]
            }
        ],
    )
    return patients_with_municipality


def compute_patient2region(delta_lake: DataSource) -> pyspark.sql.DataFrame:
    patients_with_region = delta_lake.view(
        resource="Patient",
        select=[
            {
                "column": [
                    {"name": "patient_id", "path": "getResourceKey()"},
                    {
                        "name": ColNames.REGION_CODE.value,
                        "path": "address.where(use = 'home').extension('http://hl7.dk/fhir/core/StructureDefinition/dk-core-RegionalSubDivisionCodes').valueCodeableConcept.coding.code",
                    },
                ]
            }
        ],
    )

    # Map regional subdivision codes to region names in Spark
    # See https://hl7.dk/fhir/core/1.1.0/ValueSet-dk-core-RegionalSubDivisionCodes.html
    return add_region_name_col(patients_with_region)


def add_region_name_col(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    # Map regional subdivision codes to region names in Spark
    # See https://hl7.dk/fhir/core/1.1.0/ValueSet-dk-core-RegionalSubDivisionCodes.html
    df_mapped = df.withColumn(
        "region_name",
        (
            when(col(ColNames.REGION_CODE.value) == "DK-81", "Nord Denmark Region")
            .when(col(ColNames.REGION_CODE.value) == "DK-82", "Central Denmark Region")
            .when(col(ColNames.REGION_CODE.value) == "DK-83", "Region of Southern Denmark")
            .when(col(ColNames.REGION_CODE.value) == "DK-84", "Capital Region of Denmark")
            .when(col(ColNames.REGION_CODE.value) == "DK-85", "Region Zealand")
            .otherwise(None)
        ),
    )
    return df_mapped


def compute_patient2condition(delta_lake: DataSource) -> pyspark.sql.DataFrame:
    conditions_with_code = delta_lake.view(
        resource="Condition",
        select=[
            {
                "column": [
                    {"name": "condition_id", "path": "getResourceKey()"},
                    {"name": "diagnosis_code", "path": "code.coding.code"},
                ]
            }
        ],
    )

    careplans_with_eoc = delta_lake.view(
        resource="CarePlan",
        select=[
            {
                "column": [
                    {"name": "cp_id", "path": "getResourceKey()"},
                    {
                        "name": "cp_eoc_id",
                        "path": "extension.where(url='http://hl7.org/fhir/StructureDefinition/workflow-episodeOfCare').valueReference.getReferenceKey()",
                    },
                    {"name": "addresses_condition", "path": "addresses.getReferenceKey()"},
                ]
            }
        ],
    )

    eoc_with_pt_id = delta_lake.view(
        resource="EpisodeOfCare",
        select=[
            {
                "column": [
                    {"name": "eoc_id", "path": "getResourceKey()"},
                    {"name": "eoc_patient_id", "path": "patient.getReferenceKey()"},
                ]
            }
        ],
    )

    patient2condition = (
        conditions_with_code.join(
            careplans_with_eoc,
            conditions_with_code["condition_id"] == careplans_with_eoc["addresses_condition"],
            how="inner",
        )
        .join(
            eoc_with_pt_id, careplans_with_eoc["cp_eoc_id"] == eoc_with_pt_id["eoc_id"], how="inner"
        )
        .select("eoc_patient_id", "diagnosis_code")
        .distinct()
    )

    return patient2condition
