# Gold-standard sequence diagrams

[Back to dataset README](../README.md) · [Rendered gallery](../3_visualizations/sequence_diagrams/README.md)

Reference UML sequence diagrams for all nine projects, written from the user stories (`1_user_stories/`) and the gold-standard domain model (`2_gold_standard_domain_models/`) of each project. They serve as a gold standard for evaluating LLM-generated sequence diagrams, for example in pipelines that use behavioural models to validate and repair generated domain models.

**These diagrams are an addition to this curated repository.** They are not part of the original dataset by Bragilovski et al. and were written for a master thesis. They are a draft under review and may change.

## Projects

| Project | Diagrams | Messages | User stories covered | Gold associations used |
|---|---|---|---|---|
| [Camperplus](camperplus/) | 8 | 71 | 51 of 55 | 22 of 26 |
| [Fish & Chips](fish_chips/) | 6 | 42 | 49 of 50 | 8 of 8 |
| [Grocery](grocery/) | 6 | 54 | 42 of 49 | 11 of 11 |
| [Planningpoker](planningpoker/) | 7 | 41 | 32 of 53 | 6 of 6 |
| [Recycling](recycling/) | 7 | 43 | 32 of 51 | 8 of 10 |
| [School](school/) | 9 | 87 | 56 of 61 | 24 of 24 |
| [Sports](sports/) | 7 | 60 | 61 of 63 | 12 of 12 |
| [Supermarket](supermarket/) | 7 | 57 | 50 of 51 | 16 of 16 |
| [Ticket](ticket/) | 7 | 51 | 51 of 54 | 13 of 13 |
| **Total** | **64** | **506** | **424 of 487** | **120 of 126** |

An association counts as used when at least one message runs between its two classes. The unused ones are four redundant shortcuts in Camperplus (activities–camp, activities–groups, camp–photos, facilities–groups) and employees–user and employees–safe disposal events in Recycling. No user story describes an interaction over them. The optional class Timeslot in Sports has no association and is in no diagram.

## What the diagrams show

The gold domain models contain only classes and associations. They have no attributes, operations, multiplicities or directions. A sequence diagram can therefore support or contradict such a model in two ways only: by **which classes take part** in a scenario and by **which pairs of classes interact**. The diagrams are kept at that level. They are conceptual, analysis-level diagrams that say who talks to whom and about what, not design diagrams that say how a system computes the result.

## Conventions

- **One use case per diagram:** each diagram shows the main flow of one use case. Control logic is kept to a minimum because sequence diagrams show it poorly (Fowler, *UML Distilled*, ch. 4). A diagram has at most one `alt` or `opt` fragment, and only where the stories describe a real alternative, such as guest versus registered checkout.
- **Lifelines are the gold classes plus the actors from the user stories.** Actors are on the left, followed by the objects in the order of their first message. There is no System, UI or controller lifeline: an actor addresses the object that handles the request. Optional gold classes may be used.
- **A role that is also a gold class appears twice:** as the actor `X (person)` and as the object `X`. For example, `Customer (person)` asks the `Customer` object to book a lesson.
- **A person goes through their own object** when the request concerns their own data or the objects linked to them (a guardian's child, a manager's employees, a teacher's classes, a customer's order, delivery or booking) and the gold model links their class directly to the target. Otherwise the actor addresses the target object directly, without a detour over several associations: searching products in a store, seeing how many spots are booked, or joining a game, which creates the estimator. Each such exception is marked in the Mermaid source with a `%% direct A->B: reason` comment.
- **Chains are unbroken.** Every message from an object follows a message that reached that object since the last actor request. Where two requests need the same chain, they are merged into one request or the connecting message is repeated.
- **Actors are named after the role in the user story** ("as a visitor", "as a parent"). The suffix `(person)` is added only when the role has the same name as a gold class. Parent and Guardian in Camperplus are therefore an actor and a class with different names.
- **Connecting steps:** a diagram has at most one actor message without a user story, and only where the flow needs it (entering an order before changing it, booking a lesson, playing a card).
- **Notifications go to the recipient's object** (`Booking` notifies `Customer`). They go to an actor only when the recipient has no gold class, as for the kitchen employee in Fish & Chips. There are no messages between two actors.
- **Every message between two objects follows an association of the gold domain model,** required or optional. The diagrams introduce no class or association that the gold model lacks.
- **Messages are short plain phrases.** There are no operation names, parameters or return values, because the domain models have no operations or attributes to match them against. A message from an actor names what the person wants ("view order history"). A message between two objects is a noun phrase naming what the first requests from or passes to the second ("tickets", "accepted estimate"), or `notify of ...` for a notification. Labels do not list attributes ("set lesson details", not the individual fields) and do not name technologies or formats (spreadsheets, URLs, HTML, map services).
- **No reply arrows.** That information comes back to the actor is implied by the request (Ambler, *The Elements of UML 2.0 Style*: do not model a return value when it is obvious).
- **At most one note per diagram,** and only for a rule from a story that is not an interaction, such as the resale service fee.
- **Traceability:** each file starts with three comments: `%% SDn - title`, `%% Stories:` with the user-story line numbers it covers, and `%% Description:` with a one-sentence summary. A `%% covers n, m` comment above a message names the stories that message covers. These comments are visible in the Mermaid source only, so the rendered diagrams stay uncluttered.

