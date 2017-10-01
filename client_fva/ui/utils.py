

def apply_selected_appearance(main_app, user_settings):
    main_app.setStyle(user_settings.theme)
    font = '*{{font-size: {0}pt; font-family: "{1}";}}'.format(user_settings.font_size,
                                                               user_settings.font_family)
    main_app.setStyleSheet(font)
