Notes
=========
Just some FAQs and notes about pitfalls etc.

- Errors are always thrown then the API request fails (usually an ``IoError``)
- If a object has a value of ``None`` is it likely the object hasn't synced that part of its state from the server

Versioning
_______________
As the game is in alpha the versioning system is not exactly semantic.

- Major releases happen when the code structure changes or there is a breaking matter that involves the codebase
- Minor releases can have breaking changes if the API changes
- Patch releases are guaranteed not to have breaking changes.
