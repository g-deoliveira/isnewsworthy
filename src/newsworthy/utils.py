from pathlib import Path


def get_path_to_data_parsed_dir():
    '''
    The directory structure of this project is:
        root/
            data/
            data/parsed/
            model_dev/
            model_repo/
            notebooks/
            src/
                newsworthy/

    This function returns the absolute path of the
    parsed datafolder:
        data/parsed/
    '''

    script_path = Path(__file__)
    package_root = Path(script_path, '../../..')
    assert package_root.resolve().name == 'isnewsworthy'
    data_path = Path(package_root, 'data/parsed')
    data_path = data_path.resolve()

    return data_path