# Guia de consulta: Python e Django

Resumo dos comandos e conceitos aprendidos no tutorial. É atualizado no fim de cada passo.

---

## 1. Ambiente virtual e dependências (PowerShell)

| Comando | Para quê |
|---|---|
| `.venv\Scripts\activate` | Ativar o ambiente virtual (faz-se sempre que se abre um terminal novo) |
| `deactivate` | Desativar o ambiente |
| `pip install -r requirements.txt` | Instalar as dependências do projeto |
| `pip install <pacote>` | Instalar um pacote novo |
| `pip freeze > requirements.txt` | Atualizar a lista de dependências depois de instalar um pacote |
| `python ficheiro.py` | Correr um script |
| `python` | Abrir a consola interativa do Python (`exit()` para sair) |

---

## 2. Comandos do Django (`python manage.py ...`)

| Comando | Para quê |
|---|---|
| `runserver` | Arrancar o servidor de desenvolvimento em http://127.0.0.1:8000 (Ctrl+C para parar). Recarrega sozinho quando gravas um `.py` |
| `check` | Verificar se o projeto tem erros de configuração |
| `makemigrations` | **Gerar** os ficheiros de migration a partir dos modelos |
| `migrate` | **Aplicar** as migrations à base de dados |
| `showmigrations <app>` | Ver que migrations estão aplicadas (`[X]`) e por aplicar (`[ ]`) |
| `sqlmigrate <app> <n.º>` | Ver o SQL de uma migration, sem a executar (ex.: `sqlmigrate traceability 0001`) |
| `makemigrations --check --dry-run` | Confirmar se há alterações aos modelos por migrar, sem gerar nada |
| `shell` | Abrir a shell do Django, onde os modelos já vêm importados (`exit()` para sair) |
| `createsuperuser` | Criar um utilizador administrador |
| `startapp <nome>` | Criar uma app nova |

### Quando é preciso correr as migrations?

| Alteraste… | O que fazer |
|---|---|
| Campos de um modelo, os seus rótulos ou a `class Meta` | `makemigrations` + `migrate` |
| `admin.py`, `views.py`, métodos de um modelo, `settings.py` | Nada: basta gravar |

Na dúvida, corre `makemigrations`. Se não houver nada a gerar, aparece `No changes detected`.

### ⚠️ A regra das migrations

**Numa migration, ou mudas o nome de um campo, ou mudas o tipo. Nunca as duas coisas de uma vez.**
Se fizeres as duas, o Django não reconhece que é o mesmo campo: apaga a coluna (com os dados) e cria outra nova.
O sinal de alarme é ele pedir um valor por omissão ("It is impossible to add a non-nullable field…"). Nesse caso, sai com a opção `2` e faz a alteração em dois passos.

---

## 3. Python: o essencial

### Diferenças em relação a PHP/JS

| PHP / JS | Python |
|---|---|
| `$x = 1;` / `let x = 1;` | `x = 1` |
| `true`, `false`, `null` | `True`, `False`, `None` |
| `&&`, `\|\|`, `!` | `and`, `or`, `not` |
| `// comentário` | `# comentário` |
| `else if` | `elif` |
| `{ ... }` | `:` e indentação de 4 espaços (a indentação **é** a sintaxe) |
| `` `Peso ${w} kg` `` | `f'Peso {w} kg'` |
| `count($a)` / `a.length` | `len(a)` |
| `$a[] = $x` / `a.push(x)` | `a.append(x)` |
| `foreach ($a as $x)` | `for x in a:` |
| `foreach ($a as $k => $v)` | `for k, v in a.items():` |
| `x++` | `x += 1` (não existe `++`) |

### Texto e números
```python
f"{valor:.1f}"  # 1 casa decimal
f"{valor:.{n}f}"  # n casas decimais
400 <= peso <= 600  # comparações encadeadas
7 / 2  # 3.5 (divisão normal, dá sempre decimal)
7 // 2  # 3   (divisão inteira)
```

### Listas e dicionários
```python
animals = [{'breed': 'Angus', 'weight': 700}]
animals[0]          # o primeiro
animals[-1]         # o último
animal['breed']     # acesso a um dicionário (NÃO é animal.breed)
animal.get('xyz')   # devolve None se a chave não existir (em vez de dar erro)
sum(a['weight'] for a in animals)            # soma (generator expression)
sum(1 for a in animals if a['sex'] == 'M')   # contar os que cumprem uma condição
if not animals:     # verdadeiro se a lista estiver vazia
valor or 0          # se "valor" for None (ou vazio/zero), fica o que está à direita do "or"
```

### Sets (conjuntos)
```python
lots = {"T100", "T200", "T100"}
print(lots)         # {'T100', 'T200'}: sem repetidos, sem ordem
"T100" in lots      # True (pergunta muito rápida)
```
| Escrita | Tipo | Em JS |
|---|---|---|
| `[1, 2, 2]` | `list`: tem ordem e aceita repetidos | `[1, 2, 2]` |
| `{"a": 1}` | `dict`: chave → valor | `{ a: 1 }` |
| `{1, 2}` | `set`: sem ordem, sem repetidos | `new Set([1, 2])` |

- ⚠️ `{}` vazio é um **dict**; set vazio = `set()`.
- ⚠️ No f-string, as `{ }` são o "buraco" e desaparecem (`f"{x}"` → `60,0`). Fora dele, criam um set (`{x}` → `{'60,0'}`). Ver `aprender/revisao_2026-11-16.py`.
- Serve para tirar repetidos ou para verificar depressa "este código já foi lido?".

### Funções
```python
def format_weight(weight, unit="kg", decimals=1):  # valores por omissão
    return f"{weight:.{decimals}f} {unit}"


format_weight(537.25, decimals=0)  # argumento por nome
```
- As funções **devolvem** (`return`); quem as chama decide o que fazer com o valor.
- 2 linhas em branco entre funções e classes ao nível do ficheiro; 1 linha entre métodos dentro de uma classe.

### Classes
```python
class Animal:
    def __init__(self, breed):  # o construtor (__construct)
        self.breed = breed  # self = $this

    def __str__(self):  # __toString
        return self.breed


class SlaughterAnimal(Animal):  # herança (extends)
    def __init__(self, breed, carcass_weight):
        super().__init__(breed)  # parent::__construct
        self.carcass_weight = carcass_weight


cow = Animal("Angus")  # sem "new"
```
- O `self` é sempre uma instância da classe onde o método está escrito, e não o passas ao chamar o método.

