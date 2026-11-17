# Reference guide: Python and Django

A summary of the commands and concepts learned in the tutorial, updated at the end of each step.
The application's own texts (labels, messages, URLs) are in European Portuguese, so they appear in Portuguese in the examples.

---

## 1. Virtual environment and dependencies (PowerShell)

| Command | What for |
|---|---|
| `.venv\Scripts\activate` | Activate the virtual environment (every time you open a new terminal) |
| `deactivate` | Deactivate it |
| `pip install -r requirements.txt` | Install the project's dependencies |
| `pip install <package>` | Install a new package |
| `pip freeze > requirements.txt` | Update the dependency list after installing a package |
| `python file.py` | Run a script |
| `python` | Open the interactive Python console (`exit()` to leave) |

---

## 2. Django commands (`python manage.py ...`)

| Command | What for |
|---|---|
| `runserver` | Start the development server at http://127.0.0.1:8000 (Ctrl+C to stop). Reloads by itself when you save a `.py` |
| `check` | Check the project for configuration errors |
| `makemigrations` | **Generate** the migration files from the models |
| `migrate` | **Apply** the migrations to the database |
| `showmigrations <app>` | See which migrations are applied (`[X]`) and pending (`[ ]`) |
| `sqlmigrate <app> <number>` | See a migration's SQL without running it (e.g. `sqlmigrate traceability 0001`) |
| `makemigrations --check --dry-run` | Check whether there are model changes left to migrate, without generating anything |
| `shell` | Open the Django shell, with the models ready to import (`exit()` to leave) |
| `createsuperuser` | Create an admin user |
| `startapp <name>` | Create a new app |

### When do you need to run migrations?

| You changed… | What to do |
|---|---|
| A model's fields, their labels or the `class Meta` | `makemigrations` + `migrate` |
| `admin.py`, `views.py`, model methods, `settings.py` | Nothing: just save |

When in doubt, run `makemigrations`. If there's nothing to generate, it says `No changes detected`.

### ⚠️ The migration rule

**In one migration, either rename a field or change its type. Never both at once.**
If you do both, Django doesn't recognise it as the same field: it drops the column (with its data) and creates a new one.
The warning sign is Django asking for a default value ("It is impossible to add a non-nullable field…"). If that happens, quit with option `2` and make the change in two steps.

---

## 3. Python: the essentials

### Differences from PHP/JS

| PHP / JS | Python |
|---|---|
| `$x = 1;` / `let x = 1;` | `x = 1` |
| `true`, `false`, `null` | `True`, `False`, `None` |
| `&&`, `\|\|`, `!` | `and`, `or`, `not` |
| `// comment` | `# comment` |
| `else if` | `elif` |
| `{ ... }` | `:` and 4-space indentation (indentation **is** the syntax) |
| `` `Weight ${w} kg` `` | `f"Weight {w} kg"` |
| `count($a)` / `a.length` | `len(a)` |
| `$a[] = $x` / `a.push(x)` | `a.append(x)` |
| `foreach ($a as $x)` | `for x in a:` |
| `foreach ($a as $k => $v)` | `for k, v in a.items():` |
| `x++` | `x += 1` (there is no `++`) |

### Text and numbers
```python
f"{value:.1f}"  # 1 decimal place
f"{value:.{n}f}"  # n decimal places
400 <= weight <= 600  # chained comparisons
7 / 2  # 3.5 (normal division, always a decimal)
7 // 2  # 3   (integer division)
```

### Lists and dictionaries
```python
animals = [{"breed": "Angus", "weight": 700}]
animals[0]          # the first one
animals[-1]         # the last one
animal["breed"]     # dictionary access (NOT animal.breed)
animal.get("xyz")   # returns None if the key doesn't exist (instead of an error)
sum(a["weight"] for a in animals)            # sum (generator expression)
sum(1 for a in animals if a["sex"] == "M")   # count the ones that meet a condition
if not animals:     # true if the list is empty
value or 0          # if "value" is None (or empty/zero), you get what's right of the "or"
```

### Sets
```python
lots = {"T100", "T200", "T100"}
print(lots)         # {'T100', 'T200'}: no duplicates, no order
"T100" in lots      # True (a very fast check)
```
| Written as | Type | In JS |
|---|---|---|
| `[1, 2, 2]` | `list`: ordered, allows duplicates | `[1, 2, 2]` |
| `{"a": 1}` | `dict`: key → value | `{ a: 1 }` |
| `{1, 2}` | `set`: no order, no duplicates | `new Set([1, 2])` |

- ⚠️ An empty `{}` is a **dict**; an empty set is `set()`.
- ⚠️ In an f-string, the `{ }` are the "slot" and disappear (`f"{x}"` → `60,0`). Outside one, they create a set (`{x}` → `{'60,0'}`). See `learning/review_2026-11-16.py`.
- Useful to remove duplicates or to check quickly "has this code been read already?".

### Falsy values
`if not x:` is true for `None`, `0`, `Decimal("0")`, `""`, `[]` and `{}`. But `"0"` and `"False"` are **non-empty strings**, so they're truthy. To check only for a missing value, use `is None`.

### Functions
```python
def format_weight(weight, unit="kg", decimals=1):  # default values
    return f"{weight:.{decimals}f} {unit}"


format_weight(537.25, decimals=0)  # keyword argument
```
- Functions **return** (`return`); the caller decides what to do with the value.
- 2 blank lines between top-level functions and classes; 1 between methods inside a class.

### Classes
```python
class Animal:
    def __init__(self, breed):  # the constructor (__construct)
        self.breed = breed  # self = $this

    def __str__(self):  # __toString
        return self.breed


class SlaughterAnimal(Animal):  # inheritance (extends)
    def __init__(self, breed, carcass_weight):
        super().__init__(breed)  # parent::__construct
        self.carcass_weight = carcass_weight


cow = Animal("Angus")  # no "new"
```
- `self` is always an instance of the class the method is written in, and you don't pass it when calling the method.

### Modules and imports
```python
from datetime import date  # 1st: standard library

from django.db import models  # 2nd: installed packages

from .models import Animal  # 3rd: your own code (the "." = the same package)
```
- Each `.py` file is a module; a folder with `__init__.py` is a package (a Django app is a package).
- Importing a file runs all of it. Code that should only run when you execute the file directly:
  ```python
  if __name__ == "__main__":
      ...
  ```
- Don't use names that shadow built-in functions: `id`, `list`, `type`, `sum`, `input`, `str`…

### ⚠️ Rounding
Python rounds ".5" cases to the nearest **even** number: `round(536.5)` gives `536`.
For weights and money, use `Decimal`, created from a **string**:
```python
from decimal import ROUND_HALF_UP, Decimal

Decimal("536.5").quantize(Decimal("1"), rounding=ROUND_HALF_UP)  # 537
```

### `Decimal` vs `:.1f` vs `floatformat`: which one?
| Where you are | What you want | You write |
|---|---|---|
| `.py` | **Create/calculate** an exact number | `Decimal("70")` (always in quotes) |
| `.py` | **Show** it in a string | `f"{value:.1f}"` → `37.5` (always a dot) |
| `.html` | **Show** it on the page | `{{ value\|floatformat:1 }}` → `37,5` (comma in pt-PT) |

