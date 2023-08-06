*** Variables ***

# Variables specific for Plone 4.x.
# See default.robot for all available variables.

# "Listing Collection"
${LISTING_COLLECTION_N_ITEMS}  css=#listing-collection .tileItem:nth-child(3)

# "Recent Listings"
${RECENT_LISTINGS_N_ITEMS}  css=#recent-listings .tileItem:nth-child(3)

# "Listing Search"
${LISTING_SEARCH_FORM}  css=#search-form

# "Development Collection"
${DEVELOPMENT_COLLECTION_N_ITEMS}  css=.development-summary .tileItem:nth-child(3)
