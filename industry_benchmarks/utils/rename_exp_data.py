import click
import pathlib

@click.command()
@click.option(
    "--experimental-data",
    help="The path to the experimental data CSV file.",
    type=click.Path(file_okay=True, dir_okay=False, path_type=pathlib.Path),
    required=True
)
@click.option(
    "--name-mapping-file",
    default=pathlib.Path("./ligand_name_mapping_PRIVATE.json"),
    help="The path to the JSON file with the name mappings created by the `data_gathering.py` script.",
    type=click.Path(file_okay=True, dir_okay=True, path_type=pathlib.Path),
    show_default=True,
)
@click.option(
    "--output",
    help="The name of the new blinded CSV file.",
    type=click.Path(exists=False, path_type=pathlib.Path),
    default=pathlib.Path("blinded_experimental_data.csv")
)
def main(experimental_data: pathlib.Path, name_mapping_file: pathlib.Path, output: pathlib.Path):
    """
    Rename the ligands in the experimental CSV file using the name mapping generated by the data_gathering.py script.


    Parameters
    ----------
    experimental_data:
        The CSV file containing the experimental data and the private ligand names.
    name_mapping_file:
        The JSON file mapping the ligand names to the blinded version, created by the data_gathering.py script.
    output:
        The name of the new CSV file with the private names removed.
    """
    import pandas as pd
    import json

    # load the csv with the private names
    exp_csv = pd.read_csv(experimental_data)

    # load the name mappings dict[old name, new name]
    name_mapping = json.load(name_mapping_file.open("r"))

    def _rename(row):
        try:
            return name_mapping[str(row["Ligand Name"])]
        except KeyError:
            raise RuntimeError(f"Could not convert {row['Ligand Name']} as it was not found in the name mapping.")

    exp_csv['Ligand Name'] = exp_csv.apply(_rename, axis=1)

    # write to file
    exp_csv.to_csv(output, index=False)

if __name__ == "__main__":
    main()
