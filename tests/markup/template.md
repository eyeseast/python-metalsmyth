---
title: Template test
tags: [template, jinja, python]
---

The content of this post should be rendered, but it shouldn't be inserted into an outer template.

Here's a list of tags:
{% for tag in tags %}
 - {{ tag }}{% endfor %}