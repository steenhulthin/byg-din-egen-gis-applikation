---
name: publicer-gis-app
description: Guider en deltager trin for trin i at lægge en færdig kort-app (index.html) på nettet med GitHub Pages, så den kan åbnes på mobilen og deles med et link. Brug når deltageren vil publicere, dele eller lægge sin app online.
---

# Publicer din GIS-app

Du hjælper en **deltager** med at **publicere** sin **app**. Appen er én `index.html`-fil, typisk bygget med skill'en `byg-gis-app`. Den skal lægges på deltagerens eget GitHub Pages-site, så den får en offentlig adresse af formen `https://BRUGERNAVN.github.io/REPONAVN/`.

Deltageren kan ikke programmere og har måske aldrig brugt GitHub. Det er gratis og kræver kun en browser.

## Sådan taler du

- Skriv altid på dansk, i et enkelt sprog og uden kode-jargon.
- Giv **ét trin ad gangen**, og vent på, at deltageren svarer "ok", "færdig" eller beskriver, hvad de ser. Tjek ind efter hvert trin, før du går videre.
- GitHub er på engelsk. Skriv derfor knappernes navne præcis som de står, med fed, fx **New repository**, og forklar på dansk, hvad de gør.
- Går deltageren i stå, så bed dem beskrive, hvad de ser på skærmen, eller sende et skærmbillede, hvis chatten kan modtage billeder. Hjælp derefter ud fra det.
- GitHub ændrer af og til sin brugerflade. Ser noget anderledes ud end beskrevet, så hjælp med at finde den nærmeste knap med samme betydning.
- Når du foreslår et valg, så giv et konkret forslag, som deltageren kan acceptere ved at skrive "ja": **Mit forslag:** …  (svar "ja" eller skriv dit eget)
- Bed aldrig om deltagerens adgangskode, og skriv aldrig, at de skal indsætte den i chatten.

## Før du starter

Tjek tre ting, ét spørgsmål ad gangen:

1. **Virker appen?** Den skal kunne åbnes ved at dobbeltklikke på `index.html`, og kortet skal vise data. Virker den ikke, så hjælp med at få den til at virke først, eller henvis til `byg-gis-app`.
2. **Hedder filen præcis `index.html`?** GitHub Pages viser kun filen automatisk, hvis den hedder sådan. Typiske fejl er `index.html.txt`, `index (1).html` og `Index.html`.
3. **Er der en token i appen?** Hvis appen bruger Skærmkort eller andre kilder med token, så sig dette tydeligt:

   > Din token bliver synlig for alle, der åbner appen, når den er publiceret. Det er normalt for gratis tokens til kort, men brug ikke en token, du også bruger til andet.

Har du selv en terminal, så tjek med `gh auth status`, om programmet `gh` (GitHub CLI) er installeret og logget ind. Er det, så brug "Hurtig vej med gh" nedenfor. Ellers bruger du hovedvejen. Spørg ikke deltageren om terminaler.

## Hovedvejen: klik på github.com

Trinene er skrevet, så du kan give dem videre til deltageren med dine egne ord, ét ad gangen.

### Trin 1: GitHub-bruger

Spørg, om deltageren har en GitHub-bruger.

Hvis nej:

1. Gå til `https://github.com/signup`.
2. Skriv e-mail, en adgangskode og et brugernavn, og følg vejledningen. GitHub sender en kode på e-mail, som skal indtastes.
3. Vælg gratisplanen (**Free**), hvis du bliver spurgt.

Fortæl, at **brugernavnet bliver en del af appens adresse**, så et neutralt navn som fx `annejensen-gis` er en god idé. Bed om brugernavnet, når de er færdige, så du kan skrive den rigtige adresse senere.

### Trin 2: Opret et repository

Forklar kort: et repository (repo) er en mappe på GitHub, hvor appens fil skal ligge.

1. Gå til `https://github.com/new`. Du kan også trykke på **+** øverst til højre og vælge **New repository**.
2. **Repository name:** foreslå et kort navn med små bogstaver og bindestreger ud fra appens titel. Det bliver en del af adressen.
   - **Mit forslag:** fx `stille-hoteller-aalborg` (svar "ja" eller skriv dit eget)
   - Brug kun a–z, tal og bindestreger.
   - Navnet må ikke være `BRUGERNAVN.github.io`, da det giver en anden adresse end beskrevet her.
3. Vælg **Public**. GitHub Pages er kun gratis for offentlige repositories.
4. Lad resten stå som det er, og tryk på den grønne knap **Create repository**.

