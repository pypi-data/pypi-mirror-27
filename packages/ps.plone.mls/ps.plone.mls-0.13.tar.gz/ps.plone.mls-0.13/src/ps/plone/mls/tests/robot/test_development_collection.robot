*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***


Show how to work with development collections
    Enable autologin as  Site Administrator
    Create content  type=Folder
    ...  id=${FOLDER_ID}
    ...  title=A folder
    ...  description=This is the folder
    Go to  ${PLONE_URL}/${FOLDER_ID}

    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${DEVELOPMENT_COLLECTION_ACTIVATE_LINK}
    ...  Click to activate the Development Collection
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${DEVELOPMENT_COLLECTION_ACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  development_collection_activate.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${DEVELOPMENT_COLLECTION_ACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  development_collection_activate_done.png
    ...  ${STATUS_MESSAGE}

    Capture and crop page screenshot
    ...  development_collection_default.png
    ...  css=.documentFirstHeading
    ...  ${DEVELOPMENT_COLLECTION_N_ITEMS}

    Click link  css=#contentview-development-collection-config a

    Wait until element is visible  ${CONTENT}

    Capture and crop page screenshot
    ...  development_collection_configuration.png
    ...  ${CONTENT}

    Click link  ${DEVELOPMENT_COLLECTION_CONFIG_TAB_FILTER}

    Capture and crop page screenshot
    ...  development_collection_configuration_filter.png
    ...  ${CONTENT}

    Click button  css=#form-buttons-cancel

    Click link  css=#contentview-development-collection-config a
    Wait until element is visible  ${CONTENT}
    Select Checkbox  css=#form-widgets-show_banner_image-0
    Click button  css=#form-buttons-save

    Capture and crop page screenshot
    ...  development_collection_with_banner.png
    ...  css=.documentFirstHeading
    ...  ${DEVELOPMENT_COLLECTION_N_ITEMS}

    Go to  ${PLONE_URL}/${FOLDER_ID}
    Page should contain element  ${LINK_CONTENTMENU_ACTIONS}
    Click link  ${LINK_CONTENTMENU_ACTIONS}
    Wait until element is visible  ${LIST_CONTENTMENU_ACTIONS}

    ${note1}  Add pointy note  ${DEVELOPMENT_COLLECTION_DEACTIVATE_LINK}
    ...  Click to deactivate the Development Collection
    ...  position=${POSITION_CONTENTMENU_ACTIONS_NOTE}
    Mouse over  ${DEVELOPMENT_COLLECTION_DEACTIVATE_LINK}
    Update element style  portal-footer  display  none

    Capture and crop page screenshot
    ...  development_collection_deactivate.png
    ...  ${CONTENTMENU_ACTIONS}
    ...  ${note1}
    Remove elements  ${note1}

    ${href} =  get element attribute
    ...  ${DEVELOPMENT_COLLECTION_DEACTIVATE_LINK}@href
    go to  ${href}

    Capture and crop page screenshot
    ...  development_collection_deactivate_done.png
    ...  ${STATUS_MESSAGE}
