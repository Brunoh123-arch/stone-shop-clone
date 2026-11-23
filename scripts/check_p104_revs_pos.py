txt = open('pages/produto-104.html', encoding='utf-8').read()
end_revs = txt.find('<!-- SOBRE O PRODUTO -->')
if end_revs == -1:
    end_revs = txt.find('sobre-este-produto')
print(txt[end_revs-500:end_revs+500])
