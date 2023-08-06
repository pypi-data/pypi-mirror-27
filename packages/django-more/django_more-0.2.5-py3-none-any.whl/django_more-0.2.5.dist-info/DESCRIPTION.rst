django-more
===========

| A collection of Django patches and extensions to give more of the
  features and functionality that I want or expect from Django.
| *Currently aimed only at Django 1.11*

django\_more
------------

`django\_more <django_more/>`__ contains field and classes for Django
that do not require any patching and can be used directly.

-  **django\_more.storages**
   Allows defining Django storages in *settings* and generating the
   storage classes as needed in *django\_more.storages.NAME*.
-  **django\_more.PartialIndex**
   Database partial indexes using Django query and ``Q()`` notation.
   Working on postgres, untested elsewhere.
-  **django\_more.HashField**
   Field for storing hashes and removing the issues with comparing,
   generating, and converting hashes.
-  **django\_more.OrderByField** *(requires django\_types)*
   Field for *order\_with\_respect\_to* similar functionality, with
   support for an arbitrary number of fields in the ordering, database
   constraints, bulk updates, single query creation, and generic keys.

*Placing django\_more into Django INSTALLED\_APPS will automatically
invoke django\_types.patch\_types() - only necessary for OrderByField
makemigrations*

django\_enum
------------

`django\_enum <django_enum/>`__ patches Django to add EnumFields, with
enum state information in migrations to allow for consistent migrations
compatible with postgres and mysql.

-  **django\_enum.EnumField** *(requires django\_types)*
   Django field based upon python 3.4 (PEP435) ``Enum`` with support for
   database enum fields.
-  **django\_enum.enum\_meta**
   Decorator to hide *Meta* classes in standard python ``Enum``.
-  **django\_enum.patch\_enum()**
   Applies patches to Django necessary for this module to work.

*Placing django\_enum into Django INSTALLED\_APPS will automatically
invoke patch\_enum() and django\_types.patch\_types()*

django\_types
-------------

| `django\_types <django_types/>`__ patches Django to add support for
  custom database types to be used within migrations.
| Not intended to be used directly, but by other reusable apps adding
  fields that rely on the additional functionality.

-  **django\_types.CustomTypeField**
   Base implementation for custom types that can be managed within the
   migration framework.
-  **django\_types.patch\_types()**
   Applies patches to Django necessary for this module to work.

*Apps dependent on this should check for ProjectState.add\_type()
support, and if not present apply this with patch\_types()*

django\_cte
-----------

`django\_cte <django_cte/>`__ patches Django to add CTE based
functionality.

-  **django\_cte.patch\_cte()**
   Applies patches to Django necessary for this module to work.

| **Not included in distributions until out of WIP state**
| *Placing django\_cte into Django INSTALLED\_APPS will automatically
  invoke patch\_cte()*

patchy
------

`patchy <patchy/>`__ is class based monkey patching package used by the
other *django-more* modules to apply their patches in a consistent and
safe manner that is hopefully less fragile to Django core changes.

-  **patchy.patchy()**
   Creates a class and context manager to apply patches.
-  **patchy.super\_patchy()**
   Provides functionality similar to ``super()`` to functions and
   methods that have been patched in, allowing calls the methods they
   replaced.

--------------

--------------

--------------

Version History
---------------

**0.2.5** \* Bugfix: ``EnumField`` now serialises to text value of Enum
member \* Bugfix: ``EnumField`` now accepts strings that represent an
Enum member as valid values

**0.2.4** \* Bugfix: ``EnumField`` alter operations with a missing
argument now correctly accepted

**0.2.3** \* Bugfix: *patchy* exposes exceptions more correctly. \*
Added: *django\_types* patches migrations to use field based
dependencies and moves default functionality onto ``Field`` and
``RelatedField``.

**0.2.2** \* Added: Arbitrary field dependencies via *django\_types*. \*
Bugfix: ``OrderByField`` uses dependencies to prevent field creation
order issues.

**0.2.1** \* Added: ``OrderByField`` now matches all
*order\_with\_respect\_to* functionality. \* Documentation:
*django\_more* module, substantial rewrite and expansion of
`README <django_more/README.md>`__. \* Documentation: *django-more* base
`README <readme.md>`__ substantially cleaned up. \* Bugfixes: Migrations
interacting badly with OrderByField and defaults.

| **0.2.0**
| \* Added: ``django_more.OrderByField``. \* Bugfix: A bad reference
  caused ``EnumField`` to break on cascade. \* Bugfix: Defaults to
  ``EnumField`` are stringified so that migrations don't break if Enums
  are relocated. \* Refactored: *django\_more.fields* into sub-module.
  \* Documentation: *django\_more* module, added
  `README <django_more/README.md>`__.

| **0.1.1**
| \* Bugfix: Include *django\_types* in distribution as necessary for
  *django\_enum*.

| **0.1.0**
| \* Initial release without *django\_cte* module.
| \* Added: ``django_enum.EnumField``. \* Added:
  ``django_more.PartialIndex``. \* Added: ``django_more.HashField``. \*
  Added: ``django_more.storages``. \* Documentation: *django\_enum*
  module, added `README <django_enum/README.md>`__. \* Documentation:
  *django\_types* module, added `README <django_types/README.md>`__. \*
  Documentation: *patchy* module, added `README <patchy/README.md>`__.


