import os, time, requests
from dotenv import load_dotenv
load_dotenv()

KEY  = os.getenv("PRINTIFY_API_KEY")
SHOP = os.getenv("PRINTIFY_SHOP_ID")
BASE = "https://api.printify.com/v1"
H    = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

DESCRIPTIONS = {
    "It's Not Gay If It's Food - Unisex Tee": """
Funny food humor graphic tee that walks the line between wrong and hilarious. The perfect offensive dad shirt for anyone who lives by the golden rule: if it's food, it doesn't count. Made from soft, heavyweight cotton that holds its shape wash after wash.

Ideal as a gag gift, birthday gift for dads, or a conversation-starting shirt for BBQs, tailgates, and family dinners where someone always says too much. Available in classic black in sizes S through 5XL — because the bit works at every size.

Keywords: funny graphic tee, offensive dad shirt, food humor shirt, gag gift t-shirt, inappropriate humor shirt, funny gift for dad, novelty t-shirt, adult humor shirt, unisex tee.
""".strip(),

    "It's Not Gay If It's Food - Pullover Hoodie": """
Warm, comfortable, and deeply questionable. This funny food humor hoodie is built for people who have opinions, no filter, and a strong stance on the rules of food. A great gag gift or offensive dad hoodie for the person in your life who always goes too far at dinner.

Double-lined hood, front kangaroo pocket, and a midweight fleece blend that gets softer every wash. Available in a range of dark colors in sizes S through 3XL — because great jokes belong on great hoodies.

Keywords: funny hoodie, offensive dad hoodie, food humor sweatshirt, gag gift hoodie, adult humor pullover, novelty hoodie, funny gift for men, inappropriate humor sweatshirt, graphic hoodie.
""".strip(),

    "It's Not Gay If It's Food - Kiss-Cut Stickers": """
Stick your sense of humor everywhere. These food joke kiss-cut stickers are printed on durable vinyl with a glossy finish that's waterproof, scratch-resistant, and built to outlast your questionable decisions. Perfect for laptops, water bottles, car bumpers, lunch boxes, and anywhere else you want to make someone do a double-take.

Available in sizes from 2x2 to 6x6 inches. Great as a stocking stuffer, gag gift, or addition to any funny sticker collection.

Keywords: funny stickers, offensive humor sticker, food joke sticker, adult humor vinyl sticker, gag gift sticker, laptop sticker, water bottle sticker, funny gift, novelty sticker, kiss-cut sticker.
""".strip(),

    "Drink Yerassaf! — Unisex Tee": """
Tell the world exactly what they should be doing — in style. The Drink Yerassaf! unisex tee is a funny drinking shirt made for bar nights, backyard hangouts, tailgates, and anywhere else someone hands you a cold one. Soft, durable, and built to survive as many rounds as you can.

Available in dark colors in sizes S through 2XL. Makes a great gift for the craft beer lover, party host, bartender, or anyone who takes their drinking seriously.

Keywords: funny drinking shirt, bar t-shirt, beer lover gift, funny alcohol shirt, drink humor tee, gag gift for beer lover, novelty drinking shirt, funny gift for men, party shirt, bartender gift.
""".strip(),

    "Drink Yerassaf! — Unisex Tee (B&W)": """
Classic black. Clean design. Loud message. The Drink Yerassaf! B&W unisex tee delivers the same bold drinking humor in a sharp one-color logo on black — perfect for anyone who keeps it simple but never subtle. Wear it to the bar, the brewery, or anywhere respectable people gather to do irresponsible things.

Soft heavyweight cotton, sizes S through 3XL. A great gag gift, birthday shirt, or addition to your funny t-shirt rotation.

Keywords: funny black t-shirt, drinking humor shirt, beer shirt, bar shirt, gag gift tee, funny gift for men, novelty t-shirt, alcohol humor shirt, black graphic tee, bartender shirt.
""".strip(),

    "Drink Yerassaf! — Pullover Hoodie": """
A cozy hoodie for people who drink with conviction. The Drink Yerassaf! pullover hoodie pairs warm midweight fleece with a message that belongs on every barstool, tailgate, and Friday night. Double-lined hood, kangaroo pocket, and a design that sparks exactly the kind of conversations you were hoping for.

Available in dark colors, sizes S through 2XL. Makes a killer gift for the craft beer obsessive, the designated driver who wishes they weren't, or the friend who always orders one more round.

Keywords: funny drinking hoodie, beer lover sweatshirt, bar hoodie, alcohol humor pullover, gag gift hoodie, funny gift for men, novelty sweatshirt, graphic hoodie, drink humor.
""".strip(),

    "Drink Yerassaf! — Pullover Hoodie (B&W)": """
Same great hoodie, bolder statement. The Drink Yerassaf! B&W pullover hoodie keeps it clean with a one-color logo on black — classic look, zero chill. Midweight fleece, double-lined hood, front kangaroo pocket. The kind of hoodie you wear to the brewery and never take off.

Available in black, sizes S through 3XL. Great gag gift for birthdays, holidays, or any occasion that calls for a drink.

Keywords: black drinking hoodie, funny sweatshirt, beer lover gift, bar hoodie, gag gift hoodie, funny gift for him, novelty pullover, alcohol humor hoodie, graphic sweatshirt, bartender gift.
""".strip(),

    "Drink Yerassaf! — Mug 11oz": """
Start every morning with a reminder of your priorities. The Drink Yerassaf! 11oz coffee mug is a funny drinkware gift for coffee drinkers, beer lovers, and anyone who needs a little motivation before noon. Ceramic construction with a comfortable C-handle, dishwasher safe, and printed with a vibrant full-color logo that won't fade.

Perfect as a gag gift, office gift, Secret Santa pick, or stocking stuffer for the person who runs on caffeine and questionable decisions.

Keywords: funny coffee mug, gag gift mug, beer humor mug, novelty mug, funny gift for men, drinking humor mug, ceramic coffee mug, funny office gift, Secret Santa gift, bartender gift mug.
""".strip(),

    "Drink Yerassaf! — Mug 15oz": """
Go big or go home. The Drink Yerassaf! 15oz mug holds more coffee, more soup, more whatever-you-need — and carries a message worthy of the extra capacity. Ceramic with a sturdy C-handle, dishwasher safe, and printed with a vibrant color logo built to last.

An oversized funny mug that makes a great gag gift, birthday gift, or office desk statement piece for anyone who goes hard at everything they do.

Keywords: large funny mug, oversized coffee mug, 15oz novelty mug, gag gift mug, funny drinkware, beer humor mug, big coffee mug, funny gift for men, ceramic mug, office gift.
""".strip(),

    "Drink Yerassaf! — Frosted Beer Mug": """
The only beer mug with a personality to match yours. The Drink Yerassaf! frosted beer mug is the go-to barware gift for the craft beer lover, home bar enthusiast, or anyone who takes their pint presentation seriously. Frosted glass construction for that satisfying chill, with a bold full-color logo that makes it instantly recognizable on any bar cart.

Dishwasher safe. Perfect for birthdays, Father's Day, holidays, or just because someone deserves a great beer glass.

Keywords: funny beer mug, frosted beer mug, craft beer gift, bar accessory gift, novelty beer glass, gag gift for beer lover, home bar gift, funny drinkware, beer lover gift, Father's Day gift.
""".strip(),

    "Drink Yerassaf! — Pint Glass 16oz": """
Every great beer deserves a glass that sets the tone. The Drink Yerassaf! 16oz pint glass is a classic bar-style pint with a bold full-color logo — ideal for craft beer lovers, home bartenders, and anyone who believes presentation is part of the pour. Sturdy glass construction, dishwasher safe.

Makes a great gift for beer enthusiasts, bar cart collectors, or the friend who always has the best bottle selection. Perfect for birthdays, Father's Day, and holidays.

Keywords: funny pint glass, beer gift, craft beer glass, novelty pint glass, bar accessory, gag gift for beer lover, home bar gift, 16oz beer glass, funny drinkware, Father's Day gift.
""".strip(),

    "Drink Yerassaf! — Can Cooler Sleeve": """
Keep it cold. Keep it funny. The Drink Yerassaf! can cooler sleeve fits standard 12oz cans and keeps your drink cold while broadcasting a message everyone at the party needs to see. Flexible foam construction that slips on and off easily, durable enough for tailgates, camping trips, backyard hangouts, and beach days.

A great gag gift, stocking stuffer, or party favor for anyone who likes their beer cold and their humor dry.

Keywords: funny can cooler, beer koozie, can sleeve, funny drink cooler, gag gift, tailgate gift, party gift, beer lover gift, novelty can cooler, funny gift for men.
""".strip(),

    "Drink Yerassaf! — Can Holder": """
Your drink. Your statement. The Drink Yerassaf! can holder keeps your can secure and cold while the bold logo does the talking for you. Durable collapsible foam design compatible with standard 12oz cans — ready for game days, road trips, camping, or any occasion where someone hands you a cold one.

A fun, affordable gag gift or stocking stuffer for the beer lover, sports fan, or self-declared party expert in your life.

Keywords: funny can holder, beer can holder, collapsible koozie, novelty drink holder, gag gift, beer lover gift, tailgate accessory, sports gift, funny gift for men, can sleeve.
""".strip(),

    "Drink Yerassaf! — Tote Bag": """
Carry your essentials with the energy you actually have. The Drink Yerassaf! tote bag is a reusable canvas-style tote printed with the full-color Yerassaf logo — sturdy enough for groceries, beach trips, farmer's markets, or a six-pack run. Reinforced handles and a spacious main compartment make it as practical as it is funny.

A great everyday carry gift for beer lovers, eco-conscious drinkers, and anyone who likes their bags to have opinions.

Keywords: funny tote bag, reusable grocery bag, beer lover tote, novelty tote bag, canvas tote, gag gift bag, funny gift for her, market bag, beer tote, everyday carry bag.
""".strip(),

    "Drink Yerassaf! — Classic Dad Hat": """
Low profile. High standards. The Drink Yerassaf! classic dad hat is an adjustable unstructured baseball cap with an embroidered or printed logo — made for the person who wants to rep their drinking philosophy from sunup to sundown. Comfortable fit, curved brim, adjustable strap for the perfect fit.

A great gift for dads, beer lovers, golfers, and anyone who looks better in a hat. Works for outdoor events, brewery tours, tailgates, and everything in between.

Keywords: funny dad hat, beer hat, drinking humor baseball cap, novelty hat, gag gift hat, baseball cap gift, funny gift for dad, adjustable cap, bar hat, brewery hat.
""".strip(),

    "Drink Yerassaf! — Cork Coaster": """
Protect your surfaces. Assert your brand. The Drink Yerassaf! cork coaster is a natural cork coaster printed with the full-color logo — perfect for home bars, man caves, coffee tables, and anywhere drinks get set down. Absorbent, non-slip, and durable enough to handle daily use.

Makes a great addition to any bar cart or home bar setup, and an easy, affordable gift for the host, the home bartender, or anyone who takes their drinking environment seriously.

Keywords: funny coaster, cork coaster, bar coaster, home bar accessory, beer lover gift, novelty coaster, gag gift, funny housewarming gift, man cave decor, drink coaster.
""".strip(),

    "Drink Yerassaf! — Shot Glass": """
One shot. One message. The Drink Yerassaf! shot glass is a 1.5oz barware staple with the bold Yerassaf logo printed right where everyone can see it — at the bottom of an empty glass. Thick-walled glass construction, dishwasher safe, and sized perfectly for your preferred poison.

An easy win as a gag gift, party favor, birthday gift, or bar cart addition for anyone who knows how to have a good time. Great for game nights, bachelorette parties, and holiday gift exchanges.

Keywords: funny shot glass, novelty shot glass, drinking gift, bar accessory, gag gift, party gift, bachelorette party gift, funny gift for men, shot glass gift set, bartender gift.
""".strip(),

    "Drink Yerassaf! -- Kiss-Cut Stickers": """
Stick the vibe everywhere. The Drink Yerassaf! kiss-cut stickers are printed on premium waterproof vinyl with a glossy finish built to last on laptops, water bottles, tumblers, car bumpers, coolers, and anywhere else you want to represent. The vibrant full-color logo pops on any surface and won't fade, peel, or crack.

Available in sizes from 2x2 to 6x6 inches. A great stocking stuffer, party favor, or finishing touch on any gift for the beer lover or craft drink enthusiast in your life.

Keywords: funny stickers, drinking humor sticker, beer sticker, vinyl sticker, waterproof sticker, laptop sticker, water bottle sticker, gag gift sticker, novelty sticker, beer lover gift.
""".strip(),
}

r = requests.get(f"{BASE}/shops/{SHOP}/products.json?limit=50", headers=H)
products = r.json().get("data", [])
print(f"Updating descriptions for {len(products)} products...\n")

ok = 0
skip = 0
for p in products:
    title = p["title"]
    pid   = p["id"]
    desc  = DESCRIPTIONS.get(title)
    if not desc:
        print(f"  [SKIP] No description mapped for: {title}")
        skip += 1
        continue

    resp = requests.put(f"{BASE}/shops/{SHOP}/products/{pid}.json", headers=H,
                        json={"description": desc})
    if resp.ok:
        # Publish to push description live
        requests.post(f"{BASE}/shops/{SHOP}/products/{pid}/publish.json", headers=H,
                      json={"title": True, "description": True, "images": True,
                            "variants": True, "tags": True})
        print(f"  [OK]   {title}")
        ok += 1
    else:
        print(f"  [FAIL] {title} -- {resp.status_code}: {resp.text[:80]}")
    time.sleep(0.5)

print(f"\nDone: {ok} updated, {skip} skipped.")
