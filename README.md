# Suivi-D-penses
Suivi Dépenses

Nabil VINDAS, Alexis BECHET


Contexte

On a des dépenses tous les jours qui sont de nature très varié, allant des courses au supermarché jusqu’à des achat des vêtements. La quantité de dépenses peut être aussi importante qu’on peut oublier exactement combien d’argent on a dépensé. L’idée d’un logiciel pour suivre les dépenses et d’organiser cela afin d’éviter des problèmes.
Le principe est donc de suivre les dépenses de l’utilisateur afin de l’aider à mieux s’organiser. Par ailleurs, le suiveur analysera les dépenses et l’utilisateur aura la possibilité de recevoir des alertes s’il dépasse un budget qu’il a défini préalablement. On pourra aussi définir un budget par catégorie de dépenses et alerter l’utilisateur quand il est proche de la limite du budget.


Détails techniques

L’idée du projet est de suivre les dépenses de l’utilisateur donc on devra faire un peu d’analyse statistique des données afin de donner à l’utilisateur les informations correctes sur ses dépenses et lui aider à mieux gérer son budget. 
Une des parties les plus importantes de ce projet et de faire une interface graphique ergonomique qui permet une lecture claire des informations sur les dépenses de l’utilisateur. Par ailleurs on va devoir demander à l’utilisateur de rentrer des données donc on devra inclure ceci dans l’interface graphique.
Pour l’organisation des données on va faire une base de données en utilisant sqlite3. Pour l’affichage et l’analyse des données on va utiliser la librairie pandas et pour l’affichage on va utiliser matplotlib. 
