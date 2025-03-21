DEVIS - Développement Application Mobile BRICO Delivery App (Révisé)

À l'attention de : De la part de : William Merveille AKLAMAVO / WakamTech Date :

Objet : Devis révisé pour le développement de l'application mobile BRICO Delivery App

Introduction

Suite à la mise à jour de votre cahier des charges, je vous présente ce devis révisé pour le développement de l'application BRICO Delivery App. J'ai pris en compte les modifications apportées, notamment l'ajout de nouvelles fonctionnalités (choix du véhicule, frais de livraison différenciés, code de validation de livraison, etc.), l'élaboration *complète* des maquettes, et la demande de tarification pour un MVP (Minimum Viable Product) et une version complète.

Ce devis propose une solution technique complète et évolutive, basée sur React Native (applications mobiles iOS et Android), Python/Django (Backend) et PostgreSQL (base de données).  Il détaille *deux* options : un MVP et une version complète (toutes les fonctionnalités du cahier des charges).  Les frais annexes sont également mis à jour.

1. Propositions de Services : MVP et Version Complète

Compte tenu des nouvelles exigences du cahier des charges, je propose *deux* options distinctes :

**1.1. Option 1 : MVP (Minimum Viable Product) - Phase 1 Essentielle**

Le MVP se concentre sur les fonctionnalités *absolument essentielles* pour un lancement rapide et une validation du concept auprès des utilisateurs.  Il permet de tester le marché avec un investissement initial réduit.

**Fonctionnalités Incluses dans le MVP :**

*   ⚙️ **Configuration Initiale des Environnements de Développement :**  Identique pour les deux options.
*   🧠 **Conception UX/UI (Maquettes Complètes) :**
    *   Conception *complète* des maquettes de l'application (utilisateur, livreur).  Pas de maquettes préexistantes à reprendre.
    *   Design System de base.
    *   Parcours utilisateurs optimisés pour les fonctionnalités du MVP.
