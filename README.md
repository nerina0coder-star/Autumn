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

Autumn has been adding new features and fixes/docs daily, making sure that all problems are
solved for you. Using metaprogramming, we've added tens of features to improve your experience, such
as init autocall, decorators to disable/enable features, thread safety and error handling.

### Installing

The project is available in PyPI as autumn-core, so installing it is as simple as a:
```shell
cd /path/to/new/project
python3 -m venv .venv
.venv/bin/pip install autumn-core # or .venv/Scripts/pip for windows
```

Then you can start using Autumn in any way you would like.

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
    All dynamic tags completely bypass caching.
- Building:
    At before_build, you can either just change the class and let the process
    continue, or return a string. The returned string is the final output of
    the build.

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
every public and private method is automatically thread-safe if it inherits from AbstractBase.
Well, excluding __getattribute__, __setattr__, every public/private method is thread-safe,
unless it's a protected method. We do not lock protected methods, as they are (mostly, by convenience)
used by the public/private methods themselves.

### When to prefer Autumn

As said, there are many other great options, but Autumn's unique philosophy
and traits are one of the reasons people use Autumn instead of Jinja2 or React.

<table>
    <thead>
        <tr>
            <th>Tools</th>
            <th>Autumn</th>
            <th>Jinja2</th>
            <th>React</th>
            <th>etc(e.g., Dominate)...</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Paradigm</td>
            <td>Frontend Framework</td>
            <td>Server Side Templating Language</td>
            <td>Client-Side UI Library</td>
            <td>Python HTML Generator</td>
        </tr>
        <tr>
            <td>Core Philosophy</td>
            <td>A framework that treats HTML tags and CSS Styles as Python Objects,
            Making frontend works as intuitive as ORM work.</td>
            <td>A text-based templating engine that mixes HTML with special placeholders
            and logic.</td>
            <td>A declarative, component-based JavaScript library for building interactive user interfaces.</td>
            <td>A Python library that uses a DOM API to create HTML documents in pure Python,
            eliminating the need for a separate template language.</td>
        </tr>
        <tr>
            <td>Core Abstraction</td>
            <td>Python Classes/Objects</td>
            <td>Templates</td>
            <td>Components</td>
            <td>DOM API</td>
        </tr>
        <tr>
            <td>Environment</td>
            <td>Server</td>
            <td>Server</td>
            <td>Client</td>
            <td>Server</td>
        </tr>
        <tr>
            <td>Primary Use case</td>
            <td>Generating HTML on the server-side,
            commonly used with frameworks like Flask and Django.</td>
            <td>Building complex, interactive single-page applications
            (SPAs) with dynamic user interfaces.</td>
            <td>Creating and manipulating HTML documents programmatically
            in Python scripts, often for tasks like report generation.</td>
            <td>Building front-end interfaces directly from Python,
            with a focus on developer experience and type safety.</td>
        </tr>
        <tr>
            <td>Strengths</td>
            <td>Object-Oriented DX: Provides a unique, class-based approach that may feel natural to back-end developers.<br>
            Type Safety: Type safe, a benefit over traditional templating.
            Performance: High speed (less than one millisecond for simple pages) with effective caching mechanisms.</td>
            <td>
            Mature & Widely Adopted: The standard for Python web frameworks. <br>
            Powerful Features: Template inheritance, auto-escaping for security, sandboxed execution,
            and fast just-in-time compilation.
            </td>
            <td>
            Interactive & Dynamic: Unmatched for building highly responsive user interfaces. <br>
            Ecosystem: Massive community, rich ecosystem of libraries, and strong corporate backing (Meta). <br>
            Reusability: Components are highly composable and reusable.
            </td>
            <td>
            Pythonic & Simple: No need to learn a new templating language; uses pure Python. <br>
            Concise: Allows for very concise HTML generation.<br>
            Great for Scripts: Perfect for generating HTML in scripts or automated tasks.
            </td>
        </tr>
        <tr>
            <td>Weaknesses</td>
            <td>New & Unproven: A very new framework with a small community and limited real-world usage.<br>
            Immature Ecosystem: Lacks the extensive ecosystem and tooling of Jinja2 or React.</td>
            <td>Context Switching: Requires mixing Python logic with HTML in a separate syntax.<br>
            Server-Side Only: Cannot handle client-side interactivity on its own; requires JavaScript.</td>
            <td>Complexity: Steeper learning curve, requires understanding of JSX, state, and props.<br>
            Client-Side Heavy: Relies heavily on client-side rendering, which can impact SEO and initial load time without frameworks like Next.js.</td>
            <td>Less Interactive: Not a framework for building web apps; purely for generating HTML structures.<br>
            Niche Use: Best for specific tasks like report generation, not full-scale web development.</td>
        </tr>
    </tbody>
</table>

### Autumn Essential Extensions

Autumn has a few extensions to offer. While not many, the ones currently available are:
- [Autumn Tag Extras](https://github.com/nerina0coder-star/AutumnTagExtras/?tab=readme-ov-file)

New extensions will be added eventually, as this is not all we have to offer.
Among the few extensions, these are the only ones public for now.

### Our future goals
Our future goals (currently) can be listed as:
1. Out of the box experience.
2. A stable and mature ecosystem.
3. Complete support for HTML/CSS, etc...