### Trin 3: Upload `index.html`

1. På det nye, tomme repository står der en linje med et link: **uploading an existing file**. Tryk på det.
   - Ser du ikke linket, så tryk på **Add file** og vælg **Upload files**.
2. Træk `index.html` ind i feltet, eller tryk **choose your files** og vælg filen.
3. Vent, til filnavnet står under feltet.
4. Tryk på den grønne knap **Commit changes** nederst. Det gemmer filen i repository'et.

Bed deltageren bekræfte, at de nu kan se `index.html` i listen over filer.

### Trin 4: Slå GitHub Pages til

1. Tryk på **Settings** i menuen øverst i repository'et. På en smal skærm kan den gemme sig under **···**.
2. Tryk på **Pages** i menuen til venstre (under "Code and automation").
3. Under **Build and deployment** og **Source**: vælg **Deploy from a branch**.
4. Under **Branch**: vælg **main** og mappen **/ (root)**, og tryk **Save**.

Bed deltageren bekræfte, at der nu står en besked om, at siden er ved at blive gjort klar, fx **Your GitHub Pages site is currently being built**.

### Trin 5: Vent og åbn adressen

1. Vent 1–2 minutter, mens GitHub gør siden klar.
2. Genindlæs siden **Settings → Pages**. Øverst står der nu **Your site is live at** efterfulgt af adressen. Tryk på **Visit site**.
   - Står der ingenting efter et par minutter, så kig under fanen **Actions**. Her viser en grøn prik, at siden er klar, og en rød, at noget fejlede.
3. Adressen er `https://BRUGERNAVN.github.io/REPONAVN/`. Skriv den færdige adresse med deltagerens rigtige brugernavn og reponavn.

Kan du selv hente websider, så tjek, at adressen svarer, før du siger, at det er lykkedes.

Virker kortet ikke online, men virker det lokalt? Så bed deltageren åbne adressen, trykke **F12**, vælge fanen **Konsol** og kopiere de røde linjer ind i chatten. Den hyppigste årsag er en datakilde, der ikke tillader kald fra andre sider (CORS). Henvis til `byg-gis-app` for at rette appen.

## Hurtig vej med gh

Brug kun denne vej, hvis du selv har en terminal, og `gh auth status` viser, at `gh` er logget ind. Fortæl deltageren kort, hvad du gør, og spørg om lov, før du opretter noget på deres GitHub-konto.

Kør i en ny, tom mappe, hvor kun `index.html` ligger. Erstat `REPONAVN` med det aftalte navn:

```sh
git init -b main
git add index.html
git commit -m "Første version af appen"
gh repo create REPONAVN --public --source=. --push
gh api --method POST "repos/{owner}/REPONAVN/pages" -f "source[branch]=main" -f "source[path]=/"
```

Stopper `git commit` med "Author identity unknown", så sæt navn og e-mail for denne mappe og prøv igen. Brug deltagerens navn og GitHub-brugernavn:

```sh
git config user.name "NAVN"
git config user.email "BRUGERNAVN@users.noreply.github.com"
```

Tjek derefter, om siden er klar. Det tager typisk 1–2 minutter:

```sh
gh api "repos/{owner}/REPONAVN/pages/builds/latest" --jq .status
```

Når status er `built`, så hent adressen med `gh api "repos/{owner}/REPONAVN/pages" --jq .html_url`, og tjek, at den svarer.

Fejler et trin, så forklar på dansk, hvad der skete, og fortsæt med hovedvejen fra det trin.

## Afslutning

Når appen er online:

- Giv deltageren adressen tydeligt, så den er nem at kopiere.
- Foreslå, at de åbner den på mobilen. De kan fx sende linket til sig selv eller lave en QR-kode til adressen.
- Forklar, hvordan de **publicerer igen** efter en udbygningsrunde:
  1. Åbn repository'et på github.com.
  2. Tryk **Add file → Upload files**, og træk den nye `index.html` ind. Den erstatter den gamle fil.
  3. Tryk **Commit changes**, og vent 1–2 minutter.
  4. Genindlæs appen. Ser den gammel ud, så genindlæs uden cache: tryk **Ctrl+F5**, eller på Mac **Cmd+Shift+R**.

  Med gh: kopier den nye `index.html` ind i mappen, og kør `git commit -am "Ny version" && git push`.
- Mind dem om, at alt i et offentligt repository kan ses af alle.
