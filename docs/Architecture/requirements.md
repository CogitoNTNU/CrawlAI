# Architectural Drivers / Architectural Significant Requirements

This document outlines the architectural drivers and significant requirements for the CrawlAI system. It includes both functional and non-functional (quality) requirements that define the system's behavior, performance, and operational characteristics. The goal is to ensure that TutorAI meets the needs of its users and [Stakeholders](stakeholders.md) while maintaining a high standard of quality.

## Functional Requirements

_Functional requirements define the specific behaviors, actions, and functionalities that the TutorAI system must provide to its users. They describe what the system will do under various conditions, detail the operations and activities the system must be capable of performing, and outline the explicit services it should deliver._

The functional requirements are divided into three different priorities:
| Priority | Description |
|----------|-------------|
| High | These requirements are essential for the system to function properly; without these, there will be a significant impact on the system's ability to provide an enjoyable experience. |
| Medium | These requirements are important but not critical for the system to function properly. |
| Low | These requirements are nice-to-have features that would enhance the system but are not essential for its core functionality. |

All functional requirements are listed below:

## GENETIC ALGORITHM

| ID    | Requirement Description                                                                                                  | Priority |
| ----- | ------------------------------------------------------------------------------------------------------------------------ | -------- |
| FR1.1 | The system must allow structural mutations to add a link between two neurons                                             | high     |
| FR1.2 | The system must allow structural mutations to remove an existing link between two neurons                                | high     |
| FR1.3 | The system must allow structural mutations to add new hidden neuron.                                                     | high     |
| FR1.4 | The system must allow structural mutations to remove existing hidden neuron                                              | high     |
| FR1.5 | A new link/synapse when a new hidden neuron is created must have a weight of 1, so new agent won't terminate prematurely | high     |
| FR1.6 | The system must allow non-structural mutations to update values in both neurons and synapses                             | high     |
| FR1.7 | The system must allow interspecies crossover                                                                             | high     |
| FR1.8 | The system must allow backpropagation for machine learning                                                               | low      |

## ENVIROMENT

| ID    | Requirement Description                                                                           | Priority |
| ----- | ------------------------------------------------------------------------------------------------- | -------- |
| FR2.1 | The enviroment should indicate fintness to the agents depending on how far they are able to move. | high     |
| FR2.2 | The enviroment should kill agents that are slow.                                                  | high     |
| FR2.3 | The killing mechanism must be correctly callibrated in order to allow stable evolution.           | medium   |
| FR2.4 | The enviroment should contain a hilly ground                                                      | medium   |
| FR2.5 | The enviroment must make agents compete with each other                                           | high     |
| FR2.6 | The enviroment must contain physics                                                               | high     |

## AGENTS

| ID    | Requirement Description                                                                 | Priority |
| ----- | --------------------------------------------------------------------------------------- | -------- |
| FR3.1 | An agent must be able to see the ground                                                 | high     |
| FR3.2 | An agent must be able to know the positions of each limb                                | high     |
| FR3.3 | An agent must be able to act upon the enviroment through actuators                      | high     |
| FR3.4 | An agent must have healthpoints                                                         | medium   |
| FR3.5 | An agent must have vital oragans that can be damaged if agent falls.                    | medium   |
| FR3.6 | An agent must have skin that can be damaged if dragged on the ground too much           | medium   |
| FR3.7 | The health of an agent plays a role in fitness, and is part of the performence measure. | medium   |
| FR3.8 | An agent must be able to be exported and put into another simulation                    | low      |

## DISPLAY

| ID    | Requirement Description                                              | Priority |
| ----- | -------------------------------------------------------------------- | -------- |
| FR3.1 | The neural network of a given agent must be displayed                | high     |
| FR3.2 | A user must be able to see the agents walking for each generation    | high     |
| FR3.3 | A user must be able to see the family tree of the agents             | low      |
| FR3.4 | A user must be able to see what agents are killed after a generation | low      |
| FR3.5 | A name is displayed for each species                                 | low      |

## **Quality Attributes**

_Quality attributes are the system's non-functional requirements that specify the system's operational characteristics. They define the system's behavior, performance, and other qualities that are not directly related to the system's functionality._

### **Usability**

| ID  | Requirement Description                                                                                                         | Priority |
| --- | ------------------------------------------------------------------------------------------------------------------------------- | -------- |
| U1  | The system must have an intuitive interface that allows users to understand essential functions within 30 seconds.              | High     |
| U2  | The system must comply with WCAG 2.1 Level AA guidelines to ensure accessibility for users with disabilities.                   | Low      |
| U3  | The system must enable a user to skip the display of multiple generations.                                                      | Medium   |
| U4  | The display should show enough of the process to allow a user to understand a bit of what is going on in the genetic algorithm. | Medium   |
| U5  | Instruction manual will be accessible, so that a user may understand how to navigate the system.                                | Low      |

### **Performance**

| ID  | Requirement Description                                                                                                          | Priority |
| --- | -------------------------------------------------------------------------------------------------------------------------------- | -------- |
| P1  | The system should be fast enough so that a user can see the progress of the agents over multiple generations.                    | High     |
| P2  | The system must allow neural networks with a reasonable size the evolve quickly, in less than 5 seconds between each generation. | High     |

### **Deployment**

| ID  | Requirement Description                                                                                                           | Priority |
| --- | --------------------------------------------------------------------------------------------------------------------------------- | -------- |
| D1  | The system must enable straightforward deployment processes for updates and new features that introduce zero downtime or defects. | Low      |
| D2  | The system must support automated deployment to streamline the release process.                                                   | Low      |

### **Testability**

| ID  | Requirement Description                                                                                                                           | Priority |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| T1  | The system must be designed to allow efficient testing of new features and updates to ensure functionality without extensive manual intervention. | High     |
| T2  | The system must have a test suite that covers all essential features                                                                              | High     |
| T3  | The system must be able to mock external services for testing                                                                                     | Medium   |

### **Modifiability**

| ID  | Requirement Description                                                                                                         | Priority |
| --- | ------------------------------------------------------------------------------------------------------------------------------- | -------- |
| M1  | The system must be designed to allow for easy modification and extension of features without significant rework or refactoring. | High     |
| M2  | The system must be able to change COTS (Commercial Off-The-Shelf) components with only local changes.                           | High     |
| M3  | The system must be able to get new functionalities without much refactoring of existant code.                                   | High     |
| M4  | The system must be able to easily change database without any side effects                                                      | High     |

### **Safety**

| ID  | Requirement Description                                                                 | Priority |
| --- | --------------------------------------------------------------------------------------- | -------- |
| Sa1 | The system should not display any harmfull ideas or language, nor upset creationalists. | Low      |

## **Business Requirements**

_Business requirements are the high-level needs of the business that the system must meet to fulfill its purpose. They define the system's strategic goals, objectives, and constraints that guide the system's development and operation._

### **Learning**

| ID    | Requirement Description                                           | Priority |
| ----- | ----------------------------------------------------------------- | -------- |
| BR1.1 | A user should learn about genetic algorithms by using the program | High     |

### **Compliance and Standards**

| ID    | Requirement Description                   | Priority |
| ----- | ----------------------------------------- | -------- |
| BR2.1 | The system must compy with copyright laws | High     |

### **Cost Management**

| ID    | Requirement Description                                                        | Priority |
| ----- | ------------------------------------------------------------------------------ | -------- |
| BR3.1 | The system should not cost much to run in case of necessity of cloud computing | High     |
