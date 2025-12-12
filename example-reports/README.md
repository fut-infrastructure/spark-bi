# Opsætning
De vigtigste afhængigheder er:
* Pakken i dette repository
* Pathling
* Spark

Pakken i dette repository gør forbindelse til Spark-clusteren (der, hvor beregningerne udføres) og S3-bucket'en (der, hvor data ligger) så nem som mulig for brugeren. 

Pathling tillader at skrive [FHIRPath](https://www.whitefox.cloud/articles/fhirpath-explained/) queries på data, så vi kan lave traditionelle SQL-agtige views, som derefter kan joines sammen med normal Spark-syntaks til det endelige resultat. 

Alle eksemplerne følger denne fremgangsmåde.

### Deling a Jupyter Notebooks
Bemærk at Jupyter Notebooks cacher deres resultater _i filen_. Når du kører på testdata kan du se bort fra dette, men hvis resultaterne indeholder personfølsom information vil disse være indeholdt i notebook'en. Du bør derfor _ikke_ pushe dem til `fut-infrastructure/spark-bi`.

### Kørsel på JupyterHub
1. Åben en ny terminal
2. `cd spark-bi`
3. `pip install -e .`
4. Du er nu klar til at køre notebooks.

### Kørsel lokalt
Kørsel lokalt kræver at der findes et delta-lake udtræk lokalt. Et test-udtræk med det rette skema kan rekvireres fra FUT-S/TRIFORK. Dataene skal placeres samme sted som i `data_location.py`, eller der skal rettes i denne fil.

Den nemmeste opsætning er med `uv`, den klart bedste package-manager til Python. Guide til opsætning [her](https://docs.astral.sh/uv/guides/install-python/).

1. Kør `uv sync` i roden af projektet
2. Åben en notebook i VSCode
3. Tryk "run all"
4. Vælge "Python environments" -> Miljøet i den aktuelle mappe

Resultaterne dukker op.

# Data
Rapporterne her er kørt på data fra TRIFORKs testmiljø. Derfor afspejler resultaterne _ikke_ produktion, og ser meget underlige ud.

# FHIRPath
FHIRPath queries kan med fordel testes på en testresource på [denne hjemmeside](https://hl7.github.io/fhirpath.js/). Hvis FHIRPath-udtrykket bruger relevante funktioner, men f.eks. efterspørger en extension der ikke findes på ressorucen, vil Pathling blot returnere "None" som værdi.

Pathling har desuden en række eksempler i deres [dokumentation](https://pathling.csiro.au/docs/libraries/examples/prostate-cancer).

### Detaljer
* Jeg (Martin Bernstorff) har snakket med Systematic (Erik). Vi kan godt bruge `managingOrganization.first()` fordi den faktiske kardinalitet af managingOrganization er 0..1. De har ikke opdateret IG'en til at afpsejle det, og prioriterer det ikke højt.