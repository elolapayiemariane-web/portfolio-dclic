// ===========================================
//  js/app.js
//  Scripts du portfolio (version 100% statique)
// ===========================================

// --- Effet de fond sur la navbar au défilement ---
window.addEventListener('scroll', () => {
  document.querySelector('.navbar').classList.toggle('scrolled', window.scrollY > 20);
});

// --- Scroll-spy : met à jour le lien actif de la navbar selon la section visible à l'écran ---
window.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('section[id]');
  const liensNav = document.querySelectorAll('.nav-links a[href^="#"]');

  const observateur = new IntersectionObserver((entrees) => {
    entrees.forEach((entree) => {
      if (entree.isIntersecting) {
        const idVisible = entree.target.getAttribute('id');

        liensNav.forEach((lien) => {
          lien.classList.toggle('active', lien.getAttribute('href') === '#' + idVisible);
        });
      }
    });
  }, {
    rootMargin: '-40% 0px -50% 0px',
    threshold: 0
  });

  sections.forEach((section) => observateur.observe(section));
});

// --- Filtre des projets par matière (onglets) ---
window.addEventListener('DOMContentLoaded', () => {
  const onglets = document.querySelectorAll('.tab-btn');
  const cartesProjets = document.querySelectorAll('.carte-projet-portfolio');
  const messageVide = document.getElementById('messageAucunProjet');

  onglets.forEach((onglet) => {
    onglet.addEventListener('click', () => {
      const filtre = onglet.getAttribute('data-filtre');

      onglets.forEach((o) => o.classList.remove('active'));
      onglet.classList.add('active');

      let nbVisibles = 0;
      cartesProjets.forEach((carte) => {
        const correspond = filtre === 'tous' || carte.getAttribute('data-categorie') === filtre;
        carte.style.display = correspond ? '' : 'none';
        if (correspond) nbVisibles++;
      });

      if (messageVide) {
        messageVide.style.display = nbVisibles === 0 ? 'block' : 'none';
      }
    });
  });
});

// --- Gestion du menu mobile (hamburger) ---
window.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.querySelector('.nav-links');

  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      const estOuvert = navLinks.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', estOuvert ? 'true' : 'false');
    });

    navLinks.querySelectorAll('a').forEach((lien) => {
      lien.addEventListener('click', () => {
        navLinks.classList.remove('open');
        menuToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
});

// --- Formulaire de contact : validation + envoi via Formspree (sans PHP) ---
window.addEventListener('DOMContentLoaded', () => {
  const formulaire = document.getElementById('contactForm');
  if (!formulaire) return;

  const champNom = document.getElementById('name');
  const champEmail = document.getElementById('email');
  const champMessage = document.getElementById('message');
  const noteFormulaire = document.getElementById('formNote');
  const boutonEnvoyer = formulaire.querySelector('button[type="submit"]');

  const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function afficherMessage(texte, couleur) {
    if (!noteFormulaire) return;
    noteFormulaire.textContent = texte;
    noteFormulaire.style.color = couleur;
  }

  function afficherErreurChamp(champ) {
    champ.setAttribute('aria-invalid', 'true');
  }

  function reinitialiserErreurs() {
    [champNom, champEmail, champMessage].forEach((champ) => champ.removeAttribute('aria-invalid'));
  }

  formulaire.addEventListener('submit', async (evenement) => {
    evenement.preventDefault(); // on gère l'envoi nous-mêmes, en AJAX

    reinitialiserErreurs();
    afficherMessage('', '');

    let estValide = true;

    if (champNom.value.trim() === '') {
      afficherErreurChamp(champNom);
      estValide = false;
    } else if (!regexEmail.test(champEmail.value.trim())) {
      afficherErreurChamp(champEmail);
      estValide = false;
    } else if (champMessage.value.trim() === '') {
      afficherErreurChamp(champMessage);
      estValide = false;
    }

    if (!estValide) {
      afficherMessage('⚠ Merci de remplir correctement tous les champs obligatoires.', '#b3261e');
      return;
    }

    afficherMessage('Envoi en cours...', '#6b5d4f');
    if (boutonEnvoyer) boutonEnvoyer.disabled = true;

    try {
      const reponse = await fetch(formulaire.action, {
        method: 'POST',
        body: new FormData(formulaire),
        headers: { 'Accept': 'application/json' }
      });

      if (reponse.ok) {
        afficherMessage('✓ Message envoyé avec succès ! Je vous répondrai bientôt.', '#2e7d32');
        formulaire.reset();
      } else {
        afficherMessage('⚠ Une erreur est survenue. Merci de réessayer, ou de me contacter directement par email.', '#b3261e');
      }
    } catch (erreur) {
      afficherMessage('⚠ Impossible d\'envoyer le message. Vérifiez votre connexion et réessayez.', '#b3261e');
    } finally {
      if (boutonEnvoyer) boutonEnvoyer.disabled = false;
    }
  });
});