# Card Text

Use the o: or oracle: keywords to find cards that have specific phrases in their text box.

You can put quotes " " around text with punctuation or spaces.

Unless asked for an explicit string, split the requested keywords into separate `oracle:` clause. For example, if looking for a card that "deals 1 damage", generate the following clauses: `o:deals o:1 o:damage`.

You can use ~ in your text as a placeholder for the card’s name.

This keyword usually checks the current Oracle text for cards, so it uses the most up-to-date phrasing available. For example, “dies” instead of “is put into a graveyard”.

Use the fo: or fulloracle: operator to search the full Oracle text, which includes reminder text.

You can also use keyword: or kw: to search for cards with a specific keyword ability.

## Examples

- `o:draw t:creature`: Creatures that deal with drawing cards.
- `o:"~ enters tapped"`: Cards that enter the battlefield tapped.
- `kw:flying -t:creature`: Noncreatures that have the flying keyword.
