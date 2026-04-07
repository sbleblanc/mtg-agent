# Mana Costs

Use the m: or mana: keyword to search for cards that have certain symbols in their mana costs.

This keyword uses the official text version of mana costs set forth in the Comprehensive Rules. For example, {G} represents a green mana.

Shorthand is allowed for symbols that aren’t split: G is the same as {G}

However, you must always wrap complex/split symbols like {2/G} in braces.

You can search for mana costs using comparison operators; a mana cost is greater than another if it includes all the same symbols and more, and it’s less if it includes only a subset of symbols.

You can find cards of a specific mana value with manavalue or mv, comparing with a numeric expression (>, <, =, >=, <=, and !=). You can also find even or odd mana costs with manavalue:even or manavalue:odd

You can filter cards that contain hybrid mana symbols with is:hybrid or Phyrexian mana symbols with is:phyrexian

You can find permanents that provide specific levels of devotion, using either single-color mana symbols for devotion to one color, or hybrid symbols for devotion to two, with devotion: or a comparison operator.

You can also find cards that produce specific types of mana, with produces:

## Examples

- `mana: {G}{U}`: Cards with one green and blue mana in their costs.
- `m:2WW`: Cards with two generic and two white mana in their cost.
- `m>3WU`: Cards that cost more than three generic, one white, and one blue mana.
- `m:{R/P}`: Cards with one Phyrexian red mana in their cost.
- `c:u mv=5`: Blue cards with mana value 5.
- `devotion:{u/b}{u/b}{u/b}`: Cards that contribute 3 to devotion to black and blue.
- `produces=wu`: Cards that produce blue and white mana.