### Módulos e imports
```python
from datetime import date  # 1.º: biblioteca padrão

from django.db import models  # 2.º: pacotes instalados

from .models import Animal  # 3.º: o teu código (o "." = o mesmo pacote)
```
- Cada ficheiro `.py` é um módulo; uma pasta com `__init__.py` é um pacote (uma app Django é um pacote).
- Importar um ficheiro executa-o todo. Código que só deve correr quando executas o ficheiro diretamente:
  ```python
  if __name__ == "__main__":
      ...
  ```
- Não uses nomes que tapam funções internas: `id`, `list`, `type`, `sum`, `input`…

### ⚠️ Arredondamento
O Python arredonda os casos ".5" para o **par** mais próximo: `round(536.5)` dá `536`.
Para pesos e dinheiro usa-se `Decimal`, criado a partir de **texto**:
```python
from decimal import Decimal, ROUND_HALF_UP

Decimal("536.5").quantize(Decimal("1"), rounding=ROUND_HALF_UP)  # 537
```

### `Decimal` vs `:.1f` vs `floatformat`: qual usar?
| Onde estás | O que queres | Escreves |
|---|---|---|
| `.py` | **Criar/calcular** um número exato | `Decimal('70')` (sempre entre aspas) |
| `.py` | **Mostrar** num texto | `f'{valor:.1f}'` → `37.5` (sempre com ponto) |
| `.html` | **Mostrar** na página | `{{ valor\|floatformat:1 }}` → `37,5` (vírgula em pt-pt) |

Duas perguntas: estou a **calcular** ou a **mostrar**? Estou num **`.py`** ou num **`.html`**?

### `None` e `is None`
O `None` é o "nada" do Python: o `null` do JS e o `NULL` do SQL.

| Python | JS | SQL |
|---|---|---|
| `x is None` | `x === null` | `x IS NULL` |
| `x is not None` | `x !== null` | `x IS NOT NULL` |
- Usa-se sempre `is None`, e não `== None` (o Ruff avisa).
- `if not x:` também é verdadeiro para `0` e `''`. O `is None` só apanha a ausência de valor.

### Lançar erros: `raise`
| JS | Python |
|---|---|
| `throw new Error('msg')` | `raise ValueError('msg')` |
| `try { } catch (e) { }` | `try: ... except ValueError as e: ...` |

O `raise` para o método ali mesmo, e o erro sobe até quem o chamou.

### Comparações encadeadas e `not`
```python
45 <= x <= 70  # o mesmo que 45 <= x and x <= 70 (em JS NÃO funciona assim)
not (45 <= x <= 70)  # True se estiver FORA do intervalo; not é o ! do JS
```

### ⚠️ Métodos: com `()` no Python, sem `()` nos templates
```python
carcass_yield = self.carcass_yield()  # Python: executa o método
self.carcass_yield  # Python: é o PRÓPRIO método, não o resultado
```
Nos templates escreve-se `{{ lot.total_hot_weight }}`, sem parênteses. Num `.py`, sem `()`, aparece um erro do tipo `'<' not supported between instances of 'method' and 'decimal.Decimal'`.

### Constantes
Em MAIÚSCULAS, por convenção: `MAX_YIELD = Decimal('70')`. Numa classe, leem-se com `self.MAX_YIELD`. Evitam números "mágicos" espalhados pelo código.

### Linhas em branco (PEP 8)
- **2** entre coisas do nível de topo (classes, funções soltas, depois dos imports).
- **1** dentro de uma classe (entre campos, `Meta` e métodos).

---

## 4. Modelos Django

```python
class Animal(models.Model):
    class Sex(models.TextChoices):
        MALE = "M", "Macho"  # valor guardado, rótulo mostrado

    identification_number = models.CharField(
        "n.º de identificação", max_length=14, unique=True
    )
    sex = models.CharField("sexo", max_length=1, choices=Sex.choices)
    live_weight = models.DecimalField("peso vivo (kg)", max_digits=6, decimal_places=1)

    class Meta:
        verbose_name_plural = "animais"

    def __str__(self):
        return self.identification_number
```

- Os campos declaram-se **na classe** (o Django gera o `__init__`). O `id` é criado sozinho.
- O primeiro argumento de cada campo é o rótulo visível (em PT-PT); o nome do campo é em inglês.
- `self.get_<campo>_display()` devolve o rótulo de um campo com `choices` (ex.: "Macho" em vez de `'M'`).

### Tipos de campo usados
| Campo | Para quê |
|---|---|
| `CharField(max_length=...)` | Texto curto |
| `DateField` | Só a data (convenção de nome: `_date`) |
| `DateTimeField` | Data e hora (convenção de nome: `_at`) |
| `DecimalField(max_digits, decimal_places)` | Pesos e dinheiro (nunca `FloatField`) |

### Opções de campo
| Opção | Efeito |
|---|---|
| `unique=True` | Não deixa valores repetidos (garantido pela base de dados) |
| `choices=...` | Lista fechada de valores |
| `null=True` | A **base de dados** aceita `NULL` |
| `blank=True` | Os **formulários** deixam o campo vazio |
| `auto_now_add=True` | Preenche a data sozinho quando o registo é criado |

Para campos opcionais, usa normalmente `null=True` e `blank=True` juntos.

### `class Meta`: opções do modelo como um todo
| Opção | Efeito |
|---|---|
| `verbose_name` / `verbose_name_plural` | Nome do modelo no admin |
| `ordering = ['-received_at']` | Ordem por omissão (`-` = descendente) |
| `constraints = [...]` | Regras na base de dados (ex.: unicidade combinada) |
| `indexes = [...]` | Índices |

### Relações
| | `OneToOneField` | `ForeignKey` |
|---|---|---|
| Exemplo | Animal → Carcass | DeboningLot → Carcass |
| Na base de dados | `animal_id` **UNIQUE** | `lot_id` (sem UNIQUE) |
| Do filho para o pai | `carcass.animal` (objeto) | `carcass.lot` (objeto) |
| Do pai para o filho | `animal.carcass` (um objeto) | `lot.carcasses.all()` (vários) |

```python
lot = models.ForeignKey(
    DeboningLot,
    on_delete=models.PROTECT,
    related_name="carcasses",  # o nome do acesso inverso: lot.carcasses
    verbose_name="lote de desmancha",
    null=True,
    blank=True,
)
```
- O campo chama-se `lot` (o Django cria a coluna `lot_id`). `carcass.lot` dá o objeto; `carcass.lot_id` dá o número.
- O modelo referido tem de estar definido **antes** no ficheiro (senão dá `NameError`).

