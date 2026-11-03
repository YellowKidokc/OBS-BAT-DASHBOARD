---
tags:
  - CSS
use: More Options for callouts
---
## What this does?
Gives you more options for callouts other than the default Obsidian ones.

## Example:
![[22455.png]]

### Implementation
# Never Too Many Callouts?

> [!task]- Task, Checkmark, Checkbox, Checkcircle
> Contents

> [!read]- Read, Book, Lecture
> Contents

> [!show]- Watch, TV, Show, Serie
> Contents

> [!music]- Listen, Music, Lyrics, Song, Songs
> Contents

> [!doing]- Doing, Heartbeat, Activity
> Contents

> [!reading]- Reading
> Contents

> [!watching]- Watching, Netflix, Chill
> Contents

> [!listening]- Listening
> Contents

> [!date]- Date, Meeting, Calendar
> Contents

> [!time]- Time, Hour, Clock
> Contents

> [!mention]- Mention
> Contents

> [!receipt]- Receipt, Invoice
> Contents

> [!recycle]- Recycle, Nature
> Contents

> [!inbox]- Inbox
> Contents

> [!desk]- Desk, Lamp, Reflection
> Contents

> [!leaf]- Leaf, Tree, Evergreen
> Contents

> [!snow]- Snow, Cold, Snowflake
> Contents

> [!sun]- Sun, Hot, Bright, Light
> Contents

> [!sprout]- Sprout, Evergreen, Seed
> Contents

> [!sticky]- Sticker, Sticky-Note, Sticky, Note
> Contents

> [!store]- Store
> Contents

> [!dinner]- Restaurant, Dinner, Utensils, Fork, Lunch
> Contents

