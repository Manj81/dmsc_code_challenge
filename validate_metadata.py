#!/usr/bin/env python3

import argparse
import csv

def main(source_file, output_file):
    with open(source_file, 'r', encoding='utf-8-sig', newline='') as source_io, \
            open(output_file, 'w', encoding='utf-8', newline='') as output_io:
        # Read in source file as CSV
        reader = csv.DictReader(source_io)
        # Copy fieldnames from reader for writer
        fieldnames = reader.fieldnames + ['missing_metadata','metadata_discrepancy']
        # Dictionary for Audio Configuration Code Mapping
        audio_code_map = {'20': 'Standard Stereo',
                '51': '5.1 (Discrete)',
                '50': '5.0 (Discrete)',
                'DS': 'Lt-Rt (Dolby Surround)',
                'ATM': 'Atmos'}
        # List for included assets that match asset_type_or_class
        included_assets = ['archive',
                'Audio Stem',
                'Dubbed Audio',
                'OV Audio',
                'package',
                'Restored Audio'
                ]
        # List for metadata columns
        metadata_columns = ['title_gpms_ids',
                'custom_metadata.content_details.language_dubbed',
                'custom_metadata.dcs.dcs_vendor',
                'custom_metadata.format_details.audio_configuration',
                'custom_metadata.format_details.audio_element']
        # Open output file as CSV
        writer = csv.DictWriter(output_io, fieldnames=fieldnames)

        # Write the fieldnames
        writer.writeheader()
        for row in reader:
            if 'Trailer'not in row['folder_names'] \
                    and row['asset_type_or_class'] in included_assets:
                output_row = row.copy()
            # Do Something
            # Updating missing metadata
                output_row['missing_metadata'] = ''
                for column in metadata_columns:
                    if output_row[column] == '':
                        output_row['missing_metadata'] += f' {column}'
                output_row['missing_metadata'] =  output_row['missing_metadata'].lstrip()
                if (row['custom_metadata.format_details.audio_configuration'] == '' \
                            or row['custom_metadata.format_details.audio_configuration'] != \
                                    audio_code_map.get(row['name'].split('_')[4], ' ')):
                    output_row['metadata_discrepancy'] = 'True'
                else:
                    output_row['metadata_discrepancy'] = 'False'
                writer.writerow(output_row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'source_file',
        help='Runner inventory CSV report'
    )
    parser.add_argument(
        'output_file',
        help='Filename of the resulting report'
    )
    args = parser.parse_args()
    main(args.source_file, args.output_file)