Two questions: am I **calculating** or **showing**? Am I in a **`.py`** or an **`.html`**? (For a comma in Python code, see `number_format` in section 9.)

### `None` and `is None`
`None` is Python's "nothing": JS's `null` and SQL's `NULL`.

| Python | JS | SQL |
|---|---|---|
| `x is None` | `x === null` | `x IS NULL` |
| `x is not None` | `x !== null` | `x IS NOT NULL` |
- Always use `is None`, not `== None` (Ruff warns about it).
- `if not x:` is also true for `0` and `""`. `is None` only catches a missing value.

### Raising errors: `raise`
| JS | Python |
|---|---|
| `throw new Error("msg")` | `raise ValueError("msg")` |
| `try { } catch (e) { }` | `try: ... except ValueError as e: ...` |

`raise` stops the method right there, and the error goes up to the caller.

### Chained comparisons and `not`
```python
45 <= x <= 70  # same as 45 <= x and x <= 70 (in JS this does NOT work)
not (45 <= x <= 70)  # True if OUTSIDE the range; not is JS's !
```

### ⚠️ Methods: with `()` in Python, without `()` in templates
```python
carcass_yield = self.carcass_yield()  # Python: runs the method
self.carcass_yield  # Python: the method ITSELF, not its result
```
In templates you write `{{ lot.total_hot_weight }}`, without parentheses. In a `.py`, forgetting the `()` gives an error like `'<' not supported between instances of 'method' and 'decimal.Decimal'`.

### Constants
In CAPITALS, by convention: `MAX_YIELD = Decimal("70")`. In a class, read them with `self.MAX_YIELD`. They avoid "magic" numbers scattered through the code.

### Blank lines (PEP 8)
- **2** between top-level things (classes, standalone functions, after the imports).
- **1** inside a class (between fields, `Meta` and methods).

---

## 4. Django models

```python
class Animal(models.Model):
    class Sex(models.TextChoices):
        MALE = "M", "Macho"  # stored value, displayed label

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

- Fields are declared **on the class** (Django generates the `__init__`). The `id` is created automatically.
- Each field's first argument is the visible label (in pt-PT); the field name is in English.
- `self.get_<field>_display()` returns the label of a field with `choices` (e.g. "Macho" instead of `"M"`).

### Field types used
| Field | What for |
|---|---|
| `CharField(max_length=...)` | Short text |
| `DateField` | Date only (naming convention: `_date`) |
| `DateTimeField` | Date and time (naming convention: `_at`) |
| `DecimalField(max_digits, decimal_places)` | Weights and money (never `FloatField`) |

### Field options
| Option | Effect |
|---|---|
| `unique=True` | No repeated values (enforced by the database) |
| `choices=...` | A closed list of values |
| `null=True` | The **database** accepts `NULL` |
| `blank=True` | **Forms** allow the field to be empty |
| `auto_now_add=True` | Fills in the date automatically when the record is created |

Two "gatekeepers": `blank` is the form's, `null` is the database's. An optional **number or date** needs both. An optional **text** field needs only `blank=True`: `""` is already a natural empty value, and two kinds of "empty" (`""` and `NULL`) would be confusing.

### `class Meta`: options for the model as a whole
| Option | Effect |
|---|---|
| `verbose_name` / `verbose_name_plural` | Model name in the admin |
| `ordering = ["-received_at"]` | Default order (`-` = descending) |
| `constraints = [...]` | Database rules (e.g. combined uniqueness) |
| `indexes = [...]` | Indexes |

### Relations
| | `OneToOneField` | `ForeignKey` |
|---|---|---|
| Example | Animal → Carcass | DeboningLot → Carcass |
| In the database | `animal_id` **UNIQUE** | `lot_id` (not UNIQUE) |
| Child to parent | `carcass.animal` (object) | `carcass.lot` (object) |
| Parent to child | `animal.carcass` (one object) | `lot.carcasses.all()` (many) |

```python
lot = models.ForeignKey(
    DeboningLot,
    on_delete=models.PROTECT,
    related_name="carcasses",  # the name of the reverse access: lot.carcasses
    verbose_name="lote de desmancha",
    null=True,
    blank=True,
)
```
- The field is called `lot` (Django creates the `lot_id` column). `carcass.lot` gives the object; `carcass.lot_id` gives the number.
- `related_name` is optional: without it, the reverse access is `lot.carcass_set`.
- The referenced model must be defined **earlier** in the file (otherwise `NameError`).

### `on_delete`: what happens to the children when the parent is deleted
| Option | Effect | For traceability |
|---|---|---|
| `CASCADE` | Deletes the children too | ❌ |
| `SET_NULL` | The children lose their parent (needs `null=True`) | ❌ |
| `PROTECT` | Won't delete the parent while it has children | ✅ |

### The `_id` column of relations
A `ForeignKey`/`OneToOneField` called `animal` creates the **`animal_id`** column in the table (Django does this by itself).
- `carcass.animal_id` gives the number stored in the column, e.g. `1`, or `None` if there's no animal yet.
- `carcass.animal` gives the full `Animal` **object** (Django runs a `SELECT` on the animals table). If there's no animal, it raises an **error** instead of returning `None`.
- To ask "does it have an animal yet?", use `self.animal_id is None`.

### Validation: `clean()`
Rules involving more than one field go in the model's `clean()` method:
```python
from django.core.exceptions import ValidationError


class Carcass(models.Model):
    MIN_YIELD = Decimal("45")
    MAX_YIELD = Decimal("70")
    ...

    def clean(self):
        if self.animal_id is None or self.hot_weight is None:
            return  # nothing to validate

        carcass_yield = self.carcass_yield()

        if carcass_yield is None:
            return

        if carcass_yield < self.MIN_YIELD or carcass_yield > self.MAX_YIELD:
            raise ValidationError(
                {"hot_weight": f"Rendimento de {number_format(carcass_yield, 1)} % ..."}
            )
```
- `ValidationError("msg")` shows the error at the top of the form. With a dictionary, `ValidationError({"field": "msg"})`, the error appears **next to the field**.
- The admin (and any form) calls `clean()` by itself before saving.
- ⚠️ **`save()` and `objects.create()` do NOT call `clean()`**. In code, validate with **`obj.full_clean()`**. It's an application-level check, not a database one like `UNIQUE`.
- `clean()` runs even if a field is blank. That's why it starts by checking that the fields it needs exist.

---

## 5. Admin

```python
from django.contrib import admin

from .models import DeboningLot


@admin.register(DeboningLot)
class DeboningLotAdmin(admin.ModelAdmin):
    list_display = ["lot_number", "created_at", "carcass_count"]  # columns
    list_filter = ["created_at"]  # side filters
    search_fields = ["lot_number"]  # search box

    @admin.display(description="n.º de carcaças")  # column title
    def carcass_count(self, obj):
        return obj.carcasses.count()