*   ⚙️ **Développement Back-end (Python/Django API) - MVP :**
    *   API RESTful (Django REST Framework).
    *   Gestion des utilisateurs (clients, livreurs) et authentification sécurisée.
    *   Gestion simplifiée du catalogue (intégration API *basique* des enseignes partenaires - consultation des produits, *pas* de gestion des stocks en temps réel dans le MVP).  Le MVP se concentre sur 1 ou 2 enseignes au maximum.
    *   Gestion des commandes (panier, validation, paiement Stripe, suivi basique).
    *   Géolocalisation du magasin et du client (Google Maps API ou Mapbox).
    *   Suivi *basique* de la commande (pas de tracking GPS en temps réel du livreur dans le MVP).
    *   Système de notation des livreurs.
    *   Pas d'interface d'administration pour les enseignes dans le MVP (gestion manuelle des commandes par l'équipe Brico Delivery).
    *   Base de données PostgreSQL.
*   🎨 **Développement Front-end (React Native) – Applications Utilisateur et Livreur - MVP :**
    *   Applications iOS et Android (React Native).
    *   **Application Utilisateur (MVP) :**
        *   Création de compte (email, téléphone, Google, Apple).
        *   Sélection d'une enseigne (géolocalisation).
        *   Consultation du catalogue (via API, affichage simplifié).
        *   Ajout au panier.
        *   Validation de la commande.
        *   Paiement (Stripe).
        *   Suivi *basique* de la commande.
        *   Historique des commandes.
        *   Notation des livreurs.
    *   **Application Livreur (MVP) :**
        *   Inscription et vérification (validation manuelle).
        *   Gestion des disponibilités.
        *   Notification de commande.
        *   Acceptation/refus.
        *   Itinéraire (Google Maps API ou Mapbox).
        *   Validation de la livraison (code).
        *   Historique des courses.
        *   Pas de portefeuille électronique dans le MVP.
    *   Design UI/UX optimisé pour le MVP.
*   🚀 **Déploiement sur les Stores (iOS et Android) – Déploiement Initial :**  Identique pour les deux options.

*   📄 **Nombre de Pages/Écrans Estimé (MVP) :** Environ 20-25 écrans.

**Durée Totale Estimée (MVP) :** 40-50 jours-homme.

**Prix Total MVP :** 3000 euros.

**1.2. Option 2 : Version Complète (Toutes Fonctionnalités) - Phase 1 Complète**

Cette option inclut *toutes* les fonctionnalités décrites dans le cahier des charges mis à jour, offrant une expérience utilisateur et des outils d'administration complets dès le lancement.

**Fonctionnalités Incluses dans la Version Complète (en plus du MVP) :**

*   🧠 **Conception UX/UI (Maquettes Complètes) :**
    *   Conception *complète* des maquettes de *toutes* les interfaces (utilisateur, livreur, enseigne, admin).
    *   Design System complet.
    *   Parcours utilisateurs optimisés pour *toutes* les fonctionnalités.
*   ⚙️ **Développement Back-end (Python/Django API) - Version Complète :**
    *   Tout ce qui est inclus dans le MVP, plus :
    *   Intégration API *avancée* des enseignes partenaires (gestion des stocks *en temps réel*, catalogues complets). Intégration de potentiellement toutes les enseignes (Leroy Merlin, Castorama, Bricoman).
    *   Choix de la taille du véhicule et calcul des frais de livraison (S, M, L).
    *   Suivi de commande en temps réel (tracking GPS du livreur).
    *   Interface d'administration pour les enseignes (gestion des commandes, statistiques).
        * Abonnement mensuel
    *   Interface d'administration web (admin Brico Delivery) : gestion des utilisateurs, commandes, paiements, support client.
    *   Portefeuille électronique pour les livreurs.
    *   Service client via formulaire e-mail (pour les utilisateurs).
    *   API de messagerie (Twilio ou Firebase) pour les notifications push avancées.
*   🎨 **Développement Front-end (React Native) – Applications Utilisateur et Livreur - Version Complète :**
    *   Tout ce qui est inclus dans le MVP, plus :
    *   **Application Utilisateur (Version Complète) :**
        *   Choix du véhicule de livraison.
        *   Affichage des frais de livraison différenciés.
        *   Suivi en temps réel (tracking GPS).
        *   Factures détaillées.
        *   Formulaire de service client.
    *   **Application Livreur (Version Complète) :**
        *   Portefeuille électronique.
    * **Application Web Admin**
        * Gestion utilisateurs
        * Gestion commandes et livraison
        * Gestion des paiements
        * Gestion du support
*   📄 **Nombre de Pages/Écrans Estimé (Version Complète) :** Environ 40-50 écrans (incluant l'application admin web).

**Durée Totale Estimée (Version Complète) :** 70-85 jours-homme.

**Prix Total Version Complète :** 5 900 euros.

2. Frais Annexes Estimés (à la Charge du Client) - *Mis à Jour*

Les frais annexes restent globalement similaires, mais voici quelques ajustements et précisions :

*   **Frais d'Abonnement API Tierces :**
    *   **Stripe :**  Pas de changement (1.4% + 0.25€ par transaction, environ).
    *   **Firebase :**  L'estimation reste la même (50-200€/mois en fonction de l'utilisation), mais il est *crucial* de surveiller la consommation, surtout avec le tracking GPS en temps réel dans la version complète.
    *   **Google Maps API :**  L'estimation reste la même, mais la version complète, avec le tracking GPS en temps réel, utilisera *davantage* l'API Google Maps.  L'optimisation de l'utilisation sera *essentielle* pour contrôler les coûts.
    * **API Enseignes Partenaires**: Il se peut que l'integration des catalogues produits via API des enseignes partenaires engendre des couts.

*   **Frais d'Hébergement Backend :**  L'estimation reste similaire (50-150€/mois), mais la version complète, avec plus de données et de fonctionnalités, pourrait nécessiter une infrastructure légèrement plus puissante.

*   **Frais de Publication sur les Stores :**  Pas de changement (99€/an pour Apple, 25€ pour Google).

*   **Maintenance Applicative et Support Technique Post-Lancement (Optionnel) :**  Toujours optionnel, mais fortement recommandé, surtout pour la version complète.  Un devis séparé pourra être établi après le lancement.

**Important : Transparence sur les Frais Annexes**

*   Les estimations sont toujours basées sur une utilisation *normale*.  Une utilisation intensive (très grand nombre de commandes, tracking GPS constant) entraînera des coûts plus élevés.
*   Je m'engage à optimiser l'utilisation des API, mais je ne peux *pas* garantir des montants fixes.
*   Un suivi *régulier* des coûts des API et de l'hébergement est *indispensable*, surtout dans les premiers mois après le lancement.

3. Calendrier Prévisionnel

*   **MVP :**
    *   Démarrage : [Date à définir].
    *   Livraison Beta : ~30-40 jours après le démarrage.
    *   Lancement : ~40-50 jours après le démarrage.

*   **Version Complète :**
    *   Démarrage : [Date à définir].
    *   Livraison Beta : ~60-70 jours après le démarrage.
    *   Lancement : ~70-85 jours après le démarrage.

Ces calendriers sont des estimations et seront affinés après validation du devis et étude des API des enseignes.

4. Conditions de Paiement

Paiement sur ComeUp comme la plateforme l'exige.

5. Sécurité et RGPD

Pas de changement : engagement total au respect de la sécurité et du RGPD.

6. Validité du Devis

Ce devis révisé est valable pendant 30 jours.

Conclusion

Ce devis révisé offre deux options claires : un MVP pour un lancement rapide et une validation du concept, et une version complète avec toutes les fonctionnalités du cahier des charges. Je suis à votre disposition pour discuter de ces options et choisir celle qui correspond le mieux à votre stratégie et à votre budget. J'ai hâte de collaborer avec vous sur ce projet passionnant.

Cordialement,

William Merveille AKLAMAVO / WakamTech