`scripts/render_models.py --check` validates these rules offline: every participant is a gold class, every message between two participants follows a gold association, no message runs between two actors, every object message continues a chain, a person does not skip their own object without a `%% direct` comment, at most one actor message has no story, there are no reply arrows, operation calls or more than one note, the stories in the header match the `%% covers` comments, and every lifeline and message appears in the rendered SVG.

## Considerations when creating the diagrams

- **Inputs:** only the user stories and the gold domain model of the project. Where a story is silent, the diagram stays silent too, rather than inventing steps.
- **Purpose first:** the diagrams are a reference for *evaluating* generated diagrams and for checking a domain model against behaviour. Detail that a class-and-association model cannot be checked against (operation signatures, return values, parameters) was removed after review, because it adds modelling decisions without adding evidence.
- **Consistency with the gold model by construction:** participants and object-to-object messages are restricted to gold classes and gold associations, and this is checked by script. A consistency check between these diagrams and the gold model therefore passes by definition.
- **Granularity:** one use case per diagram. An earlier version packed several scenarios into five to six diagrams per project, and another split them into 12–13 single-scenario diagrams. One use case per diagram keeps related stories together while staying readable.
- **Best practices:** a sequence diagram shows how objects collaborate, not control logic (Fowler). Actors on the left, class names as in the class model, prose for messages, only critical interactions, no obvious return values (Ambler). Analysis-level diagrams state what happens between which parties and leave the how to design.
- **Coverage is reported, not forced:** functional stories that describe a concrete interaction with at least one gold class are covered. Stories without a concrete interaction or without a gold class are listed below with the reason, instead of being bent into a diagram.
- **Same notation as the domain models:** Mermaid sources, rendered to SVG with the same script, so that both gold standards can be read, diffed and validated the same way.

## Issues that arose

- **There is no single correct set of diagrams.** User stories are a flat list of features, not ordered scenarios. Which stories form one use case, in which order the steps occur, and how many diagrams result are decisions of the modeller. Two modellers would produce different but equally valid sets.
- **The right level of detail is a judgement.** Detailed diagrams with operations, replies and notes looked more complete but contained many invented details. The simpler diagrams state less, and what they state is closer to what the stories and the gold model support.
- **The gold domain models are sparse relative to the behaviour in the stories.** Associations that a scenario needs are sometimes missing: Recycling has no association between user and recycling facility, and some classes have no association at all (Repair in Camperplus, Attendance in School, Timeslot in Sports). In these cases the actor addresses the object directly, or the interaction is routed over existing associations.
- **Classes that the stories need are missing from the gold models,** such as accounts and login (Planningpoker, School), a timer (Planningpoker), nametags and reminders (Camperplus), or bins and drop-off sites (Recycling). The affected stories are not covered.
- **Roles are both actors and classes.** User, Employee, Manager, Customer, Teacher or Counselor is the person acting and also a domain object. The diagrams separate the two (`X (person)` and `X`), which a generated diagram may not do.
- **Without a system lifeline, system-initiated behaviour has no natural sender.** Notifications are drawn as a message from the object that owns the information, to the notified object or actor.
- **Message wording is not standardised.** The stories name goals, not operations, so generated diagrams should be compared by participants and interacting pairs, not by message text.
- **Vague and non-functional stories have no interaction,** for example usability, security, "quick and easy" goals or development tasks. They are left out.
- **Similar roles are kept apart.** Where the stories use different role names for possibly the same person (superuser and facility representative in Recycling, camp worker and counselor in Camperplus), the diagrams keep separate actors rather than guessing that they are the same.
- **The diagrams inherit the gold model's view.** Because they are built to conform to the gold domain model, they cannot reveal a class or association that the gold model itself lacks. They are suited to judging generated sequence diagrams and model-to-behaviour consistency, not to validating the gold domain models.
- **The gold models changed during the work.** After the gold standard was revised, the diagrams had to be adapted: renamed, added and removed classes and associations changed which lifelines and routes are allowed. The diagrams depend on the gold model version they were written against.
- **Single author.** The diagrams were drafted by one person with LLM assistance and are still under review. They have not yet been validated by a second modeller.

## User stories not covered

**Camperplus**

- 7, 18: nametags. There is no nametag class in the gold model.
- 9: reminders for tasks. There is no reminder or task class in the gold model.
- 20: keeping information in one place, a general goal.

**Fish & Chips**

- 20: operating the screen by touch, a user-interface requirement.

**Grocery**

- 5: outsourcing part of the payment process, an organisational decision.
- 11: notifying the manager that the schedule needs manual adjustments. The gold model has no association between Schedule and Manager.
- 39, 41, 42, 46, 49: single login, usability, encryption and security.

**Planningpoker**

