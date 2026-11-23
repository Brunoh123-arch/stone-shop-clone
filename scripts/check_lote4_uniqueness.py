# -*- coding: utf-8 -*-
import json

existing_text = open('js/videos-criadores-v3.js', 'r', encoding='utf-8').read()

candidates = [
    'kethhh____', 'sara_schutz', 'maju.inspira',
    'damiris.oliveira', 'thaynacolsani', 'duardolops',
    'guga_souza6', 'thedener95', 'ozeniscofertasshopee',
    'matheus.ferreirajf', 'lyzfranco7', 'vitorx.vieira',
    'mitransformada', 'rayssa_creator', 'natmarquesvi',
    'natybottini', 'elaniacreator', 'frannovaes05'
]

print("Total candidates:", len(candidates))
for u in candidates:
    if u.lower() in existing_text.lower():
        print("EXISTS in v3:", u)
    else:
        print("OK:", u)
