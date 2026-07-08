# Portfolio Elola Payié Mariane — Version statique

Site 100% statique (HTML / CSS / JS), sans PHP ni base de données. Compatible avec **GitHub Pages**.

## ⚠️ Étapes AVANT de mettre en ligne

### 1. Remettre tes images
Ce dossier ne contient pas encore tes vraies images (elles n'ont pas été fournies lors de la conversion). Copie-les depuis ton ancien projet :

- `assets/photo-profil.png` → ta photo de profil (utilisée 2 fois sur la page)
- `assets/projets/exemple-reseaux.jpg`, `exemple-embarque.jpg`, `exemple-signal.jpg` → remplace ces noms par tes vraies images de projets (adapte aussi le nom dans `index.html`)
- `assets/documents/...` → tes vrais rapports/présentations/simulations (PDF, etc.)

### 2. Configurer Formspree pour le formulaire de contact
Le formulaire de contact a besoin d'un service externe pour envoyer les emails (il n'y a plus de PHP/SMTP côté serveur).

1. Va sur https://formspree.io et crée un compte gratuit
2. Crée un nouveau formulaire ("New Form")
3. Copie l'URL fournie, du type `https://formspree.io/f/abcd1234`
4. Ouvre `index.html`, cherche la ligne :
   ```html
   <form class="contact-form" id="contactForm" action="https://formspree.io/f/REMPLACE_PAR_TON_ID" method="POST" novalidate>
   ```
5. Remplace `REMPLACE_PAR_TON_ID` par ton vrai identifiant Formspree
6. Formspree t'enverra un email de confirmation la première fois qu'un message est envoyé — valide bien ton adresse `payiemarianeelola@gmail.com` dans les réglages du formulaire Formspree

### 3. Ajouter un nouveau projet
Comme il n'y a plus de panneau admin, l'ajout d'un projet se fait en modifiant `index.html` directement :

1. Ouvre `index.html`, repère la section `<!-- PROJET 1 -->`, `<!-- PROJET 2 -->`, etc.
2. Copie un bloc entier `<div class="carte-projet-portfolio">...</div>`
3. Colle-le juste avant la fermeture de `<div class="grille-projets-portfolio">`
4. Modifie :
   - `data-categorie` : `signal`, `reseaux`, `embarque` ou `fibre`
   - l'image et son chemin dans `assets/projets/`
   - le titre, la description, les compétences, les tags technologiques
   - les liens vers les documents dans `assets/documents/`
5. Sauvegarde, puis publie (`git add .` / `git commit` / `git push`)

## Déploiement sur GitHub Pages

1. Renomme (ou crée) le dépôt GitHub dédié à cette version statique, ou remplace le contenu de ton dépôt actuel par ces fichiers
2. Pousse ces fichiers sur la branche `main`
3. Sur GitHub → Settings → Pages
4. Source : `Deploy from a branch`, branche `main`, dossier `/ (root)`
5. Ton site sera visible après 1-2 minutes à l'adresse :
   `https://TON-PSEUDO.github.io/NOM-DU-DEPOT/`

## ✅ Qualité — Checklist avant mise en ligne finale

Une fois le site déployé, passe en revue les points suivants pour garantir un rendu propre et professionnel.

### Performances
- [ ] Compresser les images avant upload (utiliser [tinypng.com](https://tinypng.com) ou [squoosh.app](https://squoosh.app)) — viser < 300 Ko par image
- [ ] Vérifier le temps de chargement avec l'outil [PageSpeed Insights](https://pagespeed.web.dev) (colle ton URL GitHub Pages)
- [ ] Éviter les images surdimensionnées (une photo de profil n'a pas besoin de faire 4000×3000 px)

### Affichage responsive (mobile / tablette)
- [ ] Ouvrir le site sur ton téléphone, ou utiliser les outils développeur du navigateur (`F12` → icône mobile) pour tester différentes tailles d'écran
- [ ] Vérifier que le menu hamburger (☰) s'ouvre et se ferme correctement sur mobile
- [ ] Vérifier qu'aucun texte ni image ne déborde de l'écran
- [ ] Tester le filtre par onglets (Tous / Signal / Réseaux / etc.) sur mobile

### Liens et contenus
- [ ] Cliquer sur chaque lien de navigation (Accueil, Projets, Compétences, Contact) et vérifier qu'il scrolle au bon endroit
- [ ] Cliquer sur chaque document projet (Rapport, Présentation, Simulation) et vérifier qu'il s'ouvre bien (pas de 404)
- [ ] Vérifier que toutes les images s'affichent (pas d'icône "image cassée")
- [ ] Relire l'orthographe et la cohérence des textes (descriptions, compétences)
- [ ] Vérifier que le lien LinkedIn et les coordonnées de contact sont corrects

### Formulaire de contact
- [ ] Envoyer un message test via le formulaire et vérifier sa réception dans ta boîte mail
- [ ] Tester avec un email invalide (ex: `test@test`) pour vérifier que le message d'erreur s'affiche
- [ ] Tester avec des champs vides pour vérifier que la validation bloque bien l'envoi

### Accessibilité de base
- [ ] Vérifier que chaque image a un texte alternatif (`alt="..."`) descriptif
- [ ] Vérifier que le contraste texte/fond reste lisible (déjà correct avec la palette actuelle)
- [ ] Vérifier que le site reste utilisable en zoomant à 150-200% (`Ctrl` + `+`)

### Sécurité / propreté du dépôt
- [ ] Vérifier qu'aucun identifiant, mot de passe ou clé API n'apparaît dans le code source visible sur GitHub
- [ ] Vérifier que `REMPLACE_PAR_TON_ID` a bien été remplacé par le vrai identifiant Formspree
- [ ] Supprimer les fichiers ou dossiers de test inutiles (`.vscode/`, fichiers temporaires, etc.)

## Fichiers supprimés par rapport à la version PHP

- Tous les fichiers `.php` (ajouter, modifier, supprimer, connexion, admin...)
- `schema.sql` et la base de données MySQL — plus nécessaires
- `PHPMailer/` — remplacé par Formspree
- Le tableau de bord admin et la page de connexion — les projets se gèrent désormais directement dans le code
