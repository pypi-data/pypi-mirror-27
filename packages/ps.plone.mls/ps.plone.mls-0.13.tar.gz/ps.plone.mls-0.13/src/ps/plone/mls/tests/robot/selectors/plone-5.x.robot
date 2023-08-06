*** Variables ***

# Variables specific for Plone 5.x.
# See default.robot for all available variables.

${POSITION_CONTENTMENU_ACTIONS_NOTE}  right

${CONTENTMENU_ACTIONS}  id=plone-contentmenu-actions
${LINK_CONTENTMENU_ACTIONS}  css=#plone-contentmenu-actions > a
${LIST_CONTENTMENU_ACTIONS}  css=#plone-contentmenu-actions > ul
${CONTENT}  css=#main-container
${STATUS_MESSAGE}  css=#global_statusmessage

# "Development Collection"
${DEVELOPMENT_COLLECTION_CONFIG_TAB_FILTER}  css=#autotoc-item-autotoc-1


# Settings
${CONTACT_INFO_TAB_DEFAULT}  css=#autotoc-item-autotoc-1
${CONTACT_INFO_TAB_AGENCY}  css=#autotoc-item-autotoc-1
${CONTACT_INFO_TAB_AGENT}  css=#autotoc-item-autotoc-2
