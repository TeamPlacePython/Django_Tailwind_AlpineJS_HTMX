Salle d'escrime de Mandelieu.

- Page d'accueil
	- Je ne vois pas de problème, mais tous les conseils sont bons à prendre.
		- Carousel -> ok
		- Derniers posts -> ok (mais en travaux)
		- Les dernières images -> ok
		- Les membres sont en mode aléatoire -> ok
		- Les compétitions, on ne voit que celles qui sont à venir ou celle qui ont moins de 24h -> ok
		- Les résultats, on ne voit que les derniers résultats à l'accueil -> ok
		- Le placement sur la carte est bon, tout en javascript, il y a-t-il des améliorations à apporter, sinon c'est ok.
		
- Escrime
	- Cotisation
		- Le tableau est ok selon moi
		-> J'aimerais automatiser le changement de date pour les catégories, car dans 1 ans les dates ne seront plus en cohérence 
		avec les catégories et il faudra les changer à la main. Un modification annuel au 1er août par exemple. Je n'ai pas sû faire.
		je l'ai fait dans apps/membres/management/commands/reset_member_status.py
	
	- Horaires
		- Le tableau des horaires est ok car si des modifications sont à apportées ce sera à la mains.
		
	- Resultats
		- Tout s'affiche comme prévu, mais peut-on rendre ça plus dynamique? Il y a un petit saut au moment de la selection, comment l'enlever?
		
	- L'histoire
		- Le style est bon mais le fichier en dur, donc il faut voir à le modifier. En revanche pour ce genre de fichier, y a t-il un intéret à le rendre dynamique?
		
- Blog
	- Il est en cours de travail. Mais tout est bon à prendre. Il y a des erreurs pour le moment, mais je travaille dessus.
	
	- Mur d'images
		- Je veux qu'il y ai un scroll infini mais il ne fonctionne pas et là je ne saais pas pourquoi.
		J'ai repris le même principe que sur blog, mais ça ne veux pas. Si je tape ?page=2, ca fonctionne mais sur une autre page...
		
- Newsletter
	- Elle est en stand by car des choses me vont mais pas d'autre, besoin de conseils, d'avis etc...
		
- Membre
	- Membres
		- Les filtres sont -> ok
		- l'affichage est -> ok
		- Peut-être voir la sécurité.
		
		- Reset status le 1er août de chaque année
		- Changement de catégorie automatique selon la date de naissance
		
	- Création
		- Le fichier de la photo ne part pas à l'enregistrement, je suis obligé de m'y reprendre à 2 fois. Je ne vois pas m'erreur.
	
	- Tableau
		- Le tableau est ok selon moi
		
- Users
	- Voir la vérification par email plutot que dans la console.
	