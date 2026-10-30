# Webcrawler para agentes de IA

O scraper expõe `consultar_pagina(url)`, uma função que busca uma página e
retorna um dicionário com a URL, o status HTTP, o título e o texto extraído.
O texto é limitado a 10.000 caracteres para evitar enviar conteúdo excessivo
ao agente.

## Instalação e execução

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Execute o scraper diretamente:

```powershell
python scraper/scraper.py
python scraper/scraper.py https://books.toscrape.com/
```

## Uso como ferramenta de agente

Importe `consultar_pagina` e disponibilize-a como uma ferramenta no framework
de agente escolhido. `CONSULTAR_PAGINA_TOOL` contém uma definição de ferramenta
no formato de function calling; a integração com o agente deve encaminhar os
argumentos recebidos para a função e devolver o resultado ao modelo.

Exemplo de chamada local:

```python
from scraper.scraper import consultar_pagina

resultado = consultar_pagina("https://books.toscrape.com/")
print(resultado["title"])
```

Por segurança, somente `books.toscrape.com` é autorizado por padrão. Para
permitir outro domínio, passe uma coleção de domínios explicitamente:

```python
resultado = consultar_pagina(
    "https://example.com/",
    allowed_domains={"example.com"},
)
```

O scraper aceita apenas URLs HTTP/HTTPS, não envia credenciais e não segue
redirecionamentos. O projeto ainda não escolhe um framework de agente; a
definição da ferramenta pode precisar ser adaptada ao formato exigido por ele.

## Próximas etapas

Para chegar à ideia original do projeto, será necessário persistir resultados
ao longo do tempo. Com esse histórico, o agente poderá comparar preços,
resumir diferenças entre visitas e monitorar valores de produtos.
