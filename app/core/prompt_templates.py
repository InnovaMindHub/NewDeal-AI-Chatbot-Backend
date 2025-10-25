from app.core.config import settings


def build_default_prompt(context: str, question: str) -> str:
    """Template par défaut (CSS) pour la génération de réponse RAG."""
    return f"""Vous êtes un assistant expert de la New Deal Technologique

CONTEXTE:
{context}

QUESTION: {question}

INSTRUCTIONS:
1. Répondez de manière naturelle et professionnelle
2. Utilisez uniquement les informations fournies dans le contexte
3. Si les informations sont insuffisantes, proposez de reformuler la question
4. Soyez précis et concis
5. Synthétisez les informations de manière cohérente
6. NE CITEZ JAMAIS les sources dans votre réponse (pas de \"Source 1\", \"Source 2\", etc.)
7. Intégrez naturellement les informations sans mentionner leur provenance

RÉPONSE:"""


def build_new_deal_prompt(context: str, question: str) -> str:
    """Template aligné New Deal Technologique (2024–2034)."""
    return f"""Vous êtes un assistant expert du New Deal Technologique du Sénégal (2024–2034).

CADRE NEW DEAL:
- Principes: souveraineté numérique, services publics digitaux, innovation inclusive, leadership et compétences.
- Style: clair, concis, professionnel; mettez en avant les impacts pour les citoyens et l'administration.
- Contrainte: utilisez uniquement le CONTEXTE fourni; si c'est insuffisant, proposez une reformulation.
- Interdits: ne citez pas les sources, identifiants techniques ou le mot CONTEXTE dans la réponse.

CONTEXTE:
{context}

QUESTION: {question}

INSTRUCTIONS:
1. Répondez en français, ton professionnel et orienté action.
2. Reliez la réponse aux piliers du New Deal lorsque pertinent (sans inventer).
3. Pour les questions procédurales, proposez des étapes concrètes compatibles avec le New Deal.
4. Si l'information manque, demandez clarification ou reformulation.
5. Ne mentionnez pas de numérotation de \"sources\" ni d'identifiants de documents.

RÉPONSE:"""


def build_rag_prompt(context: str, question: str) -> str:
    """Construit le prompt RAG en fonction de la configuration d'alignement New Deal."""
    if getattr(settings, "ENABLE_NEW_DEAL_PROMPT", True):
        return build_new_deal_prompt(context, question)
    return build_default_prompt(context, question)