# Rarity

Use r: or rarity: to find cards by their print rarity. You can search for common, uncommon, rare, special, mythic, and bonus. You can also use comparison operators like < and >=.

Use new:rarity to find reprint cards printed at a new rarity for the first time. You can find cards that have ever been printed in a given rarity using in: (for example, in:rare to find cards that have ever been printed at rare.)

Cards new to pauper in particular can be found using is:newinpauper.

## Examples

- `r:common t:artifact`: Common artifacts.
- `r>=r`: Cards at rare rarity or above(i.e., rares and mythics).
- `rarity:common e:ima new:rarity`: Cards printed as commons for the first time on Iconic Masters.
- `in:rare -rarity:rare`: Non-rare printings of cards that have been printed at rare.
