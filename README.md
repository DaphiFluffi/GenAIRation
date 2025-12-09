# genAIRation - Evolution Simulator - Mathesis Lab TU Berlin 2017

Ein genetischer Algorithmus-basierter Evolutionssimulator, bei dem Kreaturen darum konkurrieren, ein Ziel zu erreichen und sich dabei über Generationen weiterentwickeln.

## Hauptmechaniken

### Das Simulations-Loop

- **Start & Ziel**: Jede Generation starten die Kreaturen auf der linken Plattform (100, 360) und versuchen, das Ziel auf der rechten Seite (800, 0) zu erreichen
- **Bewegungssystem**: Kreaturen bewegen sich in einer 2D-Ebene durch eine Abfolge von Drehwinkeln (gespeichert in ihrer "briefing")
- **Schrittweise Bewegung**: Jeder Schritt = Drehen um einen Winkel → Vorwärtsbewegung um die `path_length` des Spezies
- **Todsbedingungen**: Kreaturen sterben wenn sie:
  - Hindernisse treffen (Wolke, Regentropfen)
  - Aus dem Spielfeld gehen
  - `moveCap` (500) Schritte erreichen

### Fitness & Fortpflanzung

- **Bewertungssystem**: Kreaturen werden nach Nähe zum Ziel bewertet:
  ```
  score += 100 - (Distanz_zum_Ziel / Max_Distanz * 100)
  ```
- **Ranking**: Nach dem Tod werden alle Kreaturen nach ihrer `rating()` sortiert
- **Reproduktion**: Die **besten 25%** (bei `selection=2`) jeder Generation erzeugen je 2 Nachkommen

### Vererbung & Mutation

- **Weitergabe**: Siegerkreaturen geben ihre erfolgreichen Bewegungssequenzen (`legacy()`) an Nachkommen weiter
- **Mutationen**:
  - Kleine zufällige Änderungen an Drehwinkeln
  - Jedes Spezies hat seine eigene `mutation_rate` (0-7)
  - Zufällige Bewegungen ersetzen geerbt (mit `outlier_rate = 0,5%`)
  - Mutationen sind begrenzt durch spezies-spezifische Arc-Bereiche (z.B. Einhorn ±22,5-17,5°)

## 10 Spezies mit unterschiedlichen Merkmalen

| Spezies | Tendenz | Arc-Bereich | Pfadlänge | Mutationsrate |
|---------|---------|-------------|-----------|---------------|
| Einhorn | 66 | 22.5±17.5 | 7 | 2 |
| Pinguin | 40 | 42.5±27.5 | 6 | 1 |
| Schmetterling | 86 | 17.5±17.5 | 10 | 4 |
| Marienkäfer | 99 | 30±10 | 5 | 5 |
| Katze | 66 | 20±10 | 8 | 4 |
| Libelle | 50 | 25±0 | 8 | 0 |
| Daphna | 10 | 90±0 | 5 | 7 |
| Lena | 66 | 45±10 | 10 | 1 |
| Lorenz | 75 | 22.5±17.5 | 6 | 3 |
| Dodo | 81 | 35±12.5 | 10 | 2 |

**Tendenz**: Wahrscheinlichkeit, eine Drehbewegung zu machen statt geradeaus zu gehen (z.B. 99 = dreht sich fast immer)

## Evolutionsdynamiken

Spezies mit besseren Merkmalen für den Hindernisparcours werden über Generationen hinweg dominieren. Die Visualisierung zeigt die Population jedes Spezies als farbige Balken im rechten Panel, die sich in Echtzeit entwickeln.
