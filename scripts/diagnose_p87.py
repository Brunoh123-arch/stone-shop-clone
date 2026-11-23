# -*- coding: utf-8 -*-
import re

html = open('pages/produto-87.html', 'r', encoding='utf-8').read()

# Procura seções
print("Has creators-section:", 'creators-section' in html)
print("Has reviews:", 'review' in html.lower())

# Procura tags de reviews
cards = re.findall(r'class=["\']review-card["\']', html)
print("review-card count:", len(cards))

# Procura scripts importados
scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html)
print("Imported scripts in p87:", scripts)

# Procura se tem ratings
rating_m = re.findall(r'(\d+[\.,]\d+)\s*\/\s*5', html)
print("Ratings found:", rating_m)
