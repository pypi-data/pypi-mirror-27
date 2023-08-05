# DanteJcoder

Simple way to make json from standard django models

Quickstart:

Installation

`pip install django-dantejcoder`

Simple use

1. Import DanteJcoder

```python
    from dantejcoder.coder import DanteJcoder
```

2. Get one django model or queriset (for example in result variable)

3. Use DanteJcoder in JsonResponse

```python
    return JsonResponse(result, encoder=DanteJcoder)
```



