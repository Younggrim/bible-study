"""Hand-picked Stories & Topics for site search (search.html).

Most people look for a passage by what it is called, not where it is: "the
prodigal son", "David and Goliath", "the armor of God". A word search cannot find
those, because the Bible never uses the name ("prodigal" is not in the text), so
this table maps each common name to its passage(s).

One entry per line:

    Kind | Name | other names, comma separated | references, ; separated | study page (optional)

References use full book names ("1 Samuel 17", "Luke 15:11-32", "Genesis 6:9-9:17").
The first reference is where a tap goes; the rest are shown as parallels.
build_search.py checks every reference resolves to a real chapter page and verse,
and every study link to a real page and section id, and fails if one does not.

To add an entry, add a line and run:  python3 build_search.py
"""

TOPICS = r"""
Parable | The Sower | parable of the soils, four soils, seed on rocky ground | Matthew 13:1-23; Mark 4:1-20; Luke 8:4-15 | parables-of-jesus.html#sower
Parable | The Wheat and the Weeds | wheat and tares, tares | Matthew 13:24-30; Matthew 13:36-43 |
Parable | The Mustard Seed | faith like a mustard seed | Matthew 13:31-32; Mark 4:30-32; Luke 13:18-19 | parables-of-jesus.html#mustard-seed
Parable | The Leaven | yeast in the dough | Matthew 13:33; Luke 13:20-21 |
Parable | The Hidden Treasure | treasure in a field | Matthew 13:44 |
Parable | The Pearl of Great Price | pearl of great value, merchant and the pearl | Matthew 13:45-46 | parables-of-jesus.html#pearl
Parable | The Net | dragnet, fishing net | Matthew 13:47-50 |
Parable | The Lost Sheep | ninety-nine sheep, 99 sheep | Luke 15:3-7; Matthew 18:12-14 | parables-of-jesus.html#lost-sheep
Parable | The Lost Coin | woman and the lost coin | Luke 15:8-10 |
Parable | The Prodigal Son | lost son, two sons, forgiving father, the father who ran | Luke 15:11-32 | parables-of-jesus.html#prodigal-son
Parable | The Good Samaritan | who is my neighbor, love your neighbor | Luke 10:25-37 | parables-of-jesus.html#good-samaritan
Parable | The Talents | bags of gold, faithful servants | Matthew 25:14-30 | parables-of-jesus.html#talents
Parable | The Ten Minas | minas, pounds | Luke 19:11-27 |
Parable | The Ten Virgins | wise and foolish virgins, ten bridesmaids, lamps and oil | Matthew 25:1-13 | parables-of-jesus.html#ten-virgins
Parable | The Wedding Banquet | wedding feast, great banquet, great supper, many are called few are chosen | Matthew 22:1-14; Luke 14:15-24 | parables-of-jesus.html#wedding-banquet
Parable | The Rich Fool | bigger barns | Luke 12:13-21 | parables-of-jesus.html#rich-fool
Parable | The Pharisee and the Tax Collector | publican, God be merciful to me a sinner | Luke 18:9-14 | parables-of-jesus.html#pharisee-tax-collector
Parable | The Unforgiving Servant | unmerciful servant, seventy times seven, how often should I forgive | Matthew 18:21-35 | parables-of-jesus.html#unforgiving-servant
Parable | The Workers in the Vineyard | laborers in the vineyard, the last will be first | Matthew 20:1-16 |
Parable | The Two Sons | two sons in the vineyard | Matthew 21:28-32 |
Parable | The Wicked Tenants | wicked vinedressers, tenants in the vineyard | Matthew 21:33-46; Mark 12:1-12; Luke 20:9-19 |
Parable | The Persistent Widow | unjust judge, pray and not lose heart | Luke 18:1-8 |
Parable | The Friend at Midnight | persistent friend, bread at midnight | Luke 11:5-8 |
Parable | The Rich Man and Lazarus | Lazarus and the rich man, Abraham's bosom | Luke 16:19-31 |
Parable | The Shrewd Manager | unjust steward, dishonest manager | Luke 16:1-13 |
Parable | The Barren Fig Tree | fig tree with no fruit | Luke 13:6-9 |
Parable | The Growing Seed | seed growing secretly | Mark 4:26-29 |
Parable | The Two Debtors | moneylender and two debtors | Luke 7:41-43 |
Parable | The Wise and Foolish Builders | house on the rock, house on the sand | Matthew 7:24-27; Luke 6:46-49 |
Parable | New Wine in Old Wineskins | old wineskins, patch on an old garment | Matthew 9:16-17; Mark 2:21-22; Luke 5:36-39 |
Parable | The Lamp under a Basket | lamp on a stand, let your light shine | Mark 4:21-25; Matthew 5:14-16 |
Parable | The Sheep and the Goats | final judgment, the least of these | Matthew 25:31-46 |
Parable | The Faithful and Wise Servant | faithful servant, wicked servant | Matthew 24:45-51; Luke 12:42-48 |
Parable | The Watchful Servants | be ready, thief in the night | Luke 12:35-40 |
Parable | Counting the Cost | tower builder, king going to war | Luke 14:25-33 |
Parable | The Places at the Table | lowest seat, humble yourself at the feast | Luke 14:7-14 |
Parable | The Unworthy Servants | we are unworthy servants | Luke 17:7-10 |

Miracle | Water into Wine | wedding at Cana, first miracle | John 2:1-11 | miracles-of-jesus.html#water-to-wine
Miracle | Healing the Official's Son | nobleman's son | John 4:46-54 |
Miracle | The Great Catch of Fish | miraculous catch, nets breaking, fishers of men | Luke 5:1-11; John 21:1-14 | miracles-of-jesus.html#great-catch
Miracle | Healing Peter's Mother-in-Law | Peter's mother in law, fever | Mark 1:29-31; Matthew 8:14-15; Luke 4:38-39 |
Miracle | Healing the Leper | leper cleansed, if you are willing | Mark 1:40-45; Matthew 8:1-4; Luke 5:12-16 | miracles-of-jesus.html#healing-leper
Miracle | Healing the Paralytic | paralyzed man through the roof, four friends | Mark 2:1-12; Luke 5:17-26; Matthew 9:1-8 | miracles-of-jesus.html#healing-paralytic
Miracle | The Centurion's Servant | centurion's faith, just say the word | Matthew 8:5-13; Luke 7:1-10 |
Miracle | Raising the Widow's Son at Nain | widow of Nain | Luke 7:11-17 |
Miracle | Calming the Storm | Jesus stills the storm, peace be still | Mark 4:35-41; Matthew 8:23-27; Luke 8:22-25 | miracles-of-jesus.html#calming-storm
Miracle | Casting Out Legion | Gerasene demoniac, Gadarene, demons into pigs, swine | Mark 5:1-20; Luke 8:26-39; Matthew 8:28-34 | miracles-of-jesus.html#casting-out-legion
Miracle | Raising Jairus' Daughter | Jairus, little girl get up, talitha cumi | Mark 5:21-43; Luke 8:40-56 | miracles-of-jesus.html#jairus-daughter
Miracle | The Woman with the Issue of Blood | woman who touched his garment, hem of his robe, bleeding woman | Mark 5:25-34; Luke 8:43-48; Matthew 9:20-22 | miracles-of-jesus.html#woman-bleeding
Miracle | Healing the Man with a Withered Hand | withered hand, healing on the Sabbath | Mark 3:1-6; Matthew 12:9-14; Luke 6:6-11 |
Miracle | Feeding the 5,000 | five loaves and two fish, feeding the five thousand, loaves and fishes | John 6:1-14; Matthew 14:13-21; Mark 6:30-44; Luke 9:10-17 | miracles-of-jesus.html#feeding-5000
Miracle | Walking on Water | Jesus walks on the sea, Peter walks on water | Matthew 14:22-33; Mark 6:45-52; John 6:16-21 | miracles-of-jesus.html#walking-on-water
Miracle | The Syrophoenician Woman's Daughter | Canaanite woman, crumbs from the table | Mark 7:24-30; Matthew 15:21-28 |
Miracle | Healing the Deaf Man | ephphatha, be opened | Mark 7:31-37 |
Miracle | Feeding the 4,000 | seven loaves, feeding the four thousand | Mark 8:1-10; Matthew 15:32-39 |
Miracle | Healing the Blind Man at Bethsaida | men like trees walking | Mark 8:22-26 |
Miracle | Healing the Boy with a Demon | I believe help my unbelief | Mark 9:14-29; Matthew 17:14-21; Luke 9:37-43 |
Miracle | The Coin in the Fish's Mouth | temple tax | Matthew 17:24-27 |
Miracle | Healing the Man Born Blind | I was blind but now I see, mud on his eyes, pool of Siloam | John 9:1-41 | miracles-of-jesus.html#healing-blind
Miracle | Healing at the Pool of Bethesda | take up your mat and walk, 38 years | John 5:1-15 |
Miracle | Healing the Ten Lepers | one came back to give thanks | Luke 17:11-19 |
Miracle | Healing the Crippled Woman | bent over woman, eighteen years | Luke 13:10-17 |
Miracle | Blind Bartimaeus | son of David have mercy on me | Mark 10:46-52; Luke 18:35-43; Matthew 20:29-34 |
Miracle | Raising Lazarus | Lazarus come out, Jesus wept, I am the resurrection | John 11:1-44 | miracles-of-jesus.html#raising-lazarus
Miracle | Cursing the Fig Tree | withered fig tree | Mark 11:12-14; Mark 11:20-25; Matthew 21:18-22 |
Miracle | Healing Malchus' Ear | servant's ear cut off | Luke 22:49-51; John 18:10-11 |

Story | Creation | in the beginning, six days, God created | Genesis 1:1-2:3 |
Story | Adam and Eve | Garden of Eden, creation of woman, first man | Genesis 2:4-25 |
Story | The Fall | forbidden fruit, the serpent, original sin, tree of knowledge | Genesis 3:1-24 | covenants.html#adamic-covenant
Story | Cain and Abel | first murder, am I my brother's keeper | Genesis 4:1-16 |
Story | Noah's Ark | the flood, Noah, the ark, rainbow | Genesis 6:9-9:17 | covenants.html#noahic-covenant
Story | The Tower of Babel | confusion of languages | Genesis 11:1-9 |
Story | The Call of Abram | Abraham leaves Ur, I will make you a great nation | Genesis 12:1-9 | covenants.html#abrahamic-covenant
Story | God's Covenant with Abraham | stars in the sky, counted as righteousness | Genesis 15:1-21 | covenants.html#abrahamic-covenant
Story | Hagar and Ishmael | the God who sees me, El Roi | Genesis 16:1-16; Genesis 21:8-21 |
Story | Sodom and Gomorrah | Lot's wife, pillar of salt, Abraham pleads for Sodom | Genesis 18:16-19:29 |
Story | The Binding of Isaac | Abraham sacrifices Isaac, Mount Moriah, God will provide a lamb | Genesis 22:1-19 | types-of-christ.html#isaac
Story | Isaac and Rebekah | a wife for Isaac, Abraham's servant at the well | Genesis 24:1-67 |
Story | Esau Sells His Birthright | bowl of stew, Jacob and Esau | Genesis 25:19-34 |
Story | Jacob Steals the Blessing | Jacob deceives Isaac | Genesis 27:1-45 |
Story | Jacob's Ladder | stairway to heaven, Bethel dream | Genesis 28:10-22 |
Story | Jacob Marries Leah and Rachel | Laban, seven years for Rachel | Genesis 29:1-30 |
Story | Jacob Wrestles with God | Jacob becomes Israel, Peniel | Genesis 32:22-32 |
Story | Joseph's Coat and His Brothers | coat of many colors, Joseph sold into slavery, Joseph's dreams | Genesis 37:1-36 | men-of-the-bible.html#joseph
Story | Joseph and Potiphar's Wife | Joseph in prison | Genesis 39:1-23 |
Story | Joseph Interprets Pharaoh's Dreams | seven years of famine, fat and thin cows | Genesis 41:1-57 |
Story | Joseph Reveals Himself to His Brothers | you meant it for evil God meant it for good | Genesis 45:1-15; Genesis 50:15-21 | types-of-christ.html#joseph
Story | Baby Moses in the Basket | Moses in the reeds, Pharaoh's daughter | Exodus 2:1-10 | men-of-the-bible.html#moses
Story | The Burning Bush | I AM WHO I AM, Moses called, holy ground | Exodus 3:1-4:17 | names-of-god.html
Story | The Ten Plagues | let my people go, plagues of Egypt, frogs, locusts | Exodus 7:14-11:10 |
Story | The Passover | blood on the doorposts, angel of death, Passover lamb | Exodus 12:1-32 | types-of-christ.html#passover-lamb
Story | Crossing the Red Sea | parting of the Red Sea, Moses parts the sea | Exodus 14:1-31 |
Story | Manna and Quail | bread from heaven | Exodus 16:1-36 | types-of-christ.html#manna
Story | Water from the Rock | Moses strikes the rock, Massah and Meribah | Exodus 17:1-7; Numbers 20:1-13 | types-of-christ.html#rock-at-horeb
Story | The Ten Commandments Given | Mount Sinai, tablets of stone, the law given | Exodus 20:1-17; Deuteronomy 5:6-21 | ten-commandments.html
Story | The Golden Calf | Aaron's calf, idol at Sinai, broken tablets | Exodus 32:1-35 |
Story | The Tabernacle | ark of the covenant, holy of holies, tent of meeting | Exodus 25:1-40; Exodus 40:1-38 | types-of-christ.html#tabernacle
Story | The Day of Atonement | scapegoat, Yom Kippur | Leviticus 16:1-34 | types-of-christ.html#scapegoat
Story | The Priestly Blessing | the Lord bless you and keep you | Numbers 6:22-27 |
Story | The Twelve Spies | Joshua and Caleb, giants in the land, forty years in the wilderness | Numbers 13:1-14:45 |
Story | The Bronze Serpent | snake on a pole, fiery serpents | Numbers 21:4-9 | types-of-christ.html#bronze-serpent
Story | Balaam's Donkey | talking donkey | Numbers 22:21-35 |
Story | The Shema | hear O Israel, love the Lord your God with all your heart | Deuteronomy 6:4-9 |
Story | Rahab and the Spies | scarlet cord | Joshua 2:1-24 | women-of-the-bible.html#rahab
Story | Crossing the Jordan | memorial stones, twelve stones | Joshua 3:1-4:24 |
Story | The Walls of Jericho | Joshua fought the battle of Jericho, walls fall down | Joshua 6:1-27 | men-of-the-bible.html#joshua
Story | The Sun Stands Still | Joshua's long day | Joshua 10:1-15 |
Story | Choose This Day Whom You Will Serve | as for me and my house | Joshua 24:14-15 |
Story | Deborah and Barak | Jael and Sisera, tent peg | Judges 4:1-5:31 | judges-of-israel.html#deborah
Story | Gideon's Fleece | Gideon, wet fleece | Judges 6:1-40 | judges-of-israel.html#gideon
Story | Gideon's 300 | trumpets and jars, lapping water | Judges 7:1-25 | judges-of-israel.html#gideon
Story | Samson and Delilah | Samson's hair, Samson's strength | Judges 16:1-31 | judges-of-israel.html#samson
Story | Ruth and Naomi | where you go I will go, your people will be my people | Ruth 1:1-22 | women-of-the-bible.html#ruth
Story | Ruth and Boaz | kinsman redeemer, gleaning in the fields | Ruth 2:1-4:22 | women-of-the-bible.html#ruth
Story | Hannah's Prayer for a Son | birth of Samuel | 1 Samuel 1:1-2:11 | prayers-in-the-bible.html#hannah
Story | God Calls Samuel | speak Lord for your servant is listening | 1 Samuel 3:1-21 |
Story | Israel Asks for a King | give us a king | 1 Samuel 8:1-22 | kings-of-israel.html#saul
Story | Samuel Anoints David | man looks on the outward appearance, the Lord looks on the heart | 1 Samuel 16:1-13 | men-of-the-bible.html#david
Story | David and Goliath | giant, sling and stone, Philistine | 1 Samuel 17:1-58 | men-of-the-bible.html#david
Story | David and Jonathan | covenant friendship | 1 Samuel 18:1-4; 1 Samuel 20:1-42 |
Story | David Spares Saul | cave at En Gedi, the Lord's anointed | 1 Samuel 24:1-22; 1 Samuel 26:1-25 |
Story | Saul and the Medium of Endor | witch of Endor | 1 Samuel 28:3-25 |
Story | David Dances before the Ark | ark brought to Jerusalem, Uzzah | 2 Samuel 6:1-23 |
Story | God's Covenant with David | Davidic covenant, your throne established forever | 2 Samuel 7:1-29 | covenants.html#davidic-covenant
Story | David and Mephibosheth | kindness to Jonathan's son, the king's table | 2 Samuel 9:1-13 |
Story | David and Bathsheba | Uriah the Hittite, David's sin | 2 Samuel 11:1-27 |
Story | Nathan Confronts David | you are the man, the poor man's lamb | 2 Samuel 12:1-25 |
Story | David's Prayer of Repentance | create in me a clean heart, Psalm 51 | Psalms 51:1-19 | prayers-in-the-bible.html#david-repentance
Story | Absalom's Rebellion | O Absalom my son | 2 Samuel 15:1-18:33 |
Story | Solomon Asks for Wisdom | wisdom of Solomon | 1 Kings 3:1-15 | prayers-in-the-bible.html#solomon-wisdom
Story | Solomon and the Two Mothers | cut the baby in half, Solomon's judgment | 1 Kings 3:16-28 | kings-of-israel.html#solomon
Story | Solomon Dedicates the Temple | building the temple, Solomon's prayer | 1 Kings 8:1-66; 2 Chronicles 7:1-22 |
Story | The Queen of Sheba | | 1 Kings 10:1-13 |
Story | The Kingdom Divides | Rehoboam and Jeroboam, ten tribes | 1 Kings 12:1-33 | kings-of-israel.html#rehoboam
Story | Elijah Fed by Ravens | brook Cherith | 1 Kings 17:1-7 | men-of-the-bible.html#elijah
Story | Elijah and the Widow of Zarephath | flour and oil that did not run out | 1 Kings 17:8-24 |
Story | Elijah on Mount Carmel | prophets of Baal, fire from heaven | 1 Kings 18:16-46 | men-of-the-bible.html#elijah
Story | The Still Small Voice | Elijah at Horeb, gentle whisper, Elijah under the broom tree | 1 Kings 19:1-18 |
Story | Naboth's Vineyard | Ahab and Jezebel | 1 Kings 21:1-29 | kings-of-israel.html#ahab
Story | Elijah Taken Up in a Whirlwind | chariot of fire, Elisha's double portion | 2 Kings 2:1-14 |
Story | Elisha and the Widow's Oil | jars of oil | 2 Kings 4:1-7 |
Story | Elisha and the Shunammite's Son | Shunammite woman | 2 Kings 4:8-37 |
Story | Naaman Healed of Leprosy | wash in the Jordan seven times | 2 Kings 5:1-27 |
Story | The Floating Axe Head | | 2 Kings 6:1-7 |
Story | Horses and Chariots of Fire | open his eyes, those with us are more | 2 Kings 6:8-23 |
Story | Hezekiah and Sennacherib | Assyrian army, angel of the Lord struck the camp | 2 Kings 18:13-19:37; Isaiah 36:1-37:38 | kings-of-israel.html#hezekiah
Story | Hezekiah's Illness | fifteen years added, shadow on the sundial | 2 Kings 20:1-11; Isaiah 38:1-22 |
Story | Josiah Finds the Book of the Law | Josiah's reforms | 2 Kings 22:1-23:30 | kings-of-israel.html#josiah
Story | The Fall of Jerusalem | exile to Babylon, Nebuchadnezzar destroys the temple | 2 Kings 25:1-30 |
Story | The Prayer of Jabez | enlarge my territory | 1 Chronicles 4:9-10 | prayers-in-the-bible.html#jabez
Story | If My People Who Are Called by My Name | humble themselves and pray | 2 Chronicles 7:14 |
Story | Rebuilding the Temple | return from exile, Zerubbabel | Ezra 3:1-13 |
Story | Nehemiah Rebuilds the Wall | walls of Jerusalem | Nehemiah 2:1-6:16 |
Story | Ezra Reads the Law | the joy of the Lord is your strength | Nehemiah 8:1-18 |
Story | For Such a Time as This | Esther and Mordecai | Esther 4:1-17 | women-of-the-bible.html#esther
Story | Esther Goes before the King | if I perish I perish | Esther 5:1-14 |
Story | Haman's Downfall | Haman hanged on his own gallows | Esther 7:1-10 |
Story | Purim | | Esther 9:1-32 |
Story | Job's Suffering | Satan tests Job, the Lord gave and the Lord has taken away | Job 1:1-2:13 | suffering.html
Story | God Answers Job from the Whirlwind | where were you when I laid the foundations | Job 38:1-42:17 |
Story | Isaiah's Call | here am I send me, holy holy holy, coal on his lips | Isaiah 6:1-13 |
Story | Jeremiah's Call | before I formed you in the womb | Jeremiah 1:1-19 |
Story | The Potter and the Clay | potter's house | Jeremiah 18:1-12 |
Story | The Valley of Dry Bones | dry bones live | Ezekiel 37:1-14 |
Story | Daniel Refuses the King's Food | vegetables and water, Daniel's diet | Daniel 1:1-21 | men-of-the-bible.html#daniel
Story | Nebuchadnezzar's Dream of the Statue | statue of gold silver bronze iron and clay | Daniel 2:1-49 |
Story | The Fiery Furnace | Shadrach Meshach and Abednego, fourth man in the fire | Daniel 3:1-30 |
Story | Nebuchadnezzar's Madness | king eats grass like an ox | Daniel 4:1-37 |
Story | The Handwriting on the Wall | Belshazzar's feast, mene mene tekel | Daniel 5:1-31 |
Story | Daniel in the Lions' Den | lions den | Daniel 6:1-28 | men-of-the-bible.html#daniel
Story | Daniel's Seventy Weeks | seventy sevens | Daniel 9:20-27 | prayers-in-the-bible.html#daniel
Story | Hosea and Gomer | unfaithful wife, Hosea buys back his wife | Hosea 1:1-3:5 |
Story | Jonah and the Big Fish | Jonah and the whale, Jonah runs from God | Jonah 1:1-2:10 | types-of-christ.html#jonah
Story | Jonah and Nineveh | Jonah's anger, the vine | Jonah 3:1-4:11 |

Story | The Genealogy of Jesus | family tree of Jesus | Matthew 1:1-17; Luke 3:23-38 |
Story | The Annunciation | angel Gabriel visits Mary, let it be to me | Luke 1:26-38 | women-of-the-bible.html#mary-mother
Story | Mary Visits Elizabeth | the Magnificat, my soul magnifies the Lord | Luke 1:39-56 |
Story | The Birth of John the Baptist | Zechariah struck mute, Benedictus | Luke 1:5-25; Luke 1:57-80 |
Story | The Birth of Jesus | Christmas, nativity, no room at the inn, manger, Bethlehem | Luke 2:1-20; Matthew 1:18-25 | prophecy-and-fulfillment.html#bethlehem
Story | The Shepherds and the Angels | glory to God in the highest, good news of great joy | Luke 2:8-20 |
Story | The Wise Men | Magi, star of Bethlehem, gold frankincense and myrrh | Matthew 2:1-12 |
Story | The Flight to Egypt | Herod kills the babies, escape to Egypt | Matthew 2:13-23 |
Story | Jesus Presented at the Temple | Simeon and Anna, Nunc Dimittis | Luke 2:22-40 |
Story | The Boy Jesus in the Temple | my Father's house, Jesus at twelve | Luke 2:41-52 |
Story | John the Baptist Prepares the Way | voice crying in the wilderness, brood of vipers, repent | Matthew 3:1-12; Luke 3:1-20 |
Story | The Baptism of Jesus | this is my beloved Son, dove, Jesus baptized | Matthew 3:13-17; Mark 1:9-11; Luke 3:21-22 | the-trinity.html
Story | The Temptation of Jesus | Jesus tempted in the wilderness, forty days, man shall not live by bread alone | Matthew 4:1-11; Luke 4:1-13 | temptation.html
Story | Jesus Calls the First Disciples | fishers of men, follow me | Matthew 4:18-22; Mark 1:16-20 | the-12-apostles.html
Story | Jesus Rejected at Nazareth | the Spirit of the Lord is upon me, a prophet without honor | Luke 4:16-30 |
Story | Jesus Clears the Temple | money changers, den of thieves, cleansing the temple | John 2:13-22; Matthew 21:12-17 |
Story | Jesus and Nicodemus | born again, born of water and the Spirit | John 3:1-21 |
Story | For God So Loved the World | John 3:16 | John 3:16-17 | the-gospel.html
Story | The Woman at the Well | Samaritan woman, living water | John 4:1-42 |
Story | The Sermon on the Mount | | Matthew 5:1-7:29 |
Story | The Beatitudes | blessed are the poor in spirit | Matthew 5:3-12; Luke 6:20-23 | beatitudes.html
Story | Salt and Light | you are the salt of the earth, light of the world, city on a hill | Matthew 5:13-16 |
Story | Love Your Enemies | turn the other cheek, go the extra mile | Matthew 5:38-48; Luke 6:27-36 |
Story | The Lord's Prayer | Our Father, how to pray | Matthew 6:9-13; Luke 11:1-4 | prayers-in-the-bible.html#lords-prayer
Story | Treasures in Heaven | where your treasure is, you cannot serve God and money | Matthew 6:19-24 | greed-and-materialism.html
Story | Do Not Worry | consider the lilies, birds of the air, seek first the kingdom | Matthew 6:25-34; Luke 12:22-34 | anxiety-and-fear.html
Story | Judge Not | speck and the log, plank in your eye | Matthew 7:1-5; Luke 6:37-42 |
Story | Ask, Seek, Knock | ask and it will be given | Matthew 7:7-11 |
Story | The Golden Rule | do unto others | Matthew 7:12; Luke 6:31 |
Story | The Narrow Gate | narrow road, wide gate | Matthew 7:13-14 |
Story | The Calling of Matthew | Levi the tax collector, I came to call sinners | Matthew 9:9-13; Mark 2:13-17; Luke 5:27-32 | the-12-apostles.html#matthew
Story | Jesus Sends Out the Twelve | the harvest is plentiful, sheep among wolves | Matthew 10:1-42; Matthew 9:35-38 |
Story | Come to Me, All Who Are Weary | my yoke is easy, rest for your souls | Matthew 11:28-30 |
Story | The Sinful Woman Anoints Jesus | woman with the alabaster jar at Simon's house | Luke 7:36-50 |
Story | Mary and Martha | Martha distracted, the one thing needed | Luke 10:38-42 |
Story | Peter's Confession | you are the Christ, upon this rock, keys of the kingdom | Matthew 16:13-20; Mark 8:27-30 | the-12-apostles.html#simon-peter
Story | Take Up Your Cross | deny yourself, lose your life to find it | Matthew 16:24-26; Luke 9:23-25; Mark 8:34-38 |
Story | The Transfiguration | Moses and Elijah on the mountain, Jesus' face shone | Matthew 17:1-13; Mark 9:2-13; Luke 9:28-36 |
Story | The Woman Caught in Adultery | let him who is without sin cast the first stone, go and sin no more | John 8:1-11 |
Story | The Good Shepherd | I am the good shepherd, lays down his life for the sheep | John 10:1-18 | i-am-statements.html#good-shepherd
Story | Let the Little Children Come | Jesus blesses the children | Mark 10:13-16; Matthew 19:13-15 |
Story | The Rich Young Ruler | camel through the eye of a needle | Mark 10:17-31; Matthew 19:16-30; Luke 18:18-30 | greed-and-materialism.html
Story | Zacchaeus | wee little man, sycamore tree, tax collector | Luke 19:1-10 |
Story | The Greatest Commandment | love the Lord your God, love your neighbor as yourself | Matthew 22:34-40; Mark 12:28-34 |
Story | Render to Caesar | taxes to Caesar | Matthew 22:15-22; Mark 12:13-17 |
Story | The Widow's Offering | widow's mite, two small coins | Mark 12:41-44; Luke 21:1-4 |
Story | Mary Anoints Jesus at Bethany | perfume, nard | John 12:1-8; Mark 14:3-9 |
Story | The Triumphal Entry | Palm Sunday, hosanna, Jesus rides a donkey | Matthew 21:1-11; Mark 11:1-11; Luke 19:28-44; John 12:12-19 | prophecy-and-fulfillment.html#triumphal-entry
Story | The Olivet Discourse | signs of the end times, wars and rumors of wars, second coming | Matthew 24:1-51; Mark 13:1-37; Luke 21:5-36 |
Story | Jesus Washes the Disciples' Feet | foot washing, servant leadership | John 13:1-17 |
Story | The Last Supper | Lord's Supper, communion, this is my body, do this in remembrance | Matthew 26:17-30; Luke 22:7-23; Mark 14:12-26; 1 Corinthians 11:23-26 | covenants.html#new-covenant
Story | The Upper Room Discourse | let not your hearts be troubled, I am the way the truth and the life, the Helper | John 14:1-31 | i-am-statements.html#way-truth-life
Story | The Vine and the Branches | I am the true vine, abide in me | John 15:1-17 | i-am-statements.html#true-vine
Story | Jesus' High Priestly Prayer | that they may be one | John 17:1-26 |
Story | Jesus Prays in Gethsemane | not my will but yours, Garden of Gethsemane | Matthew 26:36-46; Luke 22:39-46; Mark 14:32-42 | prayers-in-the-bible.html#gethsemane
Story | Judas Betrays Jesus | kiss of Judas, thirty pieces of silver, arrest of Jesus | Matthew 26:14-16; Matthew 26:47-56; John 18:1-11 | the-12-apostles.html#judas-iscariot
Story | Peter Denies Jesus | rooster crows, three denials | Matthew 26:69-75; Luke 22:54-62; John 18:15-27 |
Story | Jesus before Pilate | what is truth, Barabbas, crucify him | John 18:28-19:16; Matthew 27:11-26; Luke 23:1-25 |
Story | The Crucifixion | Good Friday, Jesus dies on the cross, Golgotha, Calvary | Matthew 27:32-56; Mark 15:21-41; Luke 23:26-49; John 19:16-37 | prophecy-and-fulfillment.html#crucifixion
Story | It Is Finished | last words of Jesus, my God why have you forsaken me | John 19:28-30; Matthew 27:45-50 |
Story | The Thief on the Cross | today you will be with me in paradise | Luke 23:39-43 |
Story | The Burial of Jesus | Joseph of Arimathea, guards at the tomb | Matthew 27:57-66; John 19:38-42 |
Story | The Resurrection | Easter, empty tomb, he is risen | Matthew 28:1-10; Mark 16:1-8; Luke 24:1-12; John 20:1-18 | prophecy-and-fulfillment.html#resurrection
Story | Mary Magdalene at the Tomb | Jesus appears to Mary | John 20:11-18 | women-of-the-bible.html#mary-magdalene
Story | The Road to Emmaus | did not our hearts burn | Luke 24:13-35 |
Story | Doubting Thomas | my Lord and my God, put your finger here | John 20:24-29 | the-12-apostles.html#thomas
Story | Jesus Restores Peter | do you love me, feed my sheep, breakfast on the beach | John 21:15-19 |
Story | The Great Commission | go and make disciples of all nations | Matthew 28:16-20; Mark 16:15 |
Story | The Ascension | Jesus taken up into heaven | Acts 1:6-11; Luke 24:50-53 |
Story | Pentecost | Holy Spirit comes, tongues of fire, Peter's sermon, 3,000 saved | Acts 2:1-47 | gifts-of-the-holy-spirit.html
Story | Peter and John Heal the Lame Man | silver and gold have I none, Beautiful Gate | Acts 3:1-26 |
Story | Ananias and Sapphira | lying to the Holy Spirit | Acts 5:1-11 |
Story | The Stoning of Stephen | first martyr | Acts 6:8-7:60 | prayers-in-the-bible.html#stephen
Story | Philip and the Ethiopian | Ethiopian eunuch | Acts 8:26-40 |
Story | The Conversion of Saul | road to Damascus, Paul's conversion, scales fell from his eyes | Acts 9:1-19 | men-of-the-bible.html#paul
Story | Peter's Vision and Cornelius | sheet from heaven, unclean animals, gospel to the Gentiles | Acts 10:1-48 |
Story | Peter Freed from Prison | angel frees Peter, Rhoda | Acts 12:1-19 |
Story | Paul's First Missionary Journey | Paul and Barnabas | Acts 13:1-14:28 |
Story | The Jerusalem Council | circumcision debate | Acts 15:1-35 |
Story | Paul and Silas in Prison | Philippian jailer, singing in prison, earthquake, what must I do to be saved | Acts 16:16-40 |
Story | Paul at Athens | Mars Hill, to an unknown god, Areopagus | Acts 17:16-34 |
Story | Paul's Shipwreck | storm at sea, Malta, snake bite | Acts 27:1-28:10 |

Teaching | The Romans Road | all have sinned, the wages of sin is death, how to be saved | Romans 3:23; Romans 6:23; Romans 5:8; Romans 10:9-10 | the-gospel.html
Teaching | Justified by Faith | no one is righteous, righteousness of God through faith | Romans 3:21-26; Romans 5:1-11 | the-gospel.html
Teaching | Nothing Can Separate Us from God's Love | more than conquerors, if God is for us | Romans 8:31-39 |
Teaching | All Things Work Together for Good | Romans 8:28 | Romans 8:28-30 | promises-of-god.html
Teaching | A Living Sacrifice | renew your mind, be transformed, do not be conformed | Romans 12:1-2 |
Teaching | The Love Chapter | love is patient love is kind, faith hope and love | 1 Corinthians 13:1-13 |
Teaching | The Body of Christ | many members one body, spiritual gifts | 1 Corinthians 12:1-31 | gifts-of-the-holy-spirit.html
Teaching | The Resurrection Chapter | O death where is your sting | 1 Corinthians 15:1-58 |
Teaching | A New Creation | the old has gone the new has come | 2 Corinthians 5:17-21 | identity-and-self-worth.html
Teaching | Paul's Thorn in the Flesh | my grace is sufficient, power made perfect in weakness | 2 Corinthians 12:7-10 | suffering.html
Teaching | The Fruit of the Spirit | love joy peace patience | Galatians 5:16-26 | fruits-of-the-spirit.html
Teaching | Saved by Grace through Faith | not by works | Ephesians 2:1-10 | the-gospel.html
Teaching | Husbands and Wives | wives submit, husbands love your wives as Christ loved the church | Ephesians 5:21-33 | marriage-and-family.html
Teaching | The Armor of God | belt of truth, breastplate of righteousness, shield of faith, sword of the Spirit | Ephesians 6:10-20 | armor-of-god.html
Teaching | The Humility of Christ | Christ emptied himself, every knee will bow | Philippians 2:1-11 | pride.html
Teaching | Do Not Be Anxious about Anything | peace that passes understanding | Philippians 4:4-9 | anxiety-and-fear.html
Teaching | I Can Do All Things through Christ | contentment, secret of being content | Philippians 4:10-13 |
Teaching | The Coming of the Lord | rapture, caught up in the clouds, dead in Christ will rise | 1 Thessalonians 4:13-18 |
Teaching | All Scripture Is God-Breathed | inspiration of Scripture | 2 Timothy 3:14-17 | spiritual-disciplines.html
Teaching | The Hall of Faith | faith chapter, faith is the assurance of things hoped for | Hebrews 11:1-40 |
Teaching | Run the Race | cloud of witnesses, looking to Jesus | Hebrews 12:1-3 |
Teaching | Count It All Joy | trials, testing of your faith | James 1:2-18 | suffering.html
Teaching | Faith without Works Is Dead | faith and works | James 2:14-26 |
Teaching | Taming the Tongue | the tongue is a fire | James 3:1-12 | anger.html
Teaching | Always Be Ready to Give an Answer | reason for the hope | 1 Peter 3:15 |
Teaching | If We Confess Our Sins | he is faithful and just to forgive | 1 John 1:5-10 | unforgiveness-and-bitterness.html
Teaching | God Is Love | perfect love casts out fear | 1 John 4:7-21 | attributes-of-god.html
Teaching | The Lord Is My Shepherd | Psalm 23, valley of the shadow of death | Psalms 23:1-6 | i-am-statements.html#good-shepherd
Teaching | Psalm 91 | shelter of the Most High, under his wings | Psalms 91:1-16 | promises-of-god.html
Teaching | Psalm 139 | fearfully and wonderfully made, you knit me together | Psalms 139:1-24 | identity-and-self-worth.html
Teaching | Trust in the Lord with All Your Heart | lean not on your own understanding | Proverbs 3:5-6 |
Teaching | The Wife of Noble Character | Proverbs 31 woman, virtuous woman | Proverbs 31:10-31 | marriage-and-family.html
Teaching | A Time for Everything | a time to be born and a time to die | Ecclesiastes 3:1-8 |
Teaching | Unto Us a Child Is Born | Wonderful Counselor, Prince of Peace | Isaiah 9:6-7 | prophecy-and-fulfillment.html
Teaching | Immanuel | virgin shall conceive | Isaiah 7:14 | prophecy-and-fulfillment.html#virgin-birth
Teaching | They Shall Mount Up with Wings like Eagles | those who wait on the Lord | Isaiah 40:28-31 |
Teaching | Fear Not, for I Am with You | I will strengthen you, my righteous right hand | Isaiah 41:10 | anxiety-and-fear.html
Teaching | The Suffering Servant | by his wounds we are healed, he was pierced for our transgressions | Isaiah 52:13-53:12 | prophecy-and-fulfillment.html#suffering-servant
Teaching | Plans to Prosper You | I know the plans I have for you | Jeremiah 29:11-14 | promises-of-god.html
Teaching | The New Covenant | I will write my law on their hearts | Jeremiah 31:31-34 | covenants.html#new-covenant
Teaching | His Mercies Are New Every Morning | great is your faithfulness | Lamentations 3:22-24 | grief-and-loss.html
Teaching | Do Justice, Love Mercy, Walk Humbly | what does the Lord require | Micah 6:8 |
Teaching | Born in Bethlehem | ruler from Bethlehem | Micah 5:2 | prophecy-and-fulfillment.html#bethlehem
Teaching | Bring the Whole Tithe | storehouse, test me in this | Malachi 3:8-12 | greed-and-materialism.html
Teaching | The Letters to the Seven Churches | Ephesus, Laodicea, lukewarm, first love | Revelation 2:1-3:22 |
Teaching | The Throne Room of Heaven | holy holy holy, the Lamb who was slain, worthy is the Lamb | Revelation 4:1-5:14 |
Teaching | The Four Horsemen | seven seals | Revelation 6:1-17 |
Teaching | The Mark of the Beast | 666, the beast from the sea | Revelation 13:1-18 |
Teaching | The Millennium | thousand years, Satan bound | Revelation 20:1-10 |
Teaching | The Great White Throne | final judgment, book of life | Revelation 20:11-15 |
Teaching | The New Heaven and New Earth | no more tears, new Jerusalem, streets of gold | Revelation 21:1-22:5 |
"""
