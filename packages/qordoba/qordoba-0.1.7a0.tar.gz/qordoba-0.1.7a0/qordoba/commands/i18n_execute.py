from i18n_base import get_files_in_dir_with_subdirs, ignore_files, save_str_list_to_file, save_dict_to_JSON, get_config_key_format, filter_config_files

import os
import pandas as pd
import json
import logging

log = logging.getLogger('qordoba')
"""
TO DO 
Validate report status

should I create i18n file for all or by report?
shoudl I write existing keys to new i18n file?
"""
global NEW_I18N_FILE
NEW_I18N_FILE = dict()


def get_files_in_report(report_path):
    """
    takes the report path and gives back its input files """
    json_report = open(report_path).read()
    data = json.loads(json_report)
    return data.keys()


def get_filerows_as_list(file_path):
    # loads file into dict. Every line is an index and holds the sting as a value. Starting with line 1
    file_dict = {}
    count = 1
    try:
        with open(file_path, "r") as file:
            for line in file:
                file_dict[count] = line.decode('utf-8')
                count += 1

        return file_dict

    except IOError:
        print("File '{}' does not exist.".format(file_path))
        pass

    return file_dict


def transform_keys(key, key_format):
    key_value = key.strip()
    if key_format is not None:
        key = key_format.replace('KEY', key_value)
    else:
        key = key_value

    return key


def final_replace(key, picked_line, stringliteral, key_format):
    key_new = transform_keys(key, key_format)
    NEW_I18N_FILE[key] = stringliteral
    picked_line_1 = picked_line.replace("'" + stringliteral + "'", key_new)
    picked_line_2 = picked_line_1.replace('"' + stringliteral + '"', key_new)
    picked_line_3 = picked_line_2.replace('%{' + stringliteral + '}', key_new)  # ruby specific %{}
    picked_line_4 = picked_line_3.replace(stringliteral, key)
    return picked_line_4


def replace_strings_for_keys(singel_file_stringliterals, old_file_all_lines_into_dict, key_format):
    # file is list of strings. replaces strings in list

    for i in range(len(singel_file_stringliterals.index)):
        stringliteral = singel_file_stringliterals[i]["value"]
        idx_start = singel_file_stringliterals[i]["start_line"]
        idx_end = singel_file_stringliterals[i]["end_line"]

        # getting generated key
        try:
            key = singel_file_stringliterals[i]["generated_key"]["key"]
        except KeyError:
            log.info(
                "KeyError. Seems like there is no generated key to replace for stringliteral {StringLiteral}.".format(
                    StringLiteral=stringliteral))
            continue
        # if existing key exists, overwrite key withe existing key
        existing_key = singel_file_stringliterals[i].get("existing_key", None)
        if existing_key:
            key = existing_key["key"]

        # One-line StringLiteral
        if idx_start == idx_end:
            picked_line = old_file_all_lines_into_dict[idx_start]
            replaced_line = final_replace(key, picked_line, stringliteral, key_format)
            old_file_all_lines_into_dict[idx_start] = replaced_line

        # Multi-line StringLiteral
        if idx_start < idx_end:
            picked_lines = list()

            for i in range(idx_start, idx_end + 1):
                picked_lines.append(old_file_all_lines_into_dict[i])
            joined_lines = ''.join(picked_lines)

            replaced_line = final_replace(key, joined_lines, stringliteral, key_format)
            old_file_all_lines_into_dict[idx_start] = replaced_line
            # adding to the lost indexes none, so df is not fucked up for later
            for i in range(idx_start, idx_end):
                old_file_all_lines_into_dict[i] = None

    file_array_list = list()
    for i in range(len(old_file_all_lines_into_dict)):
        idx = i + 1
        file_array_list.append(old_file_all_lines_into_dict[idx])
    return file_array_list


def execute(curdir, input_dir=None, report_dir=None, key_format=None):
    """Input is the input-directory and qordoba reports.
    Output is a replaced input directory - stringliterals for keys - plus a i18n JSON file which contains the new keys"""
    reports = get_files_in_dir_with_subdirs(report_dir)
    reports = ignore_files(reports)
    for report in reports:
        try:
            df = pd.read_json(report)
        except ValueError:
            log.info("Could not parse report `{}`".format(report))
            continue

        # files_in_report are the files which are named in the report where StringLiterals have been extracted
        files_paths_in_report = get_files_in_report(report)
        files_paths_in_report = filter_config_files(files_paths_in_report)
        for single_file_path in files_paths_in_report:

            log.info("Reading old file `{}`.".format(single_file_path))
            old_file_all_lines_into_dict = get_filerows_as_list(
                single_file_path)  # reading file line by line into dictionary
            singel_file_stringliterals = (df[single_file_path])

            try:  # checking if file is empty
                if len(old_file_all_lines_into_dict) == 0:
                    log.info('File {} is empty'.format(single_file_path))
                    continue
            except TypeError:
                log.info('File {} is empty'.format(single_file_path))
                continue

            if not key_format: # get key format from config file, returns None if it doesnt exist
                key_format = get_config_key_format(single_file_path)

            # replacing StringLiterals for keys
            log.info("Replacing StringLiterals with keys in temp file")
            temp_file_all_lines_into_dict = replace_strings_for_keys(singel_file_stringliterals,
                                                                     old_file_all_lines_into_dict, key_format)
            # removing empty multi-line lines from file dictionary
            new_file_all_lines_into_dict = [x.strip('"') for x in temp_file_all_lines_into_dict if x != None]

            """ Replace old file """
            log.info("Replacing old file with stringliterals by new file with keys. File: `{}`".format(single_file_path))
            # remove old file, dump new
            os.remove(single_file_path)
            save_str_list_to_file(single_file_path, new_file_all_lines_into_dict)

            # new_file_strings = []
            # for i in range(len(new_file_all_lines_into_dict)):
            #     # converting everything to unicode, easier to join in next step
            #     new_file_strings.append((unicode(new_file_all_lines_into_dict[i])).rstrip())
            # new_file_dict = ''.join(new_file_strings)
            # if single_file_path.endswith('html'):
            # path = "/".join(single_file_path.split("/")[:-1]) + "/example.js"

    """ create new i18n file in output folder """
    new_i18n_file = report_dir + '/qordoba_i18n_file.json'
    log.info("Creating new i18n file.`{}`".format(new_i18n_file))
    save_dict_to_JSON(new_i18n_file, NEW_I18N_FILE)