```
- `self` is the admin screen; `obj` is the record of the row being shown.
- `list_display` accepts fields and also methods (from the model or the admin). A method that isn't in `list_display` shows nothing (like a Vue `computed` that the `<template>` never uses).
- Address: http://127.0.0.1:8000/admin/ (with `runserver` running).

---

## 6. ORM (queries)

In the shell: `python manage.py shell`. Variables are lost when you exit, but saved data stays.

| SQL | Django ORM |
|---|---|
| `SELECT * FROM animal` | `Animal.objects.all()` |
| `SELECT COUNT(*) ...` | `Animal.objects.count()` |
| `... WHERE sex = 'M'` | `Animal.objects.filter(sex="M")` |
| `... WHERE sex = 'M' AND breed = 'Angus'` | `Animal.objects.filter(sex="M", breed="Angus")` |
| `... WHERE live_weight > 600` | `Animal.objects.filter(live_weight__gt=600)` |
| `... ORDER BY live_weight DESC` | `.order_by("-live_weight")` |
| exactly 1 record | `Animal.objects.get(identification_number="12345")` |
| `INSERT ...` | `DeboningLot.objects.create(lot_number="L0001")` |
| `UPDATE ...` | `c.lot = lot1`, then `c.save()` |
| `SELECT SUM(hot_weight) ...` | `lot1.carcasses.aggregate(total=Sum("hot_weight"))` |

### The double underscore (`__`)
- **Operators:** `__gt`, `__gte`, `__lt`, `__lte`, `__icontains`, `__in`, `__isnull`
- **Following relations (JOIN):**
  ```python
  Carcass.objects.filter(animal__sex="M")
  Animal.objects.filter(carcass__lot=lot1, sex="M")
  Animal.objects.filter(carcass__lot__lot_number="L0001")
  ```

### Notes
- `get()` must find **exactly one** record: zero raises `DoesNotExist`, several raise `MultipleObjectsReturned`. For lists, use `filter()`.
- `Sum` must be imported: `from django.db.models import Sum`.
- `print(query.query)` shows the generated SQL (for reading only: the values go separately, as parameters).
- Weights come back as `Decimal`, never as `float`.
- `Sum("hot_weight")` **is not a number**, it's an instruction for the database. The number only exists after `aggregate()`. That's why `Decimal(Sum(...))` fails.
- `aggregate()` returns a **dictionary**: `{"total": Decimal("380.5")}`. On an empty set, `Sum` gives `None` (`{"total": None}`):
  ```python
  def total_hot_weight(self):
      total = self.carcasses.aggregate(total=Sum("hot_weight"))["total"]
      return total or Decimal("0")
  ```

---

## 7. Views, URLs and templates

The path of a request:
```
/lotes/  →  urls.py (which function handles this address?)
         →  views.py (the function fetches the data with the ORM)
         →  HTML template (filled with the data and sent back to the browser)
```

### The view (`traceability/views.py`)
```python
from django.shortcuts import render

from .models import DeboningLot


def lot_list(request):
    lots = DeboningLot.objects.all()
    return render(request, "traceability/lot_list.html", {"lots": lots})
```
- A view is a function that receives the request (`request`) and returns a response.
- The dictionary at the end defines the variables the template can use.

### The URLs
In the app (`traceability/urls.py`):
```python
from django.urls import path

from . import views

app_name = "traceability"

urlpatterns = [
    path("lotes/", views.lot_list, name="lot_list"),  # the function WITHOUT parentheses
    path("lotes/<int:pk>/", views.lot_detail, name="lot_detail"),
]
```
In the project (`config/urls.py`), include each app's URLs:
```python
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("traceability.urls")),
]
```
- Addresses the user sees are in Portuguese (`lotes/`).
- `<int:pk>` captures a whole number and passes it to the view as `pk`. The detail page uses the `pk` and not the lot number, because real lot numbers contain `/`.
- `get_object_or_404(DeboningLot, pk=pk)` returns the object or a 404 page (instead of a 500 error).
- Paths have **no leading slash**: Django strips it from the request before matching, so the root address is `""`, not `"/"` (`"/"` raises warning `urls.W002` and never matches).

### Redirecting an address: `RedirectView`
```python
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="traceability:lot_list"), name="home"),
    ...
]
```
- Django ships ready-made **class-based views** for repetitive jobs (lists, forms, redirects). `.as_view(...)` turns the class into the function `path` expects; its arguments configure it.
- `pattern_name` is the destination's URL **name**, with the namespace (`"traceability:..."`, because of `app_name`). Without it: `NoReverseMatch`.
- Name the URL by its **intention** (`home`), not its mechanism (`root_redirect`): when a real home page replaces the redirect, the name and every `{% url 'traceability:home' %}` stay valid.

| Code | Means | The browser… |
|---|---|---|
| **302** (temporary, `RedirectView`'s default) | "Go there for now" | Asks again next time |
| **301** (permanent, `permanent=True`) | "Moved for good" | **Caches** it and stops asking: hard to undo on every PC |

Test it with the address written by hand (it's what a user types) and the destination through `reverse`:
```python
response = self.client.get("/")

