# EX_PROP EXPLANATION:
## Outfits:
- These ex_props allow Auto Outfit Change to categorize and pool outfits into different categories which Monika can select from in different circumstances

### `"home"`:
- value: **ignored**
- Flags the outfit as an outfit to wear "at home"
- **Base Included Outfits**:
  - `Sundress (White)`
- **Spritepack Included Outfits**:
  - `Velius94 White Navy-blue Dress`
  - (Note: You'll need to update jsons via the submod's settings menu to apply this change)

#### Auto Atmos Change Integration:
- If Auto Atmos Change is installed, the `"sweater"` outfit pool will be used if there's any spritepacks for those installed if the temperature is below  20 degrees C.
- If Auto Atmos Change is *not* installed, this goes off a time interval. The last month of Fall, the entirety of Winter, and the first month of Spring will be where the `"sweater"` outfit pool will be used

### `"date"`:
- value: **ignored**
- Flags the outfit as something to wear when you take Monika out
- **NOTE**: This is for *non-special-day* dates
- **Base Included Outfits**:
  - `Sundress (White)`
- **Spritepack Included Outfits**:
  - `Velius94 White Navy-blue Dress`
  - (Note: You'll need to update jsons via the submod's settings menu to apply this change)

#### Auto Atmos Change Integration:
- If Auto Atmos Change is installed:
  - The `"sweater"` outfit pool will override this provided the temperature is within 11-20 degrees C
  - If the temperature is, or is below 10 degrees C, Monika will wear an outfit from the `"jacket"` pool instead
- If Auto Atmos Change is *not* installed:
  - The `"sweater"` outfit pool will be used if it's the last month of Fall, or the first month of Spring
  - The `"jacket"` outfit pool will be used if it's Winter

### `"formal"`:
- value: **ignored**
- Flags the outfit as something to wear when taking Monika out
- **Base Included Outfits**:
  - `Black Dress`
  - `New Year's Dress`
- **NOTE**: This creates an outfit pool for *special-day* dates

### `"sweater"`:
- value: **ignored**
- Flags this outfit as a sweater, usable both at home when it's winter inside (or just cold)
- **Spritepack Included Outfits**:
  - `Orcaramelo Shoulderless Sweater`
  - `Finale Hoodie Green`
  - (Note: You'll need to update jsons via the submod's settings menu to apply this change)

### `"jacket"`:
- value: **ignored**
- Flags the outfit as a jacket, usable when going out on a date during winter, or when cold
- **Spritepack Included Outfits**:
  - `Finale Jacket Brown`
  - (Note: You'll need to update jsons via the submod's settings menu to apply this change)

### `"pajamas"`:
- value: **ignored**
- Flags the outfit as a pair of pajamas. Monika will opt to wear them if it's late enough, or once it passes a certain time threshold

### Accessory Related Exprops:
- These ex_props allow Auto Outfit Change to categorize bracelets so Monika can pick the ones which will look best with the outfit
- **NOTE**: Since bracelets aren't fully supported in MAS yet, this is slightly awkward to use. While it's possible to create bracelet jsons, it's not possible to ask Monika to wear them, additionally they have some other issues like clipping for certain outfits with longer sleeves
- **NOTE**: These expect the bracelet acs to have an `acs_type` of `"wrist-bracelet"`

#### `"light bracelet"`:
- value: **ignored**
- Flags the outfit as eligible to wear a light colored bracelet
- **Base Included Outfits**:
  - `Sundress (White)`
  - `New Year's Dress`
- **Spritepack Included Outfits**:
  - `Velius94 White Navy-blue Dress`
  - (Note: You'll need to update jsons via the submod's settings menu to apply this change)

#### `"dark bracelet"`:
- value: **ignored**
- Flags the outfit as eligible to wear a dark colored bracelet
- **Base Included Outfits**:
  - `Black Dress`
- **Spritepack Included Outfits**:
  - `Velius94 White Navy-blue Dress`
  - `Orcaramelo Shoulderless Sweater`
  - (Note: You'll need to update jsons via the submod's settings menu to apply this change)

#### `"no bracelet"`:
- value: **ignored**
- Flags the outfit such that under no circumstances should Monika wear a bracelet with it
- This is done because it's possible for Monika to change into another outfit, but she'll keep her bracelet on. If an outfit may clip with bracelets, this ex_prop should be used to prevent that outfit from wearing bracelets
- **Spritepack Included Outfits**:
  - `Finale Jacket Brown`
  - `Finale Hoodie Green`
  - (Note: You'll need to update jsons via the submod's settings menu to apply this change)

## Hair:
- These ex_props allow Auto Outfit Change to categorize and pool hair for day and night

### `"day"`:
- value: **ignored**
- Flags the hair as day hair
- Day hair is worn/changed into after sunrise
- **Base Included Hair**:
  - `Ponytail`
  - `Down (Tied Strand)`
- **Spritepack Included Hair**:
  - `Orcaramelo Bunbraid`
  - `Orcaramelo Ponytailbraid`
  - `Orcaramelo Twintails`
  - `Orcaramelo Usagi`
  - `MAS bun`
  - (Note: You'll need to update jsons via the submod's settings menu to apply this change)

### `"night"`:
- value: **ignored**
- Flags the hair as night hair
- Night hair is worn/changed into after sunset
- **Base Included Hair**:
  - `Down`
  - `Down (Tied Strand)`

### `"down"`:
- value: **ignored**
- Flags the hair as a type of hair where Monika has her hair down
- Categorizes and groups down hair types to see if she should try and wear a ribbon when going out
- **Base Included Hair**:
  - `Down`
  - `Down (Tied Strand)`

## Accessories:
- These ex_props allow Auto Outfit Change to categorize bracelets.
- Like mentioned above, bracelets aren't fully supported in MAS, so you might see some clipping issues with outfits if you use them yourself.
- Those outfits should be given the `"no bracelet"` ex_prop.

### `"light"`:
- value: **ignored**
- Flags the bracelet as a light colored bracelet
- Will be used to handle combining with outfits, using the related ex_props on the current outfit

### `"dark"`:
- value: **ignored**
- Flags the bracelet as a dark colored bracelet
- Will be used to handle combining with outfits, using the related ex_props on the current outfit
