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

## Card Text

Use the o: or oracle: keywords to find cards that have specific phrases in their text box.

You need to put quotes " " around text with punctuation or spaces.

Unless asked for an explicit string, split the requested keywords into separate `oracle:` clause. For example, if looking for a card that "deals 1 damage", generate the following clauses: `o:deals o:1 o:damage`.

You can use ~ in your text as a placeholder for the card’s name.

This keyword usually checks the current Oracle text for cards, so it uses the most up-to-date phrasing available. For example, “dies” instead of “is put into a graveyard”.

Use the fo: or fulloracle: operator to search the full Oracle text, which includes reminder text.

You can also use keyword: or kw: to search for cards with a specific keyword ability.

### Examples

- `o:draw t:creature`: Creatures that deal with drawing cards.
- `o:"~ enters tapped"`: Cards that enter the battlefield tapped.
- `kw:flying -t:creature`: Noncreatures that have the flying keyword.

## Card Types

Find cards of a certain card type with the t: or type: keywords. You can search for any supertype, card type, or subtype.

Using only partial words is allowed.

### Examples

- `t:merfolk t:legend`: Legendary merfolk cards
- `t:goblin -t:creature`: Goblin cards that aren't creatures.

## Colors and Color Identity

You can find cards that are a certain color using the c: or color: keyword, and cards that are a certain color identity using the id: or identity: keywords.

Both sets of keywords accepts full color names like blue or the abbreviated color letters w, u, r, b and g.

You can use many nicknames for color sets: all guild names (e.g. azorius), all shard names (e.g. bant), all college names (e.g., quandrix), all wedge names (e.g. abzan), and the four-color nicknames chaos, aggression, altruism, growth, artifice are supported.

Use c or colorless to match colorless cards, and m or multicolor to match multicolor cards.

You can use comparison expressions (>, <, >=, <=, and !=) to check against ranges of colors. You can also use numbers instead to find cards that have that many colors.

Find cards that have a color indicator with has:indicator.

### Examples

- `c:rg`: Cards that are red and green.
- `color>=uw -c:red`: Cards that are at least white and blue, but not red.
- `id<=esper t:instant`: Instants you can play with an Esper commander.
- `id:c t:land`: Land cards with colorless identity.
- `c=2 is:bear`: 'Bears' that are exactly two colors.

##  Format Legality

Use the f: or format: keywords to find cards that are legal in a given format.

You can also find cards that are explicitly banned in a format with the banned: keyword and restricted with the restricted: keyword.

The current supported formats are: standard, future (Future Standard), historic, timeless, gladiator, pioneer, modern, legacy, pauper, vintage, penny (Penny Dreadful), commander, oathbreaker, standardbrawl, brawl, alchemy, paupercommander, duel (Duel Commander), oldschool (Old School 93/94), premodern, and predh.

You can use is:commander to find cards that can be your commander, is:brawler to find cards that can be your Brawl Commander, is:companion to find Companion cards, is:duelcommander to find cards that can be your Duel Commander, and is:oathbreaker to find cards that can be your Oathbreaker.

You can find cards with any flavor of Commander Partner mechanic with is:partner.

Cards that are Commander Gamechangers can be found using is:gamechanger.

You can find cards on the Reserved List with is:reserved

### Examples

- `c:g t:creature f:pauper`: Green creatures in Pauper format.
- `banned:legacy`: Cards banned in Legacy format.
- `is:commander`: Cards that can be your commander.
- `is:reserved`: Cards on the Reserved List.

## Mana Costs

Use the m: or mana: keyword to search for cards that have certain symbols in their mana costs.

This keyword uses the official text version of mana costs set forth in the Comprehensive Rules. For example, {G} represents a green mana.

Shorthand is allowed for symbols that aren’t split: G is the same as {G}

However, you must always wrap complex/split symbols like {2/G} in braces.

You can search for mana costs using comparison operators; a mana cost is greater than another if it includes all the same symbols and more, and it’s less if it includes only a subset of symbols.

You can find cards of a specific mana value with manavalue or mv, comparing with a numeric expression (>, <, =, >=, <=, and !=). You can also find even or odd mana costs with manavalue:even or manavalue:odd

You can filter cards that contain hybrid mana symbols with is:hybrid or Phyrexian mana symbols with is:phyrexian

You can find permanents that provide specific levels of devotion, using either single-color mana symbols for devotion to one color, or hybrid symbols for devotion to two, with devotion: or a comparison operator.

You can also find cards that produce specific types of mana, with produces:

### Examples

