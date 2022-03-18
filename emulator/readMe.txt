Kinetics_test est le même fichier que kinetic mais avec seulement les 50 premières entrées de donnée.
Avec les 45 000 lignes de kinectic.csv le chargement des données était trop long (20 min environ) ce qui rendait le debogage fastidieux.

Dans csv function on fait la moyenne entre deux données et on arrondi à trois chiffres après la virgule ce qui permet d'avoir 0.001 sec au lieu de 0.00138201039 ce qui est plus simple pour l'utilisateur.
En faisant la moyenne avec deux données on se retrouve avec une seule valeur par milliseconde