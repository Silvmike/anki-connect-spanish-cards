# Anki-Connect Spanish cards

A service allowing to generate language learning cards (Spanish to Russian, can be changed pretty easily) automatically.

# TODO

- [x] Ask for a deck to put generated cards to
- [ ] Use external LLM to generate questions for QA multi-choice card
- [ ] Avoid duplicates
- [ ] Improve generated questions refining

# Component diagram

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryBorderColor': '#ff9999', 'primaryBackgroundColor': '#ffeeee'}}}%%

flowchart TD
    subgraph Reverse_Proxy["Reverse Proxy"]
        nginx(Nginx)
    end

    subgraph Application_Services["Application Services"]
        storage(Storage Service)
        translate(Translate Service)
        yandex(Yandex Disk Service)
        anki(Anki Card Generator)
        image(Image Search Service)
        audio_orchestrator(Audio Service Orchestrator)
    end

    subgraph Machine_Learning_Services["Machine Learning Services"]
        audio(Audio Service)
        llm(LLM Service)
    end

    subgraph Data_Persistence["Data Persistence"]
        postgres(PostgreSQL)
    end

    Browser --> nginx

    nginx --> storage
    nginx --> translate
    nginx --> yandex
    nginx --> anki
    nginx --> image
    nginx --> audio_orchestrator
    nginx --> llm

    storage --> postgres

    audio_orchestrator --> audio
    audio_orchestrator --> yandex
```

# Demo
![demo.gif](demo.gif)
