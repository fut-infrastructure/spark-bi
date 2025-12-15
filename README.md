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
2. Hvis du ikke allerede har gjort det, så klon det nuværende repository (`git clone https://github.com/fut-infrastructure/spark-bi/`)
3. `cd spark-bi`
4. `pip install -e .`
5. Kontakt FUT-S/TRIFORK for at få log-in information til S3 (dataopbevaring). Kopiér `credentials_example.py` til `credentials.py`, og udfyld værdierne.
6. Du er nu klar til at køre notebooks.

### Kørsel lokalt
Kørsel lokalt kræver at der findes et delta-lake udtræk lokalt. Et test-udtræk med det rette skema kan rekvireres fra FUT-S/TRIFORK. Dataene skal placeres samme sted som i `data_location.py`, eller der skal rettes i denne fil.

Den nemmeste opsætning er med `uv`, den bedste package-manager til Python. Guide til opsætning [her](https://docs.astral.sh/uv/guides/install-python/).

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

# Performance
Som udgangspunkt, så skalerer Spark selv antallet af cores, hukommelse of executors, hvis en query tager lang tid. Hvis der er brug for manuel kontrol, kan `FutPathlingContext.create` tage spark parametre:
* `spark.cores.max`: hvor mange cores der kan allokeres til jobbet på tværs af executors (total cores)
* `spark.executor.cores`: hvor mange cores der allokeres til hver executor (worker JVM)
* `spark.executor.memory`: hvor meget hukommelse der allokeres til hver executor (worker JVM)

Sparks dokumentation giver et fint overblik over disse:
* [Spark Cluster Mode Overview](https://spark.apache.org/docs/latest/cluster-overview.html)
* [Spark Scheduling Configuration](https://spark.apache.org/docs/latest/configuration.html#scheduling)