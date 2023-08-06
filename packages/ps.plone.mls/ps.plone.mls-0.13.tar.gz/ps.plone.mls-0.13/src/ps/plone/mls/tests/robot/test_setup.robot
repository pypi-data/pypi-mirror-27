*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***

Show how to activate the add-on
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/prefs_install_products_form

    Page should contain element  xpath=//*[@value='ps.plone.mls']
    Assign id to element
    ...  xpath=//*[@value='ps.plone.mls']/ancestor::li
    ...  addons-ps-plone-mls
    Assign id to element
    ...  xpath=//*[@value='ps.plone.mls']/ancestor::li
    ...  addons-enabled

    Highlight  addons-ps-plone-mls
    Capture and crop page screenshot
    ...  setup_select_add_on.png
    ...  id=addons-enabled

    Click button  xpath=//*[@value='ps.plone.mls']/ancestor::form//input[@type='submit']

    Page should contain element  xpath=//*[@value='ps.plone.mls']

    Assign id to element
    ...  xpath=//*[@value='ps.plone.mls']/ancestor::li
    ...  addons-ps-plone-mls
    Assign id to element
    ...  xpath=//*[@value='ps.plone.mls']/ancestor::li
    ...  addons-enabled

    Highlight  addons-ps-plone-mls
    Capture and crop page screenshot
    ...  setup_select_add_on_installable.png
    ...  id=addons-enabled