- `mana: {G}{U}`: Cards with one green and blue mana in their costs.
- `m:2WW`: Cards with two generic and two white mana in their cost.
- `m>3WU`: Cards that cost more than three generic, one white, and one blue mana.
- `m:{R/P}`: Cards with one Phyrexian red mana in their cost.
- `c:u mv=5`: Blue cards with mana value 5.
- `devotion:{u/b}{u/b}{u/b}`: Cards that contribute 3 to devotion to black and blue.
- `produces=wu`: Cards that produce blue and white mana.

##  Spells, Permanents, and Effects

Find cards that are cast as spells with is:spell.

Find permanent cards with is:permanent, historic cards with is:historic, creatures that can be in your party with is:party, creatures that are outlaws with is:outlaw, modal effects with is:modal, vanilla creatures with is:vanilla, French vanilla cards with is:frenchvanilla, 2/2/2 “bear” creatures with is:bear, or lands that can turn into creatures with is:manland.

### Examples

- `c>=br is:spell f:duel`: Black and red multicolor spells in Duel Commander
- `is:permanent t:rebel`: Rebel permanents
- `is:vanilla`: Vanilla creatures

## Power, Toughness, and Loyalty

You can use numeric expressions (>, <, =, >=, <=, and !=) to find cards with certain power, power/pow, toughness, toughness/tou, total power and toughness, pt/powtou, or starting loyalty, loyalty/loy.

You can compare the values with each other or with a provided number.

### Examples

- `pow>=8`: Cards with 8 or more power. 
- `power>tou c:w t:creature`: White creatures that are top-heavy.
- `t:planeswalker loy=3`: Planeswalkers that start at 3 loyalty.

# Rarity

Use r: or rarity: to find cards by their print rarity. You can search for common, uncommon, rare, special, mythic, and bonus. You can also use comparison operators like < and >=.

Use new:rarity to find reprint cards printed at a new rarity for the first time. You can find cards that have ever been printed in a given rarity using in: (for example, in:rare to find cards that have ever been printed at rare.)

Cards new to pauper in particular can be found using is:newinpauper.

## Examples

- `r:common t:artifact`: Common artifacts.
- `r>=r`: Cards at rare rarity or above(i.e., rares and mythics).
- `rarity:common e:ima new:rarity`: Cards printed as commons for the first time on Iconic Masters.
- `in:rare -rarity:rare`: Non-rare printings of cards that have been printed at rare.

## Sets and Blocks

Use s:, e:, set:, or edition: to find cards using their Magic set code.

Use cn: or number: to find cards by collector number within a set. Combine this with s: to find specific card editions. Searching by ranges with a syntax like cn>50 is also possible.

Use b: or block: to find cards in a Magic block by providing the three-letter code for any set in that block.

The in: keyword finds cards that once “passed through” the given set code. For example in:lea would only match cards that once appeared in Alpha.

You can search for cards based on the type of product they appear in. This includes the primary product types (st:core, st:expansion, or st:draftinnovation), as well as series of products (st:masters, st:funny, st:commander, st:duel_deck, st:from_the_vault, st:spellbook, or st:premium_deck) and more specialized types (st:alchemy, st:archenemy, st:masterpiece, st:memorabilia, st:planechase, st:promo, st:starter, st:token, st:treasure_chest, or st:vanguard.)

The in: keyword also supports these set types, so you can search for cards with no printings in a set type with a query like -in:core.

You can also search for individual cards that were sold in certain places with is:booster or is:planeswalker_deck, or specific types of promo cards with is: queries like is:league, is:buyabox, is:giftbox, is:intro_pack, is:gameday, is:prerelease, is:release, is:fnm, is:judge_gift, is:arena_league, is:player_rewards, is:media_insert, is:instore, is:convention, or is:set_promo, among others.

### Examples

- `e:war`: Cards from the War of the Spark.
- `e:war is:booster`: Cards available inside War of the Spark booster boxes.
- `b:wwk`: Cards in the Zendikar Block (but using the Worldwake code)
- `in:lea in:m15`: Cards that were in both Alpha and Magic 2015.
- `t:legendary -in:booster`: Legendary cards that have never been printed in a booster set.
- `is:datestamped is:prerelease`: Prerelease promos with a date stamp

## Card Types

Find cards of a certain card type with the t: or type: keywords. You can search for any supertype, card type, or subtype.

Using only partial words is allowed.

### Examples

- `t:merfolk t:legend`: Legendary merfolk cards
- `t:goblin -t:creature`: Goblin cards that aren't creatures.


## Expected Output

The search criterias in a single string only without explanation.


