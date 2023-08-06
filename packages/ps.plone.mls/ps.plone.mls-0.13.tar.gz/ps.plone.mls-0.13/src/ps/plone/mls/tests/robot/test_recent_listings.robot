*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***


Show how to work with recent listings
    Enable autologin as  Site Administrator
    Create content  type=Folder
    ...  id=${FOLDER_ID}-2
    ...  title=Recent Listings
    ...  description=This is the folder
    Go to  ${PLONE_URL}/${FOLDER_ID}-2

    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${RECENT_LISTINGS_ACTIVATE_LINK}
    ...  Click to activate the Recent Listings
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${RECENT_LISTINGS_ACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  recent_listings_activate.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${RECENT_LISTINGS_ACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  recent_listings_activate_done.png
    ...  ${STATUS_MESSAGE}

    Capture and crop page screenshot
    ...  recent_listings_default.png
    ...  css=.documentFirstHeading
    ...  ${RECENT_LISTINGS_N_ITEMS}

    Click link  css=#contentview-recent-listings-config a

    Wait until element is visible  ${CONTENT}

    Capture and crop page screenshot
    ...  recent_listings_configuration.png
    ...  ${CONTENT}

    Click button  css=#form-buttons-cancel

    Go to  ${PLONE_URL}/${FOLDER_ID}-2
    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${RECENT_LISTINGS_DEACTIVATE_LINK}
    ...  Click to deactivate the Recent Listings
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${RECENT_LISTINGS_DEACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  recent_listings_deactivate.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${RECENT_LISTINGS_DEACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  recent_listings_deactivate_done.png
    ...  ${STATUS_MESSAGE}
