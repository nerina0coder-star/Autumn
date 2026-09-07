# Autumn Framework - Build front-end in the back-end
### What are we?
Autumn framework, a framework built to make front-end work as close as possible to back-end work.
Our goal is not to provide a server or back-end, but a tool that makes front-end look like back-end.
By making an ORM(Object Relational Mapping), we add an object-oriented way to write HTML documents and CSS styles
directly from Python.
### Why us?
You are not limited to us, there are Jinja2 and so many other libraries.
What makes us unique is making you to look at a Python class rather than a div tag.

While our top priority is Developer Experience (DX), type safety, and
over-the-top composition, we might as well note the speed and caching mechanisms:

Tests proven Autumn's speed is less than one millisecond(For simple pages),
and removing the IO for visible test outputs increases the speed even more,
pushing it towards/below 0.5ms.
Speed is improved even further by caching tags/styles, making the load time for a static
HTML page identical to a simple O(1) for a simple list lookup.

### How?
The process is straight.
But there are important things to consider:
- Thread safety:
    While we try our best to promise thread safety,
    such as features like before_build, we cannot lock every read/write for
    classes defined outside of Autumn's hands. All classes that do not inherit
    from AbstractBase are NOT made to be automatically thread-safe. Your classes are
    up to you, so, for reads/writes, it's best to access self._lock.
- Dynamicity:
    When elements are dynamic, their dynamic
    must be set to True. However, if any of the tags owned
    are dynamic, the parent will be inferred as dynamic,
    therefore no need to set dynamic to True.

here is an example with HTML, another with CSS.
#### HTML
Instead of writing:
```html
<div id="hello-world">Hello World!</div>
```
You write:
```python
from Autumn import new

Base = new()

tag = Base.tag

class MyDiv(tag.Tag):
    def __init__(self):
        self.name = "div"
        self.closable = True
        self.identifier = "hello-world"
        self.tags = ["Hello World!"]
        # How we recommend it.
        # However, you can place spaces, tabs, and newlines, but be aware that they will be
        # Replaced with -.
        
        super().__init__()
```
While this seems like writing too much, it's core benefit will be seen when writing **dynamic** tags or when you don't know about HTML too much.
Let's see an example for a dynamic tag.

```python
import time
from Autumn import new

Base = new()


class MyText(Base.tag.Tag):
    def __init__(self, classes: list[str]):
        self.name = "p"
        self.closable = True
        self.classes = classes
        self.dynamic = True
        
        super().__init__()

    def before_build(self, **_kwargs): # Recommended.
        self.tags.append(time.time())
```
This will produce a well behaving Paragraph with dynamic elements.
#### CSS
Well, this is straight forward.
```css
div.any-div#my-div-used-for-footer {color: #000000;}
```
will simply turn into:
```python
from typing import Any
from Autumn import new

Base = new()

class MyStyle(Base.style.Style):
    
    def __init__(self):
        self.name = Base.name.Name("div", Base.name.Identifier("my-div-used-for-footer"),
                                   [Base.name.Class("any-div")])
        self.styles = [
            "color: #000000;"
        ]
        
        super().__init__()

```
This will also become valuable when writing **dynamic** CSS or when you simply don't know CSS.
Let's see an example for that too.
```python
from typing import Any
from Autumn import new

Base = new()

class MyStyle(Base.style.Style):
    
    def __init__(self):
        self.name = Base.name.Name("div", Base.name.Identifier("my-div-used-for-footer"),
                                   [Base.name.Class("any-div")])
        self.styles = [
            "color: #000000;"
        ]
        
        self.dynamic = True
        
        super().__init__()

    def before_build(self, **kwargs):
        if "style" in kwargs:
            self.styles.append(kwargs["style"])
    
```

#### A note on Thread safety
Thread safety is one of the most important parts to remember,
every public and private method is thread-safe if it inherits from AbstractBase.
Well, excluding __getattribute__, __setattr__, every public/private method is thread-safe,
unless it's a protected method. We do not lock protected methods, as they are (mostly, by convenience)
used by the public/private methods themselves.

### Our future goals
Our future goals (currently) can be listed as:
1. Out of the box experience.
2. A stable and mature ecosystem.
3. Complete support for HTML/CSS.
4. Support for JavaScript, etc...
