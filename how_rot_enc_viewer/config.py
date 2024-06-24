from pathlib import Path

BASE_PATH = Path('/data/imaging/harwell_open_week/')

datasets = []
datasets.append({
    'projections': {
        'directory': BASE_PATH / 'Pikachu/Projections/Trabs',
        'name_pattern': 'Pikachu_Trabs_idx_{:04d}.tiff',
        'start': 0,
        'stop': 101,
    }
})
datasets.append({
    'projections': {
        'directory': BASE_PATH / 'Char/Projections/Trabs',
        'name_pattern': 'Char_Trabs_idx_{:04d}.tiff',
        'start': 0,
        'stop': 98,
    }
})
datasets.append({
    'projections': {
        'directory': BASE_PATH / 'Horsea/Projections/Trabs',
        'name_pattern': 'Horsea_Trabs_idx_{:04d}.tiff',
        'start': 0,
        'stop': 98,
    }
})
