# -*- coding: utf-8 -*-
import re

html = open('pages/produto-82.html', 'r', encoding='utf-8').read()
m_desc = re.search(r'id=["\']desc-content-text["\'][^>]*>([\s\S]*?)</div>', html)
if m_desc:
    print(m_desc.group(1))
