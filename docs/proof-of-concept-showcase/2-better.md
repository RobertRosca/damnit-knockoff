# Proof of Concept 2 - Better

Builds on top of the initial one:

- Loads user code from separate context file via `importlib`
- Attempts to simplify the style of the context files by:
  1. Extracting relevant classes and methods.
  2. Auto-apply `pseudo_property_decorator`, which is similar to `@property`, it runs a method and then sets that method equal to its return value.
  3. Auto-apply `before_event(Insert)`, which is what was previously applied manually.

Benefits:

- Demonstrates that it is still possible to make the context files look fairly simple and independent of the backend/db with not too much effort/complex code.
- (debatably a benefit) removes the need for the `@Variable` decorator.

## PoC 2.1

The automatic application of these decorators is kind of weird, I did it to see how it would work since the concept seemed interesting. This version is basically the same as the previous version, but without the automatic decorators.

Benefits:

- Decorators can have arguments, e.g. `direction` to set if the method gets called before or after events.
- Class methods without decorator are not treated as fields automatically, which is a bit more reasonable.

**Note** - I stuck to using class definitions in the context file since that gives an easy way to define **multiple collections**, but it is of course possible to remove that feature and have a single collection for the context file as is currently done.
