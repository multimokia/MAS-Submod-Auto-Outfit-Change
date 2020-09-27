# Changelog
## September 27th, 2020:
- Crashfixes if your internet dropped or the connection timed out
- Add support for pajama outfits
- More exprops for bracelet customization
- Added two new functions:
  - *store.ahc_utils.*`add_builtin_to_list(sprite_obj, ex_prop)`:
    - Adds a sprite object to the builtin list
  - *store.ahc_utils.*`remove_builtin_from_list(sprite_obj, ex_prop)`:
    - Removes a sprite object from the builtin list
  - These add more flexibility in controlling outfits which can be selected

## September 14th, 2020:
- Bugfixes
- Crash where having been with Monika for at least one D25 season was assumed
- Fix an issue where the conditionals wouldn't be updated for those migrating from the original auto hair change

## September 14th, 2020:
- Auto Hair Change -> Auto Outfit Change
- Now changes outfits
- Customizable with ex_props

## March 15th, 2020:
- Adjusted for more types of night hair
- Allowed spritepack support using ex_props
- Uses new emptydesk transition labels

## January 12th, 2020:
- Dependency added
- Removed overrides, replaced with function plugins

## January 1st, 2020:
- Black Ribbon fix
- Black bow can only be worn with non-twintail hairstyles

## December 8th, 2019:
- Changed action from `queue` to `push`

## October 28th, 2019:
- Adjusted dockstat for o31 consistency with base MAS

## September 22nd, 2019:
- Added another label override

## September 20th, 2019:
- Taking you somewhere farewell fix
- Added ribbon preference for special days
- Monika now only gets her hair ready when taking her out if it wasn't already, and you didn't ask for a specific style

## September 19th, 2019:
- Added new method `ahc_getDayHair()`
- Added spritepack support
- Added hair randomization

## July 6th, 2019:
- Updated conditions again
- Updated docking station farewell
- Added documentation
- Defaulted to ribbonless

## June 26th, 2019:
- Conditional fix
- Wear ribbon
- Fix for baked outfits

## June 16th, 2019:
- Initial Release
