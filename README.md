# Software-Autonome-wagen

Dit project is de software voor de autonome wagen.

Het doel is om een kleine auto te maken die zelfstandig door een doolhof kan rijden.

## Wat staat hier?

Deze repo is een eerste basis voor de software. De code is zo opgebouwd dat alles logisch gescheiden is:

- hardware: dingen die echt met de auto te maken hebben
- control: regels voor hoe de auto beweegt
- navigation: beslissen welke kant op te gaan
- safety: veilig rijden, afremmen en stoppen
- core: de basis van de auto

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

## Voorbeeld van dewerking

1. De auto leest sensoren.
2. De auto beslist wat te doen.
3. De auto stuurt de motoren aan.
4. Als er een probleem is, zoals een helling of een hindernis, wordt veilig afgeremd of gestopt.

## Belangrijk

Dit is nog een begin. De code is gemaakt zodat de groep later makkelijk nieuwe onderdelen kan toevoegen.

Als iets veranderd, is het belangrijk om de code te houden:
- duidelijk
- eenvoudig
- goed benoemd
- makkelijk te begrijpen voor anderen
