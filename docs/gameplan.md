## GEN NOTES

* from Unit, Army, to Civ. Unit is most cmoplex and has more flexibility.
* Each Civ has Army Presets. Define.
* make a file per class.
* Classes must be poly + inherited
* Army log goes in format "Army A (XX pts) defeated Army B (YY pts)" o "Was defeated by", siempre desde el punto de vista de army A (no global)
* After each part, build tests to check we're on the right track.

## CHECKLIST 

* Init repo ✓
* Create folder structure ✓
* Create Unit Class and Logic ✓
** Base logic goes in utils. Maybe unit/utils.py ✓
** Actions & Attrs: can train, get age, can transform, has strenght, can be eliminated, not queried. ✓
** Strength Training carryover edge case ✓
** Strength Transformation Carryover edge case ✓
** Build test to confirm based on notes. ✓

* Create Army Class and Logic
** Armies belong to a civilization ✓
** Three types of armies based on region. ✓
** Armies have 1k G on creation ✓ 
** Armies can attack other armies, regardless of civ/affiliation ✓ 
** Armies have a battle log ✓ 
** Army cost for transform, train
** Army log goes in format "Army A (XX pts) defeated Army B (YY pts)" o "Was defeated by", siempre desde el punto de vista de army A (no global) ✓ 
** If army has less than 2 units on defeat, kill all. ✓ 
** If tied and one army has no units, don't run logic. ✓ 

* Create Civilization Class and Logic ✓ 


## THINGS TO GO BACK TO / EDGE CASES IDENTIFIED

* InsufficientFundsError in Units 
* Strenght carryover on transform ✓ 
* Strength carryover on train + transform ✓ 
* Armies belong to civ, explicit (chinese civ can't have english armies) ✓ 
* On tie, lose strongest units (consistent with on victory, both armies losing 2 strongest units) ✓ 
* Handle case when army has no units to attack ✓ .
* Handle case when army has less than 2 units on defeat ✓.
* Handle case when army ties with no units (should never happen) ✓ 

## TIEMPO INVERTIDO
* 23 minutos utilizados para crear diagramas y gameplan inicial
* Ejercicio terminado en 2hrs 6mnts explícitamente con algunos edge cases atentidos, particularmente los de Units, tiempo restante utilizado para verificar, crear las pruebas, hacer refactoring, documentar e identificar edge cases adicionales
* Ejercicio terminado, documentado y atendido en 2hrs y 20mnts. Tiempo restante utilizado para crear pruebas unitarias (no se menciona en el enunciado que no se pueda hacer, ya que no cuenta como interacción de usuario.)
* Ejercicio totalmente terminado en 2hrs y 52 mnts (creación de tests)
* Aprox 30~ mints invertidos en crear solamente los tests.