# TPPT Concept

## Why TPPT?

Even in the current era of widespread generative AI, there are still many requests for submitting reports in pptx format.
(Are we the only ones being left behind?)

TPPT is a wrapper for python-pptx that provides type-safe usage of slide masters and more.

It also incorporates ideas to make it easy to use and intuitive to write,
hoping to make your pptx generation safer and simpler.

## Reducing Imports
Let's look at the Quick Start again:
```python
--8<-- "codes/quick_start.py"
```

This code only imports TPPT.

You can create PowerPoint presentations with an extremely minimal number of imports.

This is an experimental approach to increase the success rate of code generation by AI,
by ensuring that only importing tppt is sufficient.

Two techniques are used to achieve this:

### Active Adoption of Literal Types

For example, the shape of a Shape to be added to a slide can be written in the traditional way:

```python
--8<-- "codes/quick_start_many_import.py"
```

In other words, `tppt.types.Inches(1)` can be written as `(1, "in")`.

By expressing unit specifications with types using Literals in this way,
we have reduced the imports that were previously necessary.

This is about writing; when reading properties, they are always converted to the Inches type,
allowing for addition, subtraction, and comparison.

### Type Extraction

There are places where lambda expressions like `lambda slide: slide...` are used.
This is lazy evaluation, where the type is extracted at the time of element initialization,
and the element is completed by adding operations to it.

The characteristic of this approach is that instead of importing types and passing them to function arguments,
types are extracted from within the function and used.

This further reduces imports for code generation.

This method has another advantage.
By extracting operations on the extracted types into functions,
it becomes easier to share components.

```python
--8<-- "codes/apply_sample.py"
```

You can create your own modifier functions like `format_text` and easily reuse them.

### Type Safety
This tool is mainly targeted at users who create new slides based on slide masters.

If you're like me, you've probably struggled with giving types to python-pptx's slide masters.

TPPT allows you to give types to slide masters using declarative type hints like pydantic.

```python
--8<-- "codes/custom_slide_master.py"
```

Is writing type definitions yourself tedious? We've prepared a modest tool for you.

```bash
python -m tppt.tool.ppt2template $YOUR_TEMPLATE.pptx -o $OUTPUT_FILE.py
```

After setting placeholders in the slide layout constructor,
you can describe data such as text, pictures, and tables.

All these operations are type-safe!