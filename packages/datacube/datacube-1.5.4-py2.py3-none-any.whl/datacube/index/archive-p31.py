from datacube import Datacube


def main(dc: Datacube):
    for dataset in dc.index.datasets.search(product='ls7_level1_scene'):
        # There's no field for ga-level, so we scrape the label.
        if '_P31_' in dataset.metadata.label:

            if len(dataset.uris) > 1:
                print(f"WARNING: Other locations exist for {dataset.id}: {repr(dataset.uris)}")

            # path: Path = dataset.local_uri
            if dataset.local_uri:
                print(f"archiving {dataset.id} {dataset.metadata.label} → {dataset.local_uri}")
                dc.index.datasets.archive_location(dataset.id, dataset.local_uri)


if __name__ == '__main__':
    main(Datacube(app='p31-archiver'))
