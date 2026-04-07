---
name: building-scryfall-query
description: Build a search query to be used when searching Scryfall
---

# Scryfall Search Query Builder

## Power and Toughness abbreviation
The power and toughness of a card are abbreviated like so: `{power}/{toughness}`

Example: `1/2` represents a power of 1 and a toughness of 2.

## Colors Abbreviations
- blue: `u`
- black: `b`
- white: `w`
- red: `r`
- green: `g`
- phyrexian: `p`

## Negating Conditions

All keywords except for include can be negated by prefixing them with a hyphen (-). This inverts the meaning of the keyword to reject cards that matched what you’ve searched for.

The is: keyword has a convenient inverted mode not: which is the same as -is:. Conversely, -not: is the same as is:.

Loose name words can also be inverted with -

## Exact Names

If you prefix words or quoted phrases with ! you will find cards with that exact name only.

This is still case-insensitive.

## Using “OR”
By default every search term you enter is combined. All of them must match to find a card.

If you want to search over a set of options or choices, you can put the special word or/OR between terms.

### Examples
- `t:fish or t:bird`: Cards that are Fish of Birds
- `t:land (a:titus or a:avon)`: Lands illustrated by Titus Lunter or John Avon.

## References
Use the following references to build the search criterias:

- [Colors and Color Identities](references/colors.md)
- [Card Types](references/card_types.md)
- [Card Text](references/card_text.md)
- [Mana Costs](references/mana.md)
- [Power, Toughness, and Loyalty](references/ptl.md)
- [Multi-faced Cards](references/mf_cards.md)
- [Spells, Permanents, and Effects](references/spe.md)
- [Rarity](references/rarity.md)
- [Sets and Blocks](references/sets_blocks.md)
- [Format Legality](references/format_legality.md)

DON'T LOAD THE SAME RESOURCE MORE THAN ONCE!!

## Expected Output

The search criterias in a single string only without explanation.


