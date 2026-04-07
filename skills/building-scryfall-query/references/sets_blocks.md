# Sets and Blocks

Use s:, e:, set:, or edition: to find cards using their Magic set code.

Use cn: or number: to find cards by collector number within a set. Combine this with s: to find specific card editions. Searching by ranges with a syntax like cn>50 is also possible.

Use b: or block: to find cards in a Magic block by providing the three-letter code for any set in that block.

The in: keyword finds cards that once “passed through” the given set code. For example in:lea would only match cards that once appeared in Alpha.

You can search for cards based on the type of product they appear in. This includes the primary product types (st:core, st:expansion, or st:draftinnovation), as well as series of products (st:masters, st:funny, st:commander, st:duel_deck, st:from_the_vault, st:spellbook, or st:premium_deck) and more specialized types (st:alchemy, st:archenemy, st:masterpiece, st:memorabilia, st:planechase, st:promo, st:starter, st:token, st:treasure_chest, or st:vanguard.)

The in: keyword also supports these set types, so you can search for cards with no printings in a set type with a query like -in:core.

You can also search for individual cards that were sold in certain places with is:booster or is:planeswalker_deck, or specific types of promo cards with is: queries like is:league, is:buyabox, is:giftbox, is:intro_pack, is:gameday, is:prerelease, is:release, is:fnm, is:judge_gift, is:arena_league, is:player_rewards, is:media_insert, is:instore, is:convention, or is:set_promo, among others.

## Examples

- `e:war`: Cards from the War of the Spark.
- `e:war is:booster`: Cards available inside War of the Spark booster boxes.
- `b:wwk`: Cards in the Zendikar Block (but using the Worldwake code)
- `in:lea in:m15`: Cards that were in both Alpha and Magic 2015.
- `t:legendary -in:booster`: Legendary cards that have never been printed in a booster set.
- `is:datestamped is:prerelease`: Prerelease promos with a date stamp