### `on_delete`: o que acontece aos filhos se se apagar o pai
| Opção | Efeito | Para rastreabilidade |
|---|---|---|
| `CASCADE` | Apaga os filhos também | ❌ |
| `SET_NULL` | Os filhos ficam sem pai (exige `null=True`) | ❌ |
| `PROTECT` | Não deixa apagar o pai enquanto tiver filhos | ✅ |

### A coluna `_id` das relações
Um `ForeignKey`/`OneToOneField` chamado `animal` cria na tabela a coluna **`animal_id`** (o Django faz isto sozinho).
- `carcass.animal_id` dá o número guardado na coluna, por exemplo `1`, ou `None` se ainda não houver animal.
- `carcass.animal` dá o **objeto** `Animal` completo (o Django faz um `SELECT` à tabela dos animais). Se não houver animal, dá **erro** em vez de `None`.
- Para saber "já tem animal?", usa `self.animal_id is None`.

### Validações: `clean()`
Regras que envolvem mais do que um campo ficam num método `clean()` do modelo:
```python
from django.core.exceptions import ValidationError


class Carcass(models.Model):
    MIN_YIELD = Decimal("45")
    MAX_YIELD = Decimal("70")
    ...

    def clean(self):
        if self.animal_id is None or self.hot_weight is None:
            return  # nada para validar

        carcass_yield = self.carcass_yield()

        if carcass_yield is None:
            return

        if carcass_yield < self.MIN_YIELD or carcass_yield > self.MAX_YIELD:
            raise ValidationError(
                {"hot_weight": f"Rendimento de {carcass_yield:.1f} % ..."}
            )
```
- `ValidationError('msg')` mostra o erro no topo do formulário. Com um dicionário, `ValidationError({'campo': 'msg'})`, o erro aparece **ao lado do campo**.
- O admin (e qualquer formulário) chama o `clean()` sozinho antes de gravar.
- ⚠️ O **`save()` e o `objects.create()` NÃO chamam o `clean()`**. No código, valida-se com **`objeto.full_clean()`**. É uma validação da aplicação, e não da base de dados como o `UNIQUE`.
- O `clean()` corre mesmo que um campo esteja em branco. Por isso começa por verificar se os campos de que precisa existem.

---

## 5. Admin

```python
from django.contrib import admin

from .models import DeboningLot


@admin.register(DeboningLot)
class DeboningLotAdmin(admin.ModelAdmin):
    list_display = ["lot_number", "created_at", "carcass_count"]  # colunas
    list_filter = ["created_at"]  # filtros laterais
    search_fields = ["lot_number"]  # caixa de pesquisa

    @admin.display(description="n.º de carcaças")  # título da coluna
    def carcass_count(self, obj):
        return obj.carcasses.count()
```
- `self` é o ecrã de admin; `obj` é o registo da linha que está a ser mostrada.
- O `list_display` aceita campos e também métodos (do modelo ou do admin).
- Endereço: http://127.0.0.1:8000/admin/ (com o `runserver` a correr).

---

## 6. ORM (consultas)

Na shell: `python manage.py shell`. As variáveis perdem-se ao sair, mas os dados gravados ficam.

| SQL | Django ORM |
|---|---|
| `SELECT * FROM animal` | `Animal.objects.all()` |
| `SELECT COUNT(*) ...` | `Animal.objects.count()` |
| `... WHERE sex = 'M'` | `Animal.objects.filter(sex='M')` |
| `... WHERE sex = 'M' AND breed = 'Angus'` | `Animal.objects.filter(sex='M', breed='Angus')` |
| `... WHERE live_weight > 600` | `Animal.objects.filter(live_weight__gt=600)` |
| `... ORDER BY live_weight DESC` | `.order_by('-live_weight')` |
| exatamente 1 registo | `Animal.objects.get(identification_number='12345')` |
| `INSERT ...` | `DeboningLot.objects.create(lot_number='L0001')` |
| `UPDATE ...` | `c.lot = lot1` e depois `c.save()` |
| `SELECT SUM(hot_weight) ...` | `lot1.carcasses.aggregate(total=Sum('hot_weight'))` |

### O duplo underscore (`__`)
- **Operadores:** `__gt`, `__gte`, `__lt`, `__lte`, `__icontains`, `__in`, `__isnull`
- **Atravessar relações (JOIN):**
  ```python
  Carcass.objects.filter(animal__sex="M")
  Animal.objects.filter(carcass__lot=lot1, sex="M")
  Animal.objects.filter(carcass__lot__lot_number="L0001")
  ```

### Notas
- `get()` tem de encontrar **exatamente um** registo: com zero dá `DoesNotExist`, com vários dá `MultipleObjectsReturned`. Para listas usa `filter()`.
- O `Sum` tem de ser importado: `from django.db.models import Sum`.
- `print(consulta.query)` mostra o SQL gerado (só para leres: os valores vão à parte, como parâmetros).
- Os pesos vêm como `Decimal`, nunca como `float`.
- `Sum('hot_weight')` **não é um número**, é uma instrução para a base de dados. O número só existe depois do `aggregate()`. Por isso `Decimal(Sum(...))` dá erro.
- Num conjunto vazio, o `Sum` devolve `None`:
  ```python
  def total_hot_weight(self):
      return self.carcasses.aggregate(total=Sum("hot_weight"))["total"] or Decimal("0")
  ```

---

## 7. Views, URLs e templates

O caminho de um pedido:
```
/lotes/  →  urls.py (que função trata este endereço?)
         →  views.py (a função vai buscar os dados com o ORM)
         →  template HTML (preenchido com os dados e devolvido ao browser)
```

### A view (`traceability/views.py`)
```python
from django.shortcuts import render

from .models import DeboningLot


def lot_list(request):
    lots = DeboningLot.objects.all()
    return render(request, "traceability/lot_list.html", {"lots": lots})
```
- Uma view é uma função que recebe o pedido (`request`) e devolve uma resposta.
- O dicionário no fim define as variáveis que o template pode usar.

### Os URLs
Na app (`traceability/urls.py`):
```python
from django.urls import path

from . import views

app_name = "traceability"

urlpatterns = [
    path("lotes/", views.lot_list, name="lot_list"),  # a função SEM parênteses
]
```
No projeto (`config/urls.py`), liga os URLs de cada app:
```python
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("traceability.urls")),
]
```
- Os endereços visíveis ao utilizador ficam em português (`lotes/`).

