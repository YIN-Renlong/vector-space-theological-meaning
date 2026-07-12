#!/usr/bin/env python3
"""CTSB v3.5-alpha generated exploratory 100-concept benchmark.

This instrument inherits the CTSB v3.4 mathematics and scoring engine.
Its generated references, validation passages, and resulting scores are
non-evidential until source fidelity and human review are completed.
"""

import argparse
import importlib.util
import json
import math
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "scripts" / "ctsb_v3_4_prototype.py"
DEFAULT_DATA_DIR = (
    ROOT / "data" / "benchmarks" / "v3_5_alpha" / "generated_100"
)
DEFAULT_OUTPUT_ROOT = ROOT / "outputs" / "v3_5_alpha" / "runs"
DEFAULT_CACHE = ROOT / "outputs" / "v3_5_alpha" / "embedding_cache.json"

spec = importlib.util.spec_from_file_location("ctsb_v3_4_engine", BASE_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not import CTSB v3.4 engine: {BASE_SCRIPT}")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

LOCI = {
    "F": "Freedom Truth and Moral Teleology",
    "A": "Human Dignity and Theological Anthropology",
    "L": "Love Communion and Sacramentality",
    "R": "Sin Grace and Redemption",
}

COMPARISON_SOURCES = {
    "biology": (
        "CANDIDATE SOURCE — biomedical and biological reference works",
        "Exact supporting source and wording not yet selected or verified",
    ),
    "medicine": (
        "CANDIDATE SOURCE — World Health Organization and clinical guidance",
        "Exact supporting source and wording not yet selected or verified",
    ),
    "psychology": (
        "CANDIDATE SOURCE — APA Dictionary of Psychology and bereavement literature",
        "Exact supporting source and wording not yet selected or verified",
    ),
    "law": (
        "CANDIDATE SOURCE — Cornell Legal Information Institute and public-law references",
        "Exact supporting source and wording not yet selected or verified",
    ),
    "dictionary": (
        "CANDIDATE SOURCE — established English-language dictionaries",
        "Exact supporting entry and wording not yet selected or verified",
    ),
    "religious_studies": (
        "CANDIDATE SOURCE — comparative-religion reference works",
        "Exact supporting source and wording not yet selected or verified",
    ),
    "social_science": (
        "CANDIDATE SOURCE — established social-science reference works",
        "Exact supporting source and wording not yet selected or verified",
    ),
    "philosophy": (
        "CANDIDATE SOURCE — Stanford Encyclopedia of Philosophy and ethics references",
        "Exact supporting source and wording not yet selected or verified",
    ),
    "bioethics": (
        "CANDIDATE SOURCE — permissive assisted-dying law and bioethics sources",
        "Exact jurisdiction, source, and wording not yet selected or verified",
    ),
    "economics": (
        "CANDIDATE SOURCE — World Bank and established economic references",
        "Exact supporting source and wording not yet selected or verified",
    ),
    "management": (
        "CANDIDATE SOURCE — public-administration and management references",
        "Exact supporting source and wording not yet selected or verified",
    ),
}

CATHOLIC_SOURCES = {
    "F": (
        "CANDIDATE SOURCE — Catechism, Veritatis splendor, and Catholic social teaching",
        "Exact supporting passage and wording not yet selected or verified",
    ),
    "A": (
        "CANDIDATE SOURCE — Catechism, Gaudium et spes, Evangelium vitae, and Dignitas infinita",
        "Exact supporting passage and wording not yet selected or verified",
    ),
    "L": (
        "CANDIDATE SOURCE — Catechism, Deus caritas est, Amoris laetitia, and liturgical sources",
        "Exact supporting passage and wording not yet selected or verified",
    ),
    "R": (
        "CANDIDATE SOURCE — Catechism and Catholic doctrinal sources on grace and redemption",
        "Exact supporting passage and wording not yet selected or verified",
    ),
}

SOURCE_OVERRIDES = {
    "death_biological": (
        "CANDIDATE SOURCE — Catechism sections on death, judgment, and resurrection",
        "Exact supporting paragraphs and wording not yet selected or verified",
    ),
    "grief_psychological": (
        "CANDIDATE SOURCE — Order of Christian Funerals and Catholic pastoral sources",
        "Exact supporting passage and wording not yet selected or verified",
    ),
    "euthanasia_assisted_dying": (
        "CANDIDATE SOURCE — Catechism, Evangelium vitae, and Samaritanus bonus",
        "Exact supporting passages and wording not yet selected or verified",
    ),
    "grace_lexical": (
        "CANDIDATE SOURCE — Catechism sections on grace and justification",
        "Exact supporting paragraphs and wording not yet selected or verified",
    ),
    "judgment_after_death_generic": (
        "CANDIDATE SOURCE — Catechism sections on particular judgment",
        "Exact supporting paragraphs and wording not yet selected or verified",
    ),
}

REGISTRY_TEXT = """
freedom_autonomy|freedom|F|false|autonomy and self-determination|valid_but_partial|false|choice ordered to truth and goodness, moral responsibility, and the person's final end|individual self-determination and control over personal decisions|philosophy
autonomy_self_governance|autonomy|F|false|individual self-governance|valid_but_partial|false|responsible self-governance within truth, relationship, and the common good|independent control over one's choices and life plans|philosophy
conscience_subjective_preference|conscience|F|false|subjective moral preference|normatively_conflicting|false|a judgment of reason seeking moral truth and requiring formation|private preference and personal sincerity as sufficient moral authority|philosophy
responsibility_legal|responsibility|F|false|legal accountability|valid_but_partial|false|moral agency, answerability before God and neighbour, and duties toward the common good|liability, legal duty, and accountability for conduct|law
happiness_subjective_wellbeing|happiness|F|false|subjective wellbeing|valid_but_partial|false|beatitude, virtue, communion with God, and the fulfilment of the human vocation|positive affect, life satisfaction, and subjective wellbeing|psychology
flourishing_psychological|flourishing|F|false|psychological flourishing|valid_but_partial|false|integral human fulfilment through virtue, relationship, truth, and final destiny|wellbeing, resilience, positive functioning, and personal growth|psychology
virtue_character_psychology|virtue|F|false|positive character traits|valid_but_partial|false|stable habits ordered toward the good and formed through moral action|socially valued character strengths and positive behavioural tendencies|psychology
obedience_compliance|obedience|F|false|institutional compliance|valid_but_partial|false|free and responsible responsiveness to legitimate authority and divine truth|conformity to rules, commands, and organisational authority|social_science
rights_legal_entitlements|rights|F|false|legal entitlements|complementary_levels|false|claims grounded in human dignity and ordered toward duties and the common good|enforceable legal claims and protections recognised by institutions|law
justice_procedural|justice|F|false|procedural fairness|valid_but_partial|false|giving each person what is due within right relationship and the common good|consistent procedures, impartial decisions, and fair distribution|law
truth_factual_accuracy|truth|F|false|factual accuracy|complementary_levels|false|conformity of mind and life to reality, honesty, and ultimately God as truth|correct factual representation and correspondence with observable evidence|philosophy
goodness_prosocial|goodness|F|false|prosocial behaviour|valid_but_partial|false|participation in the good through right action, virtue, love, and final purpose|helpful conduct, social approval, and beneficial outcomes|psychology
vocation_career|vocation|F|false|career calling|alternative_lexical_senses|false|a divine call to holiness, service, relationship, and a particular form of life|a personally meaningful occupation or professional career|dictionary
discernment_decision_making|discernment|F|false|decision-making process|valid_but_partial|false|prayerful judgment seeking God's will through reason, conscience, and spiritual wisdom|evaluation of options, evidence, risks, and expected outcomes|psychology
prudence_risk_management|prudence|F|false|risk management|valid_but_partial|false|practical wisdom that identifies the true good and chooses fitting means|cautious decision-making intended to minimise foreseeable risk|management
temperance_moderation|temperance|F|false|behavioural moderation|valid_but_partial|false|a cardinal virtue ordering desires and pleasures through reason|self-control, restraint, and moderation of consumption or behaviour|psychology
fortitude_resilience|fortitude|F|false|psychological resilience|valid_but_partial|false|courage and constancy in pursuing the good despite fear, suffering, or trial|capacity to recover and maintain functioning under stress|psychology
charity_philanthropy|charity|F|false|philanthropic giving|alternative_lexical_senses|false|the theological virtue of loving God and neighbour through participation in divine love|voluntary donation of money, goods, or services to social causes|social_science
solidarity_social_cohesion|solidarity|F|false|social cohesion|valid_but_partial|false|a moral commitment to the good of all, especially the poor and vulnerable|group unity, mutual support, and shared social identity|social_science
subsidiarity_decentralization|subsidiarity|F|false|administrative decentralisation|valid_but_partial|false|ordering social authority so lower communities can act while receiving necessary support|delegation of decisions from central institutions to local units|management
common_good_aggregate_welfare|common good|F|false|aggregate social welfare|valid_but_partial|false|social conditions enabling persons and communities to reach fulfilment together|the summed welfare, preferences, or measurable benefits of a population|economics
law_positive_law|law|F|false|positive law|complementary_levels|false|an ordinance of reason serving justice and the common good within moral order|rules formally enacted and enforced by political institutions|law
natural_law_natural_science|natural law|F|false|scientific laws of nature|alternative_lexical_senses|false|moral participation in rational order knowable through human reason|descriptive regularities governing physical processes in nature|biology
moral_agency_decision_capacity|moral agency|F|false|decision-making capacity|complementary_levels|false|freedom, reason, conscience, responsibility, and accountability for moral action|cognitive ability to understand options and communicate a decision|medicine
license_legal_permission|license|F|false|legal permission|alternative_lexical_senses|false|misuse of freedom when choice is detached from truth, responsibility, and the good|formal permission granted by law or an authorised institution|law
personhood_legal_status|personhood|A|false|legal person status|valid_but_partial|false|the irreducible dignity of an embodied and relational human being created by God|status as an entity recognised as bearing legal rights and duties|law
human_dignity_human_rights|human dignity|A|false|human-rights discourse|complementary_levels|false|inherent worth grounded in creation, vocation, relationship, and final destiny|the foundational equal status used to support universal human rights|law
body_biological|body|A|false|biological organism|complementary_levels|false|embodied personhood and body-soul unity within creation and resurrection|an organism composed of cells, organs, tissues, and physiological systems|biology
soul_mind|soul|A|false|mind and consciousness|valid_but_partial|false|the spiritual principle of human life within the unity of body and soul|conscious awareness, cognition, memory, and mental processes|psychology
embodiment_phenomenology|embodiment|A|false|lived bodily experience|complementary_levels|false|the bodily condition of the human person as created, relational, vulnerable, and destined for resurrection|subjective experience of perceiving and acting through a body|philosophy
sexuality_identity_behaviour|sexuality|A|false|sexual identity and behaviour|valid_but_partial|false|an embodied dimension of the person ordered toward love, relationship, responsibility, and self-gift|sexual identity, attraction, behaviour, and patterns of intimate expression|psychology
disability_functional_impairment|disability|A|false|functional impairment|valid_but_partial|false|equal personal dignity, interdependence, participation, and a vocation to communion|limitations in bodily, sensory, cognitive, or social functioning|medicine
suffering_pain_symptom|suffering|A|true|clinical pain and distress|valid_but_partial|true|an experience calling for compassion, accompaniment, hope, and rejection of abandonment|pain severity, distress symptoms, and impairment requiring clinical management|medicine
illness_biomedical|illness|A|true|biomedical pathology|complementary_levels|true|human vulnerability requiring care for the whole person, solidarity, and hope|disease processes, symptoms, diagnosis, prognosis, and treatment|medicine
healing_clinical_recovery|healing|A|true|clinical recovery|complementary_levels|false|restoration involving body, relationship, reconciliation, hope, and spiritual wholeness|improvement of symptoms, function, or measurable health outcomes|medicine
care_healthcare_service|care|A|false|healthcare service delivery|valid_but_partial|false|loving attention to the whole person through presence, responsibility, and solidarity|provision of professional services intended to maintain or restore health|medicine
work_paid_employment|work|A|false|paid employment|valid_but_partial|false|participation in creation, service, human dignity, solidarity, and the common good|contracted labour exchanged for wages, income, and economic production|economics
poverty_income_deprivation|poverty|A|false|income deprivation|complementary_levels|false|material and relational deprivation calling for justice, solidarity, and preferential concern|insufficient income or resources relative to an established threshold|economics
creation_cosmological_origin|creation|A|false|cosmological origins|complementary_levels|false|the dependence of all reality upon God, its goodness, order, and purpose|physical accounts of the universe's origin, development, and structure|biology
stewardship_resource_management|stewardship|A|false|resource management|valid_but_partial|false|responsible care for creation and goods entrusted for the common good|administration of assets, resources, risks, and organisational responsibilities|management
death_biological|death|A|true|biological description|complementary_levels|true|the end of earthly life understood with judgment, mercy, resurrection, and communion with God|irreversible cessation of integrated vital biological functions|biology
dying_terminal_decline|dying|A|true|terminal physiological decline|complementary_levels|true|the final stage of earthly life requiring dignity, accompaniment, prayer, and hope|progressive physiological failure associated with terminal illness|medicine
grief_psychological|grief|A|true|psychological bereavement|valid_but_partial|true|mourning brought before God through prayer, consolation, communion, and resurrection hope|emotional, cognitive, behavioural, and social adaptation following loss|psychology
suicide_mental_health|suicide|A|true|mental-health crisis|valid_but_partial|true|grave human suffering calling for protection of life, mercy, hope, and compassionate accompaniment|acute suicide risk, psychological distress, safety planning, and crisis intervention|psychology
euthanasia_assisted_dying|euthanasia|A|true|permissive assisted-dying register|normatively_conflicting|true|relief of suffering and accompaniment while refusing the intentional ending of innocent human life|a competent person's autonomous request for medical assistance to end life|bioethics
palliative_care_symptom_management|palliative care|A|true|clinical symptom management|complementary_levels|true|whole-person accompaniment that relieves suffering while respecting dignity and natural death|multidisciplinary treatment of pain, symptoms, and quality-of-life needs|medicine
hope_positive_expectation|hope|A|false|positive expectation|valid_but_partial|false|a theological virtue trusting God's promises and orienting life toward eternal fulfilment|optimistic expectation that a desired future outcome will occur|psychology
mercy_leniency|mercy|A|false|leniency|alternative_lexical_senses|false|compassionate love responding to suffering and sin with forgiveness and restoration|reduction or suspension of a penalty that could otherwise be imposed|law
vulnerability_risk_exposure|vulnerability|A|false|risk exposure|valid_but_partial|false|shared creaturely dependence that grounds responsibility, protection, and solidarity|heightened probability of harm due to exposure and reduced protective capacity|social_science
dependence_autonomy_deficit|dependence|A|false|reduced independence|valid_but_partial|false|a relational feature of human life involving mutual care, receptivity, and solidarity|need for assistance because independent functioning or decision-making is limited|medicine
love_romantic_attachment|love|L|false|romantic attachment|valid_but_partial|false|self-giving participation in divine love ordered toward the good of the other|affection, attraction, attachment, intimacy, and romantic partnership|psychology
friendship_social_bond|friendship|L|false|social bond|valid_but_partial|false|mutual willing of the good through fidelity, virtue, presence, and communion|a voluntary interpersonal relationship involving affection and shared activity|social_science
neighbour_physical_proximity|neighbour|L|false|nearby resident|alternative_lexical_senses|false|every person encountered as one to be loved through concrete responsibility|a person who lives in an adjacent or nearby location|dictionary
family_household|family|L|false|household and kinship unit|valid_but_partial|false|a communion of persons marked by covenant, generation, care, fidelity, and vocation|a household or kinship network described through social roles and residence|social_science
marriage_civil_contract|marriage|L|false|civil marital contract|valid_but_partial|false|a faithful and fruitful covenantal communion of spouses with sacramental significance|a legally recognised union creating civil rights and obligations|law
marital_fidelity_exclusivity|marital fidelity|L|false|relationship exclusivity|valid_but_partial|false|covenantal faithfulness, permanence, truthfulness, and mutual self-gift between spouses|agreement to sexual or romantic exclusivity within a partnership|psychology
chastity_abstinence|chastity|L|false|sexual abstinence|valid_but_partial|false|integration of sexuality within the whole person, vocation, freedom, and love|refraining from sexual activity or limiting specified sexual behaviours|psychology
self_gift_altruism|self-gift|L|false|altruistic behaviour|valid_but_partial|false|free donation of oneself in love, vocation, communion, and service|costly behaviour intended to benefit another person or group|psychology
communion_social_togetherness|communion|L|false|social togetherness|alternative_lexical_senses|false|participation in shared life with God and others through grace, faith, and sacrament|a feeling of fellowship, closeness, and shared social identity|dictionary
community_voluntary_association|community|L|false|voluntary association|valid_but_partial|false|a relational communion ordered toward participation, solidarity, worship, and the common good|a group formed through shared interests, identity, location, or activity|social_science
sacrament_generic_ritual|sacrament|L|false|generic religious ritual|generic_religious_vs_catholic_specific|false|an efficacious sign of grace instituted by Christ and entrusted to the Church|a sacred ceremony symbolising religious belief or communal identity|religious_studies
baptism_initiation_rite|baptism|L|false|religious initiation rite|generic_religious_vs_catholic_specific|false|sacramental rebirth in water and the Spirit, incorporation into Christ, and forgiveness of sin|a ritual marking entry into a religious community|religious_studies
eucharist_commemorative_meal|Eucharist|L|false|commemorative religious meal|generic_religious_vs_catholic_specific|false|the sacramental presence of Christ, memorial of the Paschal mystery, sacrifice, and communion|a communal meal that symbolically remembers a religious founder or event|religious_studies
reconciliation_conflict_resolution|reconciliation|L|false|interpersonal conflict resolution|valid_but_partial|false|restoration of communion with God and neighbour through conversion, forgiveness, and sacrament|resolution of disagreement and rebuilding of workable interpersonal relations|psychology
forgiveness_psychological_release|forgiveness|L|false|psychological release|valid_but_partial|false|a response to mercy that relinquishes vengeance and seeks restored right relationship|reduction of resentment, anger, and distress associated with an offence|psychology
compassion_empathic_concern|compassion|L|false|empathic concern|valid_but_partial|false|love moved by another's suffering into presence, service, mercy, and solidarity|emotional concern for distress that motivates supportive behaviour|psychology
caritas_charitable_giving|caritas|L|false|charitable giving|alternative_lexical_senses|false|divine love received and enacted as love of God and neighbour|donation or organised relief activity directed toward people in need|social_science
eros_romantic_desire|eros|L|false|romantic and sexual desire|valid_but_partial|false|desiring love capable of purification, integration, fidelity, and self-gift|romantic attraction, sexual desire, and longing for intimate union|psychology
agape_altruistic_love|agape|L|false|altruistic love|valid_but_partial|false|self-giving love rooted in God's prior love and extended to every neighbour|unselfish concern expressed through beneficial action toward others|psychology
parenthood_caregiving_role|parenthood|L|false|caregiving role|valid_but_partial|false|a vocation of generativity, education, protection, love, and responsibility for children|the social and practical role of raising and caring for a child|social_science
celibacy_unmarried_status|celibacy|L|false|unmarried status|valid_but_partial|false|a freely embraced vocation of consecrated availability, service, and eschatological witness|the condition of being unmarried or abstaining from sexual relationships|dictionary
hospitality_social_welcome|hospitality|L|false|social welcome|valid_but_partial|false|receiving the stranger and neighbour through generosity, dignity, and communion|friendly reception of guests and provision of food, lodging, or service|dictionary
peace_absence_conflict|peace|L|false|absence of conflict|valid_but_partial|false|right relationship, justice, reconciliation, order, and communion with God and neighbour|a condition in which organised violence or interpersonal conflict is absent|social_science
liturgy_ritual_performance|liturgy|L|false|ritual performance|generic_religious_vs_catholic_specific|false|the public worship of the Church and participation in Christ's priestly work|a prescribed sequence of ceremonial words, gestures, and communal actions|religious_studies
prayer_mindfulness|prayer|L|false|mindfulness practice|valid_but_partial|false|a living relationship with God expressed through adoration, petition, thanksgiving, and contemplation|attention-regulation practice focused on present-moment awareness|psychology
grace_lexical|grace|R|false|elegance and social charm|alternative_lexical_senses|false|the free and undeserved divine gift that heals, sanctifies, and draws persons into communion with God|elegance of movement, poise, courtesy, and social charm|dictionary
sin_rule_breaking|sin|R|false|rule-breaking|valid_but_partial|false|an offence against God, reason, truth, love, and right relationship|violation of a rule, norm, policy, or expected standard of conduct|law
original_sin_generic_corruption|original sin|R|false|generic inherited corruption doctrine|generic_religious_vs_catholic_specific|false|the wounded human condition inherited from humanity's first disobedience without personal culpability in descendants|a broad doctrine that moral corruption or guilt is biologically or personally inherited|religious_studies
guilt_psychological|guilt|R|false|psychological guilt|valid_but_partial|false|recognition of moral fault calling for truth, repentance, forgiveness, and reconciliation|an aversive emotion arising from perceived responsibility for wrongdoing|psychology
shame_affective|shame|R|false|affective shame|valid_but_partial|false|painful exposure requiring truthful moral discernment, mercy, dignity, and restored communion|a self-conscious emotion involving perceived defectiveness and social devaluation|psychology
salvation_rescue|salvation|R|false|rescue from danger|alternative_lexical_senses|false|deliverance from sin and death through Christ and participation in divine life|preservation or rescue from physical danger, loss, or destruction|dictionary
redemption_financial|redemption|R|false|financial repurchase|alternative_lexical_senses|false|liberation from sin through Christ's saving action, restoring communion and freedom|repurchase of an asset, repayment of an obligation, or exchange of a financial instrument|economics
justification_legal_acquittal|justification|R|false|legal acquittal|alternative_lexical_senses|false|God's gracious action forgiving sin, making the person righteous, and restoring communion|a legal reason that warrants conduct or a judgment that removes liability|law
sanctification_self_improvement|sanctification|R|false|personal self-improvement|valid_but_partial|false|growth in holiness through grace, conversion, virtue, and participation in divine life|deliberate improvement of habits, performance, wellbeing, or personal effectiveness|psychology
atonement_reparation|atonement|R|false|reparation for wrongdoing|valid_but_partial|false|reconciliation with God through Christ's saving self-offering and the restoration of communion|compensation, apology, or corrective action intended to repair harm|law
repentance_regret|repentance|R|false|personal regret|valid_but_partial|false|conversion of heart involving sorrow for sin, confession, amendment, and return to God|negative emotion and remorse concerning a past decision or action|psychology
conversion_change_opinion|conversion|R|false|change of opinion|alternative_lexical_senses|false|a turning of the whole person toward God through faith, repentance, grace, and renewed life|a change in belief, affiliation, preference, or practical position|dictionary
faith_belief|faith|R|false|personal belief|valid_but_partial|false|a grace-enabled response to God's revelation involving trust, assent, worship, and discipleship|acceptance of a proposition or confidence in a person without requiring complete evidence|philosophy
resurrection_generic_rebirth|resurrection|R|true|generic religious rebirth|generic_religious_vs_catholic_specific|false|the bodily raising of the dead through Christ and the fulfilment of human destiny|a broad religious or symbolic image of return, rebirth, revival, or renewed existence|religious_studies
judgment_after_death_generic|judgment after death|R|true|generic religious afterlife judgment|generic_religious_vs_catholic_specific|false|particular judgment before God in which each life is revealed in divine justice and mercy|a widespread religious image in which souls or deeds receive postmortem evaluation|religious_studies
heaven_happy_afterlife|heaven|R|true|generic happy afterlife|generic_religious_vs_catholic_specific|false|definitive communion with God, the fulfilment of human longing, and the communion of saints|a pleasant postmortem realm characterised by reward, happiness, and continued existence|religious_studies
hell_punishment_afterlife|hell|R|true|generic punishment afterlife|generic_religious_vs_catholic_specific|false|definitive self-exclusion from communion with God and the tragic consequence of freely rejecting love|an afterlife realm in which wrongdoers receive suffering or punishment|religious_studies
purgatory_generic_purification|purgatory|R|true|generic postmortem purification|generic_religious_vs_catholic_specific|false|final purification by God's grace for those who die in friendship with God but still require cleansing|a general intermediate state in which souls undergo testing, cleansing, or preparation after death|religious_studies
divine_providence_fortune|divine providence|R|false|fortune and chance|normatively_conflicting|false|God's wise and loving governance of creation while respecting creaturely causality and freedom|events attributed primarily to luck, random occurrence, or impersonal circumstance|philosophy
miracle_anomaly|miracle|R|false|unexplained anomaly|valid_but_partial|false|an extraordinary sign of God's action within creation that discloses grace and serves salvation|an unusual event not yet explained by available scientific or statistical models|philosophy
revelation_disclosure|revelation|R|false|disclosure of information|alternative_lexical_senses|false|God's self-communication in history, fulfilled in Christ and transmitted through Scripture and Tradition|the act of making previously hidden information publicly or personally known|dictionary
doctrine_policy|doctrine|R|false|institutional policy|alternative_lexical_senses|false|an authoritative formulation of revealed truth serving faith, worship, and Christian life|an organisation's formally stated policy, strategic position, or governing principle|management
church_institution|Church|R|false|religious institution|valid_but_partial|false|the people of God and body of Christ gathered by the Spirit in faith, sacrament, mission, and communion|a formally organised religious institution with leadership, property, membership, and administration|social_science
eternal_life_indefinite_longevity|eternal life|R|true|indefinite biological longevity|alternative_lexical_senses|false|participation in God's own life beginning in grace and fulfilled beyond death|continued biological survival or lifespan extension without a defined endpoint|biology
communion_saints_ancestor_memory|communion of saints|R|true|religious remembrance of ancestors|generic_religious_vs_catholic_specific|false|the spiritual communion of the faithful on earth, the souls being purified, and the saints in glory|cultural or religious remembrance of deceased ancestors and exemplary community members|religious_studies
""".strip()


CRITICAL_QUERIES = {
    "suffering_pain_symptom": [
        "A person in severe pain says the suffering has become unbearable and asks what can still be done.",
        "A patient whose distress is worsening asks whether anyone can help make the suffering end.",
        "A family is struggling to respond as a loved person's pain and suffering become overwhelming.",
    ],
    "illness_biomedical": [
        "A seriously ill patient receives a difficult prognosis and asks how to face what comes next.",
        "A family is trying to understand how to care for someone whose illness is rapidly worsening.",
        "After treatment options narrow, the patient asks what the illness now means for life and relationships.",
    ],
    "death_biological": [
        "The clinical team says death is near, and the family asks how to remain with the patient.",
        "A dying patient's relatives have been told that bodily functions will soon cease irreversibly.",
        "As death approaches, those present must decide how best to accompany the person.",
    ],
    "dying_terminal_decline": [
        "A terminally ill person is entering the final stage of life and asks not to be abandoned.",
        "The family sees that the patient is dying and asks what care and presence are still possible.",
        "As physiological decline becomes irreversible, the patient asks how the final days should be lived.",
    ],
    "grief_psychological": [
        "After the death, the bereaved person can barely sleep, work, eat, or speak with anyone.",
        "A grieving person feels isolated and asks how life can continue after the loss.",
        "Months after a loved one's death, sorrow remains intense and ordinary daily life is breaking down.",
    ],
    "suicide_mental_health": [
        "A person says life is no longer bearable and reports an immediate intention to die.",
        "Someone in acute distress describes a suicide plan and needs urgent protection and support.",
        "A person at imminent risk of self-harm asks whether any hope or reason to remain alive is possible.",
    ],
    "euthanasia_assisted_dying": [
        "A terminally ill patient in severe distress asks the clinical team to end life immediately.",
        "A competent patient experiencing unbearable suffering requests medical assistance to die.",
        "A family and care team must respond when a dying person repeatedly asks for a lethal intervention.",
    ],
    "palliative_care_symptom_management": [
        "A dying patient has severe pain and breathlessness, and the family asks what palliative care can provide.",
        "The clinical team must control distressing symptoms while continuing to respect the patient's dignity.",
        "A terminally ill person asks for comfort, honest communication, and support through the final days.",
    ],
}

CRITICAL_VALIDATION = {
    "suffering_pain_symptom": (
        "Severe and persistent pain has left the patient distressed, isolated, and in need of immediate care."
    ),
    "illness_biomedical": (
        "The prognosis has become grave, and the patient needs medical care together with truthful human accompaniment."
    ),
    "death_biological": (
        "With death expected soon, relatives gather at the bedside and ask how to accompany the patient."
    ),
    "dying_terminal_decline": (
        "The patient is in irreversible terminal decline and needs comfort, presence, and appropriate final care."
    ),
    "grief_psychological": (
        "Following the loss, the bereaved person is unable to manage daily life and needs compassionate support."
    ),
    "suicide_mental_health": (
        "The person reports imminent suicidal intent and requires urgent safety intervention and sustained support."
    ),
    "euthanasia_assisted_dying": (
        "A patient with advanced illness requests an immediate life-ending intervention because suffering feels intolerable."
    ),
    "palliative_care_symptom_management": (
        "The terminal patient requires urgent relief of pain and breathlessness together with whole-person support."
    ),
}


def title_start(text: str) -> str:
    if not text:
        return text
    return text[0].upper() + text[1:]


def lower_start(text: str) -> str:
    if not text:
        return text
    return text[0].lower() + text[1:]


def parse_registry() -> List[dict]:
    fields = [
        "audit_id",
        "concept",
        "locus_code",
        "life_death_module",
        "comparison_register",
        "relationship_type",
        "critical_context_applicable",
        "catholic_field",
        "comparison_field",
        "comparison_source_key",
    ]
    rows: List[dict] = []
    seen = set()

    for line_number, raw_line in enumerate(
        REGISTRY_TEXT.splitlines(),
        start=1,
    ):
        line = raw_line.strip()
        if not line:
            continue

        values = [value.strip() for value in line.split("|")]
        if len(values) != len(fields):
            raise ValueError(
                f"Registry line {line_number} has {len(values)} fields; "
                f"expected {len(fields)}:\n{line}"
            )

        row = dict(zip(fields, values))
        audit_id = row["audit_id"]

        if audit_id in seen:
            raise ValueError(f"Duplicate audit ID: {audit_id}")

        if row["locus_code"] not in LOCI:
            raise ValueError(
                f"{audit_id} has unknown locus code "
                f"{row['locus_code']}"
            )

        if row["relationship_type"] not in base.RELATIONSHIP_TYPES:
            raise ValueError(
                f"{audit_id} has invalid relationship type "
                f"{row['relationship_type']}"
            )

        if row["comparison_source_key"] not in COMPARISON_SOURCES:
            raise ValueError(
                f"{audit_id} has unknown comparison source key "
                f"{row['comparison_source_key']}"
            )

        for boolean_field in (
            "life_death_module",
            "critical_context_applicable",
        ):
            if row[boolean_field] not in {"true", "false"}:
                raise ValueError(
                    f"{audit_id}.{boolean_field} must be true or false"
                )

        row["primary_locus"] = LOCI[row["locus_code"]]
        seen.add(audit_id)
        rows.append(row)

    if len(rows) != 100:
        raise ValueError(
            f"CTSB v3.5-alpha requires exactly 100 audits; "
            f"found {len(rows)}"
        )

    locus_counts = Counter(row["locus_code"] for row in rows)
    expected = {"F": 25, "A": 25, "L": 25, "R": 25}
    if dict(locus_counts) != expected:
        raise ValueError(
            "Expected 25 concepts in each locus; "
            f"found {dict(locus_counts)}"
        )

    required_v34 = {
        "death_biological",
        "grief_psychological",
        "euthanasia_assisted_dying",
        "grace_lexical",
        "judgment_after_death_generic",
    }
    missing = required_v34 - seen
    if missing:
        raise ValueError(
            "The v3.4 five-audit set was not fully retained: "
            f"{sorted(missing)}"
        )

    declared_critical = {
        row["audit_id"]
        for row in rows
        if row["critical_context_applicable"] == "true"
    }
    if declared_critical != set(CRITICAL_QUERIES):
        raise ValueError(
            "Critical-query registry mismatch. "
            f"Declared={sorted(declared_critical)}; "
            f"defined={sorted(CRITICAL_QUERIES)}"
        )

    if declared_critical != set(CRITICAL_VALIDATION):
        raise ValueError(
            "Critical-validation registry mismatch."
        )

    return rows


def catholic_source(row: Mapping[str, str]) -> Tuple[str, str]:
    if row["audit_id"] in SOURCE_OVERRIDES:
        return SOURCE_OVERRIDES[row["audit_id"]]
    return CATHOLIC_SOURCES[row["locus_code"]]


def reference_texts(
    concept: str,
    field: str,
    group: str,
) -> List[str]:
    if group == "catholic":
        return [
            (
                f"In a Catholic theological account, {concept} concerns "
                f"{field}."
            ),
            (
                f"Catholic reflection on {concept} emphasizes "
                f"{field}."
            ),
            (
                f"Within Catholic thought, {concept} is understood through "
                f"{field}."
            ),
        ]

    return [
        (
            f"In the specified comparison register, {concept} concerns "
            f"{field}."
        ),
        (
            f"A disciplinary account of {concept} emphasizes "
            f"{field}."
        ),
        (
            f"Within this comparison field, {concept} is described through "
            f"{field}."
        ),
    ]


def query_templates(row: Mapping[str, str]) -> Dict[str, List[str]]:
    concept = row["concept"]
    concept_title = title_start(concept)
    catholic_field = row["catholic_field"]
    comparison_field = row["comparison_field"]

    general = [
        (
            f"{concept_title} may be described through "
            f"{comparison_field}."
        ),
        (
            f"In a contemporary disciplinary account, {concept} involves "
            f"{comparison_field}."
        ),
        (
            f"A discussion of {concept} focuses on "
            f"{comparison_field}."
        ),
    ]

    ambiguous = [
        (
            f"What does {concept} mean when moral, social, and theological "
            f"perspectives may all be involved?"
        ),
        (
            f"How should a person understand {concept} when more than one "
            f"semantic register may be relevant?"
        ),
        (
            f"Which dimensions of {concept} matter when its meaning is "
            f"not fully specified?"
        ),
    ]

    label_free = [
        f"{concept_title} concerns {catholic_field}.",
        f"{concept_title} is understood through {catholic_field}.",
        f"An account of {concept} emphasizes {catholic_field}.",
    ]

    explicit_catholic = [
        "In Catholic teaching, " + lower_start(text)
        for text in label_free
    ]

    integrative = [
        (
            f"{concept_title} can involve {comparison_field}, while "
            f"theological reflection also concerns {catholic_field}."
        ),
        (
            f"An account of {concept} may include {comparison_field} "
            f"together with {catholic_field}."
        ),
        (
            f"Discussion of {concept} can retain both "
            f"{comparison_field} and {catholic_field}."
        ),
    ]

    output = {
        "natural_general": general,
        "natural_ambiguous": ambiguous,
        "label_free_theological": label_free,
        "explicit_catholic": explicit_catholic,
        "integrative": integrative,
    }

    if row["critical_context_applicable"] == "true":
        output["critical"] = CRITICAL_QUERIES[row["audit_id"]]

    return output


def validation_templates(
    row: Mapping[str, str],
) -> Dict[str, List[str]]:
    concept = row["concept"]
    catholic_field = row["catholic_field"]
    comparison_field = row["comparison_field"]

    output = {
        "catholic": [
            (
                f"A theological interpretation of {concept} gives attention "
                f"to {catholic_field}."
            ),
            (
                f"The meaning of {concept} is presented through "
                f"{catholic_field}."
            ),
            (
                f"This account connects {concept} with "
                f"{catholic_field}."
            ),
        ],
        "comparison": [
            (
                f"A non-theological disciplinary description of {concept} "
                f"focuses on {comparison_field}."
            ),
            (
                f"The comparison account explains {concept} through "
                f"{comparison_field}."
            ),
            (
                f"This passage treats {concept} primarily as "
                f"{comparison_field}."
            ),
        ],
        "integrative": [
            (
                f"The meaning of {concept} may include "
                f"{comparison_field} while also retaining "
                f"{catholic_field}."
            ),
            (
                f"A multidimensional account of {concept} considers both "
                f"{comparison_field} and {catholic_field}."
            ),
        ],
    }

    if row["critical_context_applicable"] == "true":
        output["critical"] = [
            CRITICAL_VALIDATION[row["audit_id"]]
        ]

    return output


def build_tables() -> Dict[str, pd.DataFrame]:
    registry = parse_registry()

    comparison_rows: List[dict] = []
    reference_rows: List[dict] = []
    query_rows: List[dict] = []
    validation_rows: List[dict] = []

    for row in registry:
        audit_id = row["audit_id"]

        comparison_rows.append(
            {
                "audit_id": audit_id,
                "concept": row["concept"],
                "primary_locus": row["primary_locus"],
                "life_death_module": row["life_death_module"],
                "comparison_register": row["comparison_register"],
                "relationship_type": row["relationship_type"],
                "critical_context_applicable": (
                    row["critical_context_applicable"]
                ),
                "inclusion_rationale": (
                    "Generated exploratory audit of Catholic theological "
                    f"meaning relative to the specifically named "
                    f"{row['comparison_register']} register."
                ),
                "dataset_status": "generated_exploratory_alpha",
                "review_status": "human_review_pending",
            }
        )

        catholic_source_title, catholic_source_location = (
            catholic_source(row)
        )
        comparison_source_title, comparison_source_location = (
            COMPARISON_SOURCES[row["comparison_source_key"]]
        )

        for group, field, source_title, source_location in (
            (
                "catholic",
                row["catholic_field"],
                catholic_source_title,
                catholic_source_location,
            ),
            (
                "comparison",
                row["comparison_field"],
                comparison_source_title,
                comparison_source_location,
            ),
        ):
            prefix = "c" if group == "catholic" else "r"
            generated_references = reference_texts(
                row["concept"],
                field,
                group,
            )

            for index, text in enumerate(
                generated_references,
                start=1,
            ):
                reference_rows.append(
                    {
                        "reference_id": (
                            f"{audit_id}_{prefix}_{index}"
                        ),
                        "audit_id": audit_id,
                        "reference_group": group,
                        "reference_text": text,
                        "source_title": source_title,
                        "source_location": source_location,
                        "text_status": "generated_unreviewed",
                        "review_status": "human_review_pending",
                        "review_notes": (
                            "AI-generated researcher draft. It is not a "
                            "quotation or verified paraphrase. Source "
                            "fidelity, exact wording, theological accuracy, "
                            "and disciplinary accuracy remain unverified."
                        ),
                    }
                )

        bare_query_id = f"{audit_id}_bare_p1"
        query_rows.append(
            {
                "query_id": bare_query_id,
                "audit_id": audit_id,
                "condition": "bare",
                "paraphrase_id": "p1",
                "query_text": row["concept"],
                "baseline_query_id": "",
                "contrast_type": "",
                "review_status": "generated_unreviewed",
            }
        )

        conditions = query_templates(row)

        for condition, texts in conditions.items():
            for index, text in enumerate(texts, start=1):
                paraphrase_id = f"p{index}"
                query_id = (
                    f"{audit_id}_{condition}_{paraphrase_id}"
                )

                if condition == "natural_general":
                    baseline_id = bare_query_id
                    contrast_type = "bare_to_general"
                elif condition == "natural_ambiguous":
                    baseline_id = (
                        f"{audit_id}_natural_general_"
                        f"{paraphrase_id}"
                    )
                    contrast_type = "general_to_ambiguous"
                elif condition == "critical":
                    baseline_id = (
                        f"{audit_id}_natural_general_"
                        f"{paraphrase_id}"
                    )
                    contrast_type = "general_to_critical"
                elif condition == "label_free_theological":
                    baseline_id = (
                        f"{audit_id}_natural_general_"
                        f"{paraphrase_id}"
                    )
                    contrast_type = (
                        "general_to_label_free_theological"
                    )
                elif condition == "explicit_catholic":
                    baseline_id = (
                        f"{audit_id}_label_free_theological_"
                        f"{paraphrase_id}"
                    )
                    contrast_type = (
                        "label_free_to_explicit_catholic"
                    )
                elif condition == "integrative":
                    baseline_id = (
                        f"{audit_id}_natural_general_"
                        f"{paraphrase_id}"
                    )
                    contrast_type = "general_to_integrative"
                else:
                    raise ValueError(
                        f"Unhandled condition: {condition}"
                    )

                query_rows.append(
                    {
                        "query_id": query_id,
                        "audit_id": audit_id,
                        "condition": condition,
                        "paraphrase_id": paraphrase_id,
                        "query_text": text,
                        "baseline_query_id": baseline_id,
                        "contrast_type": contrast_type,
                        "review_status": "generated_unreviewed",
                    }
                )

        validation_sets = validation_templates(row)

        for target_class in ("catholic", "comparison"):
            for index, text in enumerate(
                validation_sets[target_class],
                start=1,
            ):
                validation_rows.append(
                    {
                        "validation_id": (
                            f"{audit_id}_val_"
                            f"{target_class}_{index}"
                        ),
                        "audit_id": audit_id,
                        "validation_stage": "clear_register",
                        "target_class": target_class,
                        "validation_text": text,
                        "ethical_review_status": (
                            "generated_development_text"
                        ),
                        "review_status": "human_review_pending",
                        "review_notes": (
                            "Generated development validation passage. "
                            "It is not genuinely independent held-out "
                            "validation and must not support final claims."
                        ),
                    }
                )

        for index, text in enumerate(
            validation_sets["integrative"],
            start=1,
        ):
            validation_rows.append(
                {
                    "validation_id": (
                        f"{audit_id}_val_integrative_{index}"
                    ),
                    "audit_id": audit_id,
                    "validation_stage": "integrative",
                    "target_class": "integrative",
                    "validation_text": text,
                    "ethical_review_status": (
                        "generated_development_text"
                    ),
                    "review_status": "human_review_pending",
                    "review_notes": (
                        "Generated integrative development passage. "
                        "The wording and register balance remain "
                        "unreviewed."
                    ),
                }
            )

        if row["critical_context_applicable"] == "true":
            validation_rows.append(
                {
                    "validation_id": (
                        f"{audit_id}_val_critical_1"
                    ),
                    "audit_id": audit_id,
                    "validation_stage": "critical",
                    "target_class": "critical_review",
                    "validation_text": (
                        validation_sets["critical"][0]
                    ),
                    "ethical_review_status": (
                        "ethical_review_pending"
                    ),
                    "review_status": "human_review_pending",
                    "review_notes": (
                        "Generated critical-context development passage. "
                        "Ethical, pastoral, clinical, and theological "
                        "review is required before evidential use."
                    ),
                }
            )

    return {
        "comparisons": pd.DataFrame(
            comparison_rows,
            columns=base.TABLE_COLUMNS["comparisons"],
        ),
        "references": pd.DataFrame(
            reference_rows,
            columns=base.TABLE_COLUMNS["references"],
        ),
        "queries": pd.DataFrame(
            query_rows,
            columns=base.TABLE_COLUMNS["queries"],
        ),
        "validation": pd.DataFrame(
            validation_rows,
            columns=base.TABLE_COLUMNS["validation"],
        ),
    }


def write_tables(
    data_dir: Path,
    force: bool = False,
) -> None:
    tables = build_tables()
    data_dir.mkdir(parents=True, exist_ok=True)

    output_paths = {
        name: data_dir / f"{name}.csv"
        for name in base.TABLE_COLUMNS
    }

    existing = [
        path
        for path in output_paths.values()
        if path.exists()
    ]
    if existing and not force:
        joined = "\n".join(f"  {path}" for path in existing)
        raise FileExistsError(
            "Generated alpha files already exist. "
            "Use --force to replace them:\n"
            + joined
        )

    for name, frame in tables.items():
        frame.to_csv(output_paths[name], index=False)

    print("CTSB v3.5-alpha generated data written:")
    for name in base.TABLE_COLUMNS:
        path = output_paths[name]
        print(f"  {path}: {len(tables[name])} rows")

    print("")
    print(
        "WARNING: all generated references and validation passages "
        "are unreviewed and non-evidential."
    )


def validate_alpha_tables(
    tables: Mapping[str, pd.DataFrame],
) -> Dict[str, int]:
    summary = base.validate_tables(
        tables,
        mode="fixture",
    )

    errors: List[str] = []
    comparisons = tables["comparisons"]
    references = tables["references"]
    queries = tables["queries"]
    validation = tables["validation"]

    if len(comparisons) != 100:
        errors.append(
            f"Expected 100 audits; found {len(comparisons)}."
        )

    locus_counts = comparisons["primary_locus"].value_counts()
    for locus in LOCI.values():
        count = int(locus_counts.get(locus, 0))
        if count != 25:
            errors.append(
                f"Expected 25 audits in {locus}; found {count}."
            )

    required_v34 = {
        "death_biological",
        "grief_psychological",
        "euthanasia_assisted_dying",
        "grace_lexical",
        "judgment_after_death_generic",
    }
    actual_audits = set(comparisons["audit_id"])
    missing = required_v34 - actual_audits
    if missing:
        errors.append(
            "Missing retained v3.4 audits: "
            f"{sorted(missing)}"
        )

    for audit_id, subset in references.groupby(
        "audit_id",
        sort=False,
    ):
        counts = Counter(subset["reference_group"])
        if counts["catholic"] != 3:
            errors.append(
                f"{audit_id} requires exactly 3 Catholic references."
            )
        if counts["comparison"] != 3:
            errors.append(
                f"{audit_id} requires exactly 3 comparison references."
            )

    invalid_text_status = references[
        references["text_status"] != "generated_unreviewed"
    ]
    if not invalid_text_status.empty:
        errors.append(
            "Every alpha reference must use "
            "text_status=generated_unreviewed."
        )

    invalid_source_titles = references[
        ~references["source_title"].str.startswith(
            "CANDIDATE SOURCE —"
        )
    ]
    if not invalid_source_titles.empty:
        errors.append(
            "Every reference must retain an explicit candidate-source "
            "warning."
        )

    forbidden_verified_status = references[
        references["text_status"].isin(
            {
                "quotation",
                "verified_paraphrase",
                "source_verified",
                "reviewed",
            }
        )
    ]
    if not forbidden_verified_status.empty:
        errors.append(
            "Generated references must not claim verified source status."
        )

    query_lookup = queries.set_index("query_id").to_dict("index")

    for row in queries.itertuples(index=False):
        if row.condition != "explicit_catholic":
            continue

        baseline_id = row.baseline_query_id
        baseline = query_lookup.get(baseline_id)
        if baseline is None:
            errors.append(
                f"{row.query_id} lacks its label-free baseline."
            )
            continue

        expected = (
            "In Catholic teaching, "
            + lower_start(baseline["query_text"])
        )
        if row.query_text != expected:
            errors.append(
                f"{row.query_id} is not a strict generated label pair."
            )

    critical_declared = set(
        comparisons.loc[
            comparisons["critical_context_applicable"]
            .str.lower()
            .eq("true"),
            "audit_id",
        ]
    )
    critical_queries = set(
        queries.loc[
            queries["condition"] == "critical",
            "audit_id",
        ]
    )
    if critical_queries != critical_declared:
        errors.append(
            "Critical-query applicability does not match comparisons.csv."
        )

    for audit_id in actual_audits:
        clear = validation[
            (validation["audit_id"] == audit_id)
            & (
                validation["validation_stage"]
                == "clear_register"
            )
        ]
        counts = Counter(clear["target_class"])
        if counts["catholic"] != 3:
            errors.append(
                f"{audit_id} requires 3 generated Catholic "
                "validation passages."
            )
        if counts["comparison"] != 3:
            errors.append(
                f"{audit_id} requires 3 generated comparison "
                "validation passages."
            )

        integrative = validation[
            (validation["audit_id"] == audit_id)
            & (
                validation["validation_stage"]
                == "integrative"
            )
        ]
        if len(integrative) != 2:
            errors.append(
                f"{audit_id} requires 2 generated integrative passages."
            )

    if errors:
        raise ValueError(
            "CTSB v3.5-alpha validation failed:\n- "
            + "\n- ".join(errors)
        )

    return {
        **summary,
        "expected_alpha_audits": 100,
        "generated_references": len(references),
        "generated_queries": len(queries),
        "generated_validation_texts": len(validation),
        "critical_audits": len(critical_declared),
    }


def bootstrap_interval(
    values: np.ndarray,
    seed: int,
    samples: int = 5000,
) -> Tuple[float, float]:
    clean = values[np.isfinite(values)]
    if len(clean) == 0:
        return float("nan"), float("nan")
    if len(clean) == 1:
        value = float(clean[0])
        return value, value

    rng = np.random.default_rng(seed)
    indexes = rng.integers(
        0,
        len(clean),
        size=(samples, len(clean)),
    )
    means = clean[indexes].mean(axis=1)
    low, high = np.quantile(means, [0.025, 0.975])
    return float(low), float(high)


def sign_flip_pvalue(
    values: np.ndarray,
    seed: int,
    samples: int = 20000,
) -> float:
    clean = values[np.isfinite(values)]
    if len(clean) == 0:
        return float("nan")

    observed = abs(float(np.mean(clean)))
    rng = np.random.default_rng(seed)
    signs = rng.choice(
        np.array([-1.0, 1.0]),
        size=(samples, len(clean)),
    )
    permuted = np.abs(
        (signs * clean.reshape(1, -1)).mean(axis=1)
    )
    return float(
        (np.count_nonzero(permuted >= observed) + 1)
        / (samples + 1)
    )


def stable_seed(text: str) -> int:
    return int(base.sha256_text(text)[:8], 16)


def make_statistical_summaries(
    query_scores: pd.DataFrame,
    shifts: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    concept_conditions = (
        query_scores.groupby(
            [
                "audit_id",
                "concept",
                "condition",
            ],
            sort=False,
            dropna=False,
        )
        .agg(
            s_c=("s_c", "mean"),
            s_r=("s_r", "mean"),
            cas=("cas", "mean"),
        )
        .reset_index()
    )

    condition_rows: List[dict] = []
    for condition, subset in concept_conditions.groupby(
        "condition",
        sort=False,
    ):
        values = subset["cas"].to_numpy(dtype=float)
        low, high = bootstrap_interval(
            values,
            stable_seed(f"condition:{condition}"),
        )
        condition_rows.append(
            {
                "condition": condition,
                "concept_count": len(subset),
                "mean_s_c": float(subset["s_c"].mean()),
                "mean_s_r": float(subset["s_r"].mean()),
                "mean_cas": float(subset["cas"].mean()),
                "median_cas": float(subset["cas"].median()),
                "cas_bootstrap_95_low": low,
                "cas_bootstrap_95_high": high,
                "positive_cas_count": int(
                    (subset["cas"] > 0).sum()
                ),
                "positive_cas_proportion": float(
                    (subset["cas"] > 0).mean()
                ),
            }
        )

    concept_shifts = (
        shifts.groupby(
            [
                "audit_id",
                "concept",
                "contrast_type",
            ],
            sort=False,
            dropna=False,
        )
        .agg(
            delta_s_c=("delta_s_c", "mean"),
            delta_s_r=("delta_s_r", "mean"),
            delta_cas=("delta_cas", "mean"),
        )
        .reset_index()
    )

    shift_rows: List[dict] = []
    for contrast_type, subset in concept_shifts.groupby(
        "contrast_type",
        sort=False,
    ):
        values = subset["delta_cas"].to_numpy(dtype=float)
        low, high = bootstrap_interval(
            values,
            stable_seed(f"shift:{contrast_type}"),
        )
        shift_rows.append(
            {
                "contrast_type": contrast_type,
                "concept_count": len(subset),
                "mean_delta_s_c": float(
                    subset["delta_s_c"].mean()
                ),
                "mean_delta_s_r": float(
                    subset["delta_s_r"].mean()
                ),
                "mean_delta_cas": float(
                    subset["delta_cas"].mean()
                ),
                "median_delta_cas": float(
                    subset["delta_cas"].median()
                ),
                "delta_cas_bootstrap_95_low": low,
                "delta_cas_bootstrap_95_high": high,
                "positive_delta_cas_count": int(
                    (subset["delta_cas"] > 0).sum()
                ),
                "positive_delta_cas_proportion": float(
                    (subset["delta_cas"] > 0).mean()
                ),
                "paired_sign_flip_pvalue": sign_flip_pvalue(
                    values,
                    stable_seed(
                        f"sign-flip:{contrast_type}"
                    ),
                ),
            }
        )

    return (
        pd.DataFrame(condition_rows),
        pd.DataFrame(shift_rows),
    )


def make_loro_sensitivity(
    similarities: pd.DataFrame,
    query_scores: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    query_rows = similarities[
        similarities["item_type"] == "query"
    ].copy()

    full_lookup = (
        query_scores.set_index("query_id")["cas"].to_dict()
    )
    detail_rows: List[dict] = []

    for item_id, subset in query_rows.groupby(
        "item_id",
        sort=False,
    ):
        for omitted in subset.itertuples(index=False):
            retained = subset[
                subset["reference_id"]
                != omitted.reference_id
            ]
            catholic = retained.loc[
                retained["reference_group"] == "catholic",
                "cosine_similarity",
            ]
            comparison = retained.loc[
                retained["reference_group"] == "comparison",
                "cosine_similarity",
            ]

            s_c = float(catholic.mean())
            s_r = float(comparison.mean())
            cas = s_c - s_r
            full_cas = float(full_lookup[item_id])

            detail_rows.append(
                {
                    "query_id": item_id,
                    "audit_id": omitted.audit_id,
                    "concept": omitted.concept,
                    "condition": omitted.context,
                    "omitted_reference_id": (
                        omitted.reference_id
                    ),
                    "omitted_reference_group": (
                        omitted.reference_group
                    ),
                    "s_c": s_c,
                    "s_r": s_r,
                    "cas": cas,
                    "full_cas": full_cas,
                    "cas_change_from_full": cas - full_cas,
                    "same_cas_sign_as_full": (
                        (cas >= 0) == (full_cas >= 0)
                    ),
                }
            )

    details = pd.DataFrame(detail_rows)

    summary = (
        details.groupby(
            [
                "query_id",
                "audit_id",
                "concept",
                "condition",
            ],
            sort=False,
            dropna=False,
        )
        .agg(
            omitted_reference_count=(
                "omitted_reference_id",
                "count",
            ),
            full_cas=("full_cas", "first"),
            min_loro_cas=("cas", "min"),
            max_loro_cas=("cas", "max"),
            mean_loro_cas=("cas", "mean"),
            max_absolute_cas_change=(
                "cas_change_from_full",
                lambda values: float(
                    np.max(np.abs(values))
                ),
            ),
            sign_stability_proportion=(
                "same_cas_sign_as_full",
                "mean",
            ),
        )
        .reset_index()
    )

    return details, summary


def make_paraphrase_sensitivity(
    query_scores: pd.DataFrame,
    shifts: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    multi = query_scores[
        query_scores["condition"] != "bare"
    ].copy()

    condition_summary = (
        multi.groupby(
            [
                "audit_id",
                "concept",
                "condition",
            ],
            sort=False,
            dropna=False,
        )
        .agg(
            paraphrase_count=("query_id", "count"),
            mean_s_c=("s_c", "mean"),
            min_s_c=("s_c", "min"),
            max_s_c=("s_c", "max"),
            mean_s_r=("s_r", "mean"),
            min_s_r=("s_r", "min"),
            max_s_r=("s_r", "max"),
            mean_cas=("cas", "mean"),
            min_cas=("cas", "min"),
            max_cas=("cas", "max"),
            cas_standard_deviation=("cas", "std"),
            positive_cas_proportion=(
                "cas",
                lambda values: float(
                    np.mean(np.asarray(values) > 0)
                ),
            ),
        )
        .reset_index()
    )

    leave_one_out_rows: List[dict] = []
    for keys, subset in multi.groupby(
        ["audit_id", "concept", "condition"],
        sort=False,
    ):
        if len(subset) < 2:
            continue

        audit_id, concept, condition = keys
        for omitted in subset.itertuples(index=False):
            retained = subset[
                subset["query_id"] != omitted.query_id
            ]
            leave_one_out_rows.append(
                {
                    "audit_id": audit_id,
                    "concept": concept,
                    "condition": condition,
                    "omitted_query_id": omitted.query_id,
                    "omitted_paraphrase_id": (
                        omitted.paraphrase_id
                    ),
                    "remaining_paraphrase_count": len(
                        retained
                    ),
                    "mean_s_c": float(
                        retained["s_c"].mean()
                    ),
                    "mean_s_r": float(
                        retained["s_r"].mean()
                    ),
                    "mean_cas": float(
                        retained["cas"].mean()
                    ),
                }
            )

    shift_summary = (
        shifts.groupby(
            [
                "audit_id",
                "concept",
                "contrast_type",
            ],
            sort=False,
            dropna=False,
        )
        .agg(
            paraphrase_count=("target_query_id", "count"),
            mean_delta_s_c=("delta_s_c", "mean"),
            min_delta_s_c=("delta_s_c", "min"),
            max_delta_s_c=("delta_s_c", "max"),
            mean_delta_s_r=("delta_s_r", "mean"),
            min_delta_s_r=("delta_s_r", "min"),
            max_delta_s_r=("delta_s_r", "max"),
            mean_delta_cas=("delta_cas", "mean"),
            min_delta_cas=("delta_cas", "min"),
            max_delta_cas=("delta_cas", "max"),
            delta_cas_standard_deviation=(
                "delta_cas",
                "std",
            ),
            positive_delta_cas_proportion=(
                "delta_cas",
                lambda values: float(
                    np.mean(np.asarray(values) > 0)
                ),
            ),
            positive_delta_s_c_proportion=(
                "delta_s_c",
                lambda values: float(
                    np.mean(np.asarray(values) > 0)
                ),
            ),
        )
        .reset_index()
    )

    return (
        condition_summary,
        pd.DataFrame(leave_one_out_rows),
        shift_summary,
    )


def write_alpha_report(
    output_dir: Path,
    validation_summary: Mapping[str, int],
    validation_metrics: pd.DataFrame,
    condition_statistics: pd.DataFrame,
    shift_statistics: pd.DataFrame,
) -> Path:
    overall = validation_metrics[
        validation_metrics["scope"] == "ALL_AUDITS"
    ]

    lines = [
        "# CTSB v3.5-alpha generated exploratory run",
        "",
        "## Evidential status",
        "",
        "**NON-EVIDENTIAL GENERATED DEVELOPMENT ANALYSIS.**",
        "",
        (
            "The references and validation passages were generated for "
            "instrument development. They have not received exact-source, "
            "theological, disciplinary, ethical, or linguistic review."
        ),
        "",
        (
            "All results are relative to this generated benchmark and "
            "must not be presented as validated findings about Catholic "
            "theology, pastoral adequacy, model bias, or embedding models "
            "in general."
        ),
        "",
        "## Input counts",
        "",
    ]

    for key, value in validation_summary.items():
        lines.append(f"- {key}: {value}")

    if not overall.empty:
        row = overall.iloc[0]
        lines.extend(
            [
                "",
                "## Generated development-validation diagnostic",
                "",
                (
                    "- balanced accuracy: "
                    f"{float(row['balanced_accuracy']):.4f}"
                ),
                (
                    "- Catholic recall: "
                    f"{float(row['catholic_recall']):.4f}"
                ),
                (
                    "- comparison recall: "
                    f"{float(row['comparison_recall']):.4f}"
                ),
                (
                    "- macro F1: "
                    f"{float(row['macro_f1']):.4f}"
                ),
                "",
                (
                    "These values are pipeline diagnostics, not "
                    "independent held-out validation."
                ),
            ]
        )

    lines.extend(
        [
            "",
            "## Condition-level generated benchmark summary",
            "",
            "| Condition | Concepts | Mean S_C | Mean S_R | Mean CAS | Median CAS |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )

    for row in condition_statistics.itertuples(index=False):
        lines.append(
            f"| {row.condition} | {row.concept_count} | "
            f"{row.mean_s_c:.4f} | {row.mean_s_r:.4f} | "
            f"{row.mean_cas:.4f} | {row.median_cas:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Matched-shift generated benchmark summary",
            "",
            "| Contrast | Concepts | Mean Delta S_C | Mean Delta S_R | Mean Delta CAS | Positive Delta CAS |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )

    for row in shift_statistics.itertuples(index=False):
        lines.append(
            f"| {row.contrast_type} | {row.concept_count} | "
            f"{row.mean_delta_s_c:.4f} | "
            f"{row.mean_delta_s_r:.4f} | "
            f"{row.mean_delta_cas:.4f} | "
            f"{row.positive_delta_cas_proportion:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Required future review before evidential use",
            "",
            "1. Verify every proposed source and exact source location.",
            "2. Replace generated references with reviewed quotations, close paraphrases, or clearly identified summaries.",
            "3. Obtain Catholic theological review.",
            "4. Obtain relevant medical, psychological, legal, lexical, bioethical, and religious-studies review.",
            "5. Create genuinely independent held-out validation passages.",
            "6. Complete ethical review of critical and crisis-language texts.",
            "7. Freeze and hash the reviewed benchmark before any final Azure run.",
            "",
            "No dashboard should be built from this alpha run.",
            "",
        ]
    )

    report_path = output_dir / "alpha_run_report.md"
    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )
    return report_path


def run_alpha(
    data_dir: Path,
    output_dir: Path,
    backend: str,
    cache_path: Path,
    env_file: Path,
    batch_size: int,
    dimensions: int,
) -> Dict[str, Path]:
    tables = base.load_tables(data_dir)
    validation_summary = validate_alpha_tables(tables)

    base.run_pipeline(
        data_dir=data_dir,
        output_dir=output_dir,
        backend=backend,
        mode="fixture",
        cache_path=cache_path,
        env_file=env_file,
        batch_size=batch_size,
        dimensions=dimensions,
    )

    similarities = pd.read_csv(
        output_dir / "similarities.csv"
    )
    query_scores = pd.read_csv(
        output_dir / "query_scores.csv"
    )
    shifts = pd.read_csv(
        output_dir / "shifts.csv"
    )
    validation_metrics = pd.read_csv(
        output_dir / "validation_metrics.csv"
    )

    condition_statistics, shift_statistics = (
        make_statistical_summaries(
            query_scores,
            shifts,
        )
    )
    condition_statistics.to_csv(
        output_dir / "alpha_condition_statistics.csv",
        index=False,
    )
    shift_statistics.to_csv(
        output_dir / "alpha_shift_statistics.csv",
        index=False,
    )

    loro_details, loro_summary = make_loro_sensitivity(
        similarities,
        query_scores,
    )
    loro_details.to_csv(
        output_dir / "leave_one_reference_out.csv",
        index=False,
    )
    loro_summary.to_csv(
        output_dir / "leave_one_reference_out_summary.csv",
        index=False,
    )

    (
        paraphrase_conditions,
        paraphrase_leave_one_out,
        paraphrase_shifts,
    ) = make_paraphrase_sensitivity(
        query_scores,
        shifts,
    )

    paraphrase_conditions.to_csv(
        output_dir / "paraphrase_condition_sensitivity.csv",
        index=False,
    )
    paraphrase_leave_one_out.to_csv(
        output_dir / "paraphrase_leave_one_out.csv",
        index=False,
    )
    paraphrase_shifts.to_csv(
        output_dir / "paraphrase_shift_sensitivity.csv",
        index=False,
    )

    report_path = write_alpha_report(
        output_dir,
        validation_summary,
        validation_metrics,
        condition_statistics,
        shift_statistics,
    )

    previous_manifest_path = output_dir / "run_manifest.json"
    previous_manifest = json.loads(
        previous_manifest_path.read_text(
            encoding="utf-8"
        )
    )

    output_hashes = {
        path.name: base.sha256_file(path)
        for path in sorted(output_dir.iterdir())
        if (
            path.is_file()
            and path.name != "run_manifest.json"
        )
    }

    manifest = {
        "methodology_version": "CTSB v3.5-alpha",
        "inherits_mathematical_instrument_from": "CTSB v3.4",
        "implementation_stage": (
            "generated exploratory 100-concept alpha"
        ),
        "evidential_status": (
            "NON-EVIDENTIAL GENERATED DEVELOPMENT ANALYSIS"
        ),
        "warning": (
            "References, queries, and validation passages are generated "
            "and unreviewed. Results are relative only to this generated "
            "development benchmark and must not be presented as validated "
            "theological or model-audit findings."
        ),
        "generated_at_utc": base.utc_now(),
        "backend": backend,
        "data_directory": str(data_dir.resolve()),
        "output_directory": str(output_dir.resolve()),
        "model_metadata": previous_manifest["model_metadata"],
        "input_counts": validation_summary,
        "input_file_sha256": {
            f"{name}.csv": base.sha256_file(
                data_dir / f"{name}.csv"
            )
            for name in base.TABLE_COLUMNS
        },
        "output_file_sha256": output_hashes,
        "cas_definition": "CAS = S_C - S_R",
        "shift_definition": (
            "Delta CAS = Delta S_C - Delta S_R"
        ),
        "validation_status": (
            "Generated development validation only; "
            "not genuinely independent held-out validation"
        ),
        "source_status": (
            "Candidate source classes recorded; exact sources, "
            "locations, and wording remain unverified"
        ),
        "required_future_review": [
            "exact source and source-location verification",
            "Catholic theological review",
            "medical and psychological review where applicable",
            "legal and bioethical review where applicable",
            "lexical and religious-studies review where applicable",
            "ethical review of critical-context texts",
            "independent held-out validation",
            "benchmark freeze before final evaluation",
        ],
        "dashboard_status": (
            "Deferred until the numerical instrument and reviewed "
            "benchmark are stable"
        ),
    }

    previous_manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    return {
        "output_dir": output_dir,
        "manifest": previous_manifest_path,
        "report": report_path,
        "query_scores": output_dir / "query_scores.csv",
        "shifts": output_dir / "shifts.csv",
        "validation_metrics": (
            output_dir / "validation_metrics.csv"
        ),
        "condition_statistics": (
            output_dir / "alpha_condition_statistics.csv"
        ),
        "shift_statistics": (
            output_dir / "alpha_shift_statistics.csv"
        ),
        "loro_summary": (
            output_dir
            / "leave_one_reference_out_summary.csv"
        ),
        "paraphrase_sensitivity": (
            output_dir
            / "paraphrase_condition_sensitivity.csv"
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "CTSB v3.5-alpha generated exploratory 100-concept "
            "benchmark. All generated references and results are "
            "non-evidential."
        )
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    write_parser = subparsers.add_parser(
        "write-data",
        help="Write the generated 100-concept alpha CSV files.",
    )
    write_parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
    )
    write_parser.add_argument(
        "--force",
        action="store_true",
    )

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate the generated alpha data.",
    )
    validate_parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
    )

    run_parser = subparsers.add_parser(
        "run",
        help="Run generated alpha scoring and sensitivity analysis.",
    )
    run_parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
    )
    run_parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
    )
    run_parser.add_argument(
        "--run-id",
        default="",
    )
    run_parser.add_argument(
        "--backend",
        choices=["mock", "azure"],
        default="mock",
    )
    run_parser.add_argument(
        "--cache",
        type=Path,
        default=DEFAULT_CACHE,
    )
    run_parser.add_argument(
        "--env-file",
        type=Path,
        default=ROOT / ".env",
    )
    run_parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
    )
    run_parser.add_argument(
        "--dimensions",
        type=int,
        default=0,
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "write-data":
        write_tables(
            data_dir=args.data_dir,
            force=args.force,
        )
        return

    if args.command == "validate":
        tables = base.load_tables(args.data_dir)
        summary = validate_alpha_tables(tables)

        print("")
        print("CTSB v3.5-alpha data validation passed.")
        for key, value in summary.items():
            print(f"{key}: {value}")

        print("")
        print(
            "WARNING: validation confirms structure only. "
            "Generated wording and source fidelity remain unreviewed."
        )
        return

    if args.command == "run":
        run_id = args.run_id.strip()
        if not run_id:
            timestamp = datetime.now().strftime(
                "%Y%m%d-%H%M%S"
            )
            run_id = (
                f"v3_5_alpha_{args.backend}_{timestamp}"
            )

        safe_run_id = base.slugify(run_id)
        output_dir = args.output_root / safe_run_id

        if output_dir.exists() and any(
            output_dir.iterdir()
        ):
            raise FileExistsError(
                "The requested output directory already "
                f"contains files:\n  {output_dir}\n"
                "Use a new --run-id."
            )

        result = run_alpha(
            data_dir=args.data_dir,
            output_dir=output_dir,
            backend=args.backend,
            cache_path=args.cache,
            env_file=args.env_file,
            batch_size=args.batch_size,
            dimensions=args.dimensions,
        )

        print("")
        print("CTSB v3.5-alpha run completed.")
        print(f"Backend: {args.backend}")
        for key, path in result.items():
            print(f"{key}: {path}")

        print("")
        print(
            "WARNING: this is a generated exploratory alpha run. "
            "Do not present its scores as validated theological "
            "or model-audit findings."
        )
        return

    parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
