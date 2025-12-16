import enum


class ColNames(enum.Enum):
    CREATING_SOLUTION = "creating_solution"
    MUNICIPALITY_CODE = "municipality_code"
    REGION_CODE = "region_code"


class Extensions(enum.Enum):
    DK_CORE_MUNICIPALITY_CODES = (
        "http://hl7.dk/fhir/core/StructureDefinition/dk-core-municipalityCodes"
    )
    DK_CORE_REGIONAL_SUBDIVISION_CODES = (
        "http://hl7.dk/fhir/core/StructureDefinition/dk-core-RegionalSubDivisionCodes"
    )

    HL7_EPISODE_OF_CARE = "http://hl7.org/fhir/StructureDefinition/workflow-episodeOfCare"

    EHEALTH_COLOCATION = "http://ehealth.sundhed.dk/cs/ehealth-system"
    EHEALTH_MUNICIPALITY_CODES = (
        "http://ehealth.sundhed.dk/fhir/StructureDefinition/ehealth-organization-municipalityCode"
    )
    EHEALTH_REGION_CODES = (
        "http://ehealth.sundhed.dk/fhir/StructureDefinition/ehealth-organization-regionCode"
    )
