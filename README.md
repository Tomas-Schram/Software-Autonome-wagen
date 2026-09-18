# Software-Autonome-wagen

Dit project is de software voor de autonome wagen.

Het doel is om een kleine auto te maken die zelfstandig door een doolhof kan rijden.

## Wat staat hier?

Deze repo is een eerste basis voor de software. De code is zo opgebouwd dat alles logisch gescheiden is:


### Snelle uitleg per map

- core = basis van de auto
- hardware = echte toestellen en sensoren
- control = bestuurlijke logica
- navigation = route en richting kiezen
- safety = veilig rijden
- tests = controle van de code

## Waar vind je wat?

### src/autonome_wagen/
Dit is de hoofdmap van de software.

- core.py  
  De basis van de auto. Hier staat bijvoorbeeld de status van de wagen.

- hardware/  
  Hier staan de interfaces voor de echte onderdelen:
  - motoren
  - sensoren
  - Micro:bit-verbinding

- control/  
  Hier staat de logica voor beweging en veiligheid.

- navigation/  
  Hier staat de logica voor het volgen van een lijn en het kiezen van een richting in een open ruimte.

- safety/  
  Hier staat alles over veiligheid:
  - helling detecteren
  - slagboom stoppen
  - geluidssignaal

### tests/
Hier staan tests.

Deze tests laten zien of de verschillende onderdelen werken. Ze zijn handig om te controleren of de code nog goed doet wat hij moet doen.

## Voorbeeld van de werking

1. De auto leest sensoren.
2. De auto beslist wat te doen.
3. De auto stuurt de motoren aan.
4. Als er een probleem is, zoals een helling of een hindernis, wordt veilig afgeremd of gestopt.

## Belangrijk

Dit is nog een begin. De repo is breed opgezet en logisch ingedeeld, zodat zowel Tomas als Casper gemakkelijk onderdelen kunnen toevoegen aan de bijbehorende bestanden.

Als iets verandert, is het belangrijk om de code te houden:
- duidelijk
- eenvoudig
- goed benoemd
- makkelijk te begrijpen voor anderen

## Casper

Dit is alleen voor Casper. Je kunt aan de software werken door eerst de repo te openen in VS Code (of een andere codeomgeving), daarna de code te lezen en vervolgens te verbeteren, uit te breiden of toe te voegen.

Gebruik deze stappen:
1. open de repo in VS Code
2. kies een klein onderdeel om aan te werken
3. maak de code duidelijk en simpelel
4. run de tests om te checken of alles nog werkt
5. commit de verandering met een korte, duidelijke boodschap
6. push naar GitHub zodat de rest van de groep het kan zien

Zo blijven alle wijzigingen goed zichtbaar en makkelijk te bespreken.

Luuk, als je dit leest;
1. Bedankt voor het meedenken en meelezen.
2. Ik ben trots op je dat je de software doorleest en wilt begrijpen :)
3. Je bent een homo.
