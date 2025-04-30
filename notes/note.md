<h1 align="center">Bienvenu sur le readme de la Salle d'escrime de Mandelieu 👋</h1>
<p align="center">
  <a href="https://twitter.com/LaurentJouron">
    <img alt="Twitter: LaurentJouron" 
      src="https://img.shields.io/twitter/follow/LaurentJouron.svg?style=social" target="_blank" />
  </a>
  <a href="https://github.com/LaurentJouron">
    <img alt="GitHub followers" 
      src="https://img.shields.io/github/followers/LaurentJouron?style=social" />
  </a>
</p>

___________

<h1 align="center">Page d'accueil</h1>

> **Je ne vois pas de problème, mais tous les conseils sont bons à prendre**<br>

* Carousel -> ok
* Derniers posts -> ok (mais en travaux)
* Les dernières images -> ok
* Les membres sont en mode aléatoire -> ok
* Les compétitions, on ne voit que celles qui sont à venir ou celles qui ont moins de 24h -> ok
* Les résultats, on ne voit que les derniers résultats à l'accueil -> ok
* Le placement sur la carte est bon, tout en JavaScript, y a-t-il des améliorations à apporter, sinon c'est ok.
___________

<h1 align="center">Escrime</h1>

> **Il y a quelques petits détails à voir**<br>

* Cotisation
	- Le tableau est ok selon moi
		- J'aimerais automatiser le changement de date pour les catégories, car dans 1 an, les dates ne seront plus en cohérence 
		avec les catégories. J'envisage une modification annuelle au 1er août, mais je n'ai pas su faire.

* Horaires
	- Le tableau des horaires est ok car s'il y avait des modifications elles seraient à apportées à la main.

* Resultats
	- Tout s'affiche comme prévu, mais peut-on rendre ça plus dynamique? Il y a un petit saut au moment de la selection, comment l'éviter?

* L'histoire
	- Le style est bon mais le fichier en dur, donc il faut voir à le modifier. En revanche pour ce genre de fichier, y a t-il un intéret à le rendre dynamique, sauf si j'ajoute un sportif?
		
___________

<h1 align="center">Blog</h1>

> **Il est en cours de travail. Mais tout est bon à prendre. Il y a des erreurs pour le moment, mais je travaille dessus.**<br>

* Blog
    - La partie blog est en travaux, donc rien à faire pour le moment mais quelques conseils éventuellement si besoin.

* Nouveau post
    - C'est là que je compte créer un post. L'image se charge comme je veux mais elle ne part pas non plus. Je suis sur cette partie en ce moment.

* Mur d'images
	- J'ai voulu faire un scroll infini mais il ne fonctionne pas, je ne sais pas pourquoi. J'ai repris le même principe que sur le blog, mais ça ne veux pas. Si je tape ?page=2 dans ma barre, ca fonctionne mais pas en scroll...

___________

<h1 align="center">Newsletter</h1>

- Elle est en stand by car des choses me vont mais pas d'autre, besoin de conseils, d'avis etc...

___________

<h1 align="center">Membre</h1>

> **Je pense que je ne suis pas trop mal là dessus, même si j'ai quelques détails à revoir**<br>

- Membres
	- Les filtres sont -> ok (à voir)
    - L'affichage est -> ok

	- Peut-être ajouter un peu de sécurité. En effet les membres ne doivent pas pouvoir modifier, ni voir le détails des autres membres. Ils doivent juste voir la carte avec nom, prenom, catégorie et l'image.

	- Reset status le 1er août de chaque année. J'arrive à le faire manuellement, mais pas l'automatiser une fois par an. Il faudrait le changer chaque année. Il faut passer tous les membres qui ont le status "membre" de "actif" à "inactif", ensuite les repasser à actif manuellement quand les cotisations sont payés et que l'on a tous les papiers. Je l'ai fait manuellement dans apps/membres/management/commands/reset_member_status.py

    - Il faut changer les membres de catégorie automatiquement selon la date de naissance, une fois par an.

* Création
	- Le fichier de la photo ne part pas à l'enregistrement, je suis obligé de m'y reprendre à 2 fois. Je ne vois pas m'erreur. Ca créer bien le membres, mais pour ajouter l'image, il faut que je fasse une modification, ou que je passe par l'admin.

* Tableau
	- Le tableau est ok selon moi

___________


<h1 align="center">Users</h1>

> **J'ai pas mal de cinseil à recevoir à ce niveau, car pas du tout d'inspiration**<br>

* My Profile
    - J'avoue avoir très peu d'inspiration à ce stade...

* Edit Profile
    - J'avoue avoir très peu d'inspiration à ce stade... (bis)

* Settings
    - Voir la vérification par email plutot que dans le terminal.

