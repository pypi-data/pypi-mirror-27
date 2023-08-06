*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***


Show how to work with listing collections
    Enable autologin as  Site Administrator
    Create content  type=Folder
    ...  id=${FOLDER_ID}-1
    ...  title=A Listing Collection
    ...  description=This is the folder
    Go to  ${PLONE_URL}/${FOLDER_ID}-1

    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${LISTING_COLLECTION_ACTIVATE_LINK}
    ...  Click to activate the Listing Collection
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${LISTING_COLLECTION_ACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  listing_collection_activate.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${LISTING_COLLECTION_ACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  listing_collection_activate_done.png
    ...  ${STATUS_MESSAGE}

    Capture and crop page screenshot
    ...  listing_collection_default.png
    ...  css=.documentFirstHeading
    ...  ${LISTING_COLLECTION_N_ITEMS}

    Click link  css=#contentview-listing-collection-config a

    Wait until element is visible  ${CONTENT}

    Capture and crop page screenshot
    ...  listing_collection_configuration.png
    ...  ${CONTENT}

    Click button  css=#form-buttons-cancel

    Go to  ${PLONE_URL}/${FOLDER_ID}-1
    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${LISTING_COLLECTION_DEACTIVATE_LINK}
    ...  Click to deactivate the Listing Collection
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${LISTING_COLLECTION_DEACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  listing_collection_deactivate.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${LISTING_COLLECTION_DEACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  listing_collection_deactivate_done.png
    ...  ${STATUS_MESSAGE}
