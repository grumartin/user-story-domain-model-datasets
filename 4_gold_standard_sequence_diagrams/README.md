# Gold-standard sequence diagrams

[Back to dataset README](../README.md) · [Rendered gallery](../3_visualizations/sequence_diagrams/README.md)

Reference UML sequence diagrams for two projects, written from the user stories (`1_user_stories/`) and the gold-standard domain model (`2_gold_standard_domain_models/`) of each project. They serve as a gold standard for evaluating LLM-generated sequence diagrams, for example in pipelines that use behavioural models to validate and repair generated domain models.

**These diagrams are an addition to this curated repository.** They are not part of the original dataset by Bragilovski et al. and were written for a master thesis. They are a draft under review and may change.

## Projects

| Project | Role in the thesis | Diagrams | User stories covered |
|---|---|---|---|
| [Planningpoker](planningpoker/) | development project | 7 | 33 of 53 |
| [Ticket](ticket/) | held-out project | 7 | 51 of 54 |

## Conventions

- **One use case per diagram:** each diagram shows the main flow of one use case, with at most two `alt`/`opt` fragments for variants of the same goal. Control logic is kept small because sequence diagrams show it poorly (Fowler, *UML Distilled*, ch. 4). Repetition is written as "for each …" in the message instead of a `loop`.
- **Lifelines are the gold classes plus the actors from the user stories.** Actors are on the left. There is no System, UI or controller lifeline: an actor sends its request straight to the object that handles it.
- **Every message between two objects follows an association of the gold domain model.** The diagrams therefore introduce no class or association that the gold model lacks.
- **Messages from people are written as prose; messages between objects as operations.** Only the critical interactions are shown. Obvious return values and object destruction are left out, and a reply is drawn only when information goes back to an actor (Ambler, *The Elements of UML 2.0 Style*).
- **Behaviour that no gold class owns is a note,** for example the 15-estimator limit or the resale service fee.
- **Traceability:** each file starts with three comments: `%% SDn - title`, `%% Stories:` with the user-story line numbers it covers, and `%% Description:` with a one-sentence summary. `[n]` after a message or fragment names the story it covers.

`scripts/render_models.py --check` validates these rules offline: every participant is a gold class, every message between two participants follows a gold association, the stories in the header match the `[n]` tags, and every lifeline and message appears in the rendered SVG.

## User stories not covered

**Planningpoker**

- 21–26: accounts, login, timezone and password reminder. The gold model has no account or user class.
- 37, 38: two-minute timer. There is no timer class in the gold model.
- 42: thumbnail photo. There is no photo class in the gold model.
- 43–53: non-functional, developer, researcher and metrics stories.

**Ticket**

- 18, 27: quality goals for the buying process (easy, short, intuitive), without a concrete interaction.
- 40: general goal of protecting users from online fraud. Its concrete part, ticket validation, is in SD6.

## Modeling decisions

- **Planningpoker:** the accepted estimate is stored on Item, because the gold model has no other place for it. An Estimate reaches its Item through the estimate–item association, and the Round reaches estimates through its items. Moderator actions on items always go through the Round.
- **Ticket:** a guest's name and email are attached to the Order, because there is no Guest class. Saved payment details belong to User (story 2), because the gold model links Payment only to Order. Reseller is not linked to User in the gold model and therefore appears as its own lifeline.