self.assertRedirects(response, reverse("traceability:lot_list"))  # checks the 302 too
```

### ⚠️ A URL path is not a folder path
In `/lotes/5/` there is no `lotes` folder with a `5` folder inside: the server takes the text, matches it against its routes (`lotes/<int:pk>/`) and `5` is just a **value** for the view. Every website works like this. GitHub's CI badge, `.../actions/workflows/ci.yml/badge.svg`, has no `badge.svg` file stored anywhere: `ci.yml` says which workflow, and the image is drawn on the fly from the latest run. On disk, `/` separates folders; in a URL, `/` separates pieces of text that the server interprets.

### The templates
They live in `traceability/templates/traceability/name.html`. The app name is repeated on purpose, to avoid clashes with templates from other apps.

| Django template | Vue | What for |
|---|---|---|
| `{{ lot.lot_number }}` | `{{ lot.lotNumber }}` | Show a value |
| `{% for x in items %}` … `{% endfor %}` | `v-for` | Repeat |
| `{% empty %}` (inside the `for`) | `v-if` on an empty list | What to show when the list is empty |
| `{% if lot.carcasses.exists %}` … `{% endif %}` | `v-if` | Show only if… |
| `{{ value\|filter }}` | Vue 2 *filters* | Format |
| `{# comment #}` | `<!-- -->` (but not sent to the browser) | Comment |

- `{{ }}` **shows** a value; `{% %}` **does** something (a loop, an `if`, a URL). `{{ url ... }}` is wrong and renders empty, with no error.
- Methods are called **without parentheses**: `{{ lot.carcasses.all }}`, `{{ lot.total_hot_weight }}`.
- Convention: one space inside the braces, `{{ value }}`.
- With `LANGUAGE_CODE = "pt-pt"`, numbers appear with a comma (`400,0`).

| Filter | Example | Result |
|---|---|---|
| `date` | `{{ lot.created_at\|date:"d/m/Y H:i" }}` | `11/11/2026 14:03` |
| `floatformat` | `{{ weight\|floatformat:1 }}` | `765,0` |

### The 404 page with the list of URLs
It shows up because `DEBUG = True` in `settings.py`. In production it's turned off, so the inside of the application isn't exposed.

### Base template (template inheritance)
A shared skeleton with "holes" (`block`) that each page fills in. Similar to a Vue *layout* with `<slot>`.

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
Child page (`lot_list.html`):
```django
{% extends 'traceability/base.html' %}

{% block title %}Lotes de desmancha{% endblock %}

{% block content %}
    <h1>Lotes de desmancha</h1>
    ...
{% endblock %}
```
- `{% extends %}` must be the **first line**.
- In a child page, anything **outside** a `{% block %}` is **ignored**.
- A block's content in the base is the default, used if the child doesn't fill it in.

| Tag | What for |
|---|---|
| `{% extends '...' %}` | Inherit from another template |
| `{% block name %}…{% endblock %}` | Define or fill in a "hole" |
| `{% load static %}` + `{% static 'path' %}` | Address of a CSS/JS/image file |
| `{% url 'app:name' %}` | Address from the URL's **name** (`app_name` + `name` in `urls.py`); if the path changes, links update by themselves. A wrong name gives `NoReverseMatch` |
| `{% url 'app:name' lot.pk %}` | The same, with an argument (no slashes around it) |

### Overriding a Django template (e.g. a "Lotes" link in the admin)
The admin templates are in `.venv\Lib\site-packages\django\contrib\admin\templates\admin\`. They're **for reading, not editing**: they're outside git, and reinstalling the `.venv` wipes any changes. To see the final HTML, open the page in Chrome and use **Ctrl+U** or **F12**.

To change a Django template, create a file in the project with the **same path** and Django uses yours instead:
```
django-traceability-tutorial/
├── manage.py
└── templates/              ← project folder (at the ROOT, next to manage.py)
    └── admin/
        └── base_site.html  ← overrides Django's admin/base_site.html
```
1. In `settings.py`, under `TEMPLATES`: `"DIRS": [BASE_DIR / "templates"]`. `BASE_DIR` is a `Path` (from `pathlib`), and `/` joins paths, like Node's `path.join()`.
2. **Lookup order:** first the `DIRS` folders, then each app's `templates/`, in `INSTALLED_APPS` order. Since `django.contrib.admin` comes before `traceability`, an `admin/base_site.html` placed **inside the app** is ignored.
3. After creating the folder, restart `runserver`.

```django
{% extends "admin/base_site.html" %}

{% block userlinks %}
    <a href="{% url 'traceability:lot_list' %}">Lotes</a> /
    {{ block.super }}
{% endblock %}
```
- An `extends` with the file's **own name** doesn't loop: Django skips yours and fetches the next one, the original. That way you inherit everything (styles, theme, menu).
- **`{{ block.super }}`** means "paste here what the parent had in this block". It lets you **add** instead of replace. You can't insert something in the **middle** of the parent's block; that would mean copying the whole block.
- To find out which template Django is using (prints the file's path):
  ```powershell
  python -c "import django,os;os.environ['DJANGO_SETTINGS_MODULE']='config.settings';django.setup();from django.template.loader import get_template;print(get_template('admin/base_site.html').origin.name)"
  ```
- ⚠️ In VSCode, **New Folder** creates the folder inside whichever one is selected. To create it at the root, click `manage.py` first.

### ⚠️ Missing fields don't raise errors
`{{ carcass.identification_number }}` (the field belongs to `Animal`, not `Carcass`) **raises no error, it just shows nothing**. If a cell is empty, check the path: `{{ carcass.animal.identification_number }}`.

### Static files (CSS, JS, images)
They live in `traceability/static/traceability/...`, with the same naming logic as templates.
- With `runserver` and `DEBUG = True`, Django serves them by itself. In production you use `collectstatic` (later).
- CSS: **Pico CSS v2.1.1, classless version** (`pico.classless.min.css`), downloaded into the folder and **not from a CDN**: the server will be on-premise and must work without internet. `style.css` comes **after** Pico in the `<head>`, so the tweaks win.
- In Pico, a `<nav>` with two `<ul>` puts the first on the left and the second on the right.
- CSS didn't change in the browser? **Ctrl+F5** (or F12 → Network → "Disable cache"). Still unstyled? F12 → **Network** → look for a 404 on the `.css`.

### VSCode shortcuts
- **Emmet** (built into VSCode, enabled for `django-html` in the settings): `table>thead>tr>th*3`, `ul>li*2>a`, `p>strong`, `!` → Tab. It follows CSS selector logic: `>` child, `+` sibling, `*3` repeat, `.` class, `#` id.
- Django extension: type `block`, `for`, `if`, `url`, `static`, `extends` and pick from the list to insert the tag with its `end`.
- **Ctrl+Shift+D**: duplicate line (custom shortcut). **Ctrl+/**: comment. **Ctrl+K Ctrl+S**: shortcut list.

---

## 8. Tests

```powershell
python manage.py test                  # run all tests
python manage.py test traceability     # only one app's tests
python manage.py test -v 2             # list each test by name
```
Tests live in `traceability/tests.py`.

| Jest/Vitest | Django (`unittest`) |
|---|---|
| `describe("DeboningLot", ...)` | `class DeboningLotTests(TestCase):` |
| `it("sums the weights", ...)` | a method whose name starts with **`test_`** |
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
- Tests use a **temporary, empty database**: they don't see `db.sqlite3` or what you created in the admin, and `runserver` doesn't need to be on. Each test creates its own data, and after each test everything is undone (a `ROLLBACK`).
- A test's pattern: **arrange** the data, **act** (run what you're testing), **assert** the result.
- Test names are long on purpose: when one fails, the name says what broke.
- ⚠️ **A test with no `assert` always passes.** Make a test fail on purpose at least once (e.g. with an expected value of `999`) to confirm it's really testing something.
- In the output: `.` means the test passed, `F` that it failed (wrong value) and `E` that it errored (exception).
- Dates: `date(2024, 3, 1)` for a `DateField`; `timezone.now()` for a `DateTimeField` (with `USE_TZ = True`, avoids naive-datetime warnings).
- Common errors:
  - `got unexpected keyword arguments: 'x'`: the field doesn't exist, almost always a typo (e.g. `recieved_at`);
  - `IntegrityError: NOT NULL constraint failed: table.field`: a required field is missing.

### Testing a page
```python
from django.urls import reverse


class LotViewTests(TestCase):
    def setUp(self):  # runs BEFORE each test (like beforeEach)
        self.lot = DeboningLot.objects.create(lot_number="T100")
        # ... animals and carcasses (200,0 + 180,5)

    def test_page_loads(self):
        response = self.client.get(reverse("traceability:lot_list"))

        self.assertEqual(response.status_code, 200)

    def test_shows_lot_number_and_total(self):
        response = self.client.get(reverse("traceability:lot_list"))

        self.assertContains(response, "T100")
        self.assertContains(response, "380,5")
```
- `self.client` is a "fake browser": it makes requests without `runserver`.
- `reverse("app:name")` is Python's equivalent of `{% url %}`: it returns `"/lotes/"`.
- `assertContains` checks that the page answered 200 **and** that the text is in the HTML.
- ⚠️ `assertContains` looks for **text as it appears on the page**: `"380,5"` (pt-PT, with a comma), not `Decimal("380.5")`. When it fails, the error shows the whole HTML, and that's where you see what Django generated.
- ⚠️ Pick data that makes the result **unmistakable**. With a single carcass, the total equals its weight, and the test would pass even with a wrong total.
- What you store on `self.` in `setUp` is available in the tests. Each class has its own `setUp`, and one class's data doesn't show up in the others.

### A test is a "robot user" (arrange → act → assert)
Think of what a colleague would do to check the page by hand:

| The colleague | The test |
|---|---|
| 1. **Arrange:** creates the data in the admin | `setUp`, or a `create(...)` in the test itself |
| 2. **Act:** types the address in Chrome | `url = reverse(...)` and `response = self.client.get(url)` |
| 3. **Assert:** looks at the screen | `assertEqual(response.status_code, ...)`, `assertContains`, `assertNotContains` |

- A **blank line** separates each phase.
- In the `assert`s, write **the text a person would read on screen**, in quotes (`"T100"`, `"380,5"`). Don't take the expected value from the code under test (`self.lot.total_hot_weight()`): if the code is wrong, the test compares the bug with the same bug and passes.
- Don't check values that appear everywhere (`self.lot.pk` is `1`, and there are "1"s in dates and times). Pick an **unmistakable** value (`"T100"`).

### Testing the lot page (route with an argument, 404, text that must NOT appear)
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
- **`reverse(..., args=[...])`** is the equivalent of `{% url 'app:name' lot.pk %}`. `args` is a **list**, with the values in the order of the `<...>` in the path. `reverse` comes first, then the `get`.
- **`pk` ≠ `lot_number`:** the address uses the `pk` (1, 2, 3…, created by Django). `<int:pk>` only accepts integers: `args=["T200"]` gives `NoReverseMatch` before the request is even made.
- **`self.lot.pk + 1`** instead of a hand-written number (`2`): in PostgreSQL ids **don't restart** between tests, and `2` could be T100 itself. It states the intent: "the lot after the only one that exists".
- For the 404, `assertEqual(response.status_code, 404)` is enough. `assertContains` also checks that the status is **200**, so it always fails on a 404 page.
- **Only trust a test after you've seen it fail.** With the template broken (total always visible):

  | Text in `assertNotContains` | Result | The test… |
  |---|---|---|
  | `"Peso Total"` (not on the page) | `ok` | **lies**: the bug is there and it doesn't see it |
  | `"Peso total"` (exact text) | `FAIL` | caught the bug |
- ⚠️ **`assertNotContains`** always passes if the text is misspelt (`"Peso Total"`). It's case-sensitive. Prove it: break the code on purpose (here, comment out the `{% if %}` with `{# ... #}`), check the test **FAIL**s, then put it back.
- Give names that say **why** the object exists in the test: `empty_lot` rather than `lot`, especially when there's also a `self.lot`.
- `assertContains` searches the whole HTML, attributes included: `self.assertContains(response, url)` checks there's an `href` to the detail page.

### Testing validation (`full_clean` + `assertRaises`)
```python
from django.core.exceptions import ValidationError


class CarcassValidationTests(TestCase):
    def test_impossible_yield_is_rejected(self):
        carcass = Carcass(animal=self.animal, ..., hot_weight=Decimal("165.0"))  # in memory only

        with self.assertRaises(ValidationError):  # the block MUST raise this error
            carcass.full_clean()

    def test_normal_yield_is_accepted(self):
        carcass = Carcass(animal=self.animal, ..., hot_weight=Decimal("330.0"))
        carcass.full_clean()  # if it raises, the test errors (E)
```
| Python | JS / SQL |
|---|---|
| `Carcass(...)` | `new Carcass({...})`; doesn't touch the database |
| `Carcass.objects.create(...)` | creates and saves: `INSERT` |
| `with self.assertRaises(X): ...` | `expect(() => ...).toThrow(X)` |

- `full_clean()` runs every validation (required fields, `max_length`, `unique` and `clean()`) and returns nothing.
- If `assertRaises` fails with "ValidationError not raised", the error **didn't** happen (the rule let the value through).
- The related object (the animal) must be **saved**: a carcass can only point to an animal that exists.
- `with` opens a block with "setup before and cleanup after" (also used, for instance, to open files).

### ⚠️ Indentation = braces
A `def` with 4 extra spaces ends up **inside** the method above, not in the class. No error, but the test **never runs**. To remove 4 spaces from several lines: select them and press **Shift+Tab**. `python manage.py test -v 2` lists each test by name, so you see straight away if one is missing.

### Style and Ruff
**Ruff** formats the code and points out problems (*linter*), like Prettier + ESLint in JS.
- **Formats on save with Ctrl+S** in a `.py` file: quotes, indentation, spaces, blank lines, trailing commas, long lines (max 88 characters) and import order. Configured in `.vscode/settings.json` (in git).
- ⚠️ Autosave does **not** format. Only **Ctrl+S** does.
- Quotes: **double** (the Ruff and Python community default, decided 2026-11-13).
- Exceptions in `ruff.toml`: migrations aren't formatted (Django generates them), `learning/` is excluded from lint, and two rules are off (`RUF012`, `FURB157`).
```powershell
ruff format .          # format the whole project
ruff check .           # look for problems
ruff check --fix .     # fix the ones with an automatic fix
```
(With the `.venv` active; `ruff` is installed in the `.venv`.)

**djLint** does the same for **Django templates** (`.html`). Ruff only handles Python and Prettier doesn't understand `{% %}` tags.
- Formats on **Ctrl+S** in templates (extension `monosans.djlint` + the `djlint` package in the `.venv`). Configured in `pyproject.toml`: `django` profile, 4 spaces, lines up to 120 characters.
- **Prettier** formats **plain HTML and CSS** (extension `esbenp.prettier-vscode`; configured in `.prettierrc`: 4 spaces, 120 columns; `.prettierignore` excludes `.min.css`/`.min.js`, like Pico). Split: `.py` → Ruff; Django templates → djLint; plain `.html` and `.css` → Prettier.
- VSCode picks the formatter by the **file's language**, shown in the blue bar, bottom right ("HTML" or "Django HTML"). `.html` files inside `templates/` are "Django HTML". So are the ones in `learning/`, because of `files.associations` in `.vscode/settings.json`. Other `.html` files are "HTML" and go to Prettier, which **doesn't understand** `{% %}` tags.
- By default, djLint **removes all blank lines**. With `blank_line_after_tag = "load,extends"` it always keeps a blank line after `{% extends %}` and `{% load %}`.
```powershell
djlint traceability/templates --reformat    # format the templates
djlint traceability/templates --lint        # look for problems (e.g. <img> without alt)
```
- Conventions that still apply: no unused imports; a comma after the last argument when each one is on its own line (Ruff sees that comma and keeps one argument per line).

### Comments and docstrings
**Comment the *why*, not the *what*.** The "what" comes from good names (`carcass = form.save()`, not `saved_form`). Everything **in English and short**.
```python
def carcass_create(request):
    """Show the new-carcass form and save it on a valid POST."""  # docstring: what it does

    # Redirect after POST so refreshing the page doesn't submit the form twice.  # why
    return redirect("traceability:lot_list")

carcass = form.save()  # save the form   ❌ repeats the code
```
- **Docstring** (`"""..."""`, right after the `def`/`class`): one line, on classes and functions whose name doesn't say it all. It shows when you hover over the name in VSCode.
- **`#`**: business rules, non-obvious decisions, provisional values, "magic" numbers (`# 27.5 % of 600 kg`).
- Tests are documented by the method **name**; the class gets a short docstring.

---

## 9. Forms

### `ModelForm`: a form built from a model
```python
# traceability/forms.py
from django import forms  # the PACKAGE (not "from django.forms import forms")

from .models import Carcass  # YOUR model (the "." = this app)


class CarcassForm(forms.ModelForm):
    class Meta:
        model = Carcass
        fields = ["animal", "slaughter_number", "slaughtered_at", "hot_weight", "lot"]
```
- It reuses everything from the model: field types, `verbose_name` (the labels), `unique`, `OneToOneField` and **`clean()`**. The rules live in the model and apply in the admin, in the form and in the tests.
- Imports: `from <where it is> import <what you want>`. `models` is in `django.db`, `forms` is in `django`, `messages` is in `django.contrib`. Typical mistake: importing a **file** with the same name as the package (`from django.forms import forms` → no `ModelForm`).
- ⚠️ `manage.py check` only reads the files the project **uses**: a `forms.py` nobody imports can have errors without `check` complaining.

### The view: GET shows, POST saves
```python
from django.contrib import messages
from django.shortcuts import redirect, render


def carcass_create(request):
    if request.method == "POST":
        form = CarcassForm(request.POST)  # filled with what came from the browser
        if form.is_valid():  # every validation, including clean()
            carcass = form.save()  # saves and RETURNS the object
            messages.success(request, f"Carcaça {carcass.slaughter_number} adicionada.")
            return redirect("traceability:lot_list")
    else:
        form = CarcassForm()  # empty

    # GET (empty) or invalid POST (with the data and the errors)
    return render(request, "traceability/carcass_form.html", {"form": form})
```
| Piece | What it is | Equivalent |
|---|---|---|
| `request.method` | `"GET"` or `"POST"` | `req.method` (Express) |
| `request.POST` | Dictionary with the submitted data | `$_POST`, `req.body` |
| `form.is_valid()` | Runs the validations → `True`/`False` | `$request->validate()` |
| `form.save()` | Saves and returns the object | `Model::create(...)` |
| `redirect("app:name")` | "Go to this page" (302 + a new GET). **No** `request` | `return redirect()->route(...)` |
| `messages.success(request, "...")` | Message shown **once** on the next page | `session()->flash(...)` |

- ⚠️ **Missing `return`:** `redirect(...)` without `return` builds the response and throws it away; the view carries on and shows the form again.
- **POST → Redirect → GET:** after saving, redirect. If you rendered a page straight away, F5 would resend the POST and save twice (with weighings there's no `unique` to stop the duplicate). It has nothing to do with CSRF.
- The `render` sits **outside** the `if`/`else`: it serves both the GET and the invalid POST.
- ⚠️ With a misspelt name (`messages.succcess`), Python only errors when the line **runs**. Tests catch it; Pylance underlines it.

### The template
```django
<form method="post">           {# the method goes on the <form>, not the <button> #}
    {% csrf_token %}           {# required on a POST; without it: 403 (like Blade's @csrf) #}
    {{ form }}                 {# renders a <label> + <input> per field #}
    <button type="submit">Guardar</button>
</form>
```
Messages in `base.html` (for every page):
```django
{% for message in messages %}
    <article>{{ message }}</article>
{% endfor %}
```
- Names: the view states the **action** (`carcass_create`), the template states **what it shows** (`carcass_form.html`), because `carcass_update` will use the same template. It's the convention of Django's `CreateView`/`UpdateView`.
- In the path, Portuguese (`carcacas/nova/`, visible); in the `name`, English (`carcass_create`, code).

### Testing a form
```python
response = self.client.post(self.url, {"animal": self.animal.pk, "hot_weight": "330.0", ...})
self.assertRedirects(response, reverse("traceability:lot_list"))  # 302 to this address
self.assertEqual(Carcass.objects.count(), 1)  # what you measure, what you expect

response = self.client.post(self.url, data, follow=True)  # follows the redirect → the final page
self.assertContains(response, "Carcaça 50001 adicionada.")
```
- Data is sent as **text**, as it comes from the browser. For a `<select>` you send the **pk**. Dates as `"2026-11-16 10:00"`.
- To know whether it **saved**, ask the **database** (`Carcass.objects.count()`), not the page.
- **`assertEqual(what you measure, what you expect)`**: the right-hand side is written by hand (`1`, `0`, `200`), never a variable (`response`, `self.animal`).
- In a test, **only the first failure shows**: when an `assert` fails, the following lines don't run.
- A rule tested at two levels (`clean()` with `full_clean()`, and the form on the page) breaks **both** tests when it changes: double protection.
- A helper method (`valid_data()`) avoids repeating the dictionary; a test does `data = self.valid_data()` and changes one field.

### Comma decimals in the form (`localized_fields`)
```python
class Meta:
    model = Carcass
    fields = [...]
    # Portuguese users type decimals with a comma, not a dot.
    localized_fields = ["hot_weight"]
```
- By default, a form field only accepts a **dot** (`"330,0"` → "Introduza um número."), like JS's `parseFloat`. With `localized_fields`, it follows the site's language (`LANGUAGE_CODE = "pt-pt"`): it accepts `330,0` and displays with a comma.
- `localized_fields` is about number **format**, not translation: the labels come from `verbose_name`.
- **Test first, then the fix (TDD):** `test_comma_decimal_is_accepted` was written first, seen to fail (`200 != 302`: the invalid form is shown again, no redirect), and only then was the line added.
- Invalid form → **nothing is saved** (only `form.save()` creates the carcass) and the view answers **200** with the errors; a redirect would be **302**.
- A failing `assert` **raises an error** (like a JS `throw`): the rest of that test doesn't run, but the other tests do.

### Showing comma decimals from Python code (`number_format`)
```python
from django.utils.formats import number_format

number_format(Decimal("27.5"), 1)   # → "27,5"   (1 = decimal places)
f"{Decimal('27.5'):.1f}"            # → "27.5"   the f-string doesn't know the site's language
```
| Where | With a comma (pt-PT) |
|---|---|
| Template | `{{ value\|floatformat:1 }}` |
| Python code (admin, error messages) | `number_format(value, 1)` |
| Form input | `localized_fields = [...]` |

- Without the `1`, it shows **every** decimal place (`33,333333…`). With `300 ÷ 500` it looked right by luck.
- `number_format` already returns **text**: `return number_format(value, 1)`, with no `f"{...}"` around it.
- ⚠️ `return {x}` (braces outside an f-string) creates a **set** (like `new Set([x])` in JS) and the admin shows `{'60,0'}`. Neither Ruff nor the tests catch it: check with your own eyes.
- Inside an f-string's `{ }` you can put any expression, including calls: `f"{number_format(x, 1)} %"`. No spaces inside the braces (spaces belong to the templates' `{{ x }}`).
- Testing the text: `assertContains(response, "27,5")`, **not** `","`: every page has commas (e.g. `<meta name="viewport" content="width=..., initial-scale=1">`), and a text that's too generic makes the test always pass.

### Long comments: on the line above
Ruff wraps lines at **88 characters**. If code + comment goes over, it breaks what it can, in an ugly way:
```python
localized_fields = [
    "hot_weight"
]  # Portuguese users type decimals...      ❌
```
Long comment → **on its own, on the line above**. At the end of a line, only short comments, with **two spaces** before the `#` (Ctrl+S takes care of that).

---

## 10. CI with GitHub Actions

On every push to `main`, GitHub starts a **runner** (a clean **Linux** machine that only exists during the run), installs the project, runs Ruff and the tests, and marks the commit ✅ or ❌. Results are in the repository's **Actions** tab.

### The `.github/workflows/ci.yml` file
```yaml
name: CI Workflow

on:                          # the "trigger": when it runs
  push:
    branches: [main]
  pull_request:
  workflow_call:             # another workflow (release.yml) can call this one

jobs:
  test:
    runs-on: ubuntu-latest   # the runner
    steps:
      - uses: actions/checkout@v5        # = git clone
      - uses: actions/setup-python@v6    # = install Python
        with:
          python-version: "3.14"         # in quotes: without them, 3.10 would become 3.1

      - name: Install dependencies
        run: pip install -r requirements-dev.txt

      - name: Lint
        run: ruff check .

      - name: Run tests
        run: python manage.py test       # no app name: runs the whole project
```

### YAML in 30 seconds
- `key: value` (a space after the `:`); structure by **2-space indentation** (no tabs); lists with `- `; comments with `#`.
- It's the same as JSON, without braces or mandatory quotes.

### `uses` vs `run`
- **`uses:`** a ready-made action written by others (like an npm package; `@v5` is the version). **`with:`** passes it arguments.
- **`run:`** a command in the runner's terminal (Linux).
- On the runner there's **no `.venv`** (the machine is thrown away at the end), **no `migrate`** (tests create their own database), and **no `createsuperuser`** (it asks questions and nobody is at the keyboard).

### What CI caught straight away
1. **An experiment in the study folder** (`"False" or ...`) that Ruff flags as an error → `learning/` left the **lint** (`[lint] exclude` in `ruff.toml`), but is still **formatted** on save.
2. **`EXE001`: `manage.py` has a shebang (`#!/usr/bin/env python`) but isn't executable.** Windows has no such permission, so it passed on the PC; on the Linux runner it failed. Fix: `git update-index --chmod=+x manage.py` (git stores mode `100755`). The permission lives in the `.git` folder, so a fresh `git init` loses it and it must be set again. It's the classic **"works on my machine"**: CI runs on another system and catches these differences.

### CI warns, it doesn't block
A failing test on `main` turns the run ❌ and GitHub sends an email, but the broken commit is already on `main`. To block it before it gets there, you need **branch protection** (required status checks), next in the CI block.

### Seeing the results in the terminal (`gh`)
```powershell
gh run list --limit 5          # the latest runs (✓ / X)
gh run view <id> --log-failed  # only the log of the failed steps
gh run watch <id>              # follow a run live
```
The Actions page doesn't always refresh by itself: F5 (it's a GET, it's safe).

### Releases on tags (CD): `.github/workflows/release.yml`
Pushing a `vX.Y.Z` tag runs the CI on that commit and, if it passes, creates a **GitHub Release** (a page with the version, notes generated from the PR titles, and the code as `.zip`/`.tar.gz`).
```yaml
name: Release

on:
  push:
    tags: ["v*"]               # any tag starting with "v"; "*" = anything (quoted: special in YAML)

jobs:
  ci:
    uses: ./.github/workflows/ci.yml   # calls the CI (a real file path in the repository, from the root "./")

  release:
    needs: ci                  # waits for the ci job and runs only if it passed (otherwise: "skipped")
    runs-on: ubuntu-latest
    permissions:
      contents: write          # creating a release writes to the repository; only this job gets it
    steps:
      - uses: actions/checkout@v5

      - name: Check the tag matches VERSION
        run: |
          expected="v$(cat VERSION)"
          if [ "$GITHUB_REF_NAME" != "$expected" ]; then
            echo "Version $GITHUB_REF_NAME doesn't match VERSION ($expected)"
            exit 1
          fi

      - name: Create GitHub release
        run: gh release create "$GITHUB_REF_NAME" --generate-notes
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
- **Triggers are a fixed list** from GitHub (`push`, `pull_request`, `workflow_call`, `workflow_dispatch`...): you choose the workflow and job names, not the trigger names. `workflow_dispatch:` adds a "Run workflow" button.
- **Triggers are doors:** adding `workflow_call:` doesn't close `push`/`pull_request`; the PR check `test` runs as before.
- **`branches: [...]` / `tags: [...]`**: a fixed name (`"v0.14.0"`, only that one) or a pattern (`"v*"`, all versions).
- **`needs: ci`** (one job) or **`needs: [lint, test]`** (several).
- **`GITHUB_TOKEN`**: a temporary key GitHub creates for each run; `gh` reads it from the `GH_TOKEN` environment variable. `${{ }}` is GitHub's expression syntax (looks like Django's `{{ }}`, same idea, different tool).
- **`$GITHUB_REF_NAME`**: the name of the tag that started the run. In bash a variable is read with `$NAME` (PowerShell: `$env:NAME`).
- A tag uses the workflow **as it is in the tagged commit**: tagging an old commit that has no `release.yml` does nothing.
- If CI fails on a tag, the tag stays on GitHub but there's no release: fix it and release the next number (`v0.14.1`); never reuse a version number.
- **Jobs run in parallel** (each on its own runner), whatever their order in the file; only `needs` orders them. **Steps** inside a job run in order, one after the other.

#### Bash in `run: |` (the runner is Linux)
| Bash | What it does | JS |
|---|---|---|
| `run: \|` | YAML: several lines of commands | a `{ ... }` block |
| `cat VERSION` | prints the file's content | `readFile("VERSION")` |
| `"v$(cat VERSION)"` | `$( )` is replaced by the command's output; parts are joined just by writing them together → `v0.14.1` | `` `v${version}` `` |
| `name="..."` | creates a variable (**no spaces** around `=`) | `const name = "..."` |
| `"$name"` | reads it (quoted, to be safe) | `name` |
| `if [ "$a" != "$b" ]; then ... fi` | an if; spaces inside `[ ]` are required; `fi` closes it | `if (a !== b) { ... }` |
| `echo "text $name"` | writes a line to the log | `` console.log(`text ${name}`) `` |
| `exit 1` | ends with an error: the step is ❌ and the next steps don't run | `throw new Error()` |

Inside quotes, `+` is just text: `"v + $(cat VERSION)"` gives `v + 0.14.1`.

Testing the failing case without a real release: tag the branch commit with a test tag (`v9.9.9`), push it, check the run, then delete it everywhere (allowed: it was never a release):
```powershell
git tag -d v9.9.9                  # on the PC
git push origin --delete v9.9.9    # on both push URLs
```

Releasing a version (after the PR is merged):
```powershell
git switch main
git pull
git tag v0.14.0              # sticks the label on the current commit
git push origin v0.14.0      # sends the tag → starts the Release workflow
gh run watch                 # follow it live
gh release view v0.14.0      # the release, in the terminal
```

**CI vs CD:** CI = every PR is tested and `main` only gets what passes. CD = Continuous **Delivery** (every version is tested and packaged automatically, ready to install: this workflow) or Continuous **Deployment** (installed on the server automatically: not here; the server is on a local network that GitHub can't reach, so it would need a *self-hosted runner* or a script on the server).

---

## 11. Markdown and the README

The `README.md` is the repository's front page on GitHub.

| Markdown | What it does | HTML equivalent |
|---|---|---|
| `# Title`, `## Section` | Headings | `<h1>`, `<h2>` |
| `[text](url)` | Link | `<a href="url">text</a>` |
| `![alt](url)` | Image (the `!` is the difference) | `<img src="url" alt="alt">` |
| `[![alt](image)](link)` | Image **inside** a link | `<a href="link"><img src="image" alt="alt"></a>` |
| `` `code` `` | Code inside a sentence (one backtick each side) | `<code>` |
| ```` ```shell ```` … ```` ``` ```` | Code block: the fences go **on their own lines**, the language after the opening one | `<pre><code>` |

- The CI badge: `[![CI](.../actions/workflows/ci.yml/badge.svg)](.../actions)`. The image is the state of the latest run; the link opens the Actions page. On a **private** repository, only signed-in users see it.
- The `alt` describes **the image** (`CI`), not the project.
- Lines with no blank line between them form **one paragraph** (the line break disappears). One blank line between blocks.
- Code block language: `powershell` or `bash` for commands specific to one system, `shell` for commands that are the same on both.
- Write only what exists (e.g. "CI", not "CI/CD" before there's a CD).
- **Ctrl+Shift+V** in VSCode opens the Markdown preview.

---

## 12. Git

- A commit at the end of each step that works; the push (Sync Changes in VSCode) at the end of the day.
- `db.sqlite3`, `.venv` and `__pycache__` don't go into git (see `.gitignore`).
- Migrations **do** go into git.
- `git mv old new` renames a file and keeps its history; `git restore <file>` throws away uncommitted changes.

### Branches and pull requests (protected `main`)
`main` only accepts changes through a **pull request** (PR) whose CI is ✅ (ruleset "Protect main", no bypass). The server mirror imitates it with a hook.

```powershell
git switch -c step/short-name              # 1. new branch (prefix: step/, feature/, fix/, hotfix/, docs/, chore/)
# ... work, commit ...
git push -u origin step/short-name         # 2. first push: -u links the branch; afterwards just `git push`
gh pr create --fill                        # 3. open the PR (title and body from the commit)
gh pr checks --watch                       # 4. follow the CI
gh pr edit <n> --title "vX.Y.Z (date): ..." # 5. CHECK THE TITLE: it becomes the commit message on main
gh pr merge <n> --squash --delete-branch   # 6. merge, delete the branch, switch to main and pull
git fetch --prune                          # 7. forget remote branches that no longer exist
```
- A push to a branch always works, even with broken code. What CI ❌ blocks is the **merge**. Without the protection, CI would only warn and the merge button would still work.
- **Squash** (the only method allowed): the whole PR becomes one commit on `main`, so one PR = one step = one version, and the "Revert" button undoes a whole feature.
- `git push` sends the current branch only; `git push origin --all` sends every branch (useful to fill an empty mirror, not day to day); tags go with `git push --tags`.
- Versions are marked with **tags** (`v0.1.0`), not branches: a tag never moves. `git tag` lists them, `git log v0.1.0..v0.2.0 --oneline` shows what changed. Going back to a version (rollback) means installing an older tag; with migrations, the database must be migrated back too.
- Keep branches short (one thing, merged quickly) to avoid merge conflicts.

### Setting up the project on a new machine
```powershell
git clone https://github.com/tiagofcruz94/django-traceability-tutorial.git
cd django-traceability-tutorial
py install 3.14              # only if "py -3.14" says "No runtime installed"
py -3.14 -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py createsuperuser
```
- The python.org installer (Python Install Manager) installs the **latest** version, which may not be 3.14. `py list` shows the installed versions.
- If `activate` fails with "running scripts is disabled": `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (once per machine).
- **Two destinations in one Sync:** `origin` can have two push addresses (`git remote set-url --add --push origin <address>`), e.g. GitHub and a "bare" git repository on a shared folder (a bare repository only has the history, no visible files). To see the addresses: `git remote -v`. The actual addresses are in the local notes.
- Commit messages in **English**, with version and date: `v0.1.0 (2026-11-13): Add Lots link to admin header` (see `VERSION` and `CLAUDE.md`).

## 13. Authentication (login)

`django.contrib.auth` (already in `INSTALLED_APPS`, it's what the admin uses) brings the `User` model and ready-made login/logout views.

### URLs, settings, template
```python
# config/urls.py: one line, same shape as the app's include (module path as text, no import)
path("contas/", include("django.contrib.auth.urls")),   # contas/login/ (name "login"), contas/logout/ ("logout"), password change...

# config/settings.py: URL **names** (like reverse), not paths
LOGIN_URL = "login"                                  # where @login_required sends anonymous users (default: /accounts/login/)
LOGIN_REDIRECT_URL = "traceability:lot_list"         # after logging in
LOGOUT_REDIRECT_URL = "login"                        # after logging out
```
The login view looks for a fixed template name: `templates/registration/login.html`, which just shows `{{ form }}` inside a POST form with `{% csrf_token %}`.

How `{{ form }}` knows the fields: `LoginView` has `form_class = AuthenticationForm` (fields `username` and `password`) and `template_name = "registration/login.html"`; its parent `FormView` passes the form to the template as `form`. The same three things your `carcass_create` view does by hand.

- `django.contrib.auth.login(request, user)` is **not a view**: it's the function that marks a user as logged in, called inside the login view.
- A path (`"lotes/"`, what the browser shows) is not a name (`"traceability:lot_list"`, what code uses).
- Wrong password → **200** with the form's error message. A **403** after going *back* to the login page is CSRF: Django changes the token on login, and the page the browser kept still has the old one.
- With `DEBUG = True`, a missing template shows the yellow debug page; the status is **500** (F12 → Network).

### Closing pages: `@login_required`
```python
from django.contrib.auth.decorators import login_required


@login_required
def lot_list(request):
    ...
```
A **decorator** (`@...` above a function, like `@admin.display`) adds behaviour without touching the function's code. Anonymous user → the view doesn't run; **302** to `/contas/login/?next=%2Flotes%2F` (`%2F` = `/`); after logging in, `next` brings them back. Similar to a Vue Router `beforeEach` guard.

### Tests with a logged-in robot
```python
class LoggedInTestCase(TestCase):
    """Base class for tests that need a logged-in user."""

    def setUp(self):
        self.user = User.objects.create_user(username="operador", password="segredo123")
        self.client.force_login(self.user)


class LotViewTests(LoggedInTestCase):
    def setUp(self):
        super().setUp()          # a child setUp REPLACES the parent's: call it, or there's no login
        ...


class HomeRedirectTests(LoggedInTestCase):
    ...                          # no setUp of its own: inherits the parent's as it is
```
- Tests use an **empty test database**, created and destroyed on each run: `create_user` creates the user there (your `db.sqlite3` is never touched).
- `create_user`, not `create`: it stores the password **hashed**. Hashing is slow on purpose (tests went from 0.05 s to ~2 s).
- `force_login` logs in without the form (doesn't check the password).
- Without login, view tests fail with **302** (sent to the login page), not 500: a 500 is a bug in the code.
