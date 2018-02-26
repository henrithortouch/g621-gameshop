# WSD TEAM Carry Hansen Project Report.
 
### Team
* Hansen Feng **525093**
* Simo Muraja **430706**
* Henri Thor-Touch **352318**

### Feature List

In this section, we have identified our done features and associated selfevaluation for each identified feature. 

#### Mandatory Requirements

1. **Minimum functional requirements**
  * Registering as a player and developer
  * As a developer: add games to their inventory, see list of game sales
  * As a player: buy games, play games, see game high scores and record their score to it
2. **Authentication**
  * Login, logout and register
    * These features utilize the Django auth module. In addition, we check CSRF tokens for these events. E-mail verification is done via console backend.
    * We suggest full points assessment
3. **Basic player functionalities**
  * Purchasing games is functional and done via Simple Payments Service.
  * You can purchase games within the gameshop. You can also play the games when you own them.
  * You may find games to buy based on filters or see the whole list. You can also see the games you own in a separate inventory page.
    * We suggest full points assessment
4. **Basic developer functionalities**
  * You can add a game (URL) and set price for that game and manage that game (remove, modify)
  * You have a basic game inventory and sales statistics (how many of the developers' games have been bought and when)
  * You are only allowed to modify/add/etc. your own games, and you can only add games to your own inventory.
    * We suggest full points assessment
5. **Game/service interaction**
  * HANSEN PLEASE COMMENT
    * YOUR SUGGESTION FOR POINTS
6. **Quality of Work**
  * Our code aims to be as self commenting as possible, however, since our team members come from different coding backgrounds, achieving truly self commenting code is not possible. Therefore, you may find comments in sections that do not provide self commenting attributes.
  * Templates are used effectively in our project. Most of the pages where we define functionality or preview to follow a same suite, we extend a generic.html template that provides us the basic building blocks by using the Django Template Language. For more complex solutions, we wrote them as regular HTML.
  * User experience is taken into account in various functionalities. Logging out provides automatic redirection, after purchasing a game you can view the details and even launch the game right away. We attempted to minimize the amount of clicks and navigation for our users in our gameshop, without the gameshop resulting as a single-page-app. None of our group members were designers, so we attempted to make the site colourful instead of it being a black and white page with pure focus on functionality. However, we do acknowledge that our site is not up to par with current styling principles and resembles something from the 90's.
  * We conducted most of our tests as user tests by testing all interaction routes a regular user might do within our system. Our tests did not involve mechanical testing with any framework and relied more in user knowledge and user-centric approach. One of our group members has knowledge in the field of usability evaluation and our methods have followed task-oriented test evaluation cases such as Cognitive Walkthroughs throughout the system.
    * Due to not using any testing framework which any programmer at this point should create to lessen the burden, we suggest 90% assessment.
7. **Non-functional requirements**
  * Our project plan and all the documents related to it are visible within this document.
  * Project Manager of this project was assigned to the senior member of this team, Henri Thor-Touch. He coordinated communication, work division and work load division to be equally distributed within the team and peer support to be available at all times. He also managed the direction of the project and scheduled weekly working times and individual working times and tasks as needed. Our individual workload can be seen from a separate document within this repository.
  * Our teamwork during the project has been superb and team environment has been relaxing and supporting.
  * Work order has been organized and professional regarding interactions with Aalto Version (Git), despite a few humorous commits and merge requests. We believe humour to be a driving factor in upkeeping motivation while keeping work as professional as possible. We also inspect each other code before merging our branches to master to minimize conflicts. To ensure this, we always merge master branch into our development branches before committing merge requests.
    * Since the project demo is not yet done by the time of this report, we cannot give a total assessment.

#### More Features

1. **Save/load and resolution feature**
  * HANSEN PLEASE COMMENT
    * YOUR SUGGESTION FOR POINTS
2. **Own game**
  * HANSEN PLEASE COMMENT
    * YOUR SUGGESTION FOR POINTS

#### Comments about development process

