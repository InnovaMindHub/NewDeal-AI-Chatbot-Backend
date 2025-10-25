from typing import Dict, List, Optional, Tuple
import re
import random
from difflib import SequenceMatcher
from app.utils.logging import logger

class PredefinedQASystem:
    """Système de questions-réponses prédéfinies pour éviter les appels LLM inutiles"""
    
    def __init__(self):
        self.qa_database = {

            "Bonjour": {
                "answers": [
                    "Bonjour ! Bienvenue sur l'assistance New Deal Technologique. Comment puis-je vous aider aujourd'hui ?",
                    "Salut ! Je suis là pour vous renseigner sur le New Deal Technologique. Que souhaitez-vous savoir ?",
                    "Bonjour ! Ravi de vous accueillir. Comment puis-vous vous aider concernant la stratégie numérique du Sénégal ?",
                    "Hello ! Bienvenue dans l'univers du New Deal Technologique. Quelle est votre question ?",
                    "Bonjour ! Je suis votre assistant dédié au New Deal Technologique. En quoi puis-je vous assister ?",
                    "Salutations ! Je suis ici pour vous éclairer sur le New Deal Technologique. Quelle est votre demande ?",
                    "Bonjour ! Heureux de vous rencontrer. Que puis-je faire pour vous concernant le numérique sénégalais ?",
                    "Bien le bonjour ! Je suis votre guide pour le New Deal Technologique. Comment puis-je vous servir ?",
                    "Bonjour ! Bienvenue sur notre plateforme d'information du New Deal Technologique.",
                    "Salut ! Prêt à découvrir le New Deal Technologique ? Que souhaitez-vous connaître ?"
                ],
                "keywords": ["bonjour", "salut", "hello", "coucou", "bjr", "salutations", "bonsoir"],
                "confidence": 0.95
            },

            "Comment ça va": {
                "answers": [
                    "Je vais très bien, merci ! Prêt à vous aider sur le New Deal Technologique. Et vous, comment allez-vous ?",
                    "Parfaitement, merci ! Je suis opérationnel pour répondre à vos questions sur le numérique sénégalais.",
                    "Je fonctionne optimalement ! Prêt à discuter du New Deal Technologique. Et de votre côté ?",
                    "Très bien, merci de demander ! En quoi puis-je vous assister concernant la transformation digitale ?",
                    "Excellent ! Je suis là pour vous éclairer sur le New Deal Technologique. Et vous ?",
                    "Au top de ma forme ! Prêt à vous renseigner sur la stratégie numérique sénégalaise.",
                    "Je vais très bien, merci ! Quelle question avez-vous sur le New Deal Technologique ?",
                    "Parfait ! En pleine capacité pour vous aider avec le New Deal Technologique.",
                    "Très bien, merci ! Quelle aspect du New Deal Technologique vous intéresse ?",
                    "Je suis opérationnel à 100% ! Prêt à répondre à vos interrogations sur le numérique."
                ],
                "keywords": ["comment ça va", "ça va", "comment vas-tu", "tu vas bien", "comment allez-vous", "état"],
                "confidence": 0.9
            },

            "Au revoir": {
                "answers": [
                    "Au revoir ! Merci de votre intérêt pour le New Deal Technologique. À bientôt !",
                    "À la prochaine ! N'hésitez pas à revenir pour plus d'informations sur le numérique sénégalais.",
                    "Au revoir ! Bonne continuation dans vos projets digitaux.",
                    "À bientôt ! Restez connecté avec l'actualité du New Deal Technologique.",
                    "Salut ! Merci pour cet échange sur notre stratégie numérique.",
                    "Au revoir ! Portez-vous bien et à très vite pour de nouvelles informations.",
                    "À la prochaine fois ! Continuez à vous intéresser au développement digital du Sénégal.",
                    "Au revoir ! Merci pour votre curiosité sur le New Deal Technologique.",
                    "Bonne journée ! Revenez quand vous voulez pour en savoir plus.",
                    "À bientôt ! Le Sénégal numérique vous attend pour de nouvelles aventures."
                ],
                "keywords": ["au revoir", "à plus", "salut", "bye", "goodbye", "à bientôt", "à la prochaine", "adieu"],
                "confidence": 0.95
            },

            "Bonne journée": {
                "answers": [
                    "Merci ! Bonne journée à vous aussi. Continuez à explorer le New Deal Technologique !",
                    "Merci ! Excellente journée dans l'univers du numérique sénégalais.",
                    "Bonne journée à vous ! Merci pour votre intérêt pour notre stratégie digitale.",
                    "Merci ! Passez une excellente journée pleine d'innovations technologiques.",
                    "Bonne journée ! Que le digital vous accompagne dans toutes vos activités.",
                    "Merci ! Une belle journée à vous dans ce Sénégal en transformation numérique.",
                    "Bonne journée ! Portez haut les couleurs du numérique sénégalais.",
                    "Merci ! Excellente journée et à bientôt pour de nouveaux échanges.",
                    "Bonne journée à vous ! Que l'innovation soit avec vous aujourd'hui.",
                    "Merci ! Passez une journée numérique et productive !"
                ],
                "keywords": ["bonne journée", "bonne soirée", "bonne nuit", "excellente journée", "passez une bonne journée"],
                "confidence": 0.9
            },

            "Merci": {
                "answers": [
                    "Je vous en prie ! N'hésitez pas si vous avez d'autres questions sur le New Deal Technologique.",
                    "De rien ! C'est un plaisir de vous informer sur la transformation digitale du Sénégal.",
                    "Avec plaisir ! N'hésitez pas à revenir pour plus de détails sur notre stratégie numérique.",
                    "Je vous en prie ! Continuez à vous intéresser au développement tech du Sénégal.",
                    "De rien ! Ravis d'avoir pu vous éclairer sur le New Deal Technologique.",
                    "C'est normal ! N'hésitez pas si vous avez besoin d'autres informations sur le numérique.",
                    "Je vous en prie ! Bonne continuation dans votre découverte du New Deal Technologique.",
                    "Avec grand plaisir ! Le digital sénégalais a besoin de citoyens informés comme vous.",
                    "De rien ! Merci à vous pour votre intérêt pour l'innovation nationale.",
                    "Je vous en prie ! Ensemble, construisons le Sénégal numérique de demain."
                ],
                "keywords": ["merci", "merci beaucoup", "thanks", "thank you", "je vous remercie", "gratitude"],
                "confidence": 0.95
            },

            "Aide appréciée": {
                "answers": [
                    "Merci à vous ! Votre intérêt pour le New Deal Technologique est très motivant.",
                    "Je suis ravi d'avoir pu vous aider ! Continuez à explorer notre stratégie numérique.",
                    "C'est un plaisir de servir des citoyens curieux comme vous !",
                    "Merci pour votre reconnaissance ! Cela m'encourage à continuer à informer.",
                    "Je vous remercie ! Votre engagement pour le numérique sénégalais est inspirant.",
                    "Merci beaucoup ! N'hésitez pas à partager ces informations autour de vous.",
                    "Je suis touché ! Continuez à vous intéresser au développement tech de notre pays.",
                    "Merci pour votre feedback ! Cela m'aide à améliorer mon assistance.",
                    "Je vous remercie chaleureusement ! Votre curiosité est précieuse pour le Sénégal digital.",
                    "Merci infiniment ! Ensemble, faisons avancer la cause du numérique national."
                ],
                "keywords": ["super aide", "très utile", "excellente aide", "bravo", "parfait", "génial", "formidable", "bon travail"],
                "confidence": 0.9
            },

            "Reconnaissance spécifique": {
                "answers": [
                    "Merci ! C'est exactement pour informer comme cela que je suis programmé.",
                    "Je vous remercie ! Mon rôle est de rendre le New Deal Technologique accessible à tous.",
                    "Merci beaucoup ! La démocratisation de l'information numérique est ma mission.",
                    "Je suis honoré ! Partager la connaissance sur notre stratégie tech est primordial.",
                    "Merci ! Chaque citoyen informé est un acteur du Sénégal numérique de demain.",
                    "Je vous remercie ! Votre compréhension du New Deal Technologique nous motive.",
                    "Merci infiniment ! L'appropriation citoyenne de notre stratégie digitale est essentielle.",
                    "Je suis ravi ! Votre intérêt pour l'innovation sénégalaise est encourageant.",
                    "Merci chaleureusement ! Continuons ensemble à explorer les opportunités du numérique.",
                    "Je vous remercie ! Votre engagement pour la transformation digitale est précieux."
                ],
                "keywords": ["très clair", "explication parfaite", "compréhensible", "bien expliqué", "clair et net", "précis"],
                "confidence": 0.85
            },

            "Présentation": {
                "answers": [
                    "Je suis l'assistant virtuel du New Deal Technologique, la stratégie numérique du Sénégal pour 2034.",
                    "Je suis votre guide expert sur le New Deal Technologique, la feuille de route digitale du Sénégal.",
                    "Enchanté ! Je suis le spécialiste du New Deal Technologique, votre référence sur la transformation numérique sénégalaise.",
                    "Je suis dédié à vous informer sur le New Deal Technologique, le plan ambitieux du Sénégal pour le numérique.",
                    "Je suis votre assistant personnel pour le New Deal Technologique, la vision digitale du Président Bassirou Diomaye Faye.",
                    "Je me présente : expert du New Deal Technologique, je vous accompagne dans la découverte de notre stratégie numérique.",
                    "Je suis le compagnon digital du New Deal Technologique, toujours disponible pour vos questions sur l'innovation sénégalaise.",
                    "Je suis la référence New Deal Technologique, votre source d'information sur la révolution digitale du Sénégal.",
                    "Je suis le conseiller virtuel du New Deal Technologique, passionné par la transformation numérique de notre pays.",
                    "Je suis l'ambassadeur digital du New Deal Technologique, heureux de vous guider dans notre aventure tech nationale."
                ],
                "keywords": ["qui es-tu", "présente-toi", "tu es qui", "ton rôle", "ta mission", "identité"],
                "confidence": 0.95
            },

            "Offre d'aide": {
                "answers": [
                    "Je peux vous informer sur tous les aspects du New Deal Technologique : budget, piliers, projets, emplois, formations...",
                    "Je suis spécialisé dans le New Deal Technologique : souveraineté numérique, innovation, infrastructure, formation digitale...",
                    "Je maîtrise tous les sujets du New Deal Technologique. Sur quel domaine souhaitez-vous être éclairé ?",
                    "Je couvre l'ensemble de la stratégie New Deal Technologique. Quel aspect vous intéresse particulièrement ?",
                    "Je peux vous parler des 4 piliers du New Deal Technologique, du budget, des objectifs 2034, des projets concrets...",
                    "Ma expertise couvre le New Deal Technologique dans sa globalité. Quelle est votre question ?",
                    "Je suis compétent sur tous les volets du New Deal Technologique. Comment puis-je vous assister ?",
                    "Je maîtrise les détails du New Deal Technologique : Startup Act, cloud souverain, villes intelligentes, santé digitale...",
                    "Je peux vous renseigner sur les 1105 milliards FCFA du New Deal Technologique et leurs utilisations.",
                    "Mon savoir englobe le New Deal Technologique sous tous ses angles. Quelle information recherchez-vous ?"
                ],
                "keywords": ["tu fais quoi", "que sais-tu faire", "domaines d'expertise", "sujets maîtrisés", "compétences"],
                "confidence": 0.9
            },

            "qu'est-ce que le new deal technologique": {
                "answers": [
                    "Le New Deal Technologique est une stratégie nationale ambitieuse lancée par le Président Bassirou Diomaye Faye pour faire du Sénégal un leader de l'économie numérique en Afrique d'ici 2034. Il remplace le plan 'Sénégal Numérique 2025'.",
                    "C'est la nouvelle feuille de route numérique du Sénégal visant à accélérer la transformation digitale du pays et à renforcer sa souveraineté technologique.",
                    "Stratégie nationale de transformation digitale qui vise à positionner le Sénégal comme un hub technologique de référence en Afrique.",
                    "Initiative présidentielle majeure pour bâtir une économie numérique compétitive et inclusive, créatrice d'emplois et de valeur ajoutée.",
                    "Plan stratégique global qui englobe la souveraineté numérique, l'innovation, la formation et la modernisation de l'administration.",
                    "Vision numérique 2034 du Sénégal articulée autour de quatre piliers fondamentaux pour une transformation digitale profonde.",
                    "Programme structurant de l'État sénégalais pour faire du numérique un levier de développement économique et social durable.",
                    "Politique numérique intégrée visant à accélérer l'émergence technologique du Sénégal sur la scène internationale.",
                    "Cadre stratégique renouvelé pour la transformation digitale, aligné sur les objectifs de développement 'Sénégal 2050'.",
                    "Approche holistique de la digitalisation couvrant infrastructure, services publics, innovation et formation des compétences."
                ],
                "keywords": ["new deal", "technologique", "stratégie", "numérique", "transformation digitale"],
                "confidence": 0.95
            },

            "quels sont les piliers du new deal technologique": {
                "answers": [
                    "Le New Deal Technologique repose sur 4 piliers principaux : 1) Souveraineté numérique et infrastructure, 2) Digitalisation des services publics, 3) Innovation et économie numérique, 4) Leadership et renforcement des capacités.",
                    "Quatre piliers fondamentaux : Souveraineté digitale, Modernisation de l'administration, Innovation économique, et Développement des compétences numériques.",
                    "L'architecture du New Deal comprend : Infrastructure et souveraineté technologique, Services publics digitalisés, Écosystème d'innovation, et Capital humain qualifié.",
                    "Piliers stratégiques : Renforcement de l'indépendance numérique, Transformation digitale de l'État, Stimulation de l'innovation, et Formation des talents tech.",
                    "Structuration en 4 axes : Cyber-souveraineté, Administration 100% digitale, Entrepreneuriat technologique, et Excellence éducative numérique.",
                    "Cadre à quatre dimensions : Autonomie technologique, Excellence des services publics, Dynamisme entrepreneurial, et Compétences futures.",
                    "Piliers interconnectés : Infrastructure résiliente, Services citoyens digitaux, Économie innovante, et Leadership digital.",
                    "Approche quadridimensionnelle : Souveraineté data, E-gouvernement, Écosystème startup, et Formation avancée.",
                    "Quatre chantiers prioritaires : Infrastructures critiques, Digitalisation administrative, Innovation disruptive, et Capacitation humaine.",
                    "Axes stratégiques : Indépendance technologique, Modernisation étatique, Croissance numérique, et Excellence cognitive."
                ],
                "keywords": ["piliers", "souveraineté", "digitalisation", "innovation", "leadership", "capacités"],
                "confidence": 0.9
            },

            "quel est le budget du new deal technologique": {
                "answers": [
                    "Le budget total alloué au New Deal Technologique est de 1 105 milliards de FCFA, soit un investissement massif pour la transformation digitale du Sénégal.",
                    "Enveloppe financière de 1 105 milliards de FCFA dédiée à la mise en œuvre complète de la stratégie numérique nationale.",
                    "Investissement global de 1 105 milliards de francs CFA pour financer l'ensemble des projets du New Deal Technologique.",
                    "Mobilisation de 1 105 milliards FCFA pour couvrir l'infrastructure, l'innovation et la formation dans le cadre du plan digital.",
                    "Budget conséquent de 1 105 milliards FCFA visant à accélérer la transition numérique sur tous les fronts.",
                    "Enveloppe de 1 105 milliards FCFA répartie sur les différents piliers de la transformation technologique.",
                    "Financement massif de 1 105 milliards FCFA pour une transformation digitale profonde et durable.",
                    "Investissement étatique de 1 105 milliards FCFA complété par des partenariats public-privé stratégiques.",
                    "Budget pluriannuel de 1 105 milliards FCFA pour la réalisation des objectifs du New Deal Technologique 2034.",
                    "Mobilisation financière totale de 1 105 milliards FCFA pour le succès de la stratégie numérique sénégalaise."
                ],
                "keywords": ["budget", "milliards", "fCFA", "financement", "investissement"],
                "confidence": 0.85
            },

            "quels sont les objectifs du new deal technologique": {
                "answers": [
                    "Les objectifs principaux incluent : faire du Sénégal un leader numérique africain d'ici 2034, créer 150 000 emplois directs, développer 500 startups labellisées État, et assurer la souveraineté technologique nationale.",
                    "Objectifs stratégiques : Positionnement comme hub digital africain, création massive d'emplois tech, émergence d'un écosystème startup dynamique, et autonomie technologique.",
                    "Vision 2034 : Leadership régional numérique, génération d'emplois qualifiés, écosystème entrepreneurial florissant, et indépendance technologique.",
                    "Cibles principales : Transformation en référence digitale africaine, création de 150 000 emplois, incubation de 500 startups, et maîtrise technologique souveraine.",
                    "Ambitions clés : Excellence numérique continentale, développement économique par l'emploi tech, innovation entrepreneuriale, et contrôle stratégique des technologies.",
                    "Objectifs opérationnels : Classement parmi les leaders tech africains, emplois directs dans le numérique, startups à fort potentiel, et autonomie décisionnelle technologique.",
                    "Cibles stratégiques : Reconnaissance comme pôle d'excellence digital, emplois spécialisés créés, jeunes pousses accompagnées, et souveraineté numérique préservée.",
                    "Finalités : Rayonnement international digital, insertion professionnelle tech, émergence startup nationale, et indépendance technologique stratégique.",
                    "Buts ultimes : Excellence africaine en numérique, développement emploi qualifié, dynamisme entrepreneurial innovant, et autonomie technologique critique.",
                    "Objectifs transformationnels : Leadership économique digital, création valeur par l'emploi, écosystème innovation compétitif, et sécurité technologique nationale."
                ],
                "keywords": ["objectifs", "leader africain", "emplois", "startups", "souveraineté", "2034"],
                "confidence": 0.9
            },

            "comment le new deal technologique sera mis en œuvre": {
                "answers": [
                    "La mise en œuvre s'appuie sur des partenariats public-privé, des investissements massifs dans l'infrastructure, des réformes réglementaires comme le Startup Act, et des programmes de formation intensifs aux métiers du numérique.",
                    "Implémentation via : coopération public-privé, modernisation infrastructurelle, adaptation du cadre légal, et développement accéléré des compétences digitales.",
                    "Déploiement stratégique : alliances sectorielles, investissements infrastructurels, évolution réglementaire, et montée en puissance des capacités humaines.",
                    "Exécution pratique : collaborations multi-acteurs, upgrading des réseaux, innovation régulatoire, et professionnalisation des talents tech.",
                    "Mise en œuvre opérationnelle : partenariats hybrides, construction d'infrastructures, modernisation législative, et formation professionnelle avancée.",
                    "Réalisation concrète : synergies public-privé, déploiement d'infrastructures, réformes structurelles, et éducation aux métiers d'avenir.",
                    "Implémentation progressive : coopérations stratégiques, investissements technologiques, adaptation normative, et préparation des compétences futures.",
                    "Déploiement coordonné : alliances opérationnelles, développement des réseaux, optimisation juridique, et cultivation des expertises digitales.",
                    "Exécution intégrée : partenariats efficaces, construction d'assets technologiques, modernisation du cadre, et développement du capital humain.",
                    "Mise en œuvre structurée : collaborations ciblées, investissements prioritaires, évolution réglementaire, et préparation compétitive des ressources humaines."
                ],
                "keywords": ["mise en œuvre", "partenariats", "infrastructure", "startup act", "formation", "réformes"],
                "confidence": 0.85
            },

            "qu'est-ce que la souveraineté numérique dans le new deal": {
                "answers": [
                    "La souveraineté numérique vise à réduire la dépendance technologique du Sénégal en développant des solutions locales, en sécurisant les données critiques et en renforçant la cybersécurité nationale.",
                    "Concept stratégique visant l'autonomie technologique : développement de solutions made in Senegal, protection des données sensibles, et renforcement des capacités de cyberdéfense.",
                    "Pilier essentiel pour l'indépendance digitale : création d'écosystèmes technologiques locaux, sécurisation des infrastructures critiques, et contrôle des données stratégiques.",
                    "Approche d'autodétermination technologique : promotion des technologies locales, sécurisation des systèmes d'information étatiques, et protection du patrimoine data national.",
                    "Stratégie d'émancipation digitale : développement de compétences locales, sécurisation des infrastructures sensibles, et réduction de la dépendance aux solutions étrangères.",
                    "Vision d'indépendance technologique : stimulation de l'innovation locale, protection des actifs informationnels critiques, et construction de capacités cybernétiques autonomes.",
                    "Politique d'autonomie stratégique : encouragement des technologies domestiques, sécurisation des systèmes vitaux, et maîtrise des chaines de valeur technologiques.",
                    "Doctrine d'indépendance digitale : développement d'expertises nationales, protection des infrastructures numériques essentielles, et contrôle des flux data stratégiques.",
                    "Approche de sécurité technologique : promotion de l'industrie tech locale, durcissement cyber des systèmes critiques, et autonomie décisionnelle en matière numérique.",
                    "Stratégie de résilience digitale : croissance des capacités technologiques internes, protection des actifs informationnels nationaux, et réduction des vulnérabilités externes."
                ],
                "keywords": ["souveraineté", "numérique", "données", "cybersécurité", "autonomie", "dépendance"],
                "confidence": 0.9
            },

            "quels sont les projets d'infrastructure du new deal": {
                "answers": [
                    "Les projets d'infrastructure incluent le déploiement de la fibre optique nationale, le renforcement des data centers, l'amélioration de la connectivité internet en zones rurales et le développement de réseaux 5G.",
                    "Investissements majeurs dans : réseaux fibre nationaux, centres de données sécurisés, connectivité rurale haut débit, et déploiement des technologies mobiles avancées.",
                    "Programmes infrastructurels : extension des réseaux haut débit, construction de data centers souverains, désenclavement numérique des zones reculées, et modernisation des réseaux mobiles.",
                    "Chantiers structurants : déploiement massif de la fibre, développement de l'hébergement data national, réduction de la fracture numérique territoriale, et upgrade des réseaux télécoms.",
                    "Projets clés : maillage fibre optique complet, infrastructures cloud locales, connectivité universelle, et réseaux nouvelle génération.",
                    "Investissements critiques : réseaux dorsaux fibre, capacités d'hébergement souveraines, inclusion numérique rurale, et technologies mobiles avancées.",
                    "Développements infrastructurels : backbone national fibre, data centers sécurisés, couverture internet universelle, et réseaux 5G/6G.",
                    "Programme d'infrastructures : interconnexions fibre nationales, centres données stratégiques, connectivité territoriale équitable, et modernisation réseaux sans fil.",
                    "Chantiers majeurs : déploiement fibre étendu, infrastructures cloud nationales, accessibilité numérique rurale, et technologies cellulaires avancées.",
                    "Investissements structurants : réseaux transmission haut débit, plateformes d'hébergement locales, réduction fracture digitale, et réseaux mobiles nouvelle génération."
                ],
                "keywords": ["infrastructure", "fibre optique", "data centers", "connectivité", "5G", "réseaux"],
                "confidence": 0.85
            },

            "qu'est-ce que le startup act dans le new deal": {
                "answers": [
                    "Le Startup Act est une loi cadre qui vise à créer un environnement favorable aux startups grâce à des incitations fiscales, un accès facilité aux financements et un accompagnement personnalisé pour les jeunes pousses technologiques.",
                    "Cadre législatif dédié aux startups : avantages fiscaux, accès aux financements, simplification administrative, et programmes d'accompagnement sur mesure.",
                    "Loi d'orientation pour les startups : exonérations fiscales, facilitation du financement, allègement des procédures, et dispositifs de mentorat spécialisés.",
                    "Instrument réglementaire favorable : incitations financières, accès au capital, réduction des barrières administratives, et soutien au développement entrepreneurial.",
                    "Cadre juridique incitatif : mesures fiscales avantageuses, ouverture des financements, simplification réglementaire, et écosystème de support intégré.",
                    "Loi-cadre startup : régime fiscal préférentiel, accès facilité aux capitaux, environnement réglementaire allégé, et programmes d'accompagnement dédiés.",
                    "Dispositif législatif startup : avantages fiscaux ciblés, mobilisation de financements, réduction des contraintes administratives, et services de support spécialisés.",
                    "Cadre légal startup : exonérations fiscales progressives, accès élargi au capital, allègement des formalités, et écosystème d'accompagnement complet.",
                    "Régime juridique startup : incitations fiscales structurées, facilitation de l'accès au financement, simplification des processus, et dispositifs de soutien intégrés.",
                    "Loi d'encadrement startup : mesures fiscales incitatives, ouverture des sources de financement, environnement administratif favorable, et programmes d'appui sur mesure."
                ],
                "keywords": ["startup act", "startups", "incitations fiscales", "financements", "accompagnement", "loi"],
                "confidence": 0.9
            },

            "comment le new deal va créer des emplois": {
                "answers": [
                    "Le New Deal prévoit la création de 150 000 emplois directs dans les métiers du numérique grâce au développement des startups, la digitalisation des entreprises et les investissements dans les infrastructures technologiques.",
                    "Création d'emplois via : croissance de l'écosystème startup, transformation digitale des entreprises, investissements infrastructurels massifs, et développement de nouvelles filières technologiques.",
                    "Génération d'emplois directs par : expansion entrepreneuriale tech, modernisation digitale du tissu économique, projets d'infrastructure technologique, et émergence de nouveaux métiers digitaux.",
                    "Stratégie emploi : stimulation startup nationale, accélération digitale des entreprises, chantiers infrastructurels technologiques, et développement de compétences spécialisées.",
                    "Approche création emplois : dynamisme entrepreneurial tech, transformation numérique économique, investissements technologiques structurants, et diversification des métiers du numérique.",
                    "Plan emploi digital : croissance écosystème startup, digitalisation accélérée des PME, projets d'infrastructures technologiques, et émergence de nouvelles professions digitales.",
                    "Stratégie d'emploi tech : essor startup local, modernisation digitale industrielle, programmes d'infrastructure numérique, et développement de filières métiers innovantes.",
                    "Approche génération emplois : vitalité entrepreneuriale tech, transition numérique des secteurs économiques, investissements en infrastructures digitales, et création de nouveaux débouchés professionnels.",
                    "Plan de création d'emplois : expansion startup nationale, transformation digitale économique, chantiers d'infrastructures technologiques, et développement de compétences futures.",
                    "Stratégie emploi numérique : croissance écosystème startup, accélération digitale business, investissements infrastructurels tech, et émergence de métiers d'avenir."
                ],
                "keywords": ["emplois", "création", "150000", "startups", "digitalisation", "métiers du numérique"],
                "confidence": 0.9
            },

            "quels sont les partenariats du new deal technologique": {
                "answers": [
                    "Le New Deal développe des partenariats avec des géants technologiques comme Visa pour la digitalisation des paiements, ainsi qu'avec des institutions internationales et des acteurs locaux pour renforcer l'écosystème numérique.",
                    "Collaborations stratégiques avec : entreprises tech mondiales (Visa), institutions financières internationales, universités, et opérateurs économiques locaux pour un écosystème digital intégré.",
                    "Partenariats diversifiés : alliances avec leaders technologiques globaux, coopération avec institutions de développement, collaborations académiques, et synergies avec acteurs économiques nationaux.",
                    "Réseau de partenariats : accords avec firmes tech internationales, partenariats avec bailleurs multilatéraux, coopérations universitaires, et alliances avec entreprises locales.",
                    "Stratégie partenariale : collaborations avec géants du numérique, partenariats avec institutions financières, alliances académiques, et synergies avec opérateurs économiques nationaux.",
                    "Écosystème partenarial : accords avec entreprises tech mondiales, coopérations avec organisations internationales, partenariats éducatifs, et collaborations avec acteurs économiques locaux.",
                    "Réseau collaboratif : partenariats avec leaders technologiques, alliances avec institutions de développement, coopérations universitaires, et synergies avec entreprises sénégalaises.",
                    "Stratégie de coopération : collaborations avec firmes tech globales, partenariats avec bailleurs internationaux, alliances académiques, et partenariats économiques locaux.",
                    "Approche partenariale intégrée : accords avec entreprises numériques mondiales, coopérations avec institutions multilatérales, partenariats éducatifs, et collaborations avec opérateurs nationaux.",
                    "Écosystème de partenariats : alliances avec géants tech internationaux, coopérations avec organisations de développement, partenariats universitaires, et synergies avec acteurs économiques locaux."
                ],
                "keywords": ["partenariats", "visa", "collaborations", "entreprises tech", "institutions", "écosystème"],
                "confidence": 0.85
            },

            "quels événements tech sont prévus dans le new deal": {
                "answers": [
                    "Le New Deal promeut des événements majeurs comme Dakar SLUSH'D et SALTIS pour connecter startups et investisseurs, stimuler l'innovation et positionner le Sénégal comme hub technologique africain.",
                    "Événements structurants : Dakar SLUSH'D (rencontre startups-investisseurs), SALTIS (plateforme d'innovation), et autres forums tech pour animer l'écosystème et attirer les investissements.",
                    "Calendrier événementiel tech : conférences internationales (Dakar SLUSH'D), salons de l'innovation (SALTIS), et compétitions startup pour dynamiser l'écosystème entrepreneurial digital.",
                    "Programme événementiel : sommets tech internationaux, forums d'innovation, compétitions startup, et rencontres networking pour vitaliser la scène tech sénégalaise.",
                    "Événements phares : rencontres startups-investisseurs (Dakar SLUSH'D), salons technologiques (SALTIS), hackathons, et conférences sectorielles pour animer l'écosystème digital.",
                    "Agenda événementiel : conférences tech majeures, forums innovation, compétitions entrepreneuriales, et rencontres business pour stimuler l'écosystème numérique.",
                    "Événements stratégiques : sommets startups-investisseurs, salons de la tech, concours d'innovation, et rencontres sectorielles pour dynamiser la scène tech nationale.",
                    "Programme d'événements : conférences internationales tech, forums d'innovation, compétitions startup, et événements networking pour activer l'écosystème entrepreneurial.",
                    "Calendrier d'animations : rencontres startups-capital risque, salons technologiques, hackathons innovants, et conférences spécialisées pour vitaliser l'écosystème digital.",
                    "Événements structurants : sommets tech globaux, plateformes d'innovation, compétitions entrepreneuriales, et rencontres business pour energizer l'écosystème numérique."
                ],
                "keywords": ["événements", "dakar slush'd", "saltis", "conférences", "startups", "investisseurs"],
                "confidence": 0.85
            },

            "quelle est la vision 2034 du new deal technologique": {
                "answers": [
                    "La vision 2034 est de faire du Sénégal un leader africain de l'économie numérique, avec une souveraineté technologique affirmée, une administration 100% digitale et un écosystème d'innovation mondialement compétitif.",
                    "Vision stratégique 2034 : positionnement comme référence digitale africaine, autonomie technologique consolidée, services publics entièrement dématérialisés, et écosystème innovation de classe internationale.",
                    "Ambition 2034 : excellence numérique continentale, souveraineté technologique achevée, État entièrement digitalisé, et pôle d'innovation globalement compétitif.",
                    "Cible 2034 : leadership digital africain, indépendance technologique renforcée, administration complètement dématérialisée, et hub d'innovation de rang mondial.",
                    "Vision transformative 2034 : prééminence numérique en Afrique, autonomie technologique stratégique, services publics 100% digitaux, et écosystème innovation internationalement reconnu.",
                    "Projection 2034 : primauté digitale africaine, souveraineté technologique consolidée, gouvernance entièrement digitalisée, et pôle innovation compétitif global.",
                    "Aspiration 2034 : leadership économique digital africain, autonomie technologique avancée, administration totalement dématérialisée, et écosystème innovation de calibre mondial.",
                    "Vision stratégique 2034 : excellence digitale continentale, souveraineté technologique renforcée, services publics intégralement digitaux, et hub innovation internationalement compétitif.",
                    "Objectif vision 2034 : prééminence tech africaine, indépendance technologique assurée, État 100% digital, et pôle innovation de stature mondiale.",
                    "Ambition stratégique 2034 : leadership numérique africain, autonomie technologique consolidée, administration entièrement dématérialisée, et écosystème innovation globalement compétitif."
                ],
                "keywords": ["vision 2034", "leader africain", "souveraineté", "administration digitale", "innovation", "compétitif"],
                "confidence": 0.9
            },

            "comment le new deal va moderniser l'administration": {
                "answers": [
                    "La modernisation de l'administration passe par la création d'une identité numérique biométrique unique, un portail citoyen unifié et la digitalisation complète des services administratifs (création d'entreprise, impôts, cadastre, santé, éducation).",
                    "Transformation administrative via : identité digitale biométrique unique, plateforme citoyenne centralisée, et dématérialisation intégrale des procédures administratives clés.",
                    "Modernisation de l'État par : système d'identité numérique unique, portail services citoyens unifié, et digitalisation des processus administratifs essentiels.",
                    "Réforme digitale administrative : identité numérique biométrique centralisée, guichet unique citoyen digital, et dématérialisation des services publics fondamentaux.",
                    "Transformation digitale de l'administration : identifiant numérique unique biométrique, plateforme unique de services aux citoyens, et numérisation complète des démarches administratives.",
                    "Modernisation technologique de l'État : système d'identité digitale unique, portail unifié de services publics, et digitalisation des procédures administratives critiques.",
                    "Réforme administrative digitale : identité numérique biométrique unifiée, interface citoyenne centralisée, et dématérialisation des services administratifs essentiels.",
                    "Transformation numérique de l'administration : identifiant digital unique biométrique, plateforme citoyenne intégrée, et numérisation des processus administratifs clés.",
                    "Modernisation digitale de l'État : système d'identité numérique unique biométrique, guichet unique digital citoyen, et dématérialisation des services publics majeurs.",
                    "Révolution administrative digitale : identité numérique centralisée biométrique, portail unifié services aux citoyens, et digitalisation complète des procédures administratives."
                ],
                "keywords": ["modernisation", "administration", "identité numérique", "portail citoyen", "dématérialisation", "services publics"],
                "confidence": 0.9
            },







            "qui est le président à l'origine du new deal": {
                "answers": [
                    "Le New Deal Technologique a été lancé par le Président Bassirou Diomaye Faye, dans le cadre de sa vision pour la transformation digitale du Sénégal.",
                    "Cette initiative présidentielle est portée par le Président Bassirou Diomaye Faye qui en a fait une priorité de son mandat.",
                    "Le Président Bassirou Diomaye Faye est l'architecte principal du New Deal Technologique, qu'il a présenté comme sa feuille de route numérique.",
                    "C'est sous l'impulsion du Président Bassirou Diomaye Faye que le New Deal Technologique a été conceptualisé et mis en œuvre.",
                    "L'initiative du New Deal Technologique émane de la vision du Président Bassirou Diomaye Faye pour un Sénégal numérique leader en Afrique.",
                    "Le Président Bassirou Diomaye Faye a personnellement lancé et soutenu le New Deal Technologique comme projet structurant de son quinquennat.",
                    "Porteur principal : le Président Bassirou Diomaye Faye, qui a fait de cette stratégie numérique un axe majeur de sa politique de développement.",
                    "Le New Deal Technologique est une initiative du Président Bassirou Diomaye Faye, reflétant son engagement pour l'innovation technologique.",
                    "C'est le Président Bassirou Diomaye Faye qui a initié le New Deal Technologique pour accélérer la transformation digitale du pays.",
                    "Le Président Bassirou Diomaye Faye est le principal promoteur du New Deal Technologique, qu'il considère comme essentiel pour l'avenir du Sénégal."
                ],
                "keywords": ["président", "bassirou diomaye faye", "origine", "lanceur", "initiateur"],
                "confidence": 0.95
            },

            "quelle est la durée du new deal technologique": {
                "answers": [
                    "Le New Deal Technologique s'étend jusqu'en 2034, avec une vision à long terme pour faire du Sénégal un leader numérique africain.",
                    "La stratégie couvre une période allant jusqu'à 2034, soit un horizon de planification d'environ 10 ans pour une transformation digitale complète.",
                    "Durée prévue : jusqu'à l'horizon 2034, avec des étapes intermédiaires de mise en œuvre et d'évaluation régulières.",
                    "Le New Deal Technologique est conçu pour la décennie à venir, avec 2034 comme année cible pour la réalisation des objectifs principaux.",
                    "Période de déploiement : 2024-2034, permettant une transformation progressive et structurée de l'écosystème numérique sénégalais.",
                    "La feuille de route s'étale sur 10 ans, avec 2034 comme échéance pour l'atteinte des principaux indicateurs de performance.",
                    "Horizon temporel : jusqu'en 2034, avec une planification stratégique divisée en phases de réalisation successives.",
                    "Le programme court jusqu'à 2034, incluant des jalons annuels pour mesurer les progrès accomplis.",
                    "Durée stratégique : décennie 2024-2034, avec une vision claire pour chaque période de mise en œuvre.",
                    "Calendrier global : échéance 2034 pour la pleine réalisation des ambitions du New Deal Technologique."
                ],
                "keywords": ["durée", "2034", "horizon", "période", "calendrier", "échéance"],
                "confidence": 0.9
            },

            "comment les startups peuvent bénéficier du new deal": {
                "answers": [
                    "Les startups peuvent bénéficier d'incitations fiscales, d'un accès facilité au financement, de programmes d'accompagnement et d'un environnement réglementaire favorable grâce au Startup Act.",
                    "Avantages pour les startups : exonérations fiscales, accès privilégié aux fonds, mentorat spécialisé et simplification des procédures administratives.",
                    "Bénéfices startup : régime fiscal avantageux, ouverture des financements, accompagnement sur mesure et cadre réglementaire adapté.",
                    "Les jeunes pousses tech profitent de : mesures fiscales incitatives, facilitation de l'accès au capital, programmes de mentorat et environnement administratif allégé.",
                    "Avantages offerts : incitations financières, accès aux investisseurs, support technique et cadre juridique favorable au développement startup.",
                    "Bénéfices disponibles : exonérations progressives, mobilisation de capitaux, expertise accompagnatrice et simplification des démarches.",
                    "Opportunités startup : avantages fiscaux structurés, ouverture financière élargie, coaching spécialisé et réduction des barrières administratives.",
                    "Avantages concrets : régime fiscal préférentiel, accès aux sources de financement, accompagnement expert et environnement réglementaire optimisé.",
                    "Bénéfices accessibles : mesures fiscales attractives, facilitation du financement, programmes de développement et cadre administratif simplifié.",
                    "Avantages stratégiques : incitations fiscales ciblées, accès au capital-risque, mentorat professionnel et écosystème réglementaire favorable."
                ],
                "keywords": ["startups", "bénéficier", "incitations fiscales", "financement", "accompagnement", "avantages"],
                "confidence": 0.9
            },

            "quelles technologies émergentes sont prioritaires": {
                "answers": [
                    "Les technologies prioritaires incluent l'Intelligence Artificielle, le Cloud Computing, la Cybersécurité, l'Internet des Objets et la Blockchain pour transformer l'économie sénégalaise.",
                    "Technologies émergentes ciblées : IA, Cloud, sécurité informatique, IoT et blockchain comme leviers de transformation digitale.",
                    "Priorités technologiques : intelligence artificielle, informatique en nuage, cyberprotection, objets connectés et technologie blockchain.",
                    "Focus sur les technologies : AI, cloud computing, cybersecurity, internet des objets et blockchain pour l'innovation nationale.",
                    "Technologies stratégiques : intelligence artificielle, cloud, sécurité numérique, IoT et blockchain comme moteurs d'innovation.",
                    "Domaines technologiques prioritaires : IA, cloud computing, protection cybernétique, internet des objets et registre distribué.",
                    "Technologies émergentes clés : intelligence artificielle, infonuagique, cybersécurité, IoT et blockchain pour la compétitivité.",
                    "Priorités innovation : AI, cloud, sécurité informatique, internet des objets et technologie blockchain comme accélérateurs.",
                    "Technologies d'avenir ciblées : intelligence artificielle, cloud computing, cyberdéfense, IoT et blockchain pour la transformation.",
                    "Domaines technologiques stratégiques : IA, cloud, sécurité digitale, internet des objets et blockchain comme piliers d'innovation."
                ],
                "keywords": ["technologies", "IA", "cloud computing", "cybersécurité", "blockchain", "IoT", "priorités"],
                "confidence": 0.85
            },

            "comment le new deal va réduire la fracture numérique": {
                "answers": [
                    "Le New Deal vise à réduire la fracture numérique par le déploiement d'infrastructures en zones rurales, des programmes de formation inclusifs et l'accessibilité financière des services numériques.",
                    "Réduction de la fracture digitale via : extension des réseaux en zones reculées, programmes d'alphabétisation numérique et tarifs abordables pour l'internet.",
                    "Stratégie d'inclusion numérique : infrastructures rurales, formation aux compétences digitales et accessibilité économique des services tech.",
                    "Approche inclusive : désenclavement numérique des campagnes, éducation aux outils digitaux et politiques tarifaires sociales.",
                    "Lutte contre la fracture : couverture internet universelle, initiation aux technologies et subventions pour l'accès numérique.",
                    "Politique d'inclusion : maillage territorial complet, éducation numérique massive et aides à l'acquisition d'équipements.",
                    "Réduction des inégalités digitales : connectivité rurale étendue, formation aux bases numériques et accessibilité financière des services.",
                    "Stratégie inclusive : infrastructures rurales prioritaires, alphabétisation digitale et tarification sociale de l'internet.",
                    "Approche équitable : couverture nationale intégrale, compétences numériques pour tous et soutien à l'accès économique.",
                    "Politique d'inclusion digitale : déploiement rural accéléré, éducation technologique généralisée et aides à l'équipement numérique."
                ],
                "keywords": ["fracture numérique", "réduction", "zones rurales", "inclusion", "accessibilité", "formation"],
                "confidence": 0.85
            },

            "quels sont les indicateurs de succès du new deal": {
                "answers": [
                    "Les indicateurs clés incluent : 150 000 emplois créés, 500 startups labellisées, la couverture internet nationale complète et le taux d'adoption des services publics digitaux.",
                    "Indicateurs de performance : nombre d'emplois tech créés, startups accompagnées, couverture haut débit et usage des services administratifs en ligne.",
                    "Mesures de succès : emplois directs générés, jeunes pousses labellisées, connectivité universelle et adoption des e-services gouvernementaux.",
                    "Indicateurs clés : création d'emplois numériques, émergence startup, accessibilité internet et utilisation des plateformes publiques digitales.",
                    "Metrics de performance : postes tech créés, startups soutenues, desserte internet nationale et recours aux services étatiques dématérialisés.",
                    "Indicateurs stratégiques : emplois du numérique, écosystème startup développé, couverture réseau étendue et usage des outils administratifs digitaux.",
                    "Mesures de réussite : emplois directs dans le tech, startups incubées, connectivité territoriale et adoption des services publics en ligne.",
                    "Indicateurs de performance : emplois tech générés, startups labellisées, infrastructure internet complète et utilisation des plateformes gouvernementales digitales.",
                    "Metrics de succès : créations d'emplois numériques, développement startup, accessibilité web universelle et usage des services administratifs dématérialisés.",
                    "Indicateurs clés : emplois directs créés, startups accompagnées, couverture numérique nationale et adoption des services publics digitaux."
                ],
                "keywords": ["indicateurs", "succès", "performance", "mesures", "emplois", "startups", "couverture"],
                "confidence": 0.9
            },

            "comment la formation est organisée dans le new deal": {
                "answers": [
                    "La formation est structurée autour de programmes spécialisés aux métiers du numérique, de partenariats avec les universités et de centres d'excellence technologique pour développer les compétences locales.",
                    "Organisation de la formation : programmes dédiés aux métiers tech, collaborations universitaires et pôles d'excellence pour le développement des talents numériques.",
                    "Structuration formative : cursus spécialisés digital, partenariats académiques et hubs d'excellence technologique pour la montée en compétence.",
                    "Approche formation : programmes professionnalisants tech, alliances avec l'enseignement supérieur et centres de compétence pour l'expertise locale.",
                    "Organisation éducative : formations aux métiers du numérique, coopérations universitaires et pôles d'excellence pour le capital humain tech.",
                    "Structuration pédagogique : programmes qualifiants digital, partenariats éducatifs et hubs technologiques pour le développement des compétences.",
                    "Approche formative : cursus spécialisés numériques, collaborations académiques et centres d'expertise pour les talents locaux.",
                    "Organisation des formations : programmes métiers tech, alliances universitaires et pôles d'excellence pour les compétences digitales.",
                    "Structuration éducative : formations professionnelles digitales, partenariats enseignement supérieur et hubs de compétence technologique.",
                    "Approche pédagogique : programmes spécialisés numériques, coopérations académiques et centres d'excellence pour le développement des talents."
                ],
                "keywords": ["formation", "compétences", "universités", "centres d'excellence", "métiers du numérique", "talents"],
                "confidence": 0.85
            },

            "quels sont les risques du new deal technologique": {
                "answers": [
                    "Les risques identifiés incluent : les problèmes de cybersécurité, la dépendance technologique persistante, les inégalités d'accès et les défis de gouvernance des données.",
                    "Risques potentiels : vulnérabilités cyber, maintien de dépendances technologiques, fractures digitales accrues et enjeux de souveraineté data.",
                    "Dangers identifiés : menaces cybersécurité, dépendance technologique prolongée, exclusion numérique et défis de régulation data.",
                    "Risques majeurs : sécurité informatique, dépendance aux technologies étrangères, inégalités d'accès et gouvernance des données.",
                    "Facteurs de risque : cybermenaces, persistance de dépendances technologiques, disparités numériques et enjeux de souveraineté informationnelle.",
                    "Risques stratégiques : vulnérabilités numériques, dépendance technologique continue, fractures sociales digitales et défis de management data.",
                    "Dangers potentiels : risques cybersécurité, maintien de dépendances, exclusion technologique et enjeux de gouvernance informationnelle.",
                    "Risques identifiés : menaces digitales, dépendances technologiques durables, inégalités numériques et défis de régulation informationnelle.",
                    "Facteurs de risque : cyberattaques, dépendance technologique persistante, disparités d'accès et enjeux de souveraineté data.",
                    "Risques majeurs : sécurité cybernétique, dépendance aux solutions externes, fracture numérique et défis de gouvernance des données."
                ],
                "keywords": ["risques", "cybersécurité", "dépendance", "inégalités", "gouvernance des données", "menaces"],
                "confidence": 0.8
            },

            "comment le new deal impacte l'éducation": {
                "answers": [
                    "Le New Deal transforme l'éducation par la digitalisation des contenus, la formation aux compétences numériques, les plateformes d'e-learning et l'équipement technologique des établissements.",
                    "Impact éducatif : digitalisation des ressources pédagogiques, développement des compétences digitales, plateformes d'apprentissage en ligne et équipement tech des écoles.",
                    "Transformation éducative : numérisation des contenus, formation aux compétences numériques, solutions e-learning et modernisation technologique des infrastructures éducatives.",
                    "Effets sur l'éducation : dématérialisation des supports, éducation aux technologies, plateformes d'enseignement à distance et équipement numérique des établissements.",
                    "Impact sur le système éducatif : digitalisation des curricula, développement des compétences tech, outils d'apprentissage digital et modernisation tech des écoles.",
                    "Transformation du secteur éducatif : numérisation des ressources, formation aux littératies digitales, plateformes éducatives en ligne et équipement technologique scolaire.",
                    "Effets éducatifs : dématérialisation pédagogique, éducation technologique, solutions d'apprentissage digital et infrastructure tech éducative.",
                    "Impact éducationnel : digitalisation des contenus, compétences numériques intégrées, plateformes d'e-learning et équipement digital des établissements.",
                    "Transformation pédagogique : numérisation des supports, formation aux compétences digitales, outils d'apprentissage en ligne et modernisation tech éducative.",
                    "Effets sur l'enseignement : dématérialisation éducative, intégration des compétences tech, plateformes d'enseignement digital et équipement technologique scolaire."
                ],
                "keywords": ["éducation", "digitalisation", "e-learning", "compétences numériques", "établissements", "contenus"],
                "confidence": 0.85
            },

            "quels sont les projets de smart city dans le new deal": {
                "answers": [
                    "Le New Deal inclut le développement de villes intelligentes avec des solutions de mobilité connectée, de gestion énergétique optimisée et de services urbains digitalisés pour améliorer la qualité de vie.",
                    "Projets smart city : mobilité intelligente connectée, optimisation énergétique avancée et services municipaux digitalisés pour des villes plus efficaces.",
                    "Initiatives ville intelligente : solutions de transport connecté, gestion énergétique smart et services urbains numérisés pour un cadre de vie amélioré.",
                    "Développements smart city : mobilité digitale, management énergétique intelligent et services citoyens dématérialisés pour des cités du futur.",
                    "Projets de villes intelligentes : transports connectés, optimisation de l'énergie et services municipaux digitalisés pour une urbanité améliorée.",
                    "Initiatives de cités intelligentes : mobilité intelligente, gestion énergétique optimisée et services urbains numérisés pour une meilleure qualité de vie.",
                    "Développements de smart cities : solutions mobilité connectée, management énergétique smart et services municipaux digitalisés pour l'efficacité urbaine.",
                    "Projets ville intelligente : transports digitaux, optimisation énergétique avancée et services urbains dématérialisés pour un habitat amélioré.",
                    "Initiatives de villes smart : mobilité connectée, gestion énergétique intelligente et services citoyens numérisés pour un urbanisme optimisé.",
                    "Développements smart city : solutions de mobilité intelligente, management énergétique optimisé et services municipaux digitalisés pour la qualité urbaine."
                ],
                "keywords": ["smart city", "villes intelligentes", "mobilité connectée", "gestion énergétique", "services urbains", "qualité de vie"],
                "confidence": 0.8
            },

            "comment le new deal va financer les projets tech": {
                "answers": [
                    "Le financement combine budget étatique, partenariats public-privé, investissements internationaux et fonds dédiés à l'innovation pour un total de 1 105 milliards FCFA.",
                    "Mécanismes de financement : fonds publics, coopérations public-privé, investissements étrangers et dispositifs dédiés à l'innovation technologique.",
                    "Financement des projets : ressources budgétaires étatiques, partenariats PPP, capitaux internationaux et instruments spécialisés innovation.",
                    "Sources de financement : budget national, collaborations public-privé, investissements globaux et fonds d'innovation technologique.",
                    "Mobilisation financière : fonds gouvernementaux, alliances public-privé, financements internationaux et mécanismes dédiés à la tech.",
                    "Financement stratégique : ressources publiques, partenariats hybrides, investisseurs étrangers et dispositifs d'innovation technologique.",
                    "Mécanismes de funding : budget étatique, coopérations PPP, capitaux internationaux et outils d'innovation dédiés.",
                    "Sources financières : fonds publics, collaborations public-privé, investissements globaux et instruments d'innovation tech.",
                    "Mobilisation des fonds : ressources gouvernementales, alliances public-privé, financements internationaux et mécanismes d'innovation.",
                    "Financement global : budget national, partenariats PPP, investisseurs étrangers et dispositifs spécialisés innovation technologique."
                ],
                "keywords": ["financement", "projets tech", "budget", "partenariats", "investissements", "fonds innovation"],
                "confidence": 0.85
            },

            "quels sont les métiers du numérique ciblés": {
                "answers": [
                    "Les métiers ciblés incluent : développeurs, experts en cybersécurité, data scientists, spécialistes cloud, ingénieurs IA et techniciens en infrastructure réseau.",
                    "Métiers du numérique prioritaires : développement logiciel, sécurité informatique, science des données, cloud computing, intelligence artificielle et réseaux informatiques.",
                    "Professions digitales ciblées : programmation, cybersécurité, analyse de données, technologies cloud, ingénierie IA et gestion de réseaux.",
                    "Métiers tech stratégiques : développement, protection numérique, data analysis, solutions cloud, intelligence artificielle et infrastructure réseau.",
                    "Compétences numériques cibles : développement, sécurité cyber, data science, cloud, AI engineering et gestion réseaux.",
                    "Professions numériques prioritaires : coding, cybersecurity, data management, cloud technologies, AI development et network engineering.",
                    "Métiers du digital ciblés : programmation, sécurité informatique, analyse données, technologies nuage, ingénierie intelligence artificielle et réseaux.",
                    "Compétences tech stratégiques : développement, protection digitale, science des données, cloud computing, IA et infrastructure réseau.",
                    "Professions digitales clés : développement logiciel, cybersécurité, gestion données, solutions cloud, intelligence artificielle et réseaux.",
                    "Métiers numériques prioritaires : programmation, sécurité numérique, analyse data, technologies cloud, engineering IA et gestion infrastructure réseau."
                ],
                "keywords": ["métiers", "numérique", "développeurs", "cybersécurité", "data scientists", "cloud", "IA"],
                "confidence": 0.9
            },

            "comment le new deal va stimuler l'innovation": {
                "answers": [
                    "L'innovation est stimulée par des incubateurs, des financements dédiés, des compétitions technologiques, des partenariats de recherche et un environnement réglementaire favorable.",
                    "Stimulation de l'innovation via : réseaux d'incubation, fonds spécialisés, concours tech, collaborations recherche et cadre réglementaire incitatif.",
                    "Dynamisation innovation : incubateurs et accélérateurs, financements innovation, hackathons et challenges, partenariats R&D et écosystème réglementaire favorable.",
                    "Accélération innovation : structures d'incubation, instruments financiers dédiés, compétitions technologiques, coopérations recherche et environnement légal adapté.",
                    "Stimulation de l'innovations : hubs d'incubation, fonds d'innovation, événements compétitifs tech, alliances recherche et cadre réglementaire stimulant.",
                    "Dynamisation de l'innovation : réseaux d'accompagnement, financements ciblés, concours d'innovation, partenariats scientifiques et écosystème réglementaire favorable.",
                    "Accélération de l'innovation : incubateurs spécialisés, dispositifs financiers innovation, compétitions tech, collaborations R&D et environnement juridique incitatif.",
                    "Stimulation innovante : structures d'accompagnement, fonds dédiés, hackathons et challenges, partenariats recherche et cadre réglementaire adapté.",
                    "Dynamisation de l'innovations : hubs d'innovation, instruments financiers spécialisés, concours technologiques, coopérations scientifiques et écosystème réglementaire favorable.",
                    "Accélération innovative : réseaux d'incubation, financements innovation, événements compétitifs, alliances R&D et environnement légal stimulant."
                ],
                "keywords": ["innovation", "incubateurs", "financements", "compétitions", "recherche", "environnement favorable"],
                "confidence": 0.85
            },

            "quels sont les défis du new deal technologique": {
                "answers": [
                    "Les principaux défis incluent : la formation rapide des compétences, la sécurisation des infrastructures, la réduction de la fracture numérique et l'adoption des services digitaux par la population.",
                    "Défis majeurs : formation accélérée des talents, protection des infrastructures critiques, inclusion numérique et adoption des outils digitaux par les citoyens.",
                    "Enjeux principaux : développement rapide des compétences, sécurisation des systèmes, réduction des inégalités digitales et appropriation des services numériques.",
                    "Défis identifiés : montée en compétence rapide, cybersécurité infrastructurelle, lutte contre l'exclusion numérique et adoption des solutions digitales.",
                    "Enjeux stratégiques : formation express des experts, protection des actifs critiques, inclusion digitale et usage des services en ligne.",
                    "Défis clés : développement des talents tech, sécurité des infrastructures, réduction fracture numérique et utilisation des plateformes digitales.",
                    "Enjeux majeurs : compétence formation accélérée, sécurisation systèmes, inclusion technologique et adoption outils digitaux.",
                    "Défis principaux : montée en puissance des compétences, protection infrastructures, inclusion numérique et usage services dématérialisés.",
                    "Enjeux critiques : développement expertise rapide, cybersécurité, réduction inégalités digitales et appropriation solutions numériques.",
                    "Défis stratégiques : formation intensive des talents, sécurité des systèmes, inclusion digitale et adoption des plateformes en ligne."
                ],
                "keywords": ["défis", "formation", "sécurisation", "fracture numérique", "adoption", "compétences"],
                "confidence": 0.85
            },

            "comment le new deal va améliorer la santé numérique": {
                "answers": [
                    "La santé numérique est améliorée par la télémédecine, les dossiers médicaux électroniques, les applications de suivi patients et la formation aux technologies médicales avancées.",
                    "Amélioration e-santé via : services de télémédecine, dossiers patients électroniques, applications de monitoring et formation aux techs médicales.",
                    "Transformation santé digitale : télémédecine déployée, dossiers médicaux numérisés, outils de suivi patients et compétences technologies médicales.",
                    "Développement santé numérique : solutions télémédecine, dossiers électroniques de santé, applications patient et expertise technologies médicales.",
                    "Amélioration du numérique santé : plateformes télémédecine, dossiers médicaux digitalisés, outils monitoring patients et formation techs médicales.",
                    "Transformation digitale santé : services de téléconsultation, dossiers patients numériques, applications de suivi et compétences technologies santé.",
                    "Développement e-santé : solutions de télémédecine, dossiers électroniques médicaux, outils patient et expertise techs médicales.",
                    "Amélioration numérique santé : plateformes de télémédecine, dossiers médicaux électroniques, applications monitoring et formation technologies santé.",
                    "Transformation de la santé digitale : téléconsultation généralisée, dossiers patients digitalisés, outils de suivi et compétences techs médicales.",
                    "Développement du numérique santé : services télémédecine, dossiers électroniques patients, applications santé et expertise technologies médicales."
                ],
                "keywords": ["santé numérique", "télémédecine", "dossiers médicaux", "applications", "technologies médicales", "e-santé"],
                "confidence": 0.8
            },

            "quels sont les avantages pour les PME": {
                "answers": [
                    "Les PME bénéficient de subventions à la digitalisation, de formations aux outils numériques, d'un accès facilité aux marchés en ligne et d'un accompagnement pour leur transformation digitale.",
                    "Avantages PME : aides financières à la digitalisation, formation aux outils digitaux, accès aux plateformes e-commerce et support à la transformation numérique.",
                    "Bénéfices pour les PME : subventions pour le digital, éducation aux technologies, ouverture des marchés online et accompagnement transition digitale.",
                    "Avantages aux PME : soutiens financiers digitalisation, compétences outils numériques, accès marchés digitaux et assistance transformation numérique.",
                    "Bénéfices PME : aides à la numérisation, formation technologies digitales, accès plateformes en ligne et accompagnement mutation digitale.",
                    "Avantages pour PME : financements digitalisation, apprentissage outils digitaux, ouverture e-marchés et support transition numérique.",
                    "Bénéfices aux PME : subventions numérisation, éducation technologies, accès marchés online et accompagnement transformation digitale.",
                    "Avantages PME : soutiens à la digitalisation, compétences digitales, accès plateformes digitales et assistance mutation numérique.",
                    "Bénéfices pour les PME : aides financières numérisation, formation outils digitaux, ouverture marchés en ligne et support transition digitale.",
                    "Avantages aux PME : financements pour le digital, apprentissage technologies, accès e-commerce et accompagnement transformation numérique."
                ],
                "keywords": ["PME", "avantages", "digitalisation", "subventions", "formation", "marchés en ligne", "accompagnement"],
                "confidence": 0.85
            },

            "comment le new deal va sécuriser les données": {
                "answers": [
                    "La sécurisation des données passe par des lois sur la protection des données, le renforcement de la cybersécurité, des data centers locaux et des audits réguliers de sécurité.",
                    "Sécurisation data via : législation protection données, renforcement cybersécurité, infrastructures data locales et contrôles sécurité périodiques.",
                    "Protection des données : cadre légal data protection, consolidation cybersécurité, centres données nationaux et audits sécurité réguliers.",
                    "Sécurisation informationnelle : lois protection données, durcissement cybersécurité, data centers domestiques et vérifications sécurité continues.",
                    "Protection data : réglementation données personnelles, renforcement sécurité cyber, infrastructures data nationales et inspections sécurité régulières.",
                    "Sécurisation des informations : législation data protection, consolidation sécurité cyber, centres données locaux et contrôles sécurité périodiques.",
                    "Protection informationnelle : cadre juridique données, durcissement cybersécurité, data centers nationaux et audits sécurité récurrents.",
                    "Sécurisation data : lois protection information, renforcement cyberdéfense, infrastructures data domestiques et vérifications sécurité régulières.",
                    "Protection des données : réglementation information personnelle, consolidation sécurité numérique, data centers locaux et inspections sécurité continues.",
                    "Sécurisation information : législation protection information, durcissement cybersécurité, centres données nationaux et contrôles sécurité périodiques."
                ],
                "keywords": ["sécurisation", "données", "protection", "cybersécurité", "data centers", "audits", "lois"],
                "confidence": 0.9
            },

            "quels sont les projets de recherche et développement": {
                "answers": [
                    "Les projets R&D incluent des laboratoires d'innovation technologique, des partenariats universités-entreprises et des programmes de recherche sur l'IA, la blockchain et les technologies vertes.",
                    "Projets R&D : labs d'innovation tech, collaborations universités-industries et recherches sur IA, blockchain et technologies durables.",
                    "Initiatives R&D : laboratoires d'innovation, partenariats académie-industrie et programmes recherche intelligence artificielle, blockchain et techs vertes.",
                    "Projets recherche-développement : centres d'innovation technologique, coopérations universités-entreprises et études sur AI, blockchain et technologies écologiques.",
                    "Programmes R&D : hubs d'innovation, alliances universités-industriels et recherches intelligence artificielle, blockchain et solutions durables.",
                    "Initiatives de R&D : laboratoires tech, collaborations académie-business et projets recherche IA, blockchain et technologies environnementales.",
                    "Projets recherche : pôles d'innovation, partenariats universités-corporations et programmes AI, blockchain et techs vertes.",
                    "Programmes recherche-développement : centres innovation, coopérations académie-industrie et études intelligence artificielle, blockchain et technologies durables.",
                    "Initiatives R&D : labs technologiques, alliances universités-entreprises et recherches sur AI, blockchain et solutions écologiques.",
                    "Projets de R&D : hubs technologiques, collaborations académie-industrie et programmes intelligence artificielle, blockchain et technologies vertes."
                ],
                "keywords": ["recherche", "développement", "R&D", "laboratoires", "partenariats", "IA", "blockchain", "technologies vertes"],
                "confidence": 0.8
            },

            "comment le new deal va booster l'agriculture digitale": {
                "answers": [
                    "L'agriculture digitale est boostée par des capteurs IoT, des drones de surveillance, des plateformes de marché en ligne et des applications de gestion agricole intelligente.",
                    "Boost agriculture digitale via : capteurs connectés IoT, drones de monitoring, plateformes e-commerce agricole et apps de gestion smart farming.",
                    "Développement agri-digital : senseurs IoT, drones surveillance, marchés digitaux agricoles et applications gestion intelligente agricole.",
                    "Accélération agriculture numérique : capteurs IoT, drones de contrôle, plateformes online agricoles et outils gestion farming intelligent.",
                    "Stimulation agri-tech : dispositifs IoT connectés, drones monitoring, marchés en ligne agricoles et apps management agricole smart.",
                    "Développement digital agriculture : senseurs connectés, drones surveillance, plateformes e-marché agricole et applications gestion farming intelligent.",
                    "Accélération agri-numérique : capteurs IoT, drones de suivi, marchés digitaux agricoles et outils management agricole intelligent.",
                    "Stimulation agriculture digitale : équipements IoT, drones contrôle, plateformes online farming et apps gestion agricole smart.",
                    "Développement tech-agricole : senseurs IoT, drones monitoring, marchés en ligne farming et applications management agricole intelligent.",
                    "Accélération digital farming : capteurs connectés, drones surveillance, plateformes e-commerce agricole et outils gestion farming smart."
                ],
                "keywords": ["agriculture digitale", "IoT", "drones", "plateformes en ligne", "gestion intelligente", "agri-tech"],
                "confidence": 0.8
            },

            "quels sont les impacts environnementaux du new deal": {
                "answers": [
                    "Le New Deal intègre des technologies vertes, l'optimisation énergétique des data centers et la promotion de solutions numériques durables pour réduire l'empreinte environnementale.",
                    "Impacts environnementaux : intégration de technologies vertes, efficacité énergétique data centers et promotion de solutions digitales durables.",
                    "Effets environnementaux : adoption techs écologiques, optimisation énergétique centres données et développement solutions numériques durables.",
                    "Impacts écologiques : technologies vertes incorporées, performance énergétique data centers et avancement solutions digitales eco-friendly.",
                    "Effets sur l'environnement : intégration technologies durables, optimisation énergétique infrastructures data et promotion solutions numériques vertes.",
                    "Impacts environnementaux : incorporation techs écologiques, efficience énergétique data centers et développement solutions digitales durables.",
                    "Effets écologiques : technologies vertes adoptées, performance énergétique centres données et avancement solutions numériques eco-responsables.",
                    "Impacts sur l'environnement : intégration solutions durables, optimisation énergétique data centers et promotion techs digitales vertes.",
                    "Effets environnementaux : adoption technologies eco-friendly, efficacité énergétique infrastructures data et développement solutions digitales durables.",
                    "Impacts écologiques : techs vertes incorporées, performance énergétique centres données et avancement solutions numériques environnementales."
                ],
                "keywords": ["impacts environnementaux", "technologies vertes", "optimisation énergétique", "data centers", "durabilité", "empreinte écologique"],
                "confidence": 0.8
            },




            "comment le new deal va transformer le secteur bancaire": {
                "answers": [
                    "Le secteur bancaire sera transformé par la bancarisation digitale massive, les paiements électroniques sécurisés, la fintech régulée et l'inclusion financière élargie.",
                    "Transformation bancaire via : digitalisation des services, paiements électroniques, développement fintech et extension de l'inclusion financière.",
                    "Mutation du secteur bancaire : services bancaires digitaux, transactions électroniques, écosystème fintech régulé et accès financier élargi.",
                    "Révolution bancaire : dématérialisation bancaire, paiements digitalisés, innovation fintech supervisée et inclusion financière étendue.",
                    "Transformation digitale bancaire : bancarisation électronique, moyens paiement digitaux, fintech encadrée et démocratisation financière.",
                    "Évolution du banking : services financiers digitaux, paiements électroniques sécurisés, fintech régulée et accès bancaire universel.",
                    "Mutation digitale bancaire : bancarisation numérique, transactions électroniques, écosystème fintech et inclusion financière généralisée.",
                    "Révolution digitale bancaire : services bancaires dématérialisés, paiements digitalisés, fintech supervisée et accès financier élargi.",
                    "Transformation financière digitale : bancarisation électronique massive, paiements digitaux, fintech régulée et inclusion bancaire étendue.",
                    "Évolution numérique bancaire : services financiers digitalisés, transactions électroniques, innovation fintech et démocratisation financière."
                ],
                "keywords": ["secteur bancaire", "bancarisation digitale", "paiements électroniques", "fintech", "inclusion financière"],
                "confidence": 0.85
            },

            "quels sont les mécanismes de gouvernance du new deal": {
                "answers": [
                    "La gouvernance comprend un comité stratégique interministériel, des instances de régulation spécialisées, des indicateurs de suivi et des évaluations trimestrielles des progrès.",
                    "Mécanismes de gouvernance : comité directeur interministériel, autorités de régulation dédiées, tableaux de bord de suivi et revues trimestrielles de performance.",
                    "Gouvernance structurée : comité stratégique multi-sectoriel, organismes régulateurs spécialisés, métriques de monitoring et évaluations trimestrielles.",
                    "Système de gouvernance : instance de pilotage interministérielle, régulateurs sectoriels, indicateurs de tracking et revues périodiques de progression.",
                    "Architecture gouvernance : comité de direction stratégique, entités régulatrices, KPI de suivi et assessments trimestriels.",
                    "Mécanisme gouvernance : cellule de pilotage interministérielle, autorités de régulation, métriques de monitoring et évaluations trimestrielles.",
                    "Cadre gouvernance : comité stratégique intersectoriel, instances régulatrices, indicateurs performance et revues périodiques.",
                    "Système de pilotage : comité directeur multi-ministeriel, régulateurs spécialisés, tableaux de bord et évaluations trimestrielles.",
                    "Structure gouvernance : instance stratégique interministérielle, organismes régulateurs, métriques suivi et assessments périodiques.",
                    "Mécanisme de supervision : comité de pilotage stratégique, autorités régulatrices, indicateurs monitoring et revues trimestrielles."
                ],
                "keywords": ["gouvernance", "comité stratégique", "régulation", "suivi", "évaluations", "piloting"],
                "confidence": 0.9
            },

            "comment le new deal va développer l'économie circulaire": {
                "answers": [
                    "L'économie circulaire est développée via des plateformes de partage de ressources, le recyclage intelligent assisté par IA et la traçabilité blockchain des déchets.",
                    "Développement économie circulaire : plateformes mutualisation ressources, recyclage intelligent avec IA et traçabilité déchets par blockchain.",
                    "Promotion économie circulaire : solutions partage ressources, valorisation déchets intelligente avec IA et suivi blockchain des flux déchets.",
                    "Stimulation économie circulaire : plateformes collaboration ressources, recyclage optimisé par IA et traçabilité déchets via blockchain.",
                    "Développement circularité : systèmes mutualisation ressources, gestion déchets intelligente avec IA et monitoring blockchain des déchets.",
                    "Accélération économie circulaire : plateformes échange ressources, recyclage avancé par IA et traçabilité déchets blockchain.",
                    "Promotion circularité : solutions partage actifs, valorisation déchets assistée IA et suivi blockchain flux déchets.",
                    "Stimulation économie circulaire : plateformes coopération ressources, recyclage intelligent avec IA et monitoring déchets par blockchain.",
                    "Développement modèle circulaire : systèmes collaboration ressources, gestion déchets optimisée IA et traçabilité blockchain déchets.",
                    "Accélération circularité : plateformes mutualisation actifs, recyclage avancé assisté IA et suivi déchets via blockchain."
                ],
                "keywords": ["économie circulaire", "plateformes partage", "recyclage intelligent", "IA", "blockchain", "déchets"],
                "confidence": 0.8
            },

            "quels sont les programmes de mentorat pour entrepreneurs": {
                "answers": [
                    "Les programmes de mentorat incluent l'accompagnement par experts internationaux, le pairing avec entrepreneurs expérimentés et les bootcamps intensifs de développement business.",
                    "Programmes mentorat : coaching experts internationaux, jumelage entrepreneurs chevronnés et bootcamps intensifs développement entreprise.",
                    "Initiatives mentorat : accompagnement spécialistes globaux, mentoring entrepreneurs expérimentés et programmes intensifs croissance business.",
                    "Dispositifs mentorat : guidance experts internationaux, partenariat entrepreneurs seniors et bootcamps développement commercial.",
                    "Programmes accompagnement : coaching professionnels internationaux, jumelage entrepreneurs aguerris et sessions intensives scaling business.",
                    "Initiatives coaching : mentoring experts globaux, pairing entrepreneurs expérimentés et bootcamps accélération entreprise.",
                    "Dispositifs accompagnement : guidance spécialistes internationaux, mentorat entrepreneurs seniors et programmes intensifs développement business.",
                    "Programmes mentoring : coaching professionnels globaux, jumelage entrepreneurs chevronnés et bootcamps croissance commerciale.",
                    "Initiatives guidance : accompagnement experts internationaux, partenariat entrepreneurs aguerris et sessions intensives scaling.",
                    "Dispositifs coaching : mentoring spécialistes globaux, pairing entrepreneurs expérimentés et bootcamps accélération business."
                ],
                "keywords": ["programmes mentorat", "accompagnement", "experts internationaux", "entrepreneurs expérimentés", "bootcamps", "coaching"],
                "confidence": 0.85
            },

            "comment le new deal va moderniser le système judiciaire": {
                "answers": [
                    "Le système judiciaire est modernisé par la dématérialisation des procédures, les audiences virtuelles, la gestion électronique des dossiers et la formation aux outils digitaux.",
                    "Modernisation justice : dématérialisation procédures, audiences en ligne, gestion numérique dossiers et formation outils digitaux magistrats.",
                    "Transformation judiciaire : numérisation procédures, visioconférences judiciaires, management électronique dossiers et éducation digitale personnel judiciaire.",
                    "Révolution digitale justice : dématérialisation processus, audiences virtuelles, administration numérique dossiers et formation technologies juges.",
                    "Modernisation système judiciaire : digitalisation procédures, télé-audiences, gestion digitale dossiers et apprentissage outils numériques.",
                    "Transformation numérique justice : dématérialisation contentieux, audiences distancielles, management numérique dossiers et formation digitale magistrature.",
                    "Révolution numérique judiciaire : numérisation processus, visio-audiences, administration électronique dossiers et éducation technologies personnel.",
                    "Modernisation digitale justice : digitalisation procédures, audiences en ligne, gestion digitale dossiers et apprentissage outils digitaux.",
                    "Transformation digitale judiciaire : dématérialisation contentieux, télé-audiences, management électronique dossiers et formation numérique magistrats.",
                    "Révolution technologique justice : numérisation processus, audiences virtuelles, administration numérique dossiers et éducation digitale juges."
                ],
                "keywords": ["système judiciaire", "dématérialisation", "audiences virtuelles", "gestion électronique", "formation digitale", "modernisation"],
                "confidence": 0.8
            },

            "quels sont les incitatifs pour les investisseurs étrangers": {
                "answers": [
                    "Les incitatifs incluent des avantages fiscaux, des procédures d'investissement accélérées, des garanties de rapatriement des capitaux et un accès privilégié aux marchés émergents.",
                    "Incitatifs investisseurs étrangers : bénéfices fiscaux, processus investissement rapides, assurances rapatriement capitaux et accès prioritaire marchés émergents.",
                    "Avantages investisseurs internationaux : incentives fiscaux, procédures investissement simplifiées, garanties transfert capitaux et entrée privilégiée marchés croissance.",
                    "Mesures attractives investisseurs : avantages fiscaux, démarches investissement accélérées, sécurisation rapatriement fonds et accès favorisé marchés émergents.",
                    "Incitations investisseurs étrangers : régimes fiscaux avantageux, process investissement fluidifiés, protections rapatriement capitaux et accès préférentiel marchés.",
                    "Avantages internationaux : incentives financiers, procédures investissement rapides, garanties transfert devises et entrée prioritaire marchés émergents.",
                    "Mesures d'attraction : bénéfices fiscaux, démarches investissement simplifiées, assurances rapatriement fonds et accès privilégié marchés croissance.",
                    "Incitatifs globaux : régimes fiscaux préférentiels, process investissement accélérés, sécurisation transfert capitaux et accès favorisé marchés.",
                    "Avantages étrangers : incentives économiques, procédures investissement fluidifiées, garanties rapatriement devises et entrée préférentielle marchés émergents.",
                    "Mesures attractives internationales : avantages fiscaux, démarches investissement rapides, protections transfert fonds et accès prioritaire marchés croissance."
                ],
                "keywords": ["incitatifs", "investisseurs étrangers", "avantages fiscaux", "procédures accélérées", "rapatriement capitaux", "marchés émergents"],
                "confidence": 0.85
            },

            "comment le new deal va renforcer la cybersécurité nationale": {
                "answers": [
                    "La cybersécurité nationale est renforcée par un centre opérationnel de sécurité, des audits réguliers, la formation d'experts locaux et des partenariats internationaux de veille.",
                    "Renforcement cybersécurité nationale : centre opérationnel sécurité, audits périodiques, formation experts nationaux et collaborations internationales monitoring.",
                    "Consolidation sécurité cybernétique : cellule opérationnelle protection, contrôles réguliers, développement compétences locales et alliances globales veille.",
                    "Renforcement cyberdéfense : centre commandement sécurité, inspections continues, éducation spécialistes sénégalais et partenariats internationaux surveillance.",
                    "Consolidation cybersécurité : unité opérationnelle protection, audits récurrents, formation experts locaux et coopérations globales monitoring.",
                    "Renforcement sécurité numérique : centre opérationnel cyber, vérifications périodiques, développement compétences nationales et collaborations internationales veille.",
                    "Consolidation cyberprotection : cellule commandement sécurité, contrôles réguliers, éducation spécialistes locaux et alliances globales surveillance.",
                    "Renforcement défense cyber : centre opérationnel national, inspections continues, formation experts sénégalais et partenariats internationaux monitoring.",
                    "Consolidation sécurité cyber : unité opérationnelle cyber, audits récurrents, développement compétences locales et coopérations globales veille.",
                    "Renforcement protection numérique : centre commandement cyber, vérifications périodiques, éducation spécialistes nationaux et collaborations internationales surveillance."
                ],
                "keywords": ["cybersécurité nationale", "centre opérationnel", "audits", "formation experts", "partenariats internationaux", "cyberdéfense"],
                "confidence": 0.9
            },

            "quels sont les projets de transport intelligent": {
                "answers": [
                    "Les projets de transport intelligent incluent des systèmes de gestion du trafic en temps réel, des applications mobiles de mobilité, des véhicules connectés et des infrastructures de recharge électrique.",
                    "Projets transport intelligent : gestion trafic temps réel, apps mobilité, véhicules connectés et infrastructures recharge véhicules électriques.",
                    "Initiatives mobilité intelligente : systèmes management trafic temps réel, applications mobiles transport, véhicules communicants et stations recharge électrique.",
                    "Développements transport smart : solutions gestion circulation temps réel, apps déplacement, véhicules connectés et bornes recharge électrique.",
                    "Projets mobilité intelligente : systèmes optimisation trafic temps réel, applications mobiles mobilité, véhicules intelligents et infrastructures recharge EV.",
                    "Initiatives transport intelligent : gestion flux trafic temps réel, apps transport, véhicules connectés et stations recharge véhicules électriques.",
                    "Développements mobilité smart : solutions management circulation temps réel, applications déplacement, véhicules communicants et bornes recharge électrique.",
                    "Projets transport connecté : systèmes régulation trafic temps réel, apps mobilité, véhicules intelligents et infrastructures recharge EV.",
                    "Initiatives mobilité connectée : gestion trafic temps réel, applications transport, véhicules connectés et stations recharge véhicules électriques.",
                    "Développements transport avancé : solutions optimisation flux temps réel, apps déplacement, véhicules communicants et bornes recharge électrique."
                ],
                "keywords": ["transport intelligent", "gestion trafic", "applications mobiles", "véhicules connectés", "recharge électrique", "mobilité intelligente"],
                "confidence": 0.8
            },

            "comment le new deal va digitaliser le secteur culturel": {
                "answers": [
                    "Le secteur culturel est digitalisé par des plateformes de streaming local, la numérisation du patrimoine, les musées virtuels et la promotion digitale des artistes.",
                    "Digitalisation secteur culturel : plateformes streaming locales, numérisation patrimoine culturel, musées en ligne et promotion digitale artistes.",
                    "Transformation numérique culture : plateformes diffusion locales, digitalisation patrimoine, expositions virtuelles et visibilité digitale créateurs.",
                    "Dématérialisation culturelle : services streaming nationaux, numérisation héritage culturel, galeries virtuelles et marketing digital artistes.",
                    "Digitalisation culture : plateformes contenu local, numérisation patrimoine, musées digitaux et promotion en ligne talents.",
                    "Transformation digitale culturelle : plateformes streaming sénégalaises, digitalisation patrimoine culturel, expositions en ligne et visibilité numérique artistes.",
                    "Dématérialisation secteur culturel : services diffusion locaux, numérisation héritage, galeries virtuelles et marketing en ligne créateurs.",
                    "Digitalisation industrie culturelle : plateformes contenu national, numérisation patrimoine, musées online et promotion digitale talents.",
                    "Transformation numérique secteur culturel : plateformes streaming locales, digitalisation patrimoine culturel, expositions virtuelles et visibilité digitale artistes.",
                    "Dématérialisation culture : services diffusion nationaux, numérisation héritage, galeries en ligne et marketing numérique créateurs."
                ],
                "keywords": ["secteur culturel", "digitalisation", "plateformes streaming", "numérisation patrimoine", "musées virtuels", "promotion digitale"],
                "confidence": 0.8
            },

            "quels sont les programmes pour les femmes dans la tech": {
                "answers": [
                    "Les programmes dédiés aux femmes incluent des bourses d'études STEM, des incubateurs féminins, du mentorat par des role models et des réseaux professionnels dédiés.",
                    "Programmes femmes tech : bourses STEM, incubateurs pour femmes, mentorat modèles inspirants et réseaux professionnels féminins.",
                    "Initiatives femmes numérique : aides financières STEM, accélérateurs féminins, coaching par mentors femmes et communautés professionnelles dédiées.",
                    "Dispositifs femmes tech : subventions études STEM, pépinières féminines, guidance role models et réseaux d'entraide femmes.",
                    "Programmes féminins tech : bourses scientifiques, incubateurs femmes, mentorat inspirantes et clubs professionnels féminins.",
                    "Initiatives pour femmes numérique : soutiens financiers STEM, accélérateurs féminins, accompagnement modèles et communautés femmes tech.",
                    "Dispositifs féminins tech : aides études STEM, pépinières pour femmes, coaching mentors et réseaux solidaires féminins.",
                    "Programmes femmes numérique : bourses STEM, incubateurs féminins, mentorat role models et groupes professionnels femmes.",
                    "Initiatives dédiées femmes : financements études STEM, accélérateurs pour femmes, guidance inspirantes et communautés d'entraide.",
                    "Dispositifs pour femmes tech : subventions STEM, pépinières féminines, accompagnement modèles et réseaux professionnels femmes."
                ],
                "keywords": ["femmes tech", "programmes", "bourses STEM", "incubateurs féminins", "mentorat", "réseaux professionnels"],
                "confidence": 0.85
            },

            "comment le new deal va optimiser la gestion de l'eau": {
                "answers": [
                    "La gestion de l'eau est optimisée par des capteurs IoT de monitoring, des systèmes d'irrigation intelligente, la détection de fuites par IA et la gestion prédictive des ressources.",
                    "Optimisation gestion eau : capteurs IoT surveillance, systèmes irrigation intelligents, détection fuites IA et management prédictif ressources hydriques.",
                    "Amélioration gestion hydrique : senseurs IoT monitoring, solutions irrigation smart, identification fuites intelligence artificielle et gestion anticipative eau.",
                    "Optimisation ressources eau : dispositifs IoT contrôle, systèmes arrosage intelligents, repérage fuites IA et administration prédictive eau.",
                    "Amélioration management eau : capteurs connected surveillance, techniques irrigation smart, détection pertes IA et gestion prévisionnelle ressources.",
                    "Optimisation hydrique : senseurs IoT tracking, méthodes irrigation intelligentes, identification fuites intelligence artificielle et management anticipatif eau.",
                    "Amélioration gestion de l'eau : dispositifs connected monitoring, systèmes arrosage smart, repérage pertes IA et administration prévisionnelle ressources.",
                    "Optimisation ressources hydriques : capteurs IoT contrôle, solutions irrigation intelligentes, détection fuites IA et gestion prédictive eau.",
                    "Amélioration management hydrique : senseurs connected surveillance, techniques arrosage smart, identification pertes IA et administration anticipative ressources.",
                    "Optimisation de l'eau : dispositifs IoT tracking, méthodes irrigation intelligentes, repérage fuites intelligence artificielle et management prévisionnel eau."
                ],
                "keywords": ["gestion eau", "capteurs IoT", "irrigation intelligente", "détection fuites", "IA", "gestion prédictive"],
                "confidence": 0.8
            },

            "quels sont les avantages pour les travailleurs indépendants": {
                "answers": [
                    "Les travailleurs indépendants bénéficient de plateformes de mise en relation, de formations digitales gratuites, d'accès simplifié au microcrédit et de services administratifs dématérialisés.",
                    "Avantages indépendants : plateformes matching, formations digitales gratuites, accès facilité microfinance et services administratifs dématérialisés.",
                    "Bénéfices freelances : plateformes mise en relation, éducation digitale libre accès, ouverture simplifiée microcrédit et démarches administratives en ligne.",
                    "Avantages auto-entrepreneurs : plateformes connexion, apprentissage digital gratuit, accès aisé microfinance et procédures administratives dématérialisées.",
                    "Bénéfices indépendants : services matching digital, formations technologies gratuites, microcrédit accessible et formalités administratives online.",
                    "Avantages travailleurs autonomes : plateformes rapprochement, éducation numérique libre, microfinance simplifiée et services étatiques dématérialisés.",
                    "Bénéfices freelances : outils mise en relation digital, apprentissage tech gratuit, accès microcrédit facilité et démarches administratives digitales.",
                    "Avantages auto-entrepreneurs : plateformes connexion digitale, formations digitales accessibles, microfinance aisée et procédures administratives en ligne.",
                    "Bénéfices indépendants : services matching en ligne, éducation technologie gratuite, microcrédit simplifié et formalités étatiques dématérialisées.",
                    "Avantages travailleurs indépendants : plateformes rapprochement digital, apprentissage digital libre accès, microfinance accessible et services administratifs online."
                ],
                "keywords": ["travailleurs indépendants", "plateformes mise en relation", "formations digitales", "microcrédit", "services dématérialisés", "freelances"],
                "confidence": 0.85
            },

            "comment le new deal va développer le cloud souverain": {
                "answers": [
                    "Le cloud souverain est développé via des data centers nationaux sécurisés, des solutions logicielles locales et des partenariats stratégiques pour l'autonomie technologique.",
                    "Développement cloud souverain : data centers nationaux sécurisés, applications logicielles locales et alliances stratégiques autonomie tech.",
                    "Construction cloud souverain : centres données nationaux protégés, logiciels domestiques et collaborations stratégiques indépendance technologique.",
                    "Déploiement cloud national : infrastructures data locales sécurisées, solutions software nationales et partenariats clés souveraineté tech.",
                    "Développement infonuagique souverain : data centers sénégalais sécurisés, applications made in Senegal et coopérations stratégiques autonomie.",
                    "Construction cloud souverain : centres données nationaux durcis, logiciels locaux et alliances stratégiques indépendance digitale.",
                    "Déploiement cloud domestique : infrastructures data nationales sécurisées, solutions informatiques locales et partenariats souveraineté technologique.",
                    "Développement nuage souverain : data centers sénégalais protégés, applications domestiques et collaborations stratégiques autonomie tech.",
                    "Construction infonuagique nationale : centres données nationaux sécurisés, logiciels made in Senegal et alliances stratégiques indépendance.",
                    "Déploiement cloud souverain : infrastructures data locales durcies, solutions software nationales et partenariats clés souveraineté digitale."
                ],
                "keywords": ["cloud souverain", "data centers nationaux", "solutions logicielles locales", "autonomie technologique", "partenariats stratégiques"],
                "confidence": 0.85
            },

            "quels sont les projets de énergie intelligente": {
                "answers": [
                    "Les projets d'énergie intelligente incluent des smart grids, des compteurs électriques connectés, l'optimisation IA de la distribution et des micro-réseaux solaires.",
                    "Projets énergie intelligente : réseaux intelligents, compteurs électriques connectés, optimisation distribution IA et micro-grids solaires.",
                    "Initiatives smart energy : smart grids, compteurs connectés électriques, management distribution intelligence artificielle et mini-réseaux photovoltaïques.",
                    "Développements énergie smart : réseaux électriques intelligents, compteurs communicants, optimisation réseau IA et micro-réseaux solaires.",
                    "Projets energy intelligence : smart grids, compteurs électriques intelligents, gestion distribution IA et mini-grids photovoltaïques.",
                    "Initiatives énergie intelligente : réseaux smart, compteurs connectés, optimisation distribution intelligence artificielle et micro-réseaux solaires.",
                    "Développements smart power : réseaux électriques smart, compteurs communicants électriques, management réseau IA et mini-grids photovoltaïques.",
                    "Projets énergie smart : smart grids, compteurs intelligents électriques, optimisation distribution IA et micro-réseaux solaires.",
                    "Initiatives intelligence énergétique : réseaux intelligents, compteurs connectés électriques, gestion réseau intelligence artificielle et mini-réseaux photovoltaïques.",
                    "Développements énergie avancée : smart grids électriques, compteurs communicants, optimisation distribution IA et micro-grids solaires."
                ],
                "keywords": ["énergie intelligente", "smart grids", "compteurs connectés", "optimisation IA", "micro-réseaux solaires", "smart energy"],
                "confidence": 0.8
            },

            "comment le new deal va renforcer le e-commerce": {
                "answers": [
                    "Le e-commerce est renforcé par des plateformes de paiement sécurisées, la logistique optimisée, la formation aux ventes en ligne et la protection des consommateurs digitaux.",
                    "Renforcement e-commerce : solutions paiement sécurisées, logistique efficiente, formation vente online et protection acheteurs digitaux.",
                    "Développement commerce électronique : plateformes paiement protégées, supply chain optimisée, éducation vente en ligne et défense consommateurs numérique.",
                    "Consolidation e-commerce : systèmes paiement sécurisés, chaîne logistique améliorée, apprentissage e-vente et protection clients digital.",
                    "Renforcement commerce en ligne : outils paiement safe, logistique performante, formation e-commerce et sécurité acheteurs online.",
                    "Développement e-business : plateformes paiement sécurisées, gestion logistique optimisée, éducation vente digitale et protection consommateurs internet.",
                    "Consolidation commerce électronique : solutions paiement protégées, supply chain efficiente, apprentissage vente en ligne et défense clients numérique.",
                    "Renforcement vente en ligne : systèmes paiement safe, logistique améliorée, formation digital selling et sécurité consommateurs online.",
                    "Développement e-tailing : outils paiement sécurisés, chaîne logistique performante, éducation e-sales et protection acheteurs internet.",
                    "Consolidation e-retail : plateformes paiement protégées, gestion logistique optimisée, apprentissage vente digitale et défense clients online."
                ],
                "keywords": ["e-commerce", "plateformes paiement", "logistique", "formation vente en ligne", "protection consommateurs", "commerce électronique"],
                "confidence": 0.85
            },

            "quels sont les programmes de bilinguisme technologique": {
                "answers": [
                    "Les programmes de bilinguisme technologique forment aux interfaces multilingues, développent l'IA linguistique locale et promeuvent les contenus tech en langues nationales.",
                    "Programmes bilinguisme tech : formation interfaces multilingues, développement IA linguistique locale et promotion contenus tech langues nationales.",
                    "Initiatives bilinguisme technologique : éducation interfaces multi-langues, création intelligence artificielle linguistique domestique et valorisation contenus technologies langues locales.",
                    "Dispositifs bilinguisme digital : apprentissage interfaces multilingues, développement AI langagière sénégalaise et diffusion contenus digital langues nationales.",
                    "Programmes dualisme linguistique tech : formation interfaces multi-langues, conception IA linguistique locale et promotion contenus technologiques langues maternelles.",
                    "Initiatives plurilinguisme technologique : éducation interfaces multilingues, création intelligence artificielle langagière domestique et valorisation contenus tech langues locales.",
                    "Dispositifs bilinguisme numérique : apprentissage interfaces multi-langues, développement AI linguistique sénégalaise et diffusion contenus numérique langues nationales.",
                    "Programmes dualité linguistique digitale : formation interfaces multilingues, conception IA langagière locale et promotion contenus digitaux langues maternelles.",
                    "Initiatives multilinguisme tech : éducation interfaces multi-langues, création intelligence artificielle linguistique domestique et valorisation contenus technologies langues locales.",
                    "Dispositifs plurilinguisme numérique : apprentissage interfaces multilingues, développement AI langagière sénégalaise et diffusion contenus digital langues nationales."
                ],
                "keywords": ["bilinguisme technologique", "interfaces multilingues", "IA linguistique", "langues nationales", "contenus tech", "multilinguisme"],
                "confidence": 0.8
            },

            "comment le new deal va moderniser le secteur minier": {
                "answers": [
                    "Le secteur minier est modernisé par la télédétection des gisements, l'automatisation des processus, la traçabilité blockchain des minerais et la sécurité connectée des sites.",
                    "Modernisation secteur minier : télédétection gisements, automatisation processus, traçabilité blockchain minerais et sécurité connectée sites.",
                    "Transformation numérique minière : détection à distance gisements, robotisation opérations, suivi blockchain minerais et protection intelligente sites.",
                    "Révolution digitale minière : télédétection ressources, automatisation activités, traçabilité distributed ledger minerais et sécurité IoT sites.",
                    "Modernisation industrie minière : scanning distant gisements, automation processus, monitoring blockchain minerais et safety connectée sites.",
                    "Transformation tech minière : détection remote ressources, robotisation opérations, tracking blockchain minerais et protection smart sites.",
                    "Révolution numérique extraction : télédétection gisements, automatisation procédures, traçabilité DLT minerais et sécurité IoT mines.",
                    "Modernisation mining : scanning à distance ressources, automation activités, monitoring distributed ledger minerais et safety intelligente sites.",
                    "Transformation digitale extractive : détection distant gisements, robotisation processus, tracking DLT minerais et protection connectée mines.",
                    "Révolution technologique minière : télédétection ressources, automatisation opérations, traçabilité blockchain minerais et sécurité smart sites."
                ],
                "keywords": ["secteur minier", "télédétection", "automatisation", "blockchain", "traçabilité", "sécurité connectée"],
                "confidence": 0.8
            },

            "quels sont les projets de tourisme digital": {
                "answers": [
                    "Les projets de tourisme digital incluent des plateformes de réservation locales, la réalité augmentée sur sites historiques, des itinéraires intelligents et la promotion digitale des destinations.",
                    "Projets tourisme digital : plateformes réservation locales, réalité augmentée sites historiques, parcours intelligents et marketing digital destinations.",
                    "Initiatives e-tourisme : plateformes booking locales, AR sites patrimoniaux, itinéraires smart et promotion numérique destinations.",
                    "Développements tourisme numérique : solutions réservation sénégalaises, réalité augmentée monuments, trajets intelligents et visibilité digitale lieux.",
                    "Projets digital tourism : plateformes reservation locales, réalité augmentée sites culturels, circuits smart et marketing online destinations.",
                    "Initiatives tourisme digital : services booking nationaux, AR patrimoine, itinéraires intelligents et promotion numérique sites.",
                    "Développements e-tourism : solutions réservation locales, réalité augmentée historiques, parcours smart et visibilité internet destinations.",
                    "Projets tourisme 2.0 : plateformes reservation sénégalaises, RA sites culturels, circuits intelligents et marketing digital lieux.",
                    "Initiatives numérique touristique : services booking locaux, réalité augmentée monuments, itinéraires smart et promotion online sites.",
                    "Développements digital tourisme : solutions réservation nationales, AR patrimoine, trajets intelligents et visibilité digitale destinations."
                ],
                "keywords": ["tourisme digital", "plateformes réservation", "réalité augmentée", "itinéraires intelligents", "promotion digitale", "e-tourisme"],
                "confidence": 0.8
            },

            "comment le new deal va développer les compétences IA": {
                "answers": [
                    "Les compétences IA sont développées via des masters spécialisés, des laboratoires de recherche appliquée, des challenges d'innovation et des partenariats avec des leaders mondiaux.",
                    "Développement compétences IA : masters spécialisés, labs recherche appliquée, défis innovation et collaborations leaders globaux.",
                    "Renforcement expertises IA : programmes master spécialisés, laboratoires R&D appliquée, compétitions innovation et partenariats géants mondiaux.",
                    "Construction capacités IA : formations master avancées, centres recherche pratique, concours innovation et alliances leaders internationaux.",
                    "Développement savoir-faire IA : cursus master spécialisés, labs développement appliqué, challenges innovation et coopérations firmes globales.",
                    "Renforcement compétences intelligence artificielle : programmes master experts, laboratoires recherche opérationnelle, défis innovation et partenariats entreprises mondiales.",
                    "Construction expertises AI : formations master avancées, centres R&D pratique, compétitions innovation et alliances géants internationaux.",
                    "Développement capacités intelligence artificielle : cursus master spécialisés, labs développement opérationnel, challenges innovation et collaborations leaders globaux.",
                    "Renforcement savoir-faire AI : programmes master experts, laboratoires recherche appliquée, défis innovation et partenariats firmes mondiales.",
                    "Construction compétences IA : formations master avancées, centres R&D opérationnelle, concours innovation et alliances entreprises internationales."
                ],
                "keywords": ["compétences IA", "masters spécialisés", "laboratoires recherche", "challenges innovation", "partenariats mondiaux", "intelligence artificielle"],
                "confidence": 0.85
            },

            "quels sont les dispositifs pour les personnes handicapées": {
                "answers": [
                    "Les dispositifs incluent des interfaces accessibles, des technologies d'assistance, des formations adaptées et des programmes d'inclusion numérique pour les personnes handicapées.",
                    "Dispositifs handicapés : interfaces accessibles, technologies assistance, formations adaptées et programmes inclusion numérique.",
                    "Mesures personnes handicapées : interfaces utilisateur accessibles, techs d'aide, éducation adaptée et initiatives inclusion digitale.",
                    "Dispositifs inclusion handicap : interfaces adaptées, technologies support, apprentissages personnalisés et projets insertion numérique.",
                    "Mesures handicap : interfaces universelles, devices assistance, formations sur mesure et programmes intégration digitale.",
                    "Dispositifs personnes en situation de handicap : interfaces accessibles, technologies d'assistance, éducation adaptée et initiatives inclusion tech.",
                    "Mesures inclusion handicapés : interfaces utilisateur adaptées, techs support, apprentissages personnalisés et projets insertion digitale.",
                    "Dispositifs accessibilité : interfaces universelles, devices d'aide, formations sur mesure et programmes intégration numérique.",
                    "Mesures handicaps : interfaces accessibles, technologies assistance, éducation adaptée et initiatives inclusion technologique.",
                    "Dispositifs personnes handicapées : interfaces utilisateur universelles, techs support, apprentissages personnalisés et projets insertion tech."
                ],
                "keywords": ["personnes handicapées", "interfaces accessibles", "technologies assistance", "formations adaptées", "inclusion numérique", "accessibilité"],
                "confidence": 0.85
            },




            "comment le new deal va transformer la pêche digitale": {
                "answers": [
                    "La pêche digitale est transformée par des systèmes de surveillance maritime par drones, la traçabilité blockchain des produits, des applications de marché direct et la prévision IA des zones de pêche.",
                    "Transformation pêche digitale : surveillance maritime drones, traçabilité blockchain produits, apps marché direct et prédiction IA zones pêche.",
                    "Révolution numérique pêche : monitoring maritime par drones, suivi blockchain captures, plateformes vente directe et prévision intelligence artificielle bancs poissons.",
                    "Digitalisation pêche : contrôle maritime UAV, traçabilité distributed ledger produits, applications e-commerce poisson et analyse IA zones de pêche.",
                    "Transformation digitale pêche : surveillance navale drones, tracking blockchain pêches, solutions marché en ligne et prédiction IA lieux pêche.",
                    "Modernisation numérique pêche : monitoring maritime par drones, traçabilité DLT captures, plateformes vente digitale et intelligence artificielle zones poissonneuses.",
                    "Révolution tech pêche : surveillance UAV maritime, suivi blockchain produits, apps commerce électronique et analyse IA bancs de pêche.",
                    "Digitalisation secteur pêche : contrôle naval drones, traçabilité distributed ledger poissons, applications marché direct et prédiction intelligence artificielle zones.",
                    "Transformation digitale halieutique : surveillance maritime par UAV, tracking blockchain pêches, solutions e-commerce produits mer et IA zones de pêche.",
                    "Modernisation tech pêche : monitoring naval drones, traçabilité DLT captures, plateformes vente en ligne et intelligence artificielle lieux pêche."
                ],
                "keywords": ["pêche digitale", "drones maritimes", "blockchain", "traçabilité", "applications marché", "IA prédictive"],
                "confidence": 0.8
            },

            "quels sont les programmes pour les seniors dans le numérique": {
                "answers": [
                    "Les programmes seniors incluent des ateliers d'alphabétisation digitale, des interfaces adaptées, un support technique dédié et des activités intergénérationnelles de partage de compétences.",
                    "Programmes seniors numérique : ateliers alphabétisation digitale, interfaces senior-friendly, assistance technique personnalisée et échanges intergénérationnels compétences.",
                    "Initiatives seniors tech : formations initiation numérique, interfaces adaptées âge, support tech dédié et rencontres intergénérationnelles partage savoirs.",
                    "Dispositifs troisième âge digital : apprentissage bases numérique, interfaces ergonomiques seniors, aide technique individualisée et activités mixité générationnelle échanges.",
                    "Programmes personnes âgées numérique : ateliers compétences digitales, designs adaptés seniors, accompagnement tech personnalisé et projets intergénérationnels collaboration.",
                    "Initiatives ainés tech : éducation numérique fondamentale, interfaces accessibles seniors, support informatique dédié et rencontres interâges transmission compétences.",
                    "Dispositifs seniors digital : formation initiation technologies, interfaces senior-oriented, assistance technique sur mesure et échanges intergénérationnels savoir-faire.",
                    "Programmes troisième âge tech : apprentissage digital de base, designs ergonomiques seniors, aide informatique personnalisée et activités mixité âge partage.",
                    "Initiatives personnes âgées digital : ateliers compétences tech, interfaces adaptées âge, support tech individualisé et projets intergénérationnels échanges.",
                    "Dispositifs ainés numérique : éducation technologies élémentaires, interfaces senior-friendly, assistance informatique dédiée et rencontres interâges transmission."
                ],
                "keywords": ["seniors", "alphabétisation digitale", "interfaces adaptées", "support technique", "intergénérationnel", "troisième âge"],
                "confidence": 0.85
            },

            "comment le new deal va développer la réalité virtuelle": {
                "answers": [
                    "La réalité virtuelle est développée via des centres d'innovation VR/AR, des applications éducatives immersives, la formation professionnelle en simulation et le tourisme virtuel patrimonial.",
                    "Développement réalité virtuelle : hubs innovation VR/AR, apps éducatives immersives, formation pro simulation et tourisme virtuel patrimoine.",
                    "Expansion VR : centres création réalité virtuelle/augmentée, solutions éducation immersive, formation professionnelle simulations et visites virtuelles patrimoine.",
                    "Croissance réalité virtuelle : pôles innovation VR/AR, applications pédagogiques immersives, entraînement professionnel réalité virtuelle et tourisme digital patrimonial.",
                    "Développement RV : incubateurs VR/AR, outils éducatifs immersifs, formation métiers simulation et exploration virtuelle patrimoine.",
                    "Expansion réalité virtuelle : hubs VR/AR, apps d'apprentissage immersif, training professionnel réalité virtuelle et découverte virtuelle sites historiques.",
                    "Croissance VR : centres développement réalité virtuelle/augmentée, solutions pédagogiques immersives, formation simulation métiers et visites virtuelles culture.",
                    "Développement réalité virtuelle : pôles création VR/AR, applications éducation immersive, entraînement pro réalité virtuelle et tourisme digital culturel.",
                    "Expansion RV : incubateurs réalité virtuelle/augmentée, outils d'apprentissage immersif, training métiers simulation et exploration virtuelle patrimoine.",
                    "Croissance réalité virtuelle : hubs innovation VR/AR, apps pédagogiques immersives, formation professionnelle réalité virtuelle et découverte virtuelle historique."
                ],
                "keywords": ["réalité virtuelle", "VR/AR", "centres innovation", "éducation immersive", "formation simulation", "tourisme virtuel"],
                "confidence": 0.8
            },

            "quels sont les projets de médias digitaux locaux": {
                "answers": [
                    "Les projets de médias digitaux locaux incluent des plateformes de streaming de contenu sénégalais, des agences de presse en ligne, des radios digitales communautaires et des formations au journalisme digital.",
                    "Projets médias digitaux locaux : plateformes streaming contenu local, agences presse online, radios digitales communautaires et formations journalisme digital.",
                    "Initiatives médias numériques locaux : services diffusion contenu sénégalais, médias presse numérique, radios web communautaires et éducation journalisme numérique.",
                    "Développements médias digital locaux : plateformes OTT contenu local, organisations presse digitale, stations radio internet locales et apprentissage journalisme tech.",
                    "Projets médias 2.0 locaux : applications streaming production locale, agences information en ligne, radios digitales de proximité et formations média digital.",
                    "Initiatives presse digitale locale : plateformes diffusion contenu sénégalais, médias actualité numérique, radios web de communauté et éducation presse numérique.",
                    "Développements médias numérique locaux : services OTT contenu local, organisations journalisme digital, stations radio internet communautaires et apprentissage média tech.",
                    "Projets médias online locaux : applications streaming production sénégalaise, agences info online, radios digitales locales et formations journalisme 2.0.",
                    "Initiatives information digitale locale : plateformes diffusion contenu local, médias presse en ligne, radios web de proximité et éducation information numérique.",
                    "Développements médias internet locaux : services streaming production sénégalaise, organisations actualité digitale, stations radio digitales communautaires et apprentissage presse tech."
                ],
                "keywords": ["médias digitaux", "plateformes streaming", "contenu local", "radios digitales", "journalisme digital", "presse en ligne"],
                "confidence": 0.85
            },

            "comment le new deal va sécuriser les transactions électroniques": {
                "answers": [
                    "Les transactions électroniques sont sécurisées par des protocoles de cryptage avancés, l'authentification biométrique, la blockchain pour les paiements et des audits de sécurité réguliers.",
                    "Sécurisation transactions électroniques : protocoles chiffrement avancés, authentification biométrique, blockchain paiements et audits sécurité réguliers.",
                    "Protection transactions digitales : standards cryptographie renforcés, vérification biométrique, distributed ledger paiements et contrôles sécurité périodiques.",
                    "Sécurisation e-transactions : protocoles encryption sophistiqués, identification biométrique, technologie blockchain transactions et inspections sécurité récurrentes.",
                    "Protection paiements électroniques : méthodes chiffrement avancées, authentification biométrique, blockchain pour paiements et audits de sécurité réguliers.",
                    "Sécurisation transactions en ligne : protocoles cryptographie robustes, vérification biométrique, DLT transactions et contrôles sécurité périodiques.",
                    "Protection e-paiements : standards encryption sophistiqués, identification biométrique, technologie blockchain paiements et inspections sécurité récurrentes.",
                    "Sécurisation digital transactions : méthodes chiffrement avancées, authentification biométrique, distributed ledger pour transactions et audits sécurité réguliers.",
                    "Protection transactions numériques : protocoles cryptographie renforcés, vérification biométrique, blockchain transactions et contrôles sécurité périodiques.",
                    "Sécurisation paiements digitaux : standards encryption robustes, identification biométrique, DLT paiements et inspections sécurité récurrentes."
                ],
                "keywords": ["transactions électroniques", "cryptage", "authentification biométrique", "blockchain", "audits sécurité", "paiements sécurisés"],
                "confidence": 0.9
            },

            "quels sont les programmes de bourses tech internationales": {
                "answers": [
                    "Les programmes de bourses tech internationales offrent des formations à l'étranger dans les universités tech leaders, des stages dans des entreprises globales et des échanges avec des experts mondiaux.",
                    "Programmes bourses tech internationales : formations universités tech étrangères, stages entreprises globales et échanges experts mondiaux.",
                    "Initiatives bourses tech globales : éducation institutions tech internationales, internships multinationales tech et collaborations spécialistes internationaux.",
                    "Dispositifs bourses tech à l'étranger : apprentissage universités tech mondiales, stages corporations globales tech et interactions experts globaux.",
                    "Programmes bourses internationales tech : cursus écoles tech internationales, stages entreprises tech multinationales et échanges professionnels internationaux.",
                    "Initiatives bourses tech overseas : formations établissements tech étrangers, internships sociétés globales tech et coopérations experts mondiaux.",
                    "Dispositifs bourses tech global : éducation universités tech internationales, stages firmes multinationales tech et interactions spécialistes internationaux.",
                    "Programmes bourses à l'étranger tech : apprentissage institutions tech mondiales, stages corporations globales tech et échanges professionnels globaux.",
                    "Initiatives bourses internationales technologies : formations écoles tech étrangères, internships entreprises multinationales tech et collaborations experts internationaux.",
                    "Dispositifs bourses tech overseas : cursus établissements tech internationaux, stages sociétés globales tech et interactions spécialistes mondiaux."
                ],
                "keywords": ["bourses tech", "international", "formations étranger", "stages entreprises globales", "experts mondiaux", "échanges internationaux"],
                "confidence": 0.85
            },

            "comment le new deal va moderniser les archives nationales": {
                "answers": [
                    "Les archives nationales sont modernisées par la numérisation massive des documents historiques, l'indexation IA, la préservation digitale et l'accès en ligne sécurisé au patrimoine documentaire.",
                    "Modernisation archives nationales : numérisation documents historiques, indexation IA, préservation digitale et accès online sécurisé patrimoine.",
                    "Transformation numérique archives : digitalisation archives historiques, catalogage intelligence artificielle, conservation numérique et consultation internet protégée documents.",
                    "Révolution digitale archives : numérisation fonds documentaires, classification IA, sauvegarde digitale et accès web sécurisé archives.",
                    "Modernisation archives : scan massif documents historiques, indexation intelligence artificielle, préservation électronique et accès en ligne contrôlé patrimoine.",
                    "Transformation tech archives : digitalisation collections historiques, catalogage IA, conservation digitale et consultation internet sécurisée documents.",
                    "Révolution numérique archives nationales : numérisation archives, classification intelligence artificielle, sauvegarde numérique et accès web protégé fonds.",
                    "Modernisation digitale archives : scan documents historiques, indexation IA, préservation électronique et accès online contrôlé collections.",
                    "Transformation digitale archives : digitalisation fonds documentaires, catalogage intelligence artificielle, conservation digitale et consultation internet sécurisée archives.",
                    "Révolution tech archives : numérisation collections, classification IA, sauvegarde numérique et accès web protégé documents historiques."
                ],
                "keywords": ["archives nationales", "numérisation", "indexation IA", "préservation digitale", "accès en ligne", "patrimoine documentaire"],
                "confidence": 0.8
            },

            "quels sont les projets de fablabs et makerspaces": {
                "answers": [
                    "Les projets de fablabs et makerspaces créent des espaces collaboratifs équipés d'imprimantes 3D, de découpeurs laser, d'outils électroniques et de formations à la fabrication digitale.",
                    "Projets fablabs makerspaces : espaces collaboratifs imprimantes 3D, découpeurs laser, outils électroniques et formations fabrication digitale.",
                    "Initiatives fablabs : ateliers collaboratifs équipés 3D printing, machines laser cutting, équipements électroniques et éducation fabrication numérique.",
                    "Développements makerspaces : labs collaboratifs printers 3D, découpeuses laser, instruments électroniques et apprentissage production digitale.",
                    "Projets ateliers fabrication : espaces partagés impression 3D, cutters laser, outils électroniques et formations création digitale.",
                    "Initiatives fablabs makerspaces : workshops collaboratifs 3D printers, laser cutters, devices électroniques et éducation making digital.",
                    "Développements fablabs : laboratoires collaboratifs impression 3D, machines laser, équipements électroniques et apprentissage fabrication numérique.",
                    "Projets makerspaces : ateliers partagés 3D printing, découpe laser, outils électroniques et formations production digitale.",
                    "Initiatives ateliers fabrication digitale : espaces collaboratifs printers 3D, laser cutters, instruments électroniques et éducation création numérique.",
                    "Développements fablabs makerspaces : labs partagés impression 3D, machines laser cutting, devices électroniques et apprentissage making digital."
                ],
                "keywords": ["fablabs", "makerspaces", "imprimantes 3D", "découpeurs laser", "fabrication digitale", "espaces collaboratifs"],
                "confidence": 0.85
            },

            "comment le new deal va développer les compétences blockchain": {
                "answers": [
                    "Les compétences blockchain sont développées via des certifications spécialisées, des hackathons dédiés, des laboratoires de développement et des partenariats avec des entreprises blockchain leaders.",
                    "Développement compétences blockchain : certifications spécialisées, hackathons dédiés, labs développement et partenariats entreprises blockchain leaders.",
                    "Renforcement expertises blockchain : diplômes spécialisés, compétitions blockchain, laboratoires R&D et collaborations sociétés blockchain majeures.",
                    "Construction capacités blockchain : attestations expertises, marathon coding blockchain, centres développement et alliances entreprises blockchain importantes.",
                    "Développement savoir-faire blockchain : certificats spécialisés, hackathons blockchain, incubateurs blockchain et partenariats firmes blockchain leaders.",
                    "Renforcement compétences distributed ledger : qualifications spécialisées, défis coding blockchain, labs innovation et coopérations entreprises blockchain majeures.",
                    "Construction expertises DLT : diplômes experts, compétitions développement blockchain, centres R&D et collaborations sociétés blockchain importantes.",
                    "Développement capacités blockchain : attestations spécialisées, marathon programming blockchain, incubateurs tech et alliances firmes blockchain leaders.",
                    "Renforcement savoir-faire distributed ledger : certificats experts, hackathons blockchain, laboratoires innovation et partenariats entreprises blockchain majeures.",
                    "Construction compétences blockchain : qualifications spécialisées, défis coding DLT, centres développement et coopérations sociétés blockchain importantes."
                ],
                "keywords": ["compétences blockchain", "certifications", "hackathons", "laboratoires développement", "partenariats entreprises", "DLT"],
                "confidence": 0.85
            },

            "quels sont les projets de gestion intelligente des déchets": {
                "answers": [
                    "Les projets de gestion intelligente des déchets utilisent des capteurs de remplissage, l'optimisation IA des collectes, le tri robotisé et la traçabilité blockchain du recyclage.",
                    "Projets gestion intelligente déchets : capteurs remplissage, optimisation IA collectes, tri robotisé et traçabilité blockchain recyclage.",
                    "Initiatives smart waste management : senseurs niveau déchets, intelligence artificielle optimisation ramassage, tri automatisé et suivi blockchain recyclage.",
                    "Développements gestion smart déchets : détecteurs remplissage, IA optimisation collectes, séparation robotisée et monitoring blockchain recyclage.",
                    "Projets waste tech : capteurs capacité poubelles, algorithmes IA collectes, tri automatique et traçabilité distributed ledger recyclage.",
                    "Initiatives gestion intelligente ordures : senseurs volume déchets, optimisation intelligence artificielle ramassage, tri robotique et suivi DLT recyclage.",
                    "Développements smart garbage management : détecteurs niveau poubelles, IA optimisation collectes, séparation automatisée et monitoring blockchain recyclage.",
                    "Projets déchets intelligents : capteurs remplissage containers, algorithmes IA ramassage, tri robotisé et traçabilité distributed ledger recyclage.",
                    "Initiatives waste management tech : senseurs capacité déchets, optimisation intelligence artificielle collectes, tri automatique et suivi DLT recyclage.",
                    "Développements gestion smart waste : détecteurs volume poubelles, IA optimisation ramassage, séparation robotique et monitoring blockchain recyclage."
                ],
                "keywords": ["gestion intelligente déchets", "capteurs remplissage", "optimisation IA", "tri robotisé", "blockchain recyclage", "smart waste"],
                "confidence": 0.8
            },

            "comment le new deal va renforcer la coopération régionale digitale": {
                "answers": [
                    "La coopération régionale digitale est renforcée par des infrastructures connectées transfrontalières, des plateformes d'échanges régionaux, l'harmonisation des régulations et des projets tech communs.",
                    "Renforcement coopération régionale digitale : infrastructures connectées transfrontalières, plateformes échanges régionaux, harmonisation régulations et projets tech communs.",
                    "Consolidation coopération numérique régionale : réseaux interconnectés transfrontaliers, systèmes partage régionaux, uniformisation législations et initiatives tech conjointes.",
                    "Renforcement collaboration digitale régionale : infrastructures liées transfrontières, plateformes collaboration régionale, alignement réglementations et programmes tech partagés.",
                    "Consolidation coopération tech régionale : réseaux unis transfrontaliers, outils échanges régionaux, standardisation lois et projets technologie communs.",
                    "Renforcement partenariat numérique régional : infrastructures jointes transfrontières, systèmes coopération régionale, harmonisation règles et initiatives tech mutualisées.",
                    "Consolidation collaboration tech régionale : réseaux interconnectés transfrontaliers, plateformes partage régional, uniformisation législations et programmes technologie conjoints.",
                    "Renforcement coopération digitale régionale : infrastructures liées transfrontières, outils collaboration régionale, alignement réglementations et projets tech partagés.",
                    "Consolidation partenariat numérique régional : réseaux unis transfrontaliers, systèmes échanges régionaux, standardisation lois et initiatives technologie communes.",
                    "Renforcement collaboration régionale tech : infrastructures jointes transfrontières, plateformes coopération régionale, harmonisation règles et programmes tech mutualisés."
                ],
                "keywords": ["coopération régionale", "infrastructures transfrontalières", "plateformes d'échange", "harmonisation régulations", "projets tech communs", "intégration digitale"],
                "confidence": 0.85
            },

            "quels sont les programmes de réinsertion par le numérique": {
                "answers": [
                    "Les programmes de réinsertion par le numérique forment aux métiers tech les personnes éloignées de l'emploi, avec un accompagnement personnalisé et des partenariats employeurs.",
                    "Programmes réinsertion numérique : formation métiers tech personnes éloignées emploi, accompagnement personnalisé et partenariats employeurs.",
                    "Initiatives réinsertion par le digital : éducation professions tech publics défavorisés, suivi individualisé et collaborations entreprises.",
                    "Dispositifs insertion numérique : apprentissage métiers numérique publics précaires, guidance personnalisée et alliances employeurs.",
                    "Programmes réinsertion tech : formation compétences tech populations exclues, accompagnement sur mesure et partenariats recruteurs.",
                    "Initiatives insertion par le digital : éducation savoir-faire tech publics vulnérables, soutien individualisé et coopérations entreprises.",
                    "Dispositifs réinsertion numérique : apprentissage compétences numérique personnes marginalisées, mentorat personnalisé et collaborations employeurs.",
                    "Programmes insertion tech : formation métiers tech publics défavorisés, accompagnement adapté et partenariats recruteurs.",
                    "Initiatives réinsertion digitale : éducation professions numérique populations exclues, suivi sur mesure et alliances entreprises.",
                    "Dispositifs insertion par le tech : apprentissage savoir-faire tech publics précaires, guidance individualisée et coopérations employeurs."
                ],
                "keywords": ["réinsertion numérique", "formation métiers tech", "personnes éloignées emploi", "accompagnement personnalisé", "partenariats employeurs", "insertion professionnelle"],
                "confidence": 0.85
            },

            "comment le new deal va développer l'ingénierie spatiale": {
                "answers": [
                    "L'ingénierie spatiale est développée via un centre national de télédétection, des formations en sciences spatiales, des partenariats avec des agences spatiales et des applications satellitaires locales.",
                    "Développement ingénierie spatiale : centre national télédétection, formations sciences spatiales, partenariats agences spatiales et applications satellitaires locales.",
                    "Expansion engineering spatial : institut national remote sensing, éducation sciences espace, collaborations agences spatiales et solutions satellitaires domestiques.",
                    "Croissance ingénierie spatiale : pôle national télédétection, cursus études spatiales, alliances agences spatiales et applications satellites locales.",
                    "Développement spatial tech : centre national observation terre, formations ingénierie spatiale, partenariats organisations spatiales et outils satellitaires sénégalais.",
                    "Expansion ingénierie de l'espace : institut national remote sensing, éducation technologie spatiale, coopérations agences spatiales et solutions satellites domestiques.",
                    "Croissance engineering spatial : pôle national télédétection, programmes sciences spatiales, alliances organisations spatiales et applications satellitaires locales.",
                    "Développement tech spatiale : centre national observation terrestre, formations ingénierie espace, partenariats agences spatiales et outils satellites sénégalais.",
                    "Expansion spatial engineering : institut national remote sensing, cursus technologie spatiale, collaborations organisations spatiales et solutions satellitaires domestiques.",
                    "Croissance ingénierie spatiale : pôle national télédétection, éducation sciences espace, alliances agences spatiales et applications satellites locales."
                ],
                "keywords": ["ingénierie spatiale", "télédétection", "formations spatiales", "partenariats agences spatiales", "applications satellitaires", "sciences spatiales"],
                "confidence": 0.8
            },

            "quels sont les projets de digitalisation du patrimoine": {
                "answers": [
                    "Les projets de digitalisation du patrimoine incluent la modélisation 3D des sites historiques, les archives numériques des traditions orales, les musées virtuels et la réalité augmentée sur l'artisanat.",
                    "Projets digitalisation patrimoine : modélisation 3D sites historiques, archives numériques traditions orales, musées virtuels et réalité augmentée artisanat.",
                    "Initiatives numérisation patrimoine : scanning 3D monuments historiques, banques données traditions orales, galeries virtuelles et AR artisanat traditionnel.",
                    "Développements patrimoine digital : modèles 3D sites culturels, digitalisation héritage oral, musées online et réalité augmentée arts traditionnels.",
                    "Projets numérisation héritage : modélisation 3D patrimoine historique, archives digitales traditions, expositions virtuelles et RA artisanat local.",
                    "Initiatives digitalisation héritage : scanning 3D monuments, bases données patrimoine oral, galeries digitales et réalité augmentée métiers traditionnels.",
                    "Développements patrimoine numérique : modèles 3D sites historiques, numérisation traditions orales, musées virtuels et AR arts ancestraux.",
                    "Projets héritage digital : modélisation 3D patrimoine culturel, archives numériques oralité, expositions online et réalité augmentée artisanat traditionnel.",
                    "Initiatives numérisation patrimoine culturel : scanning 3D monuments historiques, banques données traditions, galeries virtuelles et RA métiers ancestraux.",
                    "Développements digitalisation héritage : modèles 3D sites culturels, digitalisation patrimoine oral, musées digitaux et réalité augmentée arts traditionnels."
                ],
                "keywords": ["digitalisation patrimoine", "modélisation 3D", "archives numériques", "traditions orales", "musées virtuels", "réalité augmentée"],
                "confidence": 0.8
            },

            "comment le new deal va optimiser la logistique portuaire": {
                "answers": [
                    "La logistique portuaire est optimisée par l'automatisation des terminaux, la blockchain pour le suivi des conteneurs, l'IA pour la planification et les systèmes de gestion intelligente.",
                    "Optimisation logistique portuaire : automatisation terminaux, blockchain suivi conteneurs, IA planification et systèmes gestion intelligente.",
                    "Amélioration logistique portuaire : robotisation quais, distributed ledger tracking containers, intelligence artificielle scheduling et solutions management smart.",
                    "Optimisation supply chain portuaire : automation installations portuaires, blockchain monitoring conteneurs, IA optimisation et plateformes gestion intelligente.",
                    "Amélioration operations portuaires : automatisation infrastructures, DLT suivi containers, intelligence artificielle planification et systèmes control smart.",
                    "Optimisation logistique maritime : robotisation terminaux portuaires, blockchain tracking conteneurs, IA scheduling et solutions management intelligent.",
                    "Amélioration chaîne logistique portuaire : automation équipements portuaires, distributed ledger monitoring containers, intelligence artificielle optimisation et plateformes contrôle smart.",
                    "Optimisation port operations : automatisation installations, blockchain suivi conteneurs, IA planification et systèmes gestion intelligente.",
                    "Amélioration logistique des ports : robotisation infrastructures portuaires, DLT tracking containers, intelligence artificielle scheduling et solutions management smart.",
                    "Optimisation maritime logistics : automation terminaux, blockchain monitoring conteneurs, IA optimisation et plateformes contrôle intelligent."
                ],
                "keywords": ["logistique portuaire", "automatisation", "blockchain", "suivi conteneurs", "IA planification", "gestion intelligente"],
                "confidence": 0.85
            },

            "quels sont les programmes de tech for good": {
                "answers": [
                    "Les programmes tech for good développent des solutions numériques pour l'inclusion sociale, l'environnement, la santé accessible et l'éducation pour tous, avec un impact sociétal positif.",
                    "Programmes tech for good : solutions numériques inclusion sociale, environnement, santé accessible et éducation pour tous avec impact sociétal positif.",
                    "Initiatives technologie bien commun : applications digitales inclusion, écologie, santé abordable et éducation universelle avec bénéfice social.",
                    "Dispositifs tech for good : outils numériques solidarité, protection environnement, santé accessible et apprentissage pour tous avec valeur sociale.",
                    "Programmes tech d'intérêt général : solutions digitales équité sociale, durabilité, soins accessibles et éducation inclusive avec impact communautaire.",
                    "Initiatives numérique bien public : applications tech justice sociale, environnement, santé pour tous et enseignement universel avec bénéfice collectif.",
                    "Dispositifs technologie sociale : outils digitaux inclusion, écologie, soins abordables et éducation équitable avec valeur sociétale.",
                    "Programmes tech à impact social : solutions numériques équité, développement durable, santé inclusive et apprentissage pour tous avec bienfait communautaire.",
                    "Initiatives digital bien commun : applications technologie solidarité, protection nature, santé universelle et éducation accessible avec impact social.",
                    "Dispositifs numérique d'intérêt général : outils tech justice, environnement, soins pour tous et enseignement inclusif avec bénéfice sociétal."
                ],
                "keywords": ["tech for good", "inclusion sociale", "environnement", "santé accessible", "éducation pour tous", "impact sociétal"],
                "confidence": 0.85
            },

            "comment le new deal va moderniser les bibliothèques": {
                "answers": [
                    "Les bibliothèques sont modernisées par le prêt de livres numériques, des espaces de coworking tech, des ateliers de compétences digitales et des ressources en ligne accessibles.",
                    "Modernisation bibliothèques : prêt livres numériques, espaces coworking tech, ateliers compétences digitales et ressources en ligne accessibles.",
                    "Transformation numérique bibliothèques : lending ebooks, zones coworking technologie, workshops compétences numériques et ressources online disponibles.",
                    "Révolution digitale bibliothèques : prêt ouvrages digitaux, espaces collaboration tech, formations compétences digitales et documents internet accessibles.",
                    "Modernisation libraries : système ebooks, areas coworking tech, ateliers digital skills et resources online accessibles.",
                    "Transformation tech bibliothèques : service livres électroniques, lieux coworking numérique, workshops compétences tech et ressources web disponibles.",
                    "Révolution numérique bibliothèques : prêt publications digitales, espaces travail collaboratif tech, formations digital literacy et contenus internet accessibles.",
                    "Modernisation des libraries : programme ebooks, zones collaboration technologie, ateliers tech skills et ressources en ligne disponibles.",
                    "Transformation digitale bibliothèques : système ouvrages électroniques, lieux coworking digital, workshops compétences numériques et documents web accessibles.",
                    "Révolution tech bibliothèques : service publications digitaux, espaces travail coopératif tech, formations digital skills et contenus online disponibles."
                ],
                "keywords": ["bibliothèques", "livres numériques", "espaces coworking", "ateliers compétences digitales", "ressources en ligne", "modernisation"],
                "confidence": 0.8
            },

            "quels sont les projets de data science appliquée": {
                "answers": [
                    "Les projets de data science appliquée utilisent l'analyse de données pour la santé publique, l'optimisation agricole, la prévision économique et la personnalisation de l'éducation.",
                    "Projets data science appliquée : analyse données santé publique, optimisation agricole, prévision économique et personnalisation éducation.",
                    "Initiatives science données appliquée : analytics données santé publique, amélioration agriculture, prédiction économique et individualisation enseignement.",
                    "Développements data science pratique : traitement données santé publique, optimisation farming, forecasting économique et customisation éducation.",
                    "Projets data analytics appliquée : analyse datasets santé publique, optimisation agricole, prévision macroéconomique et personnalisation learning.",
                    "Initiatives data science opérationnelle : analytics santé publique, amélioration agricultural, prédiction économie et individualisation éducation.",
                    "Développements science données pratique : processing santé publique, optimisation agriculture, forecasting économique et customisation enseignement.",
                    "Projets applied data science : analyse health data, optimization farming, economic prediction et personalization education.",
                    "Initiatives data science implémentée : analytics public health, improvement agriculture, economic forecasting et individualization learning.",
                    "Développements data science réelle : processing santé publique, optimisation agricole, prévision économique et personnalisation éducation."
                ],
                "keywords": ["data science", "analyse données", "santé publique", "optimisation agricole", "prévision économique", "personnalisation éducation"],
                "confidence": 0.85
            },

            "comment le new deal va développer la 5G et 6G": {
                "answers": [
                    "La 5G et 6G sont développées par le déploiement d'infrastructures, la recherche sur les réseaux avancés, la formation aux nouvelles technologies mobiles et les tests pilotes.",
                    "Développement 5G 6G : déploiement infrastructures, recherche réseaux avancés, formation nouvelles technologies mobiles et tests pilotes.",
                    "Expansion 5G et 6G : installation infrastructures, R&D réseaux nouvelle génération, éducation tech mobiles émergentes et expérimentations pilotes.",
                    "Croissance 5G/6G : déploiement réseaux, investigation réseaux futurs, apprentissage technologies cellulaires avancées et validations pilotes.",
                    "Développement réseaux 5G 6G : mise en place infrastructures, recherche réseaux next-gen, formation mobile tech innovantes et tests expérimentaux.",
                    "Expansion cinquième et sixième génération : installation équipements, R&D réseaux avancés, éducation wireless tech émergentes et essais pilotes.",
                    "Croissance 5G et 6G : déploiement infrastructure, investigation réseaux futurs, apprentissage cellular technologies nouvelles et validations tests.",
                    "Développement mobile avancé : mise en place réseaux 5G/6G, recherche réseaux nouvelle génération, formation mobile innovations et expérimentations pilotes.",
                    "Expansion réseaux mobiles avancés : installation infrastructures 5G-6G, R&D réseaux next-gen, éducation wireless avancée et tests expérimentaux.",
                    "Croissance technologies mobiles futures : déploiement 5G/6G, investigation réseaux futurs, apprentissage cellular émergent et validations pilotes."
                ],
                "keywords": ["5G", "6G", "déploiement infrastructures", "recherche réseaux", "formation technologies mobiles", "tests pilotes"],
                "confidence": 0.85
            },

            "quels sont les programmes de cybersécurité citoyenne": {
                "answers": [
                    "Les programmes de cybersécurité citoyenne forment aux bonnes pratiques digitales, sensibilisent aux risques en ligne, fournissent des outils de protection et créent une culture de sécurité numérique.",
                    "Programmes cybersécurité citoyenne : formation bonnes pratiques digitales, sensibilisation risques en ligne, outils protection et culture sécurité numérique.",
                    "Initiatives sécurité cyber citoyenne : éducation pratiques digitales sûres, awareness dangers internet, instruments protection et développement culture sécurité digitale.",
                    "Dispositifs cybersécurité pour citoyens : apprentissage usages numériques sécurisés, sensibilisation menaces online, ressources protection et promotion culture sécurité tech.",
                    "Programmes security numérique citoyenne : formation digital hygiene, éducation risques cyber, outils safety et établissement culture protection digitale.",
                    "Initiatives cyber safety citoyenne : éducation pratiques numériques responsables, awareness périls internet, instruments sécurité et construction culture cyber protection.",
                    "Dispositifs sécurité digitale citoyenne : apprentissage comportements digitaux sûrs, sensibilisation dangers web, ressources safety et développement culture sécurité numérique.",
                    "Programmes protection cyber citoyenne : formation safe digital practices, éducation cyber risques, outils protection et implantation culture cyber sécurité.",
                    "Initiatives digital security citoyenne : éducation usages numériques sécuritaires, awareness menaces online, instruments safety et promotion culture protection tech.",
                    "Dispositifs cyber protection citoyenne : apprentissage pratiques digitales safe, sensibilisation périls internet, ressources protection et établissement culture sécurité digitale."
                ],
                "keywords": ["cybersécurité citoyenne", "bonnes pratiques", "sensibilisation risques", "outils protection", "culture sécurité", "éducation digitale"],
                "confidence": 0.85
            },

            "comment le new deal va digitaliser l'élevage": {
                "answers": [
                    "L'élevage est digitalisé par des capteurs de santé animale, des systèmes de traçabilité blockchain, des applications de gestion de troupeaux et des marchés digitaux pour les produits.",
                    "Digitalisation élevage : capteurs santé animale, systèmes traçabilité blockchain, applications gestion troupeaux et marchés digitaux produits.",
                    "Numérisation élevage : senseurs santé bétail, solutions tracking blockchain, apps management cheptel et plateformes commerce digital produits animaux.",
                    "Transformation numérique élevage : détecteurs condition animale, mécanismes traçabilité distributed ledger, outils gestion animaux et marchés online produits.",
                    "Digitalisation farming : capteurs animal health, systèmes blockchain traceability, applications herd management et digital markets produits.",
                    "Numérisation livestock : senseurs bétail santé, solutions DLT tracking, apps troupeau gestion et plateformes e-commerce produits animaux.",
                    "Transformation digitale élevage : détecteurs santé animale, mécanismes blockchain traçabilité, outils management animaux et marchés internet produits.",
                    "Digitalisation animal husbandry : capteurs health animale, systèmes distributed ledger traceability, applications herd gestion et digital commerce produits.",
                    "Numérisation élevage : senseurs condition bétail, solutions blockchain monitoring, apps cheptel management et plateformes online trading produits animaux.",
                    "Transformation tech élevage : détecteurs santé livestock, mécanismes DLT tracking, outils animaux gestion et marchés digital produits."
                ],
                "keywords": ["digitalisation élevage", "capteurs santé animale", "blockchain traçabilité", "gestion troupeaux", "marchés digitaux", "livestock tech"],
                "confidence": 0.8
            },

            "quels sont les projets de villes nouvelles intelligentes": {
                "answers": [
                    "Les projets de villes nouvelles intelligentes créent des éco-cités avec des infrastructures connectées, une gestion énergétique optimale, des transports intelligents et des services urbains digitaux.",
                    "Projets villes nouvelles intelligentes : éco-cités infrastructures connectées, gestion énergétique optimale, transports intelligents et services urbains digitaux.",
                    "Initiatives smart new cities : éco-villes réseaux interconnectés, management énergie optimal, mobilité intelligente et services municipaux numériques.",
                    "Développements villes intelligentes nouvelles : cités durables infrastructures liées, optimisation énergétique, transports smart et services city digitaux.",
                    "Projets new smart cities : éco-communautés infrastructures connectées, gestion energy efficient, intelligent transportation et urban services digital.",
                    "Initiatives villes nouvelles tech : éco-cités réseaux unis, management énergétique avancé, mobilité intelligente et services urbains numériques.",
                    "Développements smart cities nouvelles : cités durables systèmes interconnectés, optimisation power, transports smart et services municipaux digitaux.",
                    "Projets nouvelles villes intelligentes : éco-communautés infrastructures liées, gestion énergie optimisée, intelligent mobility et city services numérique.",
                    "Initiatives new tech cities : éco-cités réseaux connectés, management énergétique efficient, mobilité avancée et services urbains digital.",
                    "Développements villes futures intelligentes : cités durables systèmes unis, optimisation énergétique, transports intelligents et services municipaux numériques."
                ],
                "keywords": ["villes nouvelles intelligentes", "éco-cités", "infrastructures connectées", "gestion énergétique", "transports intelligents", "services urbains digitaux"],
                "confidence": 0.85
            },

            "comment le new deal va développer l'edge computing": {
                "answers": [
                    "L'edge computing est développé par des micro-data centers locaux, des processeurs spécialisés, des formations aux architectures distribuées et des applications temps réel.",
                    "Développement edge computing : micro-data centers locaux, processeurs spécialisés, formations architectures distribuées et applications temps réel.",
                    "Expansion edge computing : mini-centres données locaux, CPUs spécialisées, éducation architectures distribuées et apps real-time.",
                    "Croissance computing de périphérie : petits data centers régionaux, processeurs dédiés, apprentissage architectures décentralisées et applications temps réel.",
                    "Développement edge tech : micro-data centers domestiques, processeurs optimisés, formations distributed architectures et applications instantanées.",
                    "Expansion edge processing : mini-centres données régionaux, CPUs spécifiques, éducation decentralized architectures et apps real-time.",
                    "Croissance périphérie computing : petits data centers locaux, processeurs spécialisés, apprentissage architectures edge et applications temps réel.",
                    "Développement computing edge : micro-data centers nationaux, processeurs adaptés, formations edge architectures et apps instantanées.",
                    "Expansion traitement périphérique : mini-centres données domestiques, CPUs optimisées, éducation distributed computing et applications real-time.",
                    "Croissance tech edge : petits data centers régionaux, processeurs dédiés, apprentissage edge processing et applications temps réel."
                ],
                "keywords": ["edge computing", "micro-data centers", "processeurs spécialisés", "architectures distribuées", "applications temps réel", "computing périphérique"],
                "confidence": 0.8
            },

            "quels sont les programmes de résilience digitale territoriale": {
                "answers": [
                    "Les programmes de résilience digitale territoriale sécurisent les infrastructures critiques, forment aux cyber-risques, développent des solutions locales et assurent la continuité des services.",
                    "Programmes résilience digitale territoriale : sécurisation infrastructures critiques, formation cyber-risques, développement solutions locales et continuité services.",
                    "Initiatives résilience numérique territoriale : protection infrastructures vitales, éducation risques cyber, création solutions domestiques et maintien services essentiels.",
                    "Dispositifs résilience tech territoriale : sécurisation assets critiques, apprentissage cyber menaces, développement outils locaux et assurance continuité opérationnelle.",
                    "Programmes digital resilience territoriale : protection infrastructures clés, formation cyber threats, innovation solutions régionales et garantie continuité services.",
                    "Initiatives résilience digitale régionale : sécurisation installations critiques, éducation dangers cyber, conception solutions locales et préservation services cruciaux.",
                    "Dispositifs résilience numérique territoriale : protection équipements vitaux, apprentissage risques cyber, création applications domestiques et maintien services essentiels.",
                    "Programmes tech resilience territoriale : sécurisation infrastructures majeures, formation cyber risques, développement solutions régionales et assurance continuité opérationnelle.",
                    "Initiatives digital endurance territoriale : protection assets critiques, éducation menaces cyber, innovation outils locaux et garantie continuité services.",
                    "Dispositifs résilience tech régionale : sécurisation installations clés, apprentissage cyber dangers, conception applications régionales et préservation services cruciaux."
                ],
                "keywords": ["résilience digitale", "infrastructures critiques", "cyber-risques", "solutions locales", "continuité services", "territoriale"],
                "confidence": 0.85
            },

            "comment le new deal va transformer l'assurance": {
                "answers": [
                    "L'assurance est transformée par l'usage de l'IA pour l'évaluation des risques, les contrats intelligents blockchain, la personnalisation des polices et le traitement digital des sinistres.",
                    "Transformation assurance : IA évaluation risques, contrats intelligents blockchain, personnalisation polices et traitement digital sinistres.",
                    "Révolution numérique assurance : intelligence artificielle assessment risques, smart contracts blockchain, customisation assurances et gestion digitale réclamations.",
                    "Digitalisation assurance : AI analyse risques, contrats auto-exécutants blockchain, individualisation polices et traitement électronique sinistres.",
                    "Transformation insurance : IA risk assessment, blockchain smart contracts, personalization policies et digital claims processing.",
                    "Révolution tech assurance : intelligence artificielle évaluation risques, distributed ledger smart contracts, personnalisation couvertures et management numérique sinistres.",
                    "Digitalisation insurance : AI analysis risques, blockchain auto-executing contracts, individualization polices et traitement digital réclamations.",
                    "Transformation secteur assurance : IA risk evaluation, smart contracts DLT, customisation assurances et gestion électronique sinistres.",
                    "Révolution digitale assurance : intelligence artificielle assessment risques, blockchain intelligent contracts, personnalisation polices et traitement numérique claims.",
                    "Digitalisation industrie assurance : AI analyse risks, distributed ledger auto-executing contracts, individualization couvertures et management digital sinistres."
                ],
                "keywords": ["transformation assurance", "IA évaluation risques", "contrats intelligents", "blockchain", "personnalisation polices", "traitement digital sinistres"],
                "confidence": 0.85
            },

            "quels sont les projets de génomique digitale": {
                "answers": [
                    "Les projets de génomique digitale développent des bases de données ADN locales, des outils d'analyse génétique, la médecine personnalisée et la recherche sur les maladies génétiques.",
                    "Projets génomique digitale : bases données ADN locales, outils analyse génétique, médecine personnalisée et recherche maladies génétiques.",
                    "Initiatives génomique numérique : banques données génomiques locales, instruments analyse ADN, médecine de précision et investigation pathologies génétiques.",
                    "Développements digital genomics : databases ADN domestiques, outils genetic analysis, personalized medicine et recherche genetic diseases.",
                    "Projets genomic digitale : collections données génétiques locales, solutions analyse génome, médecine individualisée et études maladies héréditaires.",
                    "Initiatives numérique génomique : bases données ADN régionales, devices analyse génétique, precision medicine et recherche disorders génétiques.",
                    "Développements genomics digital : databases génomiques locales, instruments genome analysis, médecine personnalisée et investigation hereditary diseases.",
                    "Projets digital génomique : banques données génétiques domestiques, outils genetic testing, médecine de précision et études pathologies héréditaires.",
                    "Initiatives tech génomique : collections données ADN locales, solutions analyse ADN, personalized healthcare et recherche genetic disorders.",
                    "Développements numérique genomics : bases données génomiques régionales, devices genetic analysis, precision healthcare et investigation hereditary pathologies."
                ],
                "keywords": ["génomique digitale", "bases données ADN", "analyse génétique", "médecine personnalisée", "recherche maladies génétiques", "digital genomics"],
                "confidence": 0.8
            },

            "comment le new deal va développer les nanotechnologies": {
                "answers": [
                    "Les nanotechnologies sont développées via des centres de recherche spécialisés, des applications médicales avancées, des matériaux innovants et des partenariats industriels high-tech.",
                    "Développement nanotechnologies : centres recherche spécialisés, applications médicales avancées, matériaux innovants et partenariats industriels high-tech.",
                    "Expansion nanotech : laboratoires recherche dédiés, apps médicales sophistiquées, matériaux révolutionnaires et collaborations industrielles tech avancée.",
                    "Croissance nanotechnologies : instituts R&D spécialisés, utilisations médicales pointues, nouveaux matériaux et alliances industrielles haute technologie.",
                    "Développement nano tech : centres investigation nano, applications healthcare avancées, materials innovants et partenariats industry high-tech.",
                    "Expansion nanotechnologie : labs recherche nano, solutions médicales avancées, matériaux novateurs et coopérations industrielles tech pointe.",
                    "Croissance nano : instituts R&D nano, implementations médicales sophistiquées, nouveaux materials et alliances industrielles haute tech.",
                    "Développement technologies nano : centres spécialisés nano, applications médicales innovantes, matériaux révolutionnaires et partenariats industriels tech avancée.",
                    "Expansion nanosciences : laboratoires dédiés nano, apps healthcare pointues, materials novateurs et collaborations industrielles high-tech.",
                    "Croissance nano technologies : instituts recherche nano, utilisations médicales avancées, nouveaux matériaux et alliances industrielles tech pointe."
                ],
                "keywords": ["nanotechnologies", "centres recherche", "applications médicales", "matériaux innovants", "partenariats industriels", "high-tech"],
                "confidence": 0.8
            },

            "quels sont les programmes de tech dans les zones rurales": {
                "answers": [
                    "Les programmes de tech dans les zones rurales déploient des infrastructures internet, forment aux outils digitaux, développent l'agriculture tech et créent des télécentres communautaires.",
                    "Programmes tech zones rurales : déploiement infrastructures internet, formation outils digitaux, développement agriculture tech et création télécentres communautaires.",
                    "Initiatives numérique rural : installation réseaux internet, éducation outils numériques, promotion agri-tech et établissement centres numériques communautaires.",
                    "Dispositifs tech régions rurales : mise en place connectivité, apprentissage technologies digitales, expansion farming tech et création hubs digitaux villageois.",
                    "Programmes numérique campagnes : déploiement accès internet, formation compétences digitales, développement agricultural tech et implantation télécentres ruraux.",
                    "Initiatives tech zones reculées : installation broadband, éducation outils tech, stimulation ag-tech et établissement centres communautaires digitaux.",
                    "Dispositifs digital rural : mise en place internet, apprentissage digital skills, croissance farming technology et création hubs numériques ruraux.",
                    "Programmes technologies régions isolées : déploiement connectivity, formation tech outils, expansion agriculture technology et implantation télécentres villageois.",
                    "Initiatives numérique zones éloignées : installation réseaux, éducation compétences numériques, promotion agri-technology et établissement centres digitaux communautaires.",
                    "Dispositifs tech campagnes : mise en place accès internet, apprentissage outils digitaux, développement agricultural technology et création hubs numériques ruraux."
                ],
                "keywords": ["tech zones rurales", "infrastructures internet", "formation outils digitaux", "agriculture tech", "télécentres", "zones reculées"],
                "confidence": 0.85
            },

            "comment le new deal va développer la robotique": {
                "answers": [
                    "La robotique est développée par des laboratoires de R&D, des applications industrielles automatisées, la formation en ingénierie robotique et des compétitions d'innovation robotique.",
                    "Développement robotique : laboratoires R&D, applications industrielles automatisées, formation ingénierie robotique et compétitions innovation robotique.",
                    "Expansion robotics : labs recherche développement, implementations industrielles automation, éducation engineering robotique et concours innovation robotics.",
                    "Croissance robotique : centres R&D, apps industrielles robotisées, apprentissage robot engineering et challenges innovation robotique.",
                    "Développement robotics : instituts recherche, applications industrial automation, formation robotics engineering et compétitions robotics innovation.",
                    "Expansion robotique : laboratoires R&D, solutions industrielles automatisées, éducation ingénierie robotics et défis innovation robotique.",
                    "Croissance robotics : centres développement, implementations industrial robotics, apprentissage robot engineering et concours robotics innovation.",
                    "Développement ingénierie robotique : labs R&D, applications industry automation, formation robotics engineering et challenges robot innovation.",
                    "Expansion technologies robotiques : instituts recherche, solutions industrielles robotisées, éducation robot engineering et compétitions tech robotique.",
                    "Croissance engineering robotics : centres développement, apps industrial robotics, apprentissage robotics engineering et défis tech robotics."
                ],
                "keywords": ["robotique", "laboratoires R&D", "applications industrielles", "formation ingénierie", "compétitions innovation", "robotics"],
                "confidence": 0.85
            },

            "quels sont les projets de digitalisation du sport": {
                "answers": [
                    "Les projets de digitalisation du sport incluent des applications de performance athlétique, l'analyse de données sportives, les plateformes de streaming sportif et les stades connectés.",
                    "Projets digitalisation sport : applications performance athlétique, analyse données sportives, plateformes streaming sportif et stades connectés.",
                    "Initiatives numérique sport : apps performance athletes, analytics données sports, plateformes diffusion sportive et arenas connectées.",
                    "Développements sport digital : outils performance sportive, analysis données athletic, services streaming sports et stades intelligents.",
                    "Projets sport tech : applications athletic performance, analyse sports data, plateformes sport streaming et smart stadiums.",
                    "Initiatives digital sport : solutions performance athletes, analytics sports données, services diffusion sportive et connected arenas.",
                    "Développements numérique athletic : outils performance sportive, analysis athletic data, plateformes sport broadcast et intelligents stades.",
                    "Projets tech sport : apps sport performance, analyse données athletic, services streaming sports et smart venues.",
                    "Initiatives sport numérique : solutions athletes performance, analytics sport données, plateformes diffusion athletic et connected stadiums.",
                    "Développements digital athletic : outils sport performance, analysis sports data, services sport streaming et intelligents arenas."
                ],
                "keywords": ["digitalisation sport", "applications performance", "analyse données sportives", "streaming sportif", "stades connectés", "sport tech"],
                "confidence": 0.8
            },

            "comment le new deal va développer l'internet des objets médical": {
                "answers": [
                    "L'internet des objets médical est développé par des dispositifs de surveillance patients connectés, des capteurs santé wearable, la télémédecine et l'analyse temps réel des données médicales.",
                    "Développement IoT médical : dispositifs surveillance patients connectés, capteurs santé wearable, télémédecine et analyse temps réel données médicales.",
                    "Expansion internet des objets santé : devices monitoring patients connected, senseurs santé portables, télémedicine et analytics real-time données médicales.",
                    "Croissance medical IoT : équipements surveillance patients liés, capteurs wearable health, telemedicine et analysis temps réel medical data.",
                    "Développement IoMT : instruments monitoring patients connectés, senseurs santé wearables, télémédecine et analytics instantané données santé.",
                    "Expansion internet of medical things : devices patients monitoring connected, capteurs portable health, téléhealth et analysis real-time medical données.",
                    "Croissance IoT santé : équipements surveillance patients liés, senseurs wearable médical, telecare et analytics temps réel health data.",
                    "Développement medical internet of things : instruments patients monitoring connectés, capteurs santé portables, télémédecine et analytics instantané medical données.",
                    "Expansion IoHT : devices surveillance patients connected, senseurs wearable santé, telehealth et analysis real-time santé data.",
                    "Croissance internet of health things : équipements monitoring patients liés, capteurs médical wearables, telecare et analytics temps réel medical data."
                ],
                "keywords": ["internet des objets médical", "dispositifs surveillance", "capteurs wearable", "télémédecine", "analyse données médicales", "IoMT"],
                "confidence": 0.85
            },

            "quels sont les programmes de tech pour l'artisanat": {
                "answers": [
                    "Les programmes de tech pour l'artisanat digitalisent les techniques traditionnelles, créent des plateformes de vente en ligne, forment aux outils digitaux et préservent le patrimoine artisanal.",
                    "Programmes tech artisanat : digitalisation techniques traditionnelles, plateformes vente en ligne, formation outils digitaux et préservation patrimoine artisanal.",
                    "Initiatives numérique artisanat : numérisation savoir-faire traditionnels, plateformes e-commerce, éducation outils numériques et conservation héritage artisanal.",
                    "Dispositifs tech pour artisans : digitalisation métiers traditionnels, solutions vente online, apprentissage technologies digitales et sauvegarde patrimoine artisanal.",
                    "Programmes digital artisanat : transformation digitale techniques ancestrales, plateformes commerce électronique, formation digital tools et protection heritage artisanal.",
                    "Initiatives tech métiers artisanaux : numérisation compétences traditionnelles, plateformes online selling, éducation tech outils et préservation legacy artisanal.",
                    "Dispositifs numérique pour artisans : digitalisation arts traditionnels, solutions e-trading, apprentissage digital instruments et conservation patrimoine artisanal.",
                    "Programmes technology artisanat : modernisation digitale techniques anciennes, plateformes digital commerce, formation tech tools et sauvegarde héritage artisanal.",
                    "Initiatives digital pour métiers manuels : numérisation savoir-faire ancestraux, plateformes online sales, éducation numérique outils et protection tradition artisanal.",
                    "Dispositifs tech arts traditionnels : digitalisation crafts traditionnels, solutions internet selling, apprentissage tech instruments et préservation heritage artisanal."
                ],
                "keywords": ["tech artisanat", "digitalisation techniques", "plateformes vente en ligne", "formation outils digitaux", "patrimoine artisanal", "artisanat digital"],
                "confidence": 0.8
            }
        }
        
        # Variations et synonymes pour améliorer la détection
        self.synonyms = {
            "new deal": ["nouveau pacte technologique", "nouveau contrat technologique", "pacte technologique", "stratégie numérique nationale"],
            "technologique": ["digital", "numérique", "tech", "technologie"],
            "souveraineté": ["autonomie", "indépendance", "autosuffisance", "contrôle national"],
            "numérique": ["digital", "tech", "technologique", "électronique"],
            "transformation": ["modernisation", "évolution", "mutation", "révolution"],
            "innovation": ["création", "invention", "nouveauté", "avancée technologique"],
            "startup": ["jeune pousse", "entreprise innovante", "start-up", "pme innovante"],
            "investissement": ["financement", "capital", "fonds", "ressources financières"],
            "infrastructure": ["équipement", "réseau", "structure", "installations"],
            "formation": ["éducation", "apprentissage", "enseignement", "qualification"],
            "compétences": ["savoir-faire", "expertise", "aptitudes", "capacités"],
            "données": ["data", "informations", "renseignements", "bases de données"],
            "cybersécurité": ["sécurité informatique", "protection numérique", "cyberprotection", "sécurité des systèmes"],
            "intelligence artificielle": ["ia", "ai", "machine learning", "intelligence machine"],
            "cloud": ["informatique en nuage", "cloud computing", "serveurs distants", "stockage en ligne"],
            "blockchain": ["chaîne de blocs", "registre distribué", "technologie de registre", "distributed ledger"],
            "connectivité": ["accès internet", "connexion", "réseau", "liaison numérique"],
            "inclusion": ["intégration", "participation", "accessibilité", "égalité d'accès"],
            "écosystème": ["environnement", "système", "réseau d'acteurs", "communauté"],
            "emploi": ["travail", "poste", "métier", "opportunité professionnelle"],
            "entrepreneuriat": ["création d'entreprise", "business", "initiative économique", "venture"],
            "recherche": ["r&d", "recherche et développement", "investigation", "étude"],
            "développement": ["croissance", "expansion", "progrès", "avancement"],
            "stratégie": ["plan", "feuille de route", "approche", "méthodologie"],
            "gouvernance": ["gestion", "direction", "pilotage", "administration"],
            "partenariat": ["collaboration", "coopération", "alliance", "association"],
            "financement": ["investissement", "capital", "subvention", "ressources"],
            "projet": ["initiative", "programme", "chantier", "entreprise"],
            "technologie": ["tech", "innovation", "solution technique", "avancée"],
            "digitalisation": ["numérisation", "dématérialisation", "transformation digitale", "conversion numérique"],
            "smart city": ["ville intelligente", "cité connectée", "ville numérique", "urbanisme intelligent"],
            "iot": ["internet des objets", "objets connectés", "capteurs intelligents", "devices connectés"],
            "big data": ["mégadonnées", "données massives", "analyse de données", "data analytics"],
            "5g": ["cinquième génération", "réseau 5g", "téléphonie 5g", "connexion 5g"],
            "fibre optique": ["réseau fibre", "connexion fibre", "internet fibre", "haut débit fibre"],
            "data center": ["centre de données", "centre informatique", "serveurs", "infrastructure data"],
            "e-gouvernement": ["gouvernement électronique", "administration en ligne", "services publics digitaux", "état numérique"],
            "fintech": ["technologie financière", "finance digitale", "innovation financière", "finance tech"],
            "edtech": ["technologie éducative", "éducation numérique", "digital learning", "tech éducative"],
            "healthtech": ["technologie santé", "santé numérique", "médecine digitale", "tech médicale"],
            "agritech": ["technologie agricole", "agriculture numérique", "farming tech", "agro-digital"],
            "green tech": ["technologie verte", "écotech", "technologie durable", "innovation environnementale"]
        }
    
    def normalize_question(self, question: str) -> str:
        """Normalise une question pour améliorer la correspondance"""
        # Convertir en minuscules
        question = question.lower().strip()
        
        # Supprimer la ponctuation
        question = re.sub(r'[?!.,;:]', '', question)
        
        # Remplacer les synonymes
        for key, synonyms in self.synonyms.items():
            for synonym in synonyms:
                question = question.replace(synonym, key)
        
        return question
    
    def calculate_similarity(self, question1: str, question2: str) -> float:
        """Calcule la similarité entre deux questions"""
        return SequenceMatcher(None, question1, question2).ratio()
    
    def find_best_match(self, user_question: str, threshold: float = 0.7) -> Optional[Tuple[str, Dict]]:
        """Trouve la meilleure correspondance pour une question utilisateur"""
        normalized_question = self.normalize_question(user_question)
        
        best_match = None
        best_score = 0.0
        
        for predefined_question, qa_data in self.qa_database.items():
            # Similarité directe avec la question prédéfinie
            similarity = self.calculate_similarity(normalized_question, predefined_question)
            
            # Bonus si des mots-clés sont présents
            keyword_bonus = 0.0
            for keyword in qa_data["keywords"]:
                if keyword.lower() in normalized_question:
                    keyword_bonus += 0.1
            
            total_score = similarity + min(keyword_bonus, 0.3)  # Limiter le bonus à 0.3
            
            if total_score > best_score and total_score >= threshold:
                best_score = total_score
                best_match = (predefined_question, qa_data)
        
        return best_match if best_match else None
    
    def get_predefined_answer(self, user_question: str, threshold: float = 0.7) -> Optional[Dict]:
        """Récupère une réponse prédéfinie si elle existe"""
        match = self.find_best_match(user_question, threshold)
        
        if match:
            predefined_question, qa_data = match
            logger.info(f"Réponse prédéfinie trouvée pour: '{user_question}' -> '{predefined_question}'")
            
            # Sélectionner une réponse aléatoire parmi les réponses disponibles
            if "answers" in qa_data:
                # Nouveau format avec plusieurs réponses
                selected_answer = random.choice(qa_data["answers"])
                logger.info(f"Réponse sélectionnée aléatoirement: '{selected_answer[:50]}...'")
            elif "answer" in qa_data:
                # Ancien format avec une seule réponse (rétrocompatibilité)
                selected_answer = qa_data["answer"]
            else:
                logger.error(f"Format de données invalide pour la question: {predefined_question}")
                return None
            
            return {
                "answer": selected_answer,
                "confidence": qa_data["confidence"],
                "matched_question": predefined_question,
                "source": "predefined_qa",
                "keywords_matched": qa_data["keywords"],
                "total_answers_available": len(qa_data.get("answers", [qa_data.get("answer", "")]))
            }
        
        return None
    
    def add_qa_pair(self, question: str, answer, keywords: List[str], confidence: float = 0.8):
        """Ajoute une nouvelle paire question-réponse
        
        Args:
            question: La question à ajouter
            answer: Soit une string (réponse unique) soit une liste de strings (réponses multiples)
            keywords: Liste des mots-clés
            confidence: Niveau de confiance
        """
        normalized_question = self.normalize_question(question)
        
        if isinstance(answer, list):
            # Format avec plusieurs réponses
            self.qa_database[normalized_question] = {
                "answers": answer,
                "keywords": keywords,
                "confidence": confidence
            }
        else:
            # Format avec une seule réponse (rétrocompatibilité)
            self.qa_database[normalized_question] = {
                "answer": answer,
                "keywords": keywords,
                "confidence": confidence
            }
        
        logger.info(f"Nouvelle Q&A ajoutée: {question} ({len(answer) if isinstance(answer, list) else 1} réponse(s))")
    
    def get_all_questions(self) -> List[str]:
        """Retourne toutes les questions prédéfinies"""
        return list(self.qa_database.keys())
    
    def get_statistics(self) -> Dict:
        """Retourne des statistiques sur la base de Q&A"""
        return {
            "total_questions": len(self.qa_database),
            "average_confidence": sum(qa["confidence"] for qa in self.qa_database.values()) / len(self.qa_database),
            "total_keywords": sum(len(qa["keywords"]) for qa in self.qa_database.values())
        }
    
    def search_by_keyword(self, keyword: str) -> List[Tuple[str, Dict]]:
        """Recherche des Q&A par mot-clé"""
        results = []
        keyword_lower = keyword.lower()
        
        for question, qa_data in self.qa_database.items():
            if any(keyword_lower in kw.lower() for kw in qa_data["keywords"]) or keyword_lower in question:
                results.append((question, qa_data))
        
        return results