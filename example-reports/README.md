# Opsætning
De følgende Jupyter Notebooks er skrevet så de selv downloader og installerer de afhængigheder, som de har. 

De vigtigste er:
* Pakken i dette repository
* Pathling

Pakken i dette repository gør forbindelse til Spark-clusteren (der, hvor beregningerne udføres) og S3-bucket'en (der, hvor data ligger) så nem som mulig for brugeren. 

Pathling tillader at skrive [FHIRPath](https://www.whitefox.cloud/articles/fhirpath-explained/) queries på data, så vi kan lave traditionelle SQL-agtige views, som derefter kan joines sammen til den endelige analyse. 

Alle eksemplerne følger denne fremgangsmåde.

### Kørsel på JupyterHub
1. Åben en ny terminal
2. `cd spark-bi`
3. `pip install -e .`
4. Du er nu klar til at køre notebooks.

### Kørsel lokalt
Den nemmeste opsætning er med `uv`, den klart bedste package-manager til Python. Guide til opsætning [her](https://docs.astral.sh/uv/guides/install-python/).

Dernæst installeres ved at køre `uv sync` i roden af projektet.

Hvis du kører VSCode, kan du herefter åbne notebooks, trykke "run all", vælge det virtuelle miljø fra denne mappe, og dernæst få dine resultater.

# Data
Rapporterne her er kørt på data fra TRIFORKs testmiljø. Derfor afspejler resultaterne _ikke_ produktion, og ser meget underlige ud.

### Detaljer
* Jeg (Martin Bernstorff) har snakket med Systematic (Erik). Vi kan godt bruge `managingOrganization.first()` fordi den faktiske kardinalitet af managingOrganization er 0..1. De har ikke opdateret IG'en til at afpsejle det, og prioriterer det ikke højt.