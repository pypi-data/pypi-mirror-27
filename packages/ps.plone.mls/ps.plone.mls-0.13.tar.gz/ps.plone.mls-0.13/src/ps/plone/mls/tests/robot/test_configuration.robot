*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***

Show how to configure the Propertyshelf MLS Embedding

    Enable autologin as  Manager

    # Show how to configure the base settings

    Go to  ${PLONE_URL}/@@mls-controlpanel-base

    Capture and crop page screenshot
    ...  controlpanel_base.png
    ...  css=#content

    # Show how to configure the ui settings

    Go to  ${PLONE_URL}/@@mls-controlpanel-ui

    Capture and crop page screenshot
    ...  controlpanel_ui.png
    ...  css=#content

    # Show how to configure the contact info settings

    Go to  ${PLONE_URL}/@@mls-controlpanel-contact-info

    Capture and crop page screenshot
    ...  controlpanel_contact_info_default.png
    ...  css=#content

    Click link  ${CONTACT_INFO_TAB_AGENCY}
    Capture and crop page screenshot
    ...  controlpanel_contact_info_agency.png
    ...  css=#content

    Click link  ${CONTACT_INFO_TAB_AGENT}
    Capture and crop page screenshot
    ...  controlpanel_contact_info_agent.png
    ...  css=#content

    # Show how to configure the caching settings

    Go to  ${PLONE_URL}/@@mls-controlpanel-caching

    Capture and crop page screenshot
    ...  controlpanel_caching.png
    ...  css=#content

    # Show how to see the usage overview

    Go to  ${PLONE_URL}/@@mls-controlpanel-usage

    Capture and crop page screenshot
    ...  controlpanel_usage.png
    ...  css=#content