### Os templates
Ficam em `traceability/templates/traceability/nome.html`. O nome da app repete-se de propósito, para não haver conflitos com templates de outras apps.

| Template Django | Vue | Para quê |
|---|---|---|
| `{{ lot.lot_number }}` | `{{ lot.lotNumber }}` | Mostrar um valor |
| `{% for x in lista %}` … `{% endfor %}` | `v-for` | Repetir |
| `{% empty %}` (dentro do `for`) | `v-if` com a lista vazia | O que mostrar se a lista estiver vazia |
| `{{ valor\|filtro }}` | os *filters* do Vue 2 | Formatar |

- Os métodos chamam-se **sem parênteses**: `{{ lot.carcasses.all }}`, `{{ lot.total_hot_weight }}`.
- Convenção: um espaço dentro das chavetas, `{{ valor }}`.
- Com `LANGUAGE_CODE = 'pt-pt'`, os números aparecem com vírgula (`400,0`).

| Filtro | Exemplo | Resultado |
|---|---|---|
| `date` | `{{ lot.created_at\|date:"d/m/Y H:i" }}` | `11/11/2026 14:03` |
| `floatformat` | `{{ peso\|floatformat:1 }}` | `765,0` |

### A página de erro 404 com a lista de URLs
Aparece porque `DEBUG = True` no `settings.py`. Em produção desliga-se, para não mostrar o interior da aplicação.

### Template base (herança de templates)
Um esqueleto comum com "buracos" (`block`), que cada página preenche. Parecido com um *layout* com `<slot>` no Vue.

`base.html`:
```django
{% load static %}
<!doctype html>
<html lang="pt-PT">
<head>
    <title>{% block title %}Rastreabilidade{% endblock %} · Protótipo</title>
    <link rel="stylesheet" href="{% static 'traceability/css/pico.classless.min.css' %}">
    <link rel="stylesheet" href="{% static 'traceability/css/style.css' %}">
</head>
<body>
    <nav> ... <a href="{% url 'traceability:lot_list' %}">Lotes</a> ... </nav>
    <main>{% block content %}{% endblock %}</main>
</body>
</html>
```
Página filha (`lot_list.html`):
```django
{% extends 'traceability/base.html' %}

{% block title %}Lotes de desmancha{% endblock %}

{% block content %}
    <h1>Lotes de desmancha</h1>
    ...
{% endblock %}
```
- O `{% extends %}` tem de ser a **primeira linha**.
- Numa página filha, tudo o que fica **fora** de um `{% block %}` é **ignorado**.
- O conteúdo de um bloco na base é o valor por omissão, usado se a filha não o preencher.

| Tag | Para quê |
|---|---|
| `{% extends '...' %}` | Herdar de outro template |
| `{% block nome %}…{% endblock %}` | Definir ou preencher um "buraco" |
| `{% load static %}` + `{% static 'caminho' %}` | Endereço de um ficheiro CSS/JS/imagem |
| `{% url 'app:nome' %}` | Endereço a partir do **nome** do URL (`app_name` + `name` no `urls.py`); se o caminho mudar, os links atualizam-se sozinhos. Um nome errado dá `NoReverseMatch` |

### Sobrepor um template do Django (ex.: link "Lotes" no admin)
Os templates do admin estão em `.venv\Lib\site-packages\django\contrib\admin\templates\admin\`. Servem **para ler e não para alterar**: ficam fora do git, e uma reinstalação da `.venv` apaga as alterações. Para veres o HTML final, abre a página no Chrome e usa **Ctrl+U** ou **F12**.

Para mudar um template do Django, crias no projeto um ficheiro com o **mesmo caminho** e o Django passa a usar o teu:
```
django-traceability-tutorial/
├── manage.py
└── templates/              ← pasta do projeto (na RAIZ, ao lado do manage.py)
    └── admin/
        └── base_site.html  ← sobrepõe o admin/base_site.html do Django
```
1. No `settings.py`, em `TEMPLATES`: `"DIRS": [BASE_DIR / "templates"]`. O `BASE_DIR` é um `Path` (do `pathlib`), e o `/` junta caminhos, como o `path.join()` do Node.
2. **Ordem de procura:** primeiro as pastas do `DIRS` e depois as `templates/` de cada app, pela ordem do `INSTALLED_APPS`. Como o `django.contrib.admin` vem antes do `traceability`, um `admin/base_site.html` posto **dentro da app** é ignorado.
3. Depois de criar a pasta, reinicia o `runserver`.

```django
{% extends "admin/base_site.html" %}

