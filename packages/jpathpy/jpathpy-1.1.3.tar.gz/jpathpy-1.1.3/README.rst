Short about jpathpy
===================
Package "jpathpy" contains all needed for selection JSON members from JSON by using JPath query.

Terminology
===========
JPath query
-----------
Each of JPath queries based on JPath syntax.

JPath query can to contain one or more JPath expressions unioned by operator "|". For example::

	$."store"."book" | $."store"."bicycle"

If JPath query contains only one JPath expresion, operator "|" don't used. Each of JPath expressions in JPath query **must starts** with root reference ($).

JPath expression
----------------
JPath expression is some expression that defines which and how JSON members must be selected from JSON. All follow expressions are correct::

	$
	$."store"."book"
	$."store".."book"
	$.."book"
	."book"[*]
	.."price".isflt()
	.val()

Each of JPath expressions can to contain one or more filtering expression, which enclose between square parentheses.

Filtering Expression
--------------------
Filtering expression is expresion that can to contain different groups of arithmetic, comparation and logic operations. Available data types of each operations:

	* String
	* Integer
	* Float number
	* Null
	* Boolean
	* All data types which returns JPath functions or JPath expresions
	
For example, all of this filtering expressions is correct::

	1
	1.5
	True
	"Hello world!"
	null
	.."price"[0].val()
	$."store"."book"[*][0]
	1 + .."price"[0].val() > 5 and $."book"."author".contains("Orwell")
	!$."store"."book"
	
Arithmetic operators
^^^^^^^^^^^^^^^^^^^^^
	* multiple (\*)
	* divide (/)
	* modulation (%)
	* addition (+)
	* subtraction (-)
	
Comparation operators
^^^^^^^^^^^^^^^^^^^^^^
	* equals (=)
	* not equals (!=)
	* less than (<)
	* less than or equal to (<=)
	* greater than (>)
	* greater than or equal to (>=)
	
Logic operators
^^^^^^^^^^^^^^^^
	* union (or)
	* intersection (and)
	
Order applying operators
^^^^^^^^^^^^^^^^^^^^^^^^^
	* \*, /, %
	* +, -
	* =, !=, >, >=, <, <=
	* and, or
	
JPath functions
===============
It's all JPath functions

+----------------------------------+
| Function                         |
+==================================+
| *toint()*                        |
+----------------------------------+
| *toflt()*                        |
+----------------------------------+
| *tostr()*                        |
+----------------------------------+
| *val()*                          |
+----------------------------------+
| *length()*                       |
+----------------------------------+
| *isnum()*                        |
+----------------------------------+
| *isint()*                        |
+----------------------------------+
| *isflt()*                        |
+----------------------------------+
| *isbool()*                       |
+----------------------------------+
| *isstr()*                        |
+----------------------------------+
| *isnull()*                       |
+----------------------------------+
| *isarr()*                        |
+----------------------------------+
| *isobj()*                        |
+----------------------------------+
| *rnd(digits)*                    |
+----------------------------------+
| *strlen()*                       |
+----------------------------------+
| *substr(startIdx, length)*       |
+----------------------------------+
| *replace(template, replacement)* |
+----------------------------------+
| *isdigit()*                      |
+----------------------------------+
| *isalpha()*                      |
+----------------------------------+
| *isalnum()*                      |
+----------------------------------+
| *islower()*                      |
+----------------------------------+
| *isupper()*                      |
+----------------------------------+
| *isspace()*                      |
+----------------------------------+
| *istitle()*                      |
+----------------------------------+
| *lower()*                        |
+----------------------------------+
| *upper()*                        |
+----------------------------------+
| *startswith(template)*           |
+----------------------------------+
| *endswith(template)*             |
+----------------------------------+
| *capitalize()*                   |
+----------------------------------+
| *ltrim()*                        |
+----------------------------------+
| *rtrim()*                        |
+----------------------------------+
| *trim()*                         |
+----------------------------------+
| *title()*                        |
+----------------------------------+
| *contains(template)*             |
+----------------------------------+
| *normalize()*                    |
+----------------------------------+
| *count()*                        |
+----------------------------------+
| *all()*                          |
+----------------------------------+
| *any()*                          |
+----------------------------------+