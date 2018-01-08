# WSD TEAM Carry Hansen Project Plan.
 
### Team
* Hansen Feng **525093**
* Simo Muraja **430706**
* Henri Thor-Touch **352318**
 
### Goal
A working implementation of an online game store for javascript games.
Game store is a platform where you can sell, buy and play games.
As an example, miniclip with the ability to buy games. 

### Priorities
At the start, we will focus on the homepage(game store) implementation. 
After that we will build views for both developer and gamer inventories, and the game page view where you can play purchased javascript games. When the major views, described above, are done, we start to implement the core features such as, adding games, paying for games and displaying sale statistics.

### Process and Time Schedule
#### Process
We’ll be using git flow as a work model. In Git Flow a master branch is used along with separate feature branches for each feature. Merging a feature branch to master requires a validation from another member during a code review. This practice is used to make sure that master doesn’t break down.
#### Time schedule
Work will be started in the beginning of the third period. We’ll be working together twice a week for two hours each working session. These sessions focus on teamwork and supporting each other and ensuring project flow. In addition group members will be working independently on their own time. We’re looking get the basic structure of the project done within a week or two to allow for easy addition of features.

### Testing
To ensure the quality and robustness of the code, Test Driven Development (TDD) will be used. In practice this means that including passing tests should be a requirement for a pull request to be accepted.

Since the group as no prior experience of javascript testing, we've decided to look into Karma and Mocha.js for our testing framework. Back-end will be tested with normal Django tests, using standard Python libraries.

Acceptance testing is done by hand to verify and validate that functional requirements are fulfilled.

### Risk Analysis
Our software architecture has a risk, as the homepage is the central hub, which is linked to every other part. If homepage breaks, we will lose access to these other parts.

Another risk is our inexperience, as none of us has really worked on these kinds of projects we have no experience in scheduling. So there is a risk that we misjudge the work required to implement these features.

### Analysis
#### User Groups
Our user groups are:
* Admin
  * The administrative users who have control over the Game Store.
* Gamer
  * User who comes to the Game Store to buy games and play them in the Game Store.
* Developer
  * User who comes to the Game Store to add their games to the store for sale at their chosen price.

#### Quality Requirements
Our project has three Quality requirements:
* Security
  * Concernred with Databse security (SQL Injection prevention by SQL Recompiling and Input Sanitation)
* Reliability
  * Our service should be operable in error situations and prevent errors from crashing our software.
* Usability
  * Our service should be easy to use and UI be intuitive to provide a pleasant user experience.

#### Architecture Design
![Architecture Design](./architecture.png)

#### Element Catalogue
[Element Catalogue](./element_catalogue.pdf)