{% block userlinks %}
    <a href="{% url 'traceability:lot_list' %}">Lotes</a> /
    {{ block.super }}
{% endblock %}
```
- O `extends` com o **mesmo nome** do próprio ficheiro não fica em ciclo: o Django salta o teu e vai buscar o seguinte, que é o original. Assim herdas tudo (estilos, tema, menu).
- O **`{{ block.super }}`** devolve o conteúdo que o pai tinha nesse bloco. Serve para **acrescentar** em vez de substituir. Não dá para meter algo **a meio** do bloco do pai; isso obrigaria a copiar o bloco inteiro.
- Para saber que template o Django está a usar (o resultado é o caminho do ficheiro):
  ```powershell
  python -c "import django,os;os.environ['DJANGO_SETTINGS_MODULE']='config.settings';django.setup();from django.template.loader import get_template;print(get_template('admin/base_site.html').origin.name)"
  ```
- ⚠️ No VSCode, o **New Folder** cria a pasta dentro da que estiver selecionada. Para criar na raiz, clica antes no `manage.py`.

### ⚠️ Campos inexistentes não dão erro
`{{ carcass.identification_number }}` (o campo é do `Animal`, não da `Carcass`) **não dá erro, simplesmente não mostra nada**. Se uma célula aparece vazia, confirma o caminho: `{{ carcass.animal.identification_number }}`.

### Ficheiros estáticos (CSS, JS, imagens)
Ficam em `traceability/static/traceability/...`, com a mesma lógica de nomes dos templates.
- Com `runserver` e `DEBUG = True`, o Django serve-os sozinho. Em produção usa-se o `collectstatic` (fica para mais tarde).
- CSS: **Pico CSS v2.1.1, versão classless** (`pico.classless.min.css`), descarregado para a pasta e **não por CDN**: o servidor vai ficar na fábrica e tem de funcionar sem internet. O `style.css` vem **depois** do Pico no `<head>`, para os ajustes se sobreporem.
- No Pico, um `<nav>` com duas `<ul>` põe a primeira à esquerda e a segunda à direita.
- O CSS não mudou no browser? **Ctrl+F5**. Continua sem estilo? F12 → **Network** → procura um 404 no `.css`.

### Atalhos no VSCode
- **Emmet** (incluído no VSCode, ligado para `django-html` nas definições): `table>thead>tr>th*3`, `ul>li*2>a`, `p>strong`, `!` → Tab. Segue a lógica dos seletores CSS: `>` filho, `+` irmão, `*3` repete, `.` classe, `#` id.
- Extensão Django: escreve `block`, `for`, `if`, `url`, `static`, `extends` e escolhe na lista para inserir a tag com o respetivo `end`.
- **Ctrl+Shift+D**: duplicar a linha (atalho personalizado). **Ctrl+/**: comentar. **Ctrl+K Ctrl+S**: lista de atalhos.

---

## 7b. Testes

```powershell
python manage.py test                  # corre todos os testes
python manage.py test traceability     # só os de uma app
```
Os testes ficam em `traceability/tests.py`.

| Jest/Vitest | Django (`unittest`) |
|---|---|
| `describe('DeboningLot', ...)` | `class DeboningLotTests(TestCase):` |
| `it('soma os pesos', ...)` | um método cujo nome começa por **`test_`** |
| `expect(a).toBe(b)` | `self.assertEqual(a, b)` |
| `beforeEach(...)` | `def setUp(self):` |
| `npm test` | `python manage.py test` |

```python
from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from .models import Animal, Carcass, DeboningLot


class DeboningLotTests(TestCase):
    def test_total_hot_weight_empty_lot_is_zero(self):
        lot = DeboningLot.objects.create(lot_number="T001")

        self.assertEqual(lot.total_hot_weight(), Decimal("0"))
```
- Os testes usam uma **base de dados temporária e vazia**: não veem o `db.sqlite3` nem o que criaste no admin, e o `runserver` não precisa de estar ligado. Cada teste cria os seus dados, e no fim de cada teste tudo é desfeito (um `ROLLBACK`).
- Padrão de um teste: **preparar** os dados, **executar** o que se quer testar e **verificar** o resultado.
- Os nomes dos testes são compridos de propósito: quando um falha, o nome diz o que se partiu.
- ⚠️ **Um teste sem `assert` passa sempre.** Faz o teste falhar de propósito pelo menos uma vez (por exemplo, com o valor esperado `999`), para confirmares que está mesmo a testar alguma coisa.
- No resultado: `.` quer dizer que o teste passou, `F` que falhou (o valor não é o esperado) e `E` que deu erro (exceção).
- Datas: `date(2024, 3, 1)` para um `DateField`; `timezone.now()` para um `DateTimeField` (com `USE_TZ = True`, evita avisos de data sem fuso horário).
- Erros comuns:
  - `got unexpected keyword arguments: 'x'`: o campo não existe, quase sempre por gralha (ex.: `recieved_at`);
  - `IntegrityError: NOT NULL constraint failed: tabela.campo`: falta um campo obrigatório.

### Testar uma página
```python
from django.urls import reverse


class LotListViewTests(TestCase):
    def setUp(self):  # corre ANTES de cada teste (como o beforeEach)
        self.lot = DeboningLot.objects.create(lot_number="T100")
        # ... animais e carcaças (200,0 + 180,5)

    def test_page_loads(self):
        response = self.client.get(reverse("traceability:lot_list"))

        self.assertEqual(response.status_code, 200)

    def test_shows_lot_number_and_total(self):
        response = self.client.get(reverse("traceability:lot_list"))

        self.assertContains(response, "T100")
        self.assertContains(response, "380,5")
```
- `self.client` é um "browser falso": faz pedidos sem precisar do `runserver`.
- `reverse('app:nome')` é o equivalente, em Python, ao `{% url %}`: devolve `'/lotes/'`.
- `assertContains` confirma que a página respondeu com 200 **e** que o texto aparece no HTML.
- ⚠️ O `assertContains` procura **texto, tal como aparece na página**: `'380,5'` (pt-pt, com vírgula), e não `Decimal('380.5')`. Quando falha, o erro mostra o HTML inteiro, e é aí que se vê o que o Django gerou.
- ⚠️ Escolhe dados que tornem o resultado **inconfundível**. Com uma só carcaça, o total é igual ao peso dela, e o teste passaria mesmo com o total errado.
- O que se guarda em `self.` no `setUp` fica disponível nos testes. Cada classe tem o seu próprio `setUp`, e os dados de uma classe não aparecem nas outras.

### Um teste é um "utilizador robot" (preparar → agir → verificar)
Pensa no que um colega faria para verificar a página à mão:

| O colega | O teste |
|---|---|
| 1. **Preparar:** cria os dados no admin | O `setUp`, ou um `create(...)` no próprio teste |
| 2. **Agir:** escreve o endereço no Chrome | `url = reverse(...)` e `response = self.client.get(url)` |
| 3. **Verificar:** olha para o ecrã | `assertEqual(response.status_code, ...)`, `assertContains`, `assertNotContains` |

- Uma **linha em branco** separa cada fase.
- Nos `assert`, escreve **o texto que uma pessoa leria no ecrã**, entre aspas (`"T100"`, `"380,5"`). Não vás buscar o valor esperado ao código que estás a testar (`self.lot.total_hot_weight()`): se o código estiver errado, o teste compara o erro com o mesmo erro e passa.
- Não verifiques valores que aparecem em todo o lado (o `self.lot.pk` vale `1`, e há "1" nas datas e nas horas). Escolhe um valor **inconfundível** (`"T100"`).

### Testar a ficha do lote (rota com argumento, 404, texto que NÃO aparece)
```python
def test_detail_shows_lot_and_total(self):
    url = reverse("traceability:lot_detail", args=[self.lot.pk])  # → "/lotes/1/"
    response = self.client.get(url)

    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "T100")
    self.assertContains(response, "380,5")

def test_detail_unknown_lot_returns_404(self):
    url = reverse("traceability:lot_detail", args=[self.lot.pk + 1])
    response = self.client.get(url)

    self.assertEqual(response.status_code, 404)

def test_detail_empty_lot_hides_total(self):
    empty_lot = DeboningLot.objects.create(lot_number="T002")

    url = reverse("traceability:lot_detail", args=[empty_lot.pk])
    response = self.client.get(url)

    self.assertNotContains(response, "Peso total")
```
- **`reverse(..., args=[...])`** é o equivalente a `{% url 'app:nome' lot.pk %}`. O `args` é uma **lista**, com os valores pela ordem dos `<...>` do caminho.
- **`pk` ≠ `lot_number`:** o endereço usa o `pk` (1, 2, 3..., criado pelo Django). O `<int:pk>` só aceita inteiros: `args=["T200"]` dá `NoReverseMatch` antes de o pedido sair.
- **`self.lot.pk + 1`** em vez de um número escrito à mão (`2`): no PostgreSQL os ids **não recomeçam** entre testes, e o `2` podia ser o próprio T100. Diz a intenção: "o lote a seguir ao único que existe".
- Para o 404 basta o `assertEqual(response.status_code, 404)`. O `assertContains` verifica por baixo que o status é **200**, por isso falha sempre numa página 404.
- **Um teste só merece confiança depois de o teres visto falhar.** Com o template estragado (total sempre visível):

  | Texto no `assertNotContains` | Resultado | O teste... |
  |---|---|---|
  | `"Peso Total"` (não existe na página) | `ok` | **mente**: o bug está lá e ele não o vê |
  | `"Peso total"` (texto exato) | `FAIL` | apanhou o bug |
- ⚠️ O **`assertNotContains`** passa sempre se o texto estiver mal escrito (`"Peso Total"`). Distingue maiúsculas de minúsculas. Prova-o: estraga o código de propósito (aqui, comentar o `{% if %}` com `{# ... #}`) e confirma que o teste dá **FAIL**; depois repõe.
- Dá nomes que digam **porque** o objeto existe no teste: `empty_lot` em vez de `lot`, sobretudo quando também há um `self.lot`.
- O `assertContains` procura em todo o HTML, incluindo os atributos: `self.assertContains(response, url)` confirma que há um `href` para a ficha.

### Testar validações (`full_clean` + `assertRaises`)
```python
from django.core.exceptions import ValidationError


class CarcassValidationTests(TestCase):
    def test_impossible_yield_is_rejected(self):
        carcass = Carcass(animal=self.animal, ..., hot_weight=Decimal('165.0'))   # só em memória

        with self.assertRaises(ValidationError):    # o bloco TEM de lançar este erro
            carcass.full_clean()

    def test_normal_yield_is_accepted(self):
        carcass = Carcass(animal=self.animal, ..., hot_weight=Decimal('330.0'))
        carcass.full_clean()                         # se lançar um erro, o teste rebenta (E)
```
| Python | JS / SQL |
|---|---|
| `Carcass(...)` | `new Carcass({...})`; não toca na base de dados |
| `Carcass.objects.create(...)` | cria e grava: `INSERT` |
| `with self.assertRaises(X): ...` | `expect(() => ...).toThrow(X)` |

- O `full_clean()` corre todas as validações (campos obrigatórios, `max_length`, `unique` e o `clean()`) e não devolve nada.
- O objeto relacionado (o animal) tem de estar **gravado**: uma carcaça só pode apontar para um animal que exista.
- O `with` abre um bloco com "preparação antes e arrumação depois" (também se usa, por exemplo, para abrir ficheiros).

### ⚠️ Indentação = chavetas
Um `def` com 4 espaços a mais fica **dentro** do método de cima, e não na classe. Não dá erro, mas o teste **nunca corre**. Para tirar 4 espaços a várias linhas: seleciona-as e carrega em **Shift+Tab**.
```powershell
python manage.py test -v 2     # lista cada teste pelo nome: vê-se logo se algum ficou de fora
```

### Estilo e Ruff
O **Ruff** formata o código e aponta problemas (*linter*), como o Prettier + ESLint em JS.
- **Formata sozinho ao gravar com Ctrl+S**, num ficheiro `.py`: aspas, indentação, espaços, linhas em branco, vírgulas finais, linhas compridas (máx. 88 caracteres) e a ordem dos imports. Configurado em `.vscode/settings.json` (vai no git).
- ⚠️ O gravar automático (autosave) **não** formata. Só formata quando carregas em **Ctrl+S**.
- Aspas: **duplas** (o padrão do Ruff e da comunidade Python, decidido a 2026-11-13).
- Exceções em `ruff.toml`: as migrations não se formatam (são geradas pelo Django) e há dois avisos desligados (`RUF012`, `FURB157`).
```powershell
ruff format .          # formata o projeto todo
ruff check .           # procura problemas
ruff check --fix .     # corrige os que tiverem correção automática
```
(Com o `.venv` ativo; o `ruff` está instalado no `.venv`.)

O **djLint** faz o mesmo para os **templates Django** (`.html`). O Ruff só trabalha com Python e o Prettier não percebe as tags `{% %}`.
- Formata ao gravar com **Ctrl+S** nos templates (extensão `monosans.djlint` + o pacote `djlint` no `.venv`). Configuração em `pyproject.toml`: perfil `django`, 4 espaços, linhas até 120 caracteres.
- O **Prettier** formata o **HTML puro e o CSS** (extensão `esbenp.prettier-vscode`; configuração em `.prettierrc`: 4 espaços, 120 colunas; o `.prettierignore` exclui os `.min.css`/`.min.js`, como o Pico). Divisão: `.py` → Ruff; templates Django → djLint; `.html` puro e `.css` → Prettier.
- O VSCode decide o formatador pela **linguagem do ficheiro**, que aparece na barra azul, em baixo à direita ("HTML" ou "Django HTML"). Os `.html` dentro de `templates/` são "Django HTML". Os de `aprender/` também, por causa do `files.associations` no `.vscode/settings.json`. Os outros `.html` são "HTML" e vão para o Prettier, que **não percebe** as tags `{% %}`.
- ⚠️ O **autosave não formata**. O Ruff e o djLint só atuam com **Ctrl+S** manual: carrega nele quando acabares de mexer num ficheiro.
- Por omissão, o djLint **apaga todas as linhas em branco**. Com `blank_line_after_tag = "load,extends"` põe sempre uma linha em branco depois do `{% extends %}` e do `{% load %}`.
```powershell
djlint traceability/templates --reformat    # formata os templates
djlint traceability/templates --lint        # procura problemas (ex.: <img> sem alt)
```
- Convenções que continuam a valer: não deixar imports por usar; vírgula depois do último argumento quando cada um está na sua linha (o Ruff, ao ver essa vírgula, mantém um argumento por linha).

### Comentários e docstrings
**Comenta o *porquê*, não o *o quê*.** O "o quê" vem de bons nomes (`carcass = form.save()`, e não `saved_form`). Tudo **em inglês e curto**.
```python
def carcass_create(request):
    """Show the new-carcass form and save it on a valid POST."""   # docstring: o que faz

    # Redirect after POST so refreshing the page doesn't submit the form twice.   # porquê
    return redirect("traceability:lot_list")

carcass = form.save()  # save the form   ❌ repete o código
```
- **Docstring** (`"""..."""`, logo a seguir ao `def`/`class`): uma linha nas classes e funções cujo nome não diz tudo. Aparece ao passar o rato por cima do nome, no VSCode.
- **`#`**: regras do negócio, decisões não óbvias, valores provisórios, números "mágicos" (`# 27.5 % of 600 kg`).
- Os testes documentam-se pelo **nome** do método; a classe leva uma docstring curta.

---

## 7c. Formulários

### `ModelForm`: um formulário a partir de um modelo
```python
# traceability/forms.py
from django import forms          # o PACOTE (não "from django.forms import forms")

from .models import Carcass       # o TEU modelo (o "." = esta app)


class CarcassForm(forms.ModelForm):
    class Meta:
        model = Carcass
        fields = ["animal", "slaughter_number", "slaughtered_at", "hot_weight", "lot"]
```
- Aproveita tudo do modelo: tipos de campo, `verbose_name` (os rótulos), `unique`, `OneToOneField` e o **`clean()`**. As regras vivem no modelo e valem no admin, no formulário e nos testes.
- Imports: `from <onde está> import <o que queres>`. O `models` está em `django.db`, o `forms` está em `django`, o `messages` está em `django.contrib`. Erro típico: importar um **ficheiro** com o mesmo nome do pacote (`from django.forms import forms` → sem `ModelForm`).
- ⚠️ O `manage.py check` só lê os ficheiros que o projeto **usa**: um `forms.py` que ninguém importa pode ter erros sem o `check` se queixar.

### A view: GET mostra, POST grava
```python
from django.contrib import messages
from django.shortcuts import redirect, render


def carcass_create(request):
    if request.method == "POST":
        form = CarcassForm(request.POST)        # preenchido com o que veio do browser
        if form.is_valid():                     # todas as validações, incluindo o clean()
            carcass = form.save()               # grava e DEVOLVE o objeto
            messages.success(request, f"Carcaça {carcass.slaughter_number} adicionada.")
            return redirect("traceability:lot_list")
    else:
        form = CarcassForm()                    # vazio

    # GET (vazio) ou POST inválido (com os dados e os erros)
    return render(request, "traceability/carcass_form.html", {"form": form})
```
| Peça | O que é | Equivalente |
|---|---|---|
| `request.method` | `"GET"` ou `"POST"` | `req.method` (Express) |
| `request.POST` | Dicionário com os dados enviados | `$_POST`, `req.body` |
| `form.is_valid()` | Corre as validações → `True`/`False` | `$request->validate()` |
| `form.save()` | Grava e devolve o objeto | `Model::create(...)` |
| `redirect("app:nome")` | "Vai para esta página" (302). **Sem** `request` | `return redirect()->route(...)` |
| `messages.success(request, "...")` | Mensagem mostrada **uma vez** na página seguinte | `session()->flash(...)` |

- ⚠️ **Falta de `return`:** `redirect(...)` sem `return` cria a resposta e deita-a fora; a view continua e mostra o formulário outra vez.
- **POST → Redirect → GET:** depois de gravar, redireciona. Se mostrasses logo uma página, um F5 reenviava o POST e gravava duas vezes.
- O `render` fica **fora** do `if`/`else`: serve o GET e o POST inválido.
- ⚠️ Num nome mal escrito (`messages.succcess`), o Python só dá erro quando a linha **corre**. Os testes apanham-no; o Pylance sublinha-o.

### O template
```django
<form method="post">           {# o method vai no <form>, não no <button> #}
    {% csrf_token %}           {# obrigatório num POST; sem ele: 403 (como o @csrf do Blade) #}
    {{ form }}                 {# gera um <label> + <input> por campo #}
    <button type="submit">Guardar</button>
</form>
```
Mensagens no `base.html` (para todas as páginas):
```django
{% for message in messages %}
    <article>{{ message }}</article>
{% endfor %}
```
- Nomes: a view diz a **ação** (`carcass_create`), o template diz **o que mostra** (`carcass_form.html`), porque o `carcass_update` vai usar o mesmo template. É a convenção das `CreateView`/`UpdateView` do Django.
- No caminho, português (`carcacas/nova/`, visível); no `name`, inglês (`carcass_create`, código).

### Testar um formulário
```python
response = self.client.post(self.url, {"animal": self.animal.pk, "hot_weight": "330.0", ...})
self.assertRedirects(response, reverse("traceability:lot_list"))   # 302 para este endereço
self.assertEqual(Carcass.objects.count(), 1)                       # o que medes, o que esperas

response = self.client.post(self.url, data, follow=True)   # segue o redirect → a página final
self.assertContains(response, "Carcaça 50001 adicionada.")
```
- Os dados vão como **texto**, como chegam do browser. Num `<select>` envia-se o **pk**. A data como `"2026-11-16 10:00"`.
- Para saber se **gravou**, pergunta-se à **base de dados** (`Carcass.objects.count()`), não à página.
- **`assertEqual(o que medes, o que esperas)`**: o lado direito é escrito à mão (`1`, `0`, `200`), nunca uma variável (`response`, `self.animal`).
- Num teste, **só aparece a primeira falha**: quando um `assert` falha, as linhas seguintes não correm.
- Uma regra testada em dois níveis (o `clean()` com `full_clean()` e o formulário na página) parte **os dois** testes quando muda: é proteção a dobrar.
- Um método auxiliar (`valid_data()`) evita repetir o dicionário; um teste faz `data = self.valid_data()` e muda só um campo.

### Números com vírgula no formulário (`localized_fields`)
```python
class Meta:
    model = Carcass
    fields = [...]
    # Portuguese users type decimals with a comma, not a dot.
    localized_fields = ["hot_weight"]
```
- Por defeito, um campo de formulário só aceita o **ponto** (`"330,0"` → "Introduza um número."), como o `parseFloat` do JS. Com `localized_fields`, segue a língua do site (`LANGUAGE_CODE = "pt-pt"`): aceita `330,0` e mostra com vírgula.
- **Primeiro o teste, depois a correção (TDD):** escreveu-se o `test_comma_decimal_is_accepted`, viu-se falhar (`200 != 302`: o formulário inválido volta a ser mostrado, não há redirect), e só depois se acrescentou a linha.
- Formulário inválido → **nada é gravado** (só o `form.save()` cria a carcaça) e a view responde **200** com os erros; um redirect seria **302**.
- Um `assert` que falha **lança um erro** (como um `throw` em JS): o resto do teste não corre, mas os outros testes sim.

### Mostrar números com vírgula no código Python (`number_format`)
```python
from django.utils.formats import number_format

number_format(Decimal("27.5"), 1)   # → "27,5"   (1 = casas decimais)
f"{Decimal('27.5'):.1f}"            # → "27.5"   o f-string não sabe a língua do site
```
| Onde | Com vírgula (pt-PT) |
|---|---|
| Template | `{{ valor\|floatformat:1 }}` |
| Código Python (admin, mensagens de erro) | `number_format(valor, 1)` |
| Entrada no formulário | `localized_fields = [...]` |

- Sem o `1`, mostra **todas** as casas decimais (`33,333333…`). Com `300 ÷ 500` parecia certo por sorte.
- O `number_format` já devolve **texto**: `return number_format(value, 1)`, sem `f"{...}"` à volta.
- ⚠️ `return {x}` (chavetas fora de um f-string) cria um **set** (como `new Set([x])` em JS) e o admin mostra `{'60,0'}`. Nem o Ruff nem os testes o apanham: confirma com os olhos.
- Dentro das `{ }` de um f-string pode ir qualquer expressão, incluindo chamadas: `f"{number_format(x, 1)} %"`. Sem espaços dentro das chavetas (os espaços são do `{{ x }}` dos templates).
- Teste do texto: `assertContains(response, "27,5")`, e **não** `","`: há vírgulas em todas as páginas (ex.: `<meta name="viewport" content="width=..., initial-scale=1">`), e um texto genérico demais faz o teste passar sempre.

### Comentários longos: na linha de cima
O Ruff corta as linhas aos **88 caracteres**. Se código + comentário passar disso, parte o que puder, de forma feia:
```python
localized_fields = [
    "hot_weight"
]  # Portuguese users type decimals...      ❌
```
Comentário longo → **sozinho, na linha de cima**. No fim da linha, só comentários curtos, com **dois espaços** antes do `#` (o Ctrl+S trata disso).

---

## 7d. CI com o GitHub Actions

A cada push ao `main`, o GitHub liga um **runner** (uma máquina **Linux** limpa, que só existe durante a execução), instala o projeto, corre o Ruff e os testes, e marca o commit com ✅ ou ❌. Os resultados estão no separador **Actions** do repositório.

### O ficheiro `.github/workflows/ci.yml`
```yaml
name: CI Workflow

on:                          # o "trigger": quando corre
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest   # o runner
    steps:
      - uses: actions/checkout@v5        # = git clone
      - uses: actions/setup-python@v6    # = instalar o Python
        with:
          python-version: "3.14"         # com aspas: sem elas, 3.10 virava 3.1

      - name: Install dependencies
        run: pip install -r requirements-dev.txt

      - name: Lint
        run: ruff check .

      - name: Run tests
        run: python manage.py test       # sem o nome da app: corre o projeto todo
```

### YAML em 30 segundos
- `chave: valor` (espaço depois dos `:`); estrutura por **indentação de 2 espaços** (sem tabs); listas com `- `; comentários com `#`.
- É o mesmo que um JSON, sem chavetas nem aspas obrigatórias.

### `uses` vs `run`
- **`uses:`** uma ação pronta feita por outros (como um pacote npm; `@v5` é a versão). **`with:`** passa-lhe argumentos.
- **`run:`** um comando no terminal do runner (Linux).
- No runner **não há `.venv`** (a máquina é deitada fora no fim), **nem `migrate`** (os testes criam a sua própria base de dados), **nem `createsuperuser`** (pergunta coisas e não há ninguém ao teclado).

### O que o CI apanhou logo à primeira
1. **Uma experiência no `aprender/`** (`"False" or ...`) que o Ruff marca como erro → o `aprender/` saiu do **lint** (`[lint] exclude` no `ruff.toml`), mas continua a ser **formatado** ao gravar.
2. **`EXE001`: o `manage.py` tem shebang (`#!/usr/bin/env python`) mas não é executável.** No Windows não existe essa permissão, por isso passava no PC; no runner Linux, falhou. Correção: `git update-index --chmod=+x manage.py` (o git passa a guardar o modo `100755`). É o clássico **"no meu PC funciona"**: o CI corre noutro sistema e apanha estas diferenças.

### Ver os resultados no terminal (`gh`)
```powershell
gh run list --limit 5          # as últimas execuções (✓ / X)
gh run view <id> --log-failed  # só o registo dos passos que falharam
```
A página do Actions não se atualiza sozinha em alguns casos: F5 (é um GET, é seguro).

---

## 8. Git

- Um commit no fim de cada passo que funcione; o push (Sync Changes no VSCode) no fim do dia.
- O `db.sqlite3`, o `.venv` e o `__pycache__` não vão para o git (ver `.gitignore`).
- As migrations **vão** para o git.

### Montar o projeto numa máquina nova
```powershell
git clone https://github.com/tiagofcruz94/django-traceability-tutorial.git
cd django-traceability-tutorial
py install 3.14              # só se o "py -3.14" disser "No runtime installed"
py -3.14 -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py createsuperuser
```
- O instalador do python.org (Python Install Manager) instala a versão **mais recente**, que pode não ser a 3.14. O `py list` mostra as versões instaladas.
- Se o `activate` der erro de "execução de scripts desativada": `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (uma vez por máquina).
- **Dois destinos no mesmo Sync:** o `origin` pode ter dois endereços de push (`git remote set-url --add --push origin <endereço>`), por exemplo o GitHub e um repositório git "bare" numa pasta partilhada (um "bare" só tem o histórico, sem os ficheiros à vista). Para ver os endereços: `git remote -v`. Os endereços concretos estão nas notas internas.
- Mensagens de commit em **inglês**, com versão e data: `v0.1.0 (2026-11-13): Add Lots link to admin header` (ver `VERSION` e o CLAUDE.md).