> [!video]- YouTube, YT, Video, YouTuber, Channel
> ![Conversation with an engineer](https://youtu.be/P9BUyWVg1xI?feature=shared)

> [!twitter]- Twitter, Twit, Tweet, Tuit, X
> Contents

> [!shopping]- Shopping, Kart, Cart, Grocery, Groceries
> Contents

> [!ai]- AI, Artificial-Intelligence, Sparkle, Sparkles
> Contents

> [!lock]- Lock, Private, Privacy
> Contents

> [!mail]- Gmail, Email, Mail
> Contents

> [!whatsapp]- Message, Messages, WhatsApp, Signal
> Contents

> [!pin]- Location, Pin, Place
> Contents

> [!map]- Map
> Contents

> [!rest]- Beach, Rest, Holidays, Vacation
> Contents

> [!art]- Design, Art, Artistic
> Contents

> [!moon]- Moon, Night, Midnight
> Contents

> [!path]- Mountain, Hiking, Hiker, Path, Walking
> Contents

> [!tool]- Wrench, Tool
> Contents

> [!cook]- Recipe, Cooking, Cook, Chef
> Contents

> [!apps]- App, Apps, Application, Plugin
> Contents

> [!ingredients]- Ingredient, Ingredients
> Contents

> [!box]- Box, Package, Packages, Delivery
> Contents

> [!paper]- Paper, Paperclip, Doc, Docs, Document
> Contents

> [!party]- Party, Popper, Fiesta, Celebration
> Contents

> [!archive]- Archive, Property, Properties
> Contents

> [!heart]- Health, Heart
> Contents

> [!bot]- Bot, Robot
> Contents

> [!projects]- Projects
> Contents

> [!project]- Project
> Contents

> [!code]- Code, Snippet
> Contents

> [!command]- Command, Shortcut, Hotkey
> Contents

> [!contact]- Contact, People, Team, Crew, Users
> Contents

> [!goal]- Effort, Efforts, Milestone, Meta, Goal
> Contents

> [!earth]- Planet, Earth
> Contents

> [!compass]- Navigation, Navigator, Compass
> Contents

> [!dice]- Dice, Dices, Role
> Contents

> [!game]- Game, Gaming, Videogame
> Contents

> [!star]- Star, Favorite, Favourite
> Contents

> [!bookmark]- Bookmark, Bookmarks
> Contents

> [!link]- Link, Links, Reference, References
> Contents

> [!tables]- Table, Tables
> Contents

> [!toc]- Empty, #, Transparent, Void, Heading, Title, TOC
> Contents


# Callout Colors

> [!blue]- Blue
> Contents

> [!cyan]- Cyan
> Contents

> [!red]- Red
> Contents

> [!purple]- Purple
> Contents

> [!magenta]- Magenta
> Contents

> [!pink]- Pink
> Contents

> [!orange]- Orange
> Contents

> [!yellow]- Yellow
> Contents

> [!mist]- Mist
> Contents

> [!green]- Green
> Contents

> [!lemon]- Lemon
> Contents

> [!apple]- Apple
> Contents

> [!grey]- Grey
> Contents

> [!tan]- Tan
> Contents

> [!none]- No, None
> Contents


# Callout Colors no Icon

> [!bluex]- BlueX
> Contents

> [!cyanx]- CyanX
> Contents

> [!redx]- RedX
> Contents

> [!purplex]- PurpleX
> Contents

> [!magentax]- MagentaX
> Contents

> [!pinkx]- PinkX
> Contents

> [!orangex]- OrangeX
> Contents

> [!yellowx]- YellowX
> Contents

> [!mistx]- MistX
> Contents

> [!greenx]- GreenX
> Contents

> [!lemonx]- LemonX
> Contents

> [!applex]- AppleX
> Contents

> [!greyx]- GreyX
> Contents

> [!tanx]- TanX
> Contents

> [!nonex]- NoX, NoneX
> Contents


## Source
-

## Code
```css
/*########## CUSTOM CALLOUTS SNIPPET ##########*/
/*### COLORS & VARIABLES ###*/

.theme-light,
.theme-dark {
	--new-blue: 80, 124, 165;
	--new-cyan: 66, 162, 168;
	--new-red: 211, 47, 47;
	--new-purple: 112, 112, 202;
	--new-magenta: 189, 94, 180;
	--new-pink: 245, 116, 116;
	--new-orange: 223, 119, 22;
	--new-yellow: 211, 167, 12;
	--new-mist: 173, 138, 16;
	--new-green: 48, 193, 62;
	--new-lemon: 135, 170, 79;
	--new-apple: 79, 151, 115;
	--new-grey: 135, 135, 135;
	--new-tan: 113, 98, 61;
}


body {
	--new-callout-blue: var(--new-blue);
	--new-callout-cyan: var(--new-cyan);
	--new-callout-purple: var(--new-purple);
	--new-callout-magenta: var(--new-magenta);
	--new-callout-pink: var(--new-pink);
	--new-callout-red: var(--new-red);
	--new-callout-orange: var(--new-orange);
	--new-callout-yellow: var(--new-yellow);
	--new-callout-mist: var(--new-mist);
	--new-callout-green: var(--new-green);
	--new-callout-lemon: var(--new-lemon);
	--new-callout-apple: var(--new-apple);
	--new-callout-grey: var(--new-grey);
	--new-callout-tan: var(--new-tan);
}


/*########## GENERAL CALLOUT SETTINGS ##########*/

/*### PADDING ###*/

.callout-content > p,
.callout-content > ul {
	margin: var(--size-4-4) 0px var(--size-4-2) 0px;
}

/*### BORDER RADIUS (S, M, L, XL) ###*/

.callout {
	--callout-radius: var(--radius-l);

}

/*### BORDER RADIUS (S, M, L, XL) ###*/

.callout-title-inner {
	margin-right: auto;

}


/*####################### Custom Callouts Go Here #######################*/

/*### TASK, CHECKMARK, CHECKBOX ###*/

.callout[data-callout="task"],
.callout[data-callout="checkmark"],
.callout[data-callout="checkcircle"],
.callout[data-callout="checkbox"] {
	--callout-color: var(--new-callout-yellow);
	--callout-icon: check-circle;
}


/*### READ, BOOK, LECTURE ###*/

.callout[data-callout="read"],
.callout[data-callout="lecture"],
.callout[data-callout="book"] {
	--callout-color: var(--new-callout-red);
	--callout-icon: book;
}


/*### WATCH, TV, SHOW, SERIE ###*/

.callout[data-callout="watch"],
.callout[data-callout="tv"],
.callout[data-callout="show"],
.callout[data-callout="serie"] {
	--callout-color: var(--new-callout-tan);
	--callout-icon: clapperboard;
}


/*### LISTEN, MUSIC, LYRICS, SONG, SONGS ###*/

.callout[data-callout="listen"],
.callout[data-callout="music"],
.callout[data-callout="lyrics"],
.callout[data-callout="song"],
.callout[data-callout="songs"] {
	--callout-color: var(--new-callout-magenta);
	--callout-icon: music;
}


/*### DOING, HEARTBEAT, ACTIVITY ###*/

.callout[data-callout="doing"],
.callout[data-callout="heartbeat"],
.callout[data-callout="activity"] {
	--callout-color: var(--new-callout-red);
	--callout-icon: activity;
}


/*### READING ###*/

.callout[data-callout="reading"] {
	--callout-color: var(--new-callout-red);
	--callout-icon: book-marked;
}


/*### WATCHING, NETFLIX, CHILL ###*/

.callout[data-callout="watching"],
.callout[data-callout="netflix"],
.callout[data-callout="chill"] {
	--callout-color: var(--new-callout-red);
	--callout-icon: film;
}


/*### LISTENING ###*/

.callout[data-callout="listening"] {
	--callout-color: var(--new-callout-red);
	--callout-icon: speaker;
}


/*### DATE, MEETING, CALENDAR ###*/

.callout[data-callout="date"],
.callout[data-callout="calendar"],
.callout[data-callout="meeting"] {
	--callout-color: var(--new-callout-purple);
	--callout-icon: calendar;
}


/*### TIME, HOUR, CLOCK ###*/

.callout[data-callout="time"],
.callout[data-callout="hour"],
.callout[data-callout="clock"] {
	--callout-color: var(--new-callout-grey);
	--callout-icon: clock;
}


/*### MENTION ###*/

.callout[data-callout="mention"] {
	--callout-color: var(--new-callout-pink);
	--callout-icon: at-sign;
}


/*### RECEIPT, INVOICE ###*/

.callout[data-callout="receipt"],
.callout[data-callout="invoice"] {
	--callout-color: var(--new-callout-tan);
	--callout-icon: receipt;
}


/*### RECYCLE, NATURE ###*/

.callout[data-callout="recycle"],
.callout[data-callout="nature"] {
	--callout-color: var(--new-callout-lemon);
	--callout-icon: recycle;
}


/*### INBOX ###*/

.callout[data-callout="inbox"] {
	--callout-color: var(--new-callout-orange);
	--callout-icon: inbox;
}


/*### DESK, LAMP, REFLECTION ###*/

.callout[data-callout="desk"],
.callout[data-callout="reflection"],
.callout[data-callout="lamp"] {
	--callout-color: var(--new-callout-apple);
	--callout-icon: lamp-desk;
}


/*### LEAF, TREE, EVERGREEN ###*/

.callout[data-callout="leaf"],
.callout[data-callout="tree"],
.callout[data-callout="evergreen"] {
	--callout-color: var(--new-callout-green);
	--callout-icon: leaf;
}


/*### SNOW, COLD, SNOWFLAKE ###*/

.callout[data-callout="snow"],
.callout[data-callout="cold"],
.callout[data-callout="snowflake"] {
	--callout-color: var(--new-callout-cyan);
	--callout-icon: snowflake;
}


/*### SUN, BRIGHT, LIGHT ###*/

.callout[data-callout="sun"],
.callout[data-callout="hot"],
.callout[data-callout="bright"],
.callout[data-callout="light"] {
	--callout-color: var(--new-callout-yellow);
	--callout-icon: sun;
}


/*### SPROUT, EVERGREEN, SEED ###*/

.callout[data-callout="sprout"],
.callout[data-callout="evergreen"],
.callout[data-callout="seed"] {
	--callout-color: var(--new-callout-green);
	--callout-icon: sprout;
}


/*### STICKER, STICKY-NOTE, STICKY, NOTE ###*/

.callout[data-callout="sticky"],
.callout[data-callout="sticky-note"],
.callout[data-callout="sticker"] {
	--callout-color: var(--new-callout-orange);
	--callout-icon: sticker;
}


/*### STORE ###*/

.callout[data-callout="store"] {
	--callout-color: var(--new-callout-tan);
	--callout-icon: store;
}


/*### RESTAURANT, DINNER, UTENSILS, FORK, LUNCH ###*/

.callout[data-callout="restaurant"],
.callout[data-callout="dinner"],
.callout[data-callout="utensils"],
.callout[data-callout="fork"],
.callout[data-callout="lunch"] {
	--callout-color: var(--new-callout-purple);
	--callout-icon: utensils;
}


/*### YOUTUBE, YT, VIDEO, YOUTUBER, CHANNEL ###*/

.callout[data-callout="youtube"],
.callout[data-callout="yt"],
.callout[data-callout="video"],
.callout[data-callout="youtuber"],
.callout[data-callout="channel"] {
	--callout-color: var(--new-callout-red);
	--callout-icon: youtube;
}


/*### TWITTER, TWIT, TWEET, TUIT, X ###*/

.callout[data-callout="twitter"],
.callout[data-callout="tweet"],
.callout[data-callout="twit"],
.callout[data-callout="tuit"],
.callout[data-callout="x"] {
	--callout-color: var(--new-callout-blue);
	--callout-icon: twitter;
}


/*### SHOPPING, KART, CART, GROCERY, GROCERIES ###*/

.callout[data-callout="shopping"],
.callout[data-callout="kart"],
.callout[data-callout="cart"],
.callout[data-callout="grocery"],
.callout[data-callout="groceries"] {
	--callout-color: var(--new-callout-orange);
	--callout-icon: shopping-bag;
}


/*### AI, ARTIFICIAL INTELLIGENCE, SPARKLE, SPARKLES ###*/

.callout[data-callout="ai"],
.callout[data-callout="artificial-intelligence"],
.callout[data-callout="sparkle"],
.callout[data-callout="sparkles"] {
	--callout-color: var(--new-callout-yellow);
	--callout-icon: wand-2;
}


/*### LOCK, PRIVATE, PRIVACY ###*/

.callout[data-callout="lock"],
.callout[data-callout="private"],
.callout[data-callout="privacy"] {
	--callout-color: var(--new-callout-grey);
	--callout-icon: lock;
}


/*### GMAIL, EMAIL, MAIL ###*/

.callout[data-callout="gmail"],
.callout[data-callout="email"],
.callout[data-callout="mail"] {
	--callout-color: var(--new-callout-blue);
	--callout-icon: mail;
}


/*### MESSAGE, MESSAGES, WHATSAPP, SIGNAL ###*/

.callout[data-callout="message"],
.callout[data-callout="messages"],
.callout[data-callout="messanger"],
.callout[data-callout="whatsapp"],
.callout[data-callout="signal"] {
	--callout-color: var(--new-callout-green);
	--callout-icon: message-circle;
}


/*### LOCATION, PIN, PLACE ###*/

.callout[data-callout="location"],
.callout[data-callout="place"],
.callout[data-callout="pin"] {
	--callout-color: var(--new-callout-purple);
	--callout-icon: pin;
}


/*### MAP ###*/

.callout[data-callout="map"] {
	--callout-color: var(--new-callout-purple);
	--callout-icon: map;
}


/*### HOLIDAYS, VACATION, REST, BEACH ###*/

.callout[data-callout="beach"],
.callout[data-callout="rest"],
.callout[data-callout="holidays"],
.callout[data-callout="vacation"] {
	--callout-color: var(--new-callout-yellow);
	--callout-icon: palmtree;
}


/*### DESIGN, ART, ARTISTIC ###*/

.callout[data-callout="design"],
.callout[data-callout="art"],
.callout[data-callout="artistic"] {
	--callout-color: var(--new-callout-pink);
	--callout-icon: brush;
}


/*### MOON, NIGHT, MIDNIGHT ###*/

.callout[data-callout="moon"],
.callout[data-callout="night"],
.callout[data-callout="midnight"] {
	--callout-color: var(--new-callout-cyan);
	--callout-icon: moon;
}


/*### MOUNTAIN, HIKING, HIKER, PATH, WALKING ###*/

.callout[data-callout="mountain"],
.callout[data-callout="hiking"],
.callout[data-callout="hiker"],
.callout[data-callout="path"],
.callout[data-callout="walking"] {
	--callout-color: var(--new-callout-green);
	--callout-icon: mountain-snow;
}


/*### WRENCH, TOOL ###*/

.callout[data-callout="wrench"],
.callout[data-callout="tool"] {
	--callout-color: var(--new-callout-tan);
	--callout-icon: wrench;
}


/*### RECIPE, COOKING, COOK, CHEF ###*/

.callout[data-callout="recipe"],
.callout[data-callout="cooking"],
.callout[data-callout="cook"],
.callout[data-callout="chef"] {
	--callout-color: var(--new-callout-pink);
	--callout-icon: chef-hat;
}

/*### App, Application, Plugin  ###*/

.callout[data-callout="app"],
.callout[data-callout="apps"],
.callout[data-callout="application"],
.callout[data-callout="plugin"] {
	--callout-color: var(--new-callout-mist);
	--callout-icon: puzzle;
}


/*### INGREDIENT, INGREDIENTS ###*/

.callout[data-callout="ingredient"],
.callout[data-callout="ingredients"] {
	--callout-color: var(--new-callout-yellow);
	--callout-icon: carrot;
}


/*### BOX, PACKAGE, PACKAGES, DELIVERY ###*/

.callout[data-callout="box"],
.callout[data-callout="package"],
.callout[data-callout="packages"],
.callout[data-callout="delivery"] {
	--callout-color: var(--new-callout-magenta);
	--callout-icon: package;
}


/*### PAPERCLIP, PAPER, DOC, DOCS, DOCUMENT ###*/

.callout[data-callout="paper"],
.callout[data-callout="paperclip"],
.callout[data-callout="doc"],
.callout[data-callout="docs"],
.callout[data-callout="documents"] {
	--callout-color: var(--new-callout-blue);
	--callout-icon: paperclip;
}


/*### PARTY, POPPER, FIESTA, CELEBRATION ###*/

.callout[data-callout="party"],
.callout[data-callout="popper"],
.callout[data-callout="fiesta"],
.callout[data-callout="celebration"] {
	--callout-color: var(--new-callout-magenta);
	--callout-icon: party-popper;
}


/*### ARCHIVE, PROPERTY, PROPERTIES ###*/

.callout[data-callout="properties"],
.callout[data-callout="Property"],
.callout[data-callout="archive"] {
	--callout-color: var(--new-callout-tan);
	--callout-icon: archive;
}

/*### HEALTH, HEART ###*/

.callout[data-callout="health"],
.callout[data-callout="heart"] {
	--callout-color: var(--new-callout-red);
	--callout-icon: heart;
}


/*### BOT, ROBOT ###*/

.callout[data-callout="bot"],
.callout[data-callout="robot"] {
	--callout-color: var(--new-callout-grey);
	--callout-icon: bot;
}


/*### PROJECTS ###*/

.callout[data-callout="projects"] {
	--callout-color: var(--new-callout-blue);
	--callout-icon: boxes;
}


/*### PROJECT ###*/

.callout[data-callout="project"] {
	--callout-color: var(--new-callout-apple);
	--callout-icon: box;
}


/*### CODE, SNIPPET ###*/

.callout[data-callout="code"],
.callout[data-callout="snippet"] {
	--callout-color: var(--new-callout-grey);
	--callout-icon: code-2;
}


/*### COMMAND, SHORTCUT, HOTKEY ###*/

.callout[data-callout="command"],
.callout[data-callout="shortcut"],
.callout[data-callout="hotkey"] {
	--callout-color: var(--new-callout-grey);
	--callout-icon: command;
}


/*### CONTACT, PEOPLE, TEAM, CREW, USERS ###*/

.callout[data-callout="contact"],
.callout[data-callout="people"],
.callout[data-callout="team"],
.callout[data-callout="crew"],
.callout[data-callout="users"] {
	--callout-color: var(--new-callout-cyan);
	--callout-icon: contact;
}


/*### EFFORT, MILESTONE, META, GOAL ###*/

.callout[data-callout="effort"],
.callout[data-callout="efforts"],
.callout[data-callout="milestone"],
.callout[data-callout="meta"],
.callout[data-callout="goal"] {
	--callout-color: var(--new-callout-lemon);
	--callout-icon: milestone;
}


/*### PLANET, EARTH ###*/

.callout[data-callout="planet"],
.callout[data-callout="earth"] {
	--callout-color: var(--new-callout-blue);
	--callout-icon: globe-2;
}


/*### NAVIGATION, COMPASS ###*/

.callout[data-callout="navigation"],
.callout[data-callout="navigator"],
.callout[data-callout="compass"] {
	--callout-color: var(--new-callout-pink);
	--callout-icon: compass;
}

/*### DICE, DICES, ROLE ###*/

.callout[data-callout="dice"],
.callout[data-callout="role"],
.callout[data-callout="dices"] {
	--callout-color: var(--new-callout-red);
	--callout-icon: dices;
}


/*### GAME, GAMING, VIDEOGAME ###*/

.callout[data-callout="game"],
.callout[data-callout="gaming"],
.callout[data-callout="videogame"] {
	--callout-color: var(--new-callout-tan);
	--callout-icon: gamepad-2;
}


/*### STAR, FAVORITE, FAVOURITE ###*/

.callout[data-callout="star"],
.callout[data-callout="favorite"],
.callout[data-callout="favourite"] {
	--callout-color: var(--new-callout-yellow);
	--callout-icon: star;
}


/*### BOOKMARK, BOOKMARKS ###*/

.callout[data-callout="bookmark"],
.callout[data-callout="bookmarks"] {
	--callout-color: var(--new-callout-orange);
	--callout-icon: bookmark;
}


/*### LINK, LINKS, REFERENCE, REFERENCES ###*/

.callout[data-callout="link"],
.callout[data-callout="links"],
.callout[data-callout="reference"],
.callout[data-callout="references"] {
	--callout-color: var(--new-callout-grey);
	--callout-icon: link;
}


/*### TABLE, TABLES ###*/

.callout[data-callout="table"],
.callout[data-callout="tables"] {
	--callout-color: var(--new-callout-lemon);
	--callout-icon: table-2;
}


/*### EMPTY, TRANSPARENT, VOID, HEADING, TITLE ###*/

.callout[data-callout="empty"],
.callout[data-callout="transparent"],
.callout[data-callout="void"],
.callout[data-callout="heading"],
.callout[data-callout="table"],
.callout[data-callout="#"],
.callout[data-callout="toc"],
.callout[data-callout="title"] {
	--callout-color: var(--new-callout-empty);
	--callout-icon: heading;
	border: 1px solid;
	border-color: var(--text-faint);
}


/*############### BY COLORS WITH ICON ###############*/

.callout[data-callout="blue"] {
	--callout-color: var(--new-callout-blue);
	--callout-icon: palette;
}

.callout[data-callout="cyan"] {
	--callout-color: var(--new-callout-cyan);
	--callout-icon: palette;
}

.callout[data-callout="red"] {
	--callout-color: var(--new-callout-red);
	--callout-icon: palette;
}

.callout[data-callout="purple"] {
	--callout-color: var(--new-callout-purple);
	--callout-icon: palette;
}

.callout[data-callout="magenta"] {
	--callout-color: var(--new-callout-magenta);
	--callout-icon: palette;
}

.callout[data-callout="pink"] {
	--callout-color: var(--new-callout-pink);
	--callout-icon: palette;
}

.callout[data-callout="orange"] {
	--callout-color: var(--new-callout-orange);
	--callout-icon: palette;
}

.callout[data-callout="yellow"] {
	--callout-color: var(--new-callout-yellow);
	--callout-icon: palette;
}

.callout[data-callout="mist"] {
	--callout-color: var(--new-callout-mist);
	--callout-icon: palette;
}

.callout[data-callout="green"] {
	--callout-color: var(--new-callout-green);
	--callout-icon: palette;
}

.callout[data-callout="lemon"] {
	--callout-color: var(--new-callout-lemon);
	--callout-icon: palette;
}

.callout[data-callout="apple"] {
	--callout-color: var(--new-callout-apple);
	--callout-icon: palette;
}

.callout[data-callout="grey"] {
	--callout-color: var(--new-callout-grey);
	--callout-icon: palette;
}

.callout[data-callout="tan"] {
	--callout-color: var(--new-callout-tan);
	--callout-icon: palette;
}

.callout[data-callout="none"],
.callout[data-callout="no"] {
	--callout-color: var(--new-callout-empty);
	--callout-icon: palette;
	border: 1px solid;
	border-color: var(--text-faint);
}


/*############### BY COLORS WITH NO ICON ###############*/

.callout[data-callout="bluex"] {
	--callout-color: var(--new-callout-blue);
	--callout-icon: none;
}

.callout[data-callout="cyanx"] {
	--callout-color: var(--new-callout-cyan);
	--callout-icon: none;
}

.callout[data-callout="redx"] {
	--callout-color: var(--new-callout-red);
	--callout-icon: none;
}

.callout[data-callout="purplex"] {
	--callout-color: var(--new-callout-purple);
	--callout-icon: none;
}

.callout[data-callout="magentax"] {
	--callout-color: var(--new-callout-magenta);
	--callout-icon: none;
}

.callout[data-callout="pinkx"] {
	--callout-color: var(--new-callout-pink);
	--callout-icon: none;
}

.callout[data-callout="orangex"] {
	--callout-color: var(--new-callout-orange);
	--callout-icon: none;
}

.callout[data-callout="yellowx"] {
	--callout-color: var(--new-callout-yellow);
	--callout-icon: none;
}

.callout[data-callout="mistx"] {
	--callout-color: var(--new-callout-mist);
	--callout-icon: none;
}

.callout[data-callout="greenx"] {
	--callout-color: var(--new-callout-green);
	--callout-icon: none;
}

.callout[data-callout="lemonx"] {
	--callout-color: var(--new-callout-lemon);
	--callout-icon: none;
}

.callout[data-callout="applex"] {
	--callout-color: var(--new-callout-apple);
	--callout-icon: none;
}

.callout[data-callout="greyx"] {
	--callout-color: var(--new-callout-grey);
	--callout-icon: none;
}

.callout[data-callout="tanx"] {
	--callout-color: var(--new-callout-tan);
	--callout-icon: none;
}

.callout[data-callout="nonex"],
.callout[data-callout="nox"] {
	--callout-color: var(--new-callout-empty);
	--callout-icon: none;
	border: 1px solid;
	border-color: var(--text-faint);
}


```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