- 21–26: accounts, login, timezone and password reminder. The gold model has no account or user class.
- 37, 38: two-minute timer. There is no timer class in the gold model.
- 40: cards always in the same order, a display requirement.
- 42: thumbnail photo. There is no photo class in the gold model.
- 43–53: non-functional, developer, researcher and metrics stories.

**Recycling**

- 9, 10: maps of public recycling bins and special-waste drop-off sites. There is no gold class for them.
- 13, 19, 20, 23, 27, 29, 31, 34, 35: documentation, user interface, devices, security, API and development stories.
- 22, 41: admin monitoring of site status and error logs. There is no gold class for them.
- 24, 25, 32, 33: company data for executives, route planning, employee notifications and activity fees. No gold class takes part in a concrete interaction.
- 45: replying to user questions. The revised gold model has no question class.
- 51: a facility reporting issues to the admin. The admin is not a gold class and there is no issue or message class, so this would be a message between two actors.

**School**

- 47, 50, 51, 58, 60: passwords, accounts and roles. The gold model has no account class.

**Sports**

- 48: adding an admin. There is no admin class in the gold model.
- 50: logging in. There is no account or user class in the gold model.

**Supermarket**

- 15: contacting customer service. There is no gold class for it.

**Ticket**

- 18, 27: quality goals for the buying process (easy, short, intuitive), without a concrete interaction.
- 40: general goal of protecting users from online fraud. Its concrete part, ticket validation, is in SD6.

## Modeling decisions

- **Camperplus:** bi-weekly feedback reaches the Guardian from the Camper through Feedback. Submitted forms run from Guardian to Form to Camper. Inappropriate behaviour is reported to Behavior, which is linked to the Camper. Repair has no association and is addressed by the camp worker directly. Staff, groups and facilities are reached through Camp where the story speaks of the camp's staff, groups or facilities. Parents reach their camper through Guardian, but message counselors and staff directly, because Guardian has no association to them.
- **Fish & Chips:** the optional Cashier class is used for checking a cashier's balance. Status labels are set on the order's products, as the stories describe. Payment methods and tips are handled on the Order, since the revised model has no payment-method class. The customer reviews their order through the Customer object, but requests a payment confirmation directly, because Customer is not linked to Payment. Cashier is not linked to Order, so the cashier addresses the order directly. Kitchen employees have no gold class and receive notifications as an actor. The notification of a new order follows the cashier sending the ticket to the kitchen.
- **Grocery:** Manager is both an actor and a gold class. Complaints are linked only to Manager, so a handled complaint reaches the employee through Manager. Messages between employees and managers run through Message. A manager hires, views employees and handles complaints through the Manager object, but generates the schedule directly, because Manager is not linked to Schedule. The office employee is kept as its own actor. The manager is notified of a completed hiring through the optional Manager–Employee association.
- **Planningpoker:** the accepted estimate is set on Item. An Estimate reaches its Item through the estimate–item association, and the Round reaches estimates through its items. Moderator actions on items go through the Round. Joining a game is addressed to Game, which creates the Estimator.
- **Recycling:** there is no association between User and RecyclingFacility, so the user addresses the facility directly and recommendations run through Schedule. The transaction history is read as the user's Activity and rewards as Reward. SafeDisposalEvent and Employee take part only in messages from actors. Updates for facilities are sent to RecyclingFacility. The gold model has one Schedule class linked to both User and RecyclingFacility. It is read as the schedule that connects a facility's opening hours with the availability of its users, so a facility reaches its users through Schedule. A user's contact with the administrators is either a feedback or a complaint.
- **School:** files uploaded for a class reach Material through DigitalLearningModule, the only class associated with Material. Attendance has no association and is addressed by teacher and administrator directly. A teacher is notified of a submission through Assignment and Class. A teacher reaches classes, and students in their class, through the Teacher object; module, submission and attendance have no association to Teacher and are addressed directly. Each recipient of a message is notified through Message, which the gold model links to all five roles. A guardian's absence form is a Message that notifies the Administrator, because Attendance has no association.
- **Sports:** the optional Timeslot class has no association and appears in no diagram. Booking or cancelling by phone is drawn as the customer addressing Booking. Fines for no-shows are a message to Customer, because the gold model has no fine class. A customer books, cancels and confirms through the Customer object, but sees available lessons and booked spots directly.
- **Supermarket:** "products I like" (story 14) is read as the products on the wishlist. Personal discounts and suggestions are derived from the customer's orders. The optional Payment class is used for digital payment of an order. Searching products, stock and locations is addressed to Store directly; orders and deliveries go through the Customer object. A personal discount notifies the customer through PersonalDiscount. Sale and back-in-stock notifications are drawn as the customer's request to be notified, because the gold model has no route from Product to Customer.
- **Ticket:** a guest's name and email are entered on the Order, because there is no Guest class. Saved payment details belong to User (story 2), because the gold model links Payment only to Order. Reseller is not linked to User in the gold model and appears as its own lifeline. Recommended events are requested by a registered user, not a visitor, because they come from the user profile. Ticket validation is drawn as the ticket checking its event, instead of a self-message. A buyer is a Visitor, as in the stories, whether logged in or a guest.
