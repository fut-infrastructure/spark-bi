Tabellen viser dækning af de efterspurgte analyser i CCR0274/ÆØ 'samlet ledelsesinformation'. Rækkerne er ressource-typen, kolonnerne er grupperinger.

Organisatorisk enhed kan ikke entydigt identificeres udfra FHIR data, hvorfor denne gruppering ikke er analyseret.

Det viser sig, at meget få episodes-of-care har en kommune tilknyttet på TRIFORKs testmiljø. Derfor bruges patientens bopælskommune som proxy for e.g. en spørgeskemabesvarelses "kommune". 

I produktion bør man overveje, om man vil bruge `QuestionnaireResponse.episodeOfCare.managingOrganization.municipalityCode`.

| Ehealth profil              | Dansk                | Notes                          | Anvenderløsning | Careteam | Diagnose | Kommune | Region |
| --------------------------- | -------------------- | ------------------------------ | --------------- | -------- | -------- | ------- | ------ |
| eh-careplan                 | Plan                 |                                | ✅               | ✅        | ✅        | ✅       | ✅      |
| eh-careteam                 | Careteam             |                                | 🔍              | N/A      | ✅        | ✅       | ✅      |
| eh-patient                  | Borger               | Inkl. active/inactive          | ✅               | ✅        | ✅        | ✅       | ✅      |
| Document-transformation (?) | Delinger nationalt   |                                | 🔱              | 🔱       | 🔱       | 🔱      | 🔱     |
| eh-episodesofcare           | Forløb               |                                | ✅               | ✅        | ✅        | ✅       | ✅      |
| eh-observation              | Måling               |                                | 🔱              | 🔱       | 🔱       | 🔱      | 🔱     |
| eh-plandefinition           | Plan-skabelon        | See evt. careplan.             | 🔍              | 🔍       | 🔍       | 🔍      | 🔍     |
| eh-questionnaire            | Spørgeskema-skabelon | Se evt. questionnaire response | 🔍              | 🔍       | 🔍       | 🔍      | 🔍     |
| eh-questionnaireresponse    | Spørgeskema          | Inkl. by spørgeskemaId         | ✅               | ✅        | ✅        | ✅       | ✅      |
| eh-videoappointment         | Videomøde            | Inkl. by planlagt varighed     | ✅               | ✅        | ✅        | ✅       | ✅      |
**Legend:**
* 🔍: Insufficient data in model
* 🔱: Insufficient data on TRIFORKs test environment