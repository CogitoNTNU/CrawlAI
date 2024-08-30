# Architectural Design

## Quality Attribute Scenarios

See [Quality Attribute Scenarios](quality_attribute_scenarios.md)

## Architectural Drivers / Architecturally Significant Requirements (ASRs)

See [Architectural Drivers](requirements.md)

## Components

CrawlAI uses the following COTS components:
[COTS Components](cots.md)

## Stakeholders and Concerns

See [Stakeholders and Concerns](stakeholders.md)

## Architectural tactics and patterns

### Tactics

| Tactic                   | Affected Quality Attribute | Reasoning                                                                    |
| ------------------------ | -------------------------- | ---------------------------------------------------------------------------- |
| Schedule Resources       | Performance                | Optimizes performance by dynamically allocating resources based on demand.   |
| Continuous Deployment    | Deployability              | Allows for updates without downtime, maintaining high availability.          |
| Reduce Size of Modules   | Modifiability              | Breaks down modules into smaller, more manageable components.                |
| Increase Cohesion        | Modifiability              | Ensures each module has a single, well-defined purpose.                      |
| Encapsulate              | Modifiability              | Limits dependencies by encapsulating functionalities.                        |
| Use an Intermediary      | Modifiability              | Manages interactions between modules through intermediaries.                 |
| Restrict Dependencies    | Modifiability              | Minimizes dependencies between modules.                                      |
| Abstract Common Services | Modifiability              | Creates common services that can be reused across the system.                |
| Defer Binding            | Modifiability              | Increases flexibility by delaying the binding of components until needed.    |
| Prioritize Events        | Modifiability              | Manages event priorities to handle critical operations efficiently.          |
| Introduce Concurrency    | Modifiability              | Improves responsiveness by implementing concurrent processing.               |
| Heartbeat Monitoring     | Availability               | Regularly checks the health of the system to detect and respond to failures. |

| Maintain Task Model | Usability | Continuously updates the model of user tasks to ensure the system remains user-friendly. |
| User Model | Usability | Maintains an understanding of the user base to tailor interactions and improve UX. |
| System Model | Usability | Keeps a model of system interactions to ensure predictable and intuitive behavior. |

### Patterns

Describe the architectural patterns used
ECS?
data access object?
State (design pattern)

## Architectural Viewpoints

### Physical View

_The physical view should describe how the software is allocated to
hardware. This includes the client, the server, and network connections you develop
and other services you use (like cloud-based services, etc.). A typical notation for this
view is a deployment diagram._

### Logical View

_It is recommended to use multiple diagrams for this view, e.g., provide
one high-level diagram and one or more diagrams for more detail. Typical notations
for this view include a UML class diagram, UML package diagram, layers diagram,
ER diagram, and combination of UML class and package diagrams._

### Process View

_It is also recommended to use multiple diagrams for the view to give a
complete description of the run-time behavior of the system. Typical notations for this
view include a UML activity diagram, a UML state diagram, and a UML sequence
diagram._

### Development View

_The purpose of the development view is to make it easier to
allocate work to various team members and make it possible to allow development in
parallel. Based on this view, it should be easy to give programming tasks to group
members and make it easy to integrate the results after completion with the rest of the
system_

## Architectural Rationale
