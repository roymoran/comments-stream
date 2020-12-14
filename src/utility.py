def resolve_data_directory(dir_indicator) -> str:
    if 'training_set' in dir_indicator:
        if '_valid' in dir_indicator:
            return 'training_set/valid'
        elif '_invalid' in dir_indicator:
            return 'training_set/invalid'
    elif 'testing_set' in dir_indicator:
        if '_valid' in dir_indicator:
            return 'training_set/valid'
        elif '_invalid' in dir_indicator:
            return 'training_set/invalid'