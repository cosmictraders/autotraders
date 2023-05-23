Notes
=========
Just some FAQs and notes about pitfalls etc.

- Errors are always thrown then the API request fails (usually an ``IoError``)


Odd Values
____________
- ``math.nan`` - When an int hasn't been updated to a value yet.
- ``None`` -  When any other type hasn't been updated to a value yet.

Versioning
_______________
As the game is in alpha the versioning system is not exactly semantic.

- Major releases happen when the code structure changes or there is a breaking matter that involves the codebase
- Minor releases can have breaking changes if the API changes
- Patch releases are guaranteed not to have breaking changes.
