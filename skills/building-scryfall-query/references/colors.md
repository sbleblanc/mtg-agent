# Colors and Color Identity

You can find cards that are a certain color using the c: or color: keyword, and cards that are a certain color identity using the id: or identity: keywords.

Both sets of keywords accepts full color names like blue or the abbreviated color letters w, u, r, b and g.

You can use many nicknames for color sets: all guild names (e.g. azorius), all shard names (e.g. bant), all college names (e.g., quandrix), all wedge names (e.g. abzan), and the four-color nicknames chaos, aggression, altruism, growth, artifice are supported.

Use c or colorless to match colorless cards, and m or multicolor to match multicolor cards.

You can use comparison expressions (>, <, >=, <=, and !=) to check against ranges of colors. You can also use numbers instead to find cards that have that many colors.

Find cards that have a color indicator with has:indicator.

## Examples

- `c:rg`: Cards that are red and green.
- `color>=uw -c:red`: Cards that are at least white and blue, but not red.
- `id<=esper t:instant`: Instants you can play with an Esper commander.
- `id:c t:land`: Land cards with colorless identity.
- `c=2 is:bear`: 'Bears' that are exactly two colors.
